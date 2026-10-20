---
name: end
description: "Rituel de clôture de session sur un projet équipé du kit _LLM/ : mettre à jour JOURNAL et TODO, réécrire START comme message de reprise autoportant, vérifier _ADD et _TRASH, puis produire le point de décision de clôture. Déclencher quand l'utilisateur dit « /end », « end », « clôture », « on clôture », « fin de session », « termine la session », ou demande la passation à un autre agent."
---

# end : clôturer une session proprement

Le contrat : la prochaine session (un autre agent, un autre jour, un autre contexte) doit pouvoir reprendre SANS poser de question. Tout ce qui n'est pas écrit dans le kit sera perdu avec le contexte de cette session.

## Garde-fou : est-ce bien `end` qu'il fallait ?

| Ce qu'on voit | Ce que c'est | La question à poser |
| --- | --- | --- |
| Pas de `_LLM/` | Rien à clôturer | « Ce projet n'a pas le kit : il n'y a ni JOURNAL ni START à mettre à jour. Tu voulais `new` ou `migrate` ? » |
| Le kit est là, mais rien n'a bougé depuis la dernière clôture (aucun commit, aucun fichier modifié depuis la date du START) | Session sans travail | « Rien n'a changé depuis la clôture du <date>. Réécrire START effacerait un message de reprise encore valable. Je clôture quand même ? » |

> **Principe du garde-fou** : quand ce qui est demandé ne colle pas à ce que
> montre le dossier, on ne corrige pas tout seul et on n'exécute pas quand même.
> On dit ce qu'on VOIT, avec les faits (dates, nombre de fichiers, dernier
> commit), on pose UNE question, et on attend. Aucune modification avant la
> réponse. C'est l'humain qui décide du rituel, pas l'agent.

## Règles permanentes

- Tout en français. Aucun tiret quadratin.
- Ne rien supprimer : déplacement vers `_TRASH/` uniquement.
- Ne jamais marquer comme fait ce qui n'est pas vérifié (livrable présent, test passé, fichier bien écrit).
- Secrets : ne jamais recopier une valeur de `.env.local` dans le JOURNAL, le START ou un point de décision.

## Procédure

1. Reconstituer ce qui s'est passé dans la session : livrables produits ou modifiés, décisions prises par l'humain (y compris via les retours de points de décision), tâches avancées, problèmes rencontrés. Si dépôt Git : s'appuyer sur le diff et les commits.
2. Mettre à jour `_LLM/JOURNAL.md` : UNE entrée datée, append-only (jamais de réécriture des entrées passées), avec : fait, décisions, en cours, à reprendre.
3. Mettre à jour `_LLM/TODO.md` : cocher le fait (vérifié), ajouter le découvert, consigner dans « Mis de côté » les décisions reportées (avec date et identifiant Dx du point de décision).
3bis. Règles apprises : si une erreur a été rencontrée et comprise pendant la session (déploiement raté, consigne mal interprétée, piège technique), distiller la leçon en une règle datée dans `_LLM/RULES.md` (section « Règles apprises ») et la signaler au checkpoint de clôture. Le récit détaillé reste au JOURNAL.
4. RÉÉCRIRE `_LLM/START.md` en entier comme message de reprise autoportant : état du projet en quelques lignes, décisions actées, la prochaine session étape par étape, ce qu'il ne faut pas oublier. Un agent qui ne lit QUE ce fichier et la charte du projet (AGENTS.md) doit pouvoir travailler.
4bis. Mettre le tableau CANAL au propre (archiver le résolu, dater ce qui reste). Levée du courrier dès qu'un canal existe (_LLM/MAILBOX.md renseignée OU .amqrc à la racine du projet) : envoyer ce qui doit partir, répondre à ce qui attend, vérifier qu'aucun reply_requested reçu ne reste sans réponse, et que chaque question posée par nous a sa tâche TODO bloquée. Chaque envoi est signalé à l'humain avec la phrase à relayer.
5. Vérifier : `_ADD/` vide ou son contenu tracé dans TODO ; rien n'a été supprimé pendant la session (le cas échéant, le déplacement vers _TRASH est mentionné au JOURNAL) ; aucun fichier du kit ne contredit un autre.
6. Clôturer par la compétence checkpoint : artefact dans _LLM/checkpoints/ avec l'essentiel de la session, les dernières décisions à trancher s'il y en a, les suites proposées pour la prochaine session, et `session.cloture: true`. Si un message doit partir vers un autre agent, remplir `session.canal`.

## Cas particuliers

- Session interrompue en plein milieu : le noter tel quel dans START (« tâche X interrompue à l'étape Y, reprendre là »), c'est plus utile qu'un état embelli.
- L'humain demande une passation vers un agent précis (ex : Claude Code) : orienter START vers ce destinataire (ce qu'il doit lire, dans quel ordre, quoi faire en premier).
