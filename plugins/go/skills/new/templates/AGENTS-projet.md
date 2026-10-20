# {{PROJET}} : conventions projet

Objectif : {{OBJECTIF}}

Tout agent qui travaille sur ce projet lit ce fichier en premier, puis _LLM/START.md.

## Rôle de ce fichier
AGENTS.md est la charte permanente du projet, au format commun à Claude Code, Codex, Cursor et Copilot : lu au début de CHAQUE session (chargé automatiquement par Claude Code 2.1.277 et plus récent, lu en premier par les rituels du kit partout). ATTENTION : un CLAUDE.md ou un CLAUDE.local.md présent à la racine MASQUE ce fichier pour Claude Code, sans message. Ne jamais en créer un ; en trouver un est une anomalie à signaler au start. Il ne contient que ce qui reste vrai d'une session à l'autre : conventions, structure, commandes, règles, rituels. Ce qui change de session en session vit ailleurs : l'état courant dans _LLM/START.md, l'historique dans _LLM/JOURNAL.md, les tâches dans _LLM/TODO.md, le fond dans _DOCS/. Le garder court : il consomme du contexte à chaque session. Le modifier, c'est changer les règles du jeu : faire valider par un checkpoint.

## Langue et typographie
- Tout en français (le code garde ses identifiants en anglais ; commentaires et interfaces en français).
- Aucun tiret quadratin dans les textes générés (utiliser deux points, parenthèses ou virgules).

## Kit de pilotage
- _LLM/START.md : message de reprise, réécrit à chaque clôture. Point d'entrée de toute session.
- _LLM/TODO.md : backlog + section « Mis de côté » (décisions reportées, datées).
- _LLM/JOURNAL.md : une entrée datée par session, en ajout uniquement.
- _LLM/MAILBOX.md : carte d'identité postale (mailroom, handle, annuaire). Relève au start et via inbox ; envoi via send, TOUJOURS signalé à l'humain ; question bloquante = reply_requested + tâche TODO bloquée, jamais de travail sans la réponse.
- _LLM/CANAL.md : tableau d'affichage INTERNE (sessions parallèles, attentes de l'humain, gelés) ; relu au start, mis au propre au end.
- _LLM/checkpoints/ : artefacts HTML des points de décision.
- _ADD/ (racine) : boîte de dépôt de l'humain. L'agent traite ce qui s'y trouve puis le range dans _DOCS/ (fiche + original).
- _DOCS/ (racine) : TOUTE la documentation du projet. Les pièces déposées deviennent des fiches markdown (frontmatter + note + texte intégral recopié) rangées par thème ; les specs et plans rédigés sont des fiches natives ; les originaux vont dans _DOCS/pieces/ (hors Git, peut peser lourd) ; _DOCS/INDEX.md est une vue générée depuis les frontmatters, jamais éditée à la main.
- _LLM/RULES.md : règles vivantes, lues à chaque start : consignes dictées par l'humain + leçons apprises des erreurs par les agents.
- _TRASH/ (racine) : un agent ne supprime JAMAIS un fichier, il le déplace ici. Seul l'humain vide _TRASH.
- _GEN/ (racine) : images générées par la compétence gen (hors Git), tracées dans _GEN/INDEX.md.
- _ADD/, _DOCS/pieces/, _GEN/, _TRASH/, .amqrc et .env* sont exclus du Git (les fiches et l'index de _DOCS sont versionnés).
- Règle du matériau accessible : le pilotage est versionné, l'atelier est local. Un fichier versionné (AGENTS, START, TODO, RULES, MAILBOX, CANAL) est lu depuis n'importe quel poste : il ne prescrit une action que si le matériau est ACCESSIBLE AU POSTE QUI LE LIRA, sinon il nomme le poste ET dit par quel geste obtenir la pièce. Sans ça, « les journaux sont dans _ADD/ » se lit ailleurs « les journaux ont disparu ». La règle vaut aussi pour les OUTILS, et c'est là qu'elle coûte le plus cher : « lance-le avec `python3` » est faux sur une machine où `python3` est un miniconda dont le navigateur embarqué ne démarre pas. Un fichier absent se voit tout de suite, un outil qui existe mais ne marche pas se voit après une heure : nommer l'outil PRÉCIS (le Python du projet, pas celui du système) et dire pourquoi.
- Courrier : le `.amqrc` est LOCAL à chaque poste (chemin absolu et handle propres à la machine) ; le dépôt ne versionne que `.amqrc.example`. Un handle désigne un poste, pas un projet : deux postes sur un même projet prennent deux handles.

## Secrets
- `.env.local` à la racine : les secrets du projet, rempli par l'humain, JAMAIS commité (couvert par .gitignore).
- Un agent ne recopie JAMAIS une valeur de ce fichier dans une conversation, un journal, un commit ou une restitution : seuls les noms de variables peuvent être cités.

## Traitement des dépôts
- Compétence add : les pièces de _ADD/ deviennent des fiches _DOCS (note + texte intégral) ; les audio sont transcrits mot pour mot via l'API Gemini (clé dans .env.local) puis mis en forme dans _DOCS/notes/.

## Génération d'images
- Compétence gen : clé GEMINI_API_KEY dans .env.local, images dans _GEN/, charte d'images éventuelle dans _LLM/RULES.md (elle prime).

## Rituels (obligatoires)
- Début de session : compétence `start` du plugin go. Audit de cohérence et restitution AVANT toute modification.
- Fin de session : compétence `end`. JOURNAL, TODO, réécriture de START, point de décision de clôture.

## Restitution et décisions (obligatoire)
- Toute restitution (fin de tâche, point d'étape, choix à valider, fin de session) passe par la compétence `checkpoint` : artefact HTML interactif dans _LLM/checkpoints/.
- Jamais de long résumé en prose ; message de chat : 3 lignes maximum.
- Quand un bloc « ## RETOUR CHECKPOINT » est collé, le parser et l'appliquer selon la compétence (rediscuter d'abord, « Plus tard » dans TODO).

## Personnalisation (à adapter librement pour ce projet)
- Stack technique : à compléter.
- Commandes utiles (lancement, tests, déploiement) : à compléter.
- Port de développement local (utilisé par les liens des points de décision) : à compléter.
- Particularités du projet : à compléter.
