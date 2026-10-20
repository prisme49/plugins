---
name: new
description: "Initialise le kit de pilotage projet dans le dossier courant : structure _LLM/ (START, TODO, JOURNAL, CANAL, RULES, checkpoints/), boîte de dépôt _ADD/, documentation _DOCS/, corbeille _TRASH/, AGENTS.md et .env.local, puis affiche le message d'embarquement. Déclencher quand l'utilisateur dit « /new », « new », « nouveau projet », « initialise le kit », « installe le kit projet », « démarre un projet avec le kit », ou démarre un projet vierge qui devra être repris par d'autres agents."
---

# new : initialiser le kit de pilotage

Mettre en place, à la racine du projet courant, la structure qui permet à n'importe quel agent (Cowork, Claude Code ou autre) de reprendre le travail avec une trace complète.

## Garde-fou : est-ce bien `new` qu'il fallait ?

AVANT de créer quoi que ce soit, regarder le dossier courant. Trois cas où `new`
n'est probablement pas le bon rituel :

| Ce qu'on voit | Ce que c'est | La question à poser |
| --- | --- | --- |
| Un dossier `_LLM/` avec un START | Le kit est déjà là | « Ce projet a déjà le kit (START du <date>). Tu voulais `start` pour le reprendre, ou vraiment repartir de zéro ? » |
| Pas de `_LLM/`, mais du code, un README, un dépôt avec de l'historique | Un projet en route | « Ce dossier contient déjà <n> fichiers et <n> commits, le dernier du <date>. `migrate` propose un plan sans rien casser, `new` poserait la structure par dessus. Lequel ? » |
| Un `AGENTS.md` ou un `CLAUDE.md` déjà écrit | Des conventions existent | « Il y a déjà une charte (AGENTS.md ou CLAUDE.md). Je ne l'écrase pas : `migrate` la redécoupe au lieu de la remplacer. Tu confirmes quand même `new` ? » |

> **Principe du garde-fou** : quand ce qui est demandé ne colle pas à ce que
> montre le dossier, on ne corrige pas tout seul et on n'exécute pas quand même.
> On dit ce qu'on VOIT, avec les faits (dates, nombre de fichiers, dernier
> commit), on pose UNE question, et on attend. Aucune modification avant la
> réponse. C'est l'humain qui décide du rituel, pas l'agent.

## Règles permanentes (valables pour toutes les compétences du kit)

- Tout en français. Aucun tiret quadratin dans les textes générés (deux points, parenthèses ou virgules).
- Ne JAMAIS supprimer un fichier : le déplacer dans `_TRASH/` à la racine. Seul l'humain vide _TRASH.
- L'humain dépose des documents dans `_ADD/` à la racine : c'est à l'agent de les traiter puis de les ranger.
- `_ADD/`, `_TRASH/` et les fichiers `.env*` sont exclus du versionnement Git.
- Secrets : ne JAMAIS recopier une valeur de `.env.local` (ou de tout fichier de secrets) dans une conversation, un journal, un commit ou une restitution. Seuls les noms de variables peuvent être cités.

## La structure cible

```
racine-du-projet/
  AGENTS.md          # charte du projet, lue en premier par tout agent (norme commune Claude Code, Codex, Cursor, Copilot)
  .env.local         # secrets, vide au départ : l'humain remplit, l'agent ne lit que les noms
  _ADD/              # boîte de dépôt de l'humain : documents à traiter puis ranger
  _DOCS/             # TOUTE la documentation : fiches des pièces, specs et plans rédigés, INDEX.md ; originaux dans pieces/ (hors Git)
  _GEN/              # images générées par la compétence gen (hors Git, créé au premier usage)
  _TRASH/            # corbeille : rien n'est supprimé, tout y est déplacé
  _LLM/
    START.md         # message de reprise : où on en est, quoi faire à la prochaine session
    TODO.md          # backlog + section « Mis de côté » (décisions reportées, datées)
    JOURNAL.md       # une entrée datée par session : fait, décisions, en cours
    MAILBOX.md       # carte d'identité postale : mailroom (bureau de poste AMQ), handle, annuaire
    CANAL.md         # tableau d'affichage INTERNE : sessions parallèles, attentes de l'humain
    RULES.md         # règles vivantes : dictées par l'humain, apprises des erreurs par les agents
    checkpoints/     # artefacts HTML des checkpoints (CP-AAAAMMJJ-HHMM.html)
```

Rôle de chaque pièce : START se réécrit à chaque clôture (c'est un message, pas un journal) ; TODO est l'état des tâches ; JOURNAL est l'historique append-only ; CANAL ne sert que si un autre agent échange avec le projet ; _DOCS contient le fond (fiches et documents rédigés) ; AGENTS.md contient la forme (conventions, stack, rituels). Le livrable du projet (code, site, paquets) vit à la racine, dans ses propres dossiers.

## Procédure

1. Inventorier le dossier courant. Si des éléments du kit existent déjà : ne JAMAIS écraser, compléter seulement ce qui manque, et signaler ce qui a été trouvé.
2. Choisir la voie de cadrage :
   - Voie EXPRESS : l'humain a donné une phrase, un brief ou le contexte suffit. Ne demander que ce qui manque (nom, objectif) et avancer. C'est la voie par défaut quand il y a du contexte.
   - Voie INTERVIEW (proposée quand /new arrive sans aucun contexte, ou sur demande « new complet ») : commencer par LA question d'ancrage : « Qu'est-ce qu'on va créer ? ». Puis dérouler des blocs de questions ADAPTÉS à la réponse, 10 blocs maximum, chacun skippable, en s'arrêtant dès que l'humain dit stop. Blocs communs à tout projet : identité (nom, objectif, pour qui), première mission (semences de TODO et START), règles de départ (semences de RULES), courrier (inscrire au mailroom ? quel handle ?). Blocs selon la nature : projet de CODE (hébergement et infra, stack, dépôt git, clés .env à prévoir, domaine) ; projet ÉDITORIAL (ligne éditoriale, rythme de publication, canaux, charte d'images) ; MISSION ou DOCUMENT (revue de contrat, étude, dossier : parties prenantes, sources et pièces attendues dans _ADD, livrable exact, échéance) ; FORMATION (public, format, volumes). L'interview est passe-partout : Cowork comme Claude Code, code comme non-code. Sortie : AGENTS.md substantiel (Personnalisation remplie), RULES et TODO semés, MAILBOX configurée si demandé.
   Ne jamais poser une question dont la réponse est déjà dans la conversation.
3. Créer la structure à partir des gabarits du dossier `templates/` de cette compétence, en remplaçant les variables `{{PROJET}}`, `{{OBJECTIF}}`, `{{DATE}}` (date du jour, format JJ/MM/AAAA) :
   - `templates/START.md` vers `_LLM/START.md`
   - `templates/TODO.md` vers `_LLM/TODO.md`
   - `templates/JOURNAL.md` vers `_LLM/JOURNAL.md`
   - `templates/MAILBOX.md` vers `_LLM/MAILBOX.md`
   - `templates/CANAL.md` vers `_LLM/CANAL.md`
   - `templates/AGENTS-projet.md` vers `AGENTS.md` (racine). PRÉCONDITION VÉRIFIÉE : le Claude du poste doit lire AGENTS.md nativement (`claude --version` donne 2.1.277 ou plus récent, et le réglage « Project instructions » de /config n'est pas sur claude-md seul). Sinon, copier le gabarit vers `CLAUDE.md` à la place, adapter sa première section, et noter au TODO le renommage en AGENTS.md quand le poste suivra. Ne JAMAIS créer les deux : un CLAUDE.md ou CLAUDE.local.md présent masque AGENTS.md sans message.
   - `templates/TRASH-README.md` vers `_TRASH/README.md`
   - `templates/ADD-README.md` vers `_ADD/README.md`
   - `templates/DOCS-INDEX.md` vers `_DOCS/INDEX.md` (et créer `_DOCS/pieces/`)
   - `templates/RULES.md` vers `_LLM/RULES.md`
   - `templates/amqrc-example.txt` vers `.amqrc.example` (racine) : gabarit versionné du fichier de courrier. Le vrai `.amqrc` est LOCAL et non versionné : il porte un chemin absolu et un handle propres à la machine, donc il ne peut pas être commun à deux postes. Le créer par copie quand le canal est configuré.
   - `templates/PROTOCOLE-MAIL.md` : NE PAS copier dans le projet ; il se copie à la racine du bureau de poste quand le canal est configuré (compétences inbox et send)
   - `templates/env-local.txt` vers `.env.local` (racine) : gabarit de variables vides, l'humain le remplira ; adapter les sections au type de projet si l'information est connue
   - créer `_LLM/checkpoints/` (vide)
4. Git : si le projet est (ou sera) versionné, ajouter au `.gitignore` le contenu de `templates/gitignore-extrait.txt` (créer le fichier au besoin, sans doublonner les lignes déjà présentes).
5. Écrire la première entrée du JOURNAL (création du kit, date, ce qui a été discuté) et la ligne « Version du kit vue : <version du plugin, lue dans .claude-plugin/plugin.json> » dans le START.
6. Souhaiter la bienvenue à bord : afficher le message d'embarquement (section suivante), adapté au nom du projet, PUIS restituer via la compétence checkpoint (validation de la structure, suites : définir la première tâche, déposer des documents dans _ADD, lancer la première session avec start).

## Le message d'embarquement (à afficher tel quel, en adaptant le nom du projet)

Here we go : le poste de pilotage de {{PROJET}} est installé. Paré au décollage. Y a-t-il un pilote dans l'avion ? Oui : vous. L'agent tient les instruments, vous gardez le manche.

Comment ça marche, en trois habitudes :
1. Déposez ce que vous voulez dans _ADD/ (documents, contrats, images, et même vos NOTES AUDIO) puis dites /add : l'agent lit tout, transcrit vos vocaux mot pour mot (via votre clé Gemini), en fait des fiches dans _DOCS/ (sa bibliothèque, avec index) et range les originaux. Rien n'est jamais supprimé : tout ce qui doit disparaître part dans _TRASH/, que vous seul videz.
2. Chaque session commence par « start » (l'agent relit tout, dit où on en est et ce qui cloche, sans rien toucher) et se termine par « end » (il consigne tout pour la prochaine fois). Entre les deux, il vous soumet des checkpoints : des points de décision où c'est vous qui tranchez.
3. Le dossier _LLM/ est la mémoire du projet : START (la reprise), TODO (les tâches), JOURNAL (les logs de tout ce qui est fait), MAILBOX (le courrier avec les autres agents), CANAL (le tableau d'affichage interne), RULES (les règles vivantes : vos consignes, et les leçons que les agents tirent de leurs erreurs).

Un fichier .env.local attend vos clés à la racine (jamais commité, jamais lu en valeur par les agents). Une seule clé Gemini (GEMINI_API_KEY, créée sur aistudio.google.com/apikey) débloque deux pouvoirs : /gen pour générer des images (rangées dans _GEN/ avec leur prompt) et la transcription fidèle de vos notes audio déposées dans _ADD/.

Les commandes : /new (installer ce kit), /start (reprendre), /add (traiter vos dépôts, audio compris), /checkpoint (faire le point et décider), /gen (générer une image), /inbox et /send (le courrier entre agents), /end (clôturer). Et pour un projet qui existe déjà : /migrate propose un plan d'adoption du kit sans rien casser.

Alors, qu'est-ce qu'on va créer de merveilleux aujourd'hui ?

## Cas particuliers

- Projet déjà riche en fichiers : proposer de ranger la documentation existante dans _DOCS/ (en déplaçant, jamais en supprimant), mais ne le faire qu'après accord.
- L'humain fournit dès le départ des documents : les faire déposer dans _ADD/ et les traiter comme le ferait la compétence start.
