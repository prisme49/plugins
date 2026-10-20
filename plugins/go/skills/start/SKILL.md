---
name: start
description: "Rituel de début de session sur un projet équipé du kit _LLM/ : lire START, TODO et JOURNAL, traiter la boîte _ADD, auditer la cohérence entre l'état déclaré et l'état réel du dossier, puis dire où on en est, ce qui est proposé et ce qui paraît douteux ou contradictoire, AVANT de toucher à quoi que ce soit. Déclencher quand l'utilisateur dit « /start », « start », « démarre la session », « reprends le projet », « lis le start et suis-le », ou ouvre une session de travail sur un projet contenant un dossier _LLM/."
---

# start : reprendre un projet proprement

Le contrat : l'agent reconstitue l'état du projet, le restitue, signale ce qui cloche, et NE MODIFIE RIEN avant l'accord de l'humain. Raison d'être : à la clôture précédente, l'agent avait beaucoup de contexte et a pu oublier des choses ; au démarrage, un regard neuf voit ce qui a été commencé sans être terminé. Cet audit est essentiel, ne jamais le sauter.

## Règles permanentes

- Tout en français. Aucun tiret quadratin.
- Ne rien supprimer : déplacement vers `_TRASH/` uniquement.
- Aucune modification de fichier avant l'accord explicite de l'humain (seule exception : les mises à jour du kit validées en fin de rituel).
- Secrets : ne jamais recopier une valeur de `.env.local` ; seuls les noms de variables peuvent être cités (ex : signaler une variable vide ou manquante).

## Procédure

1. Lire, dans cet ordre : la charte du projet à la racine (`AGENTS.md`, ou `CLAUDE.md` si le projet n'est pas encore basculé), `_LLM/RULES.md` (règles vivantes, à appliquer toute la session), `_LLM/START.md`, `_LLM/TODO.md`, les dernières entrées de `_LLM/JOURNAL.md`. GARDE-FOU DE MASQUAGE : si `AGENTS.md` coexiste avec un `CLAUDE.md` ou un `CLAUDE.local.md`, le signaler dans la restitution : pour Claude Code, le CLAUDE masque l'AGENTS sans message, et le projet ne doit avoir qu'UNE charte. Si le kit n'existe pas : ne rien créer, DIRE ce qu'on voit avec les faits (nombre de fichiers, présence d'une charte ou d'un README, dernier commit et sa date), puis proposer `new` pour un dossier vierge ou `migrate` pour un projet déjà riche, et s'arrêter là. Ne jamais choisir à la place de l'humain : c'est lui qui décide du rituel.
1bis. Rituel de version : comparer la version du plugin installé (.claude-plugin/plugin.json du plugin) à la ligne « Version du kit vue » du START du projet. LIGNE ABSENTE : le projet n'a jamais été migré, la traiter comme une version 0.0.0 et dérouler le rituel complet. Si les versions diffèrent : lire RELEASES.md du plugin, proposer les actions de migration des versions intermédiaires (checkpoint si structurantes), les appliquer, mettre la ligne à jour (la créer si elle manquait). PIÈGE À CONNAÎTRE : si l'humain affirme avoir mis à jour et que la version lue est pourtant l'ancienne, ne pas le contredire et ne pas rejouer une migration déjà faite. Il y a DEUX installations distinctes (ligne de commande et application de bureau) et l'application sert une copie figée au démarrage de la session, prise sur une copie serveur de la marketplace qui ne se resynchronise pas toute seule quand on pousse. Le dire, et renvoyer à INSTALL.md.
1ter. Lire `_LLM/CANAL.md` (tableau interne) : messages laissés par d'autres sessions, attentes de l'humain, sujets gelés. Relever le courrier dès qu'un canal existe, c'est à dire si `_LLM/MAILBOX.md` est renseigné OU si un fichier `.amqrc` est présent à la racine du projet : le .amqrc suffit et fait foi pour la racine du bureau et le handle. Ne JAMAIS conclure « canal non configuré » sur la seule absence de MAILBOX.md : un projet pas encore migré a du courrier qui l'attend, et c'est souvent ce courrier qui lui demande de créer sa MAILBOX. Relève : compter et lire inbox/new selon la compétence inbox, débloquer les tâches dont la réponse est arrivée, signaler les reply_requested en souffrance.
2. Inventorier `_ADD/` : lister les fichiers déposés depuis la dernière session (ignorer README.md) et préparer une proposition de traitement selon le processus pièce de la compétence add (fiches, audio transcrit via Gemini, INDEX régénéré).

## Ce qu'il ne faut pas faire

- Commencer à coder ou à produire avant la restitution.
- Masquer une incohérence pour ne pas déranger : la signaler est précisément le rôle de ce rituel.
- Marquer une tâche comme faite sans avoir vérifié le livrable.
