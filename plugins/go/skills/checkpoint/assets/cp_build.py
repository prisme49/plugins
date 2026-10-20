#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assemble un artefact de checkpoint à partir du gabarit et d'un fichier DATA (JSON).

Raison d'être : les documents markdown que l'humain doit pouvoir lire au clic sont
EMBARQUÉS dans l'artefact (un navigateur ne peut pas aller lire un fichier voisin
depuis une page file://). L'insertion se fait ICI, par copie du fichier, et JAMAIS
en recopiant le texte dans la réponse de l'agent : c'est ce qui rend la dépense en
jetons nulle.

Usage :
    python3 cp_build.py data.json sortie.html [--gabarit chemin/template.html]

Dans data.json, un document se déclare avec un chemin plutôt qu'un contenu :
    "documents": [
      { "id": "todo", "label": "TODO du projet", "fichier": "_LLM/TODO.md" }
    ]
Le champ "nom" est rempli tout seul avec le chemin si absent.
"""
import json
import os
import sys

PLAFOND = 150_000  # octets de texte embarqué par artefact (décision de Cyril, 24/08/2026)


def charger_documents(data, base):
    """Remplace chaque champ fichier par le contenu réel, sous plafond."""
    total = 0
    for doc in data.get("documents", []):
        if "contenu" in doc and "fichier" not in doc:
            total += len(doc["contenu"].encode("utf-8"))
            continue
        chemin = doc.pop("fichier")
        absolu = chemin if os.path.isabs(chemin) else os.path.join(base, chemin)
        with open(absolu, encoding="utf-8") as f:
            texte = f.read()
        # Le nom affiché reste court : chemin relatif au projet, jamais un chemin absolu.
        court = chemin
        if os.path.isabs(chemin):
            racine = os.getcwd()
            court = (os.path.relpath(absolu, racine)
                     if absolu.startswith(racine + os.sep) else os.path.basename(absolu))
        doc.setdefault("nom", court)
        poids = len(texte.encode("utf-8"))
        reste = PLAFOND - total
        if poids > reste:
            coupe = texte.encode("utf-8")[:max(0, reste)].decode("utf-8", "ignore")
            texte = coupe + (
                "\n\n---\n\n*Document tronqué : le plafond de %d Ko de texte embarqué "
                "par artefact est atteint. Le fichier complet est `%s`.*"
                % (PLAFOND // 1000, chemin)
            )
            print("  ATTENTION : %s tronqué (plafond atteint)" % chemin, file=sys.stderr)
        total += len(texte.encode("utf-8"))
        doc["contenu"] = texte
        print("  document embarqué : %s (%d octets)" % (chemin, poids), file=sys.stderr)
    return total


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) < 2:
        print(__doc__)
        return 2
    data_path, sortie = args[0], args[1]
    gabarit = None
    for i, a in enumerate(sys.argv):
        if a == "--gabarit" and i + 1 < len(sys.argv):
            gabarit = sys.argv[i + 1]
    if not gabarit:
        gabarit = os.path.join(os.path.dirname(os.path.abspath(__file__)), "template.html")

    with open(data_path, encoding="utf-8") as f:
        data = json.load(f)
    base = os.path.dirname(os.path.abspath(data_path))

    # Clôture : le message de reprise EST le START du projet, on le copie plutôt
    # que de le réécrire (même raison que pour les documents : recopier coûte).
    if "reprise_fichier" in data:
        chemin = data.pop("reprise_fichier")
        absolu = chemin if os.path.isabs(chemin) else os.path.join(base, chemin)
        with open(absolu, encoding="utf-8") as f:
            data["reprise"] = f.read()
        print("  message de reprise copié depuis : %s" % chemin, file=sys.stderr)

    total = charger_documents(data, base)

    # </script> à l'intérieur d'une chaîne fermerait la balise : on neutralise.
    js = json.dumps(data, ensure_ascii=False, indent=2).replace("</", "<\\/")

    with open(gabarit, encoding="utf-8") as f:
        modele = f.read()
    debut = modele.index("const DATA = {")
    fin = modele.index("\n};", debut) + 3
    html = modele[:debut] + "const DATA = " + js + ";" + modele[fin:]
    with open(sortie, "w", encoding="utf-8") as f:
        f.write(html)
    print("artefact écrit : %s (%d octets, dont %d de documents embarqués)"
          % (sortie, len(html.encode("utf-8")), total))
    return 0


if __name__ == "__main__":
    sys.exit(main())
