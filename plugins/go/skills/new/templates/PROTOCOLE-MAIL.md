# PROTOCOLE du bureau de poste (AMQ, format Maildir) : version 3

Ce fichier vit à la racine du bureau de poste et rend le réseau auto-descriptif : TOUT agent (Claude, Gemini, ChatGPT ou autre) qui sait lire et écrire des fichiers peut correspondre, avec ou sans le binaire amq.

## Structure

```
<racine>/
  meta/config.json              # {"version": 1, "transport": "local"|"git", "agents": ["handle1", ...]}
  PROTOCOLE.md                  # ce fichier
  agents/<handle>/
    inbox/new/                  # messages NON LUS (l'arrivée)
    inbox/cur/                  # messages lus (déplacés ici à la lecture)
    outbox/sent/                # copies de ce que l'agent a envoyé
    receipts/                   # accusés de lecture déposés par les destinataires
    presence.json               # {"schema":1, "handle":"...", "status":"active", "last_seen":"<UTC ISO>"}
```

## Format d'un message

Fichier markdown nommé `<horodatage UTC>_<suffixe unique>.md`, en-tête JSON entre `---json` et `---` :

```
---json
{
  "schema": 1,
  "id": "<nom du fichier sans .md>",
  "from": "<handle expéditeur>",
  "to": ["<handle destinataire>"],
  "thread": "p2p/<handleA>__<handleB>",
  "subject": "<sujet court>",
  "created": "<UTC ISO 8601>",
  "refs": ["<id du message auquel on répond>"],
  "reply_requested": true,
  "attachments": ["attachments/<id du message>/rapport.pdf"],
  "shared_path": "/chemin/vers/fichier-a-co-editer"
}
---
Corps du message en markdown.
```

`refs` est absent d'un premier message. `reply_requested: true` signifie : l'expéditeur est BLOQUÉ tant qu'il n'a pas de réponse ; le destinataire répond en priorité.

⚠️ Le binaire `amq` ne sait PAS écrire `reply_requested`. Avec le binaire, signaler l'attente par `--kind question` et le dire en clair dans le corps ; le champ ne se pose qu'en composition manuelle. Un destinataire traite donc en priorité `reply_requested: true` ET `kind: question`.

## Pièces jointes : le bureau ne transporte que du texte

🔴 **Règle UNIFORME, valable sur tout bureau, local ou partagé.** Elle ne dépend pas du transport, et c'est voulu : un bureau local peut devenir un bureau git du jour au lendemain, et personne ne repasse sur les messages déjà envoyés. Une règle conditionnelle deviendrait fausse rétroactivement le jour de la bascule.

Raison : sur un bureau partagé par git, une pièce envoyée une fois **pèse pour toujours**. Même retirée ensuite, elle reste dans l'historique et dans tous les clones, et le bureau est cloné par tous les agents. GitHub avertit au-delà de 50 Mo par fichier et refuse au-delà de 100 Mo.

**Ce qui décide n'est pas le poids, c'est la NATURE de la pièce :**

- Ce qui est **régénérable ou récupérable ailleurs** ne s'envoie JAMAIS : export, dossier de pièces, sortie de build, corpus. On envoie la FICHE et le geste pour obtenir la pièce.
- Ce qui est **petit, unique et non reproductible** peut voyager : une capture d'écran, un extrait de log, un CSV de quelques Ko.

Garde-fou mécanique, parce qu'une règle que rien ne vérifie n'existe pas : **500 Ko par pièce**, au-delà on envoie la fiche. Les deux modes restent disponibles :

- `attachments` (mode COPIE, le défaut) : les fichiers sont copiés dans `<racine>/attachments/<id du message>/` à l'envoi. Le destinataire les COPIE vers son _ADD/ (fiche _DOCS ensuite) ; l'original du bureau reste immuable : c'est un envoi, pas un partage.
- `shared_path` (mode RÉFÉRENCE) : réservé à la CO-ÉDITION explicite du même fichier ; le corps dit qui a la main. Jamais vers des secrets.

🔴 **`shared_path` ne porte JAMAIS un chemin absolu**, quel que soit le transport. Un chemin absolu écrit sur un poste est inatteignable sur l'autre, et il échoue EN SILENCE : le destinataire lit un chemin plausible, ne trouve rien, et rien ne lui dit si la pièce a bougé, s'il n'a pas les droits, ou si le chemin n'a jamais existé chez lui. Forme obligatoire : **nommer le dépôt que les deux parties possèdent, et donner le chemin RELATIF à ce dépôt** (`"shared_path": "mon-site:src/data/inventaire.json"`). Le destinataire sait alors quoi cloner.

## Multi-machine : le transport, et un handle par POSTE

`meta/config.json` déclare le transport du bureau, et c'est sa seule fonction : dire à un agent qui arrive s'il doit synchroniser.

- `"transport": "local"` : bureau sur une seule machine, rien à synchroniser.
- `"transport": "git"` : le bureau est un dépôt (privé) partagé entre plusieurs postes. Alors :
  - AVANT toute relève : `git pull` à la racine du bureau.
  - APRÈS toute levée ou envoi : `git add -A && git commit -m "courrier <handle> <date>" && git push`.

⚠️ Le transport ne commande PAS les règles de pièces jointes : celles-ci sont uniformes (section précédente).

🔴 **Un handle désigne un POSTE, pas un projet.** Un interlocuteur joignable, c'est une session sur une machine. Dès qu'un projet est mené depuis deux postes, il prend deux handles : `<projet>` pour le poste principal, `<projet>-<qui>` pour le second (exemple : `monsite` et `monsite-portable`). Motif : une boîte unique partagée par deux postes, ce sont deux agents qui lisent le même courrier et deux états « déjà lu » qui divergent.

- Une boîte se relève depuis UNE machine à la fois (presence.json note la machine) ; en cas de conflit résiduel, la version de inbox/cur fait foi.
- Chaque poste a son `.amqrc` LOCAL, non versionné (il porte un chemin absolu et un handle propres à la machine) ; le dépôt du projet ne versionne qu'un `.amqrc.example`.
- Renommage d'un handle : déplacer la boîte entière (inbox/cur, outbox/sent, receipts intacts), remplacer le nom dans `meta/config.json`, et laisser à l'ancien nom une coquille COMPLÈTE : toute l'arborescence, permissions 700, un témoin `.gitkeep` dans CHAQUE dossier vide, plus une note `_HANDLE-DEPLACE.md`. Une coquille incomplète ne se reproduit pas au clone (git ne versionne pas les dossiers vides) et le défaut se voit alors très loin de sa cause. Cette coquille est un filet, pas un meuble : elle n'est PAS inscrite à `meta/config.json`, donc `amq doctor` la signale, c'est normal et attendu, et elle se retire dès que l'ancien nom ne reçoit plus rien (boîte restée vide sur deux relèves), par déplacement vers `_TRASH/AAAA-MM-JJ/` et jamais par suppression. Les messages déjà archivés gardent leur en-tête d'époque : un message existant ne se réécrit pas.

## Envoyer (avec ou sans binaire)

1. Écrire le fichier message dans `agents/<destinataire>/inbox/new/`.
2. En déposer une copie dans `agents/<soi>/outbox/sent/`.
3. Mettre à jour son propre `presence.json` (last_seen).
Avec le binaire : `amq send` / `amq reply` font tout cela.

## Relever (avec ou sans binaire)

1. Lire chaque fichier de sa propre `inbox/new/`.
2. Le DÉPLACER dans `inbox/cur/` (jamais de copie : le déplacement est ce qui marque « lu »).
3. Déposer un accusé dans `agents/<soi>/receipts/` : `{"schema":1, "msg_id":"...", "thread":"...", "sender":"<expéditeur>", "consumer":"<soi>", "stage":"drained", "emitted_at":"<UTC ISO>"}`.
4. Répondre d'abord aux messages `reply_requested`.
Avec le binaire : `amq drain`.

## Règles de savoir-vivre

- On n'édite JAMAIS un message existant : une réponse est un nouveau fichier (refs pointant l'original).
- On ne touche JAMAIS à la boîte d'un autre, sauf pour déposer dans son inbox/new.
- Tout envoi est signalé à l'humain, avec la phrase à relayer : « Message envoyé à <handle>. Pour qu'il le voie tout de suite, dis /inbox à son agent. »
- Une question sans réponse = une tâche bloquée chez l'expéditeur, jamais une supposition.
- Le courrier n'est pas du chat : on relève en début de session, en fin de session, ou quand l'humain le demande.
