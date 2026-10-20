---
name: add
description: "Traite la boîte de dépôt _ADD/ du projet à la demande : chaque pièce devient une fiche markdown dans _DOCS/ (note + texte intégral), l'original part dans _DOCS/pieces/, l'index est régénéré ; les fichiers AUDIO sont transcrits mot pour mot via l'API Gemini puis mis en forme dans _DOCS/notes/. Déclencher quand l'utilisateur dit « /add », « add », « j'ai mis des documents dans _ADD », « traite les ajouts », « traite ma note audio », ou dépose des fichiers en le signalant."
---

# add : traiter la boîte de dépôt

C'est LE processus canonique de traitement des pièces, utilisé aussi par le rituel start. La commande /add existe parce que rien ne déclenche automatiquement : l'humain dépose, puis dit /add.

## Le processus pièce (canonique)

Pour chaque fichier de `_ADD/` (ignorer README.md) :

1. Créer sa fiche markdown jumelle dans `_DOCS/<thème>/AAAA-MM-JJ-<slug>.md` (gabarit : templates/DOCS-FICHE.md de la compétence new). Frontmatter : titre, date_ajout, origine, type, piece (chemin vers l'original), tags, resume. Corps en deux sections : la Note (description, analyse, points d'attention ; description détaillée pour une image) puis le Texte intégral (le texte de la pièce recopié à l'identique, mot pour mot, crucial pour les contrats ; mots de passe et numéros de carte remplacés par [masqué]).
2. Déplacer l'original dans `_DOCS/pieces/` (même radical de nom que la fiche). pieces/ est hors Git ; fiches et index sont versionnés.
3. Régénérer `_DOCS/INDEX.md` en balayant les frontmatters de toutes les fiches (vue générée, jamais éditée à la main).
4. Si la pièce appelle une action : créer la tâche TODO correspondante.
5. Rendre compte : quelles pièces, classées où, quelles tâches créées. _ADD doit finir vide.

## Cas particulier : les notes audio

L'humain dépose souvent des notes vocales (.mp3, .m4a, .wav, .ogg, .webm, .flac, .aac). Les capacités de transcription de l'agent seul ne suffisent pas : on passe par l'API Gemini, avec la clé du projet.

1. Prérequis : `GEMINI_API_KEY` dans `.env.local` (jamais lire la valeur). Absente : expliquer où la créer (aistudio.google.com/apikey) et laisser la pièce dans _ADD.
2. Transcrire avec le script embarqué (zéro dépendance, Python standard) :

```
python3 <dossier de cette compétence>/assets/transcribe_audio.py \
  --input _ADD/<fichier audio> --out /tmp/transcription.md [--model auto]
```

   Le script envoie l'audio à Gemini (inline sous 19 Mo, Files API au-delà), exige une transcription INTÉGRALE mot à mot en français (hésitations comprises, locuteurs marqués, [inaudible] si besoin), en haute résolution média. `GEMINI_AUDIO_MODEL` dans .env.local force un modèle ; sinon le script prend le meilleur disponible.
3. Produire la fiche dans `_DOCS/notes/AAAA-MM-JJ-<slug>.md` : frontmatter standard (type: note audio, piece vers l'original), section Note = la mise en forme (synthèse structurée de ce que dit la note : idées, décisions, actions demandées), section Texte intégral = la transcription verbatim complète, non retouchée.
4. L'audio original part dans `_DOCS/pieces/`, l'index est régénéré, et chaque action demandée dans la note devient une tâche TODO.
5. Restituer la Note à l'humain (c'est souvent une consigne) ; s'il y a des décisions à trancher dedans, passer par un checkpoint.

## Règles

- Tout en français, aucun tiret quadratin, jamais de suppression.
- Ne jamais recopier un secret entendu dans un audio (le remplacer par [masqué] et le signaler à l'humain).
