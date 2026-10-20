---
name: inbox
description: "Relève le courrier inter-agents du projet (mailroom décrit dans _LLM/MAILBOX.md) : lit les messages non lus, les marque lus, dépose les accusés, répond à ce qui attend et met à jour le TODO. Déclencher quand l'utilisateur dit « /inbox », « inbox », « relève le courrier », « tu as un message », « va voir ta boîte », « l'autre agent t'a écrit »."
---

# inbox : relever le courrier

L'humain est le facteur : quand il dit /inbox, un message attend probablement. Cette compétence relève, traite et rend compte.

## Préconditions (non négociables)

1. Terminer proprement l'action en cours AVANT de relever : on ne lâche pas une tâche à moitié pour lire son courrier. Si une action longue est en cours, le dire à l'humain et convenir du moment.
2. Vider sa propre plume d'abord : si des messages devaient partir (réponses promises, envois en attente), les envoyer AVANT de relever, pour ne pas répondre avec un état périmé.

## Procédure

1. Lire `_LLM/MAILBOX.md` : racine du mailroom et handle. MAILBOX absente ou vide mais `.amqrc` présent à la racine du projet : le .amqrc fait foi (racine du bureau et handle), on relève quand même et on propose de créer la MAILBOX ensuite. Si le bureau est un dépôt git avec remote : `git pull` à sa racine AVANT la relève. Canal vraiment non configuré (ni MAILBOX renseignée, ni .amqrc) : le dire et proposer de le configurer (renseigner MAILBOX.md, vérifier que PROTOCOLE.md existe à la racine du bureau, sinon l'y copier depuis les gabarits de la compétence new).
2. Relever selon PROTOCOLE.md : lire chaque message de `inbox/new/`, le déplacer dans `inbox/cur/`, déposer l'accusé dans `receipts/`, mettre à jour `presence.json`. Avec le binaire amq disponible : `amq drain` fait le travail.
3. Traiter, dans cet ordre : d'abord les messages `reply_requested` (y répondre, ou dire à l'humain ce qui empêche de répondre), puis les autres (créer les tâches TODO qu'ils appellent, débloquer les tâches « en attente de réponse <msg_id> » dont la réponse vient d'arriver).
3bis. Si le bureau est un dépôt git avec remote : commit et push après la relève et les réponses.
4. Rendre compte à l'humain, court : combien de messages, de qui, quoi de bloquant, ce qui a été répondu, ce qui entre au TODO. Une ligne au JOURNAL si un message change le cours du projet.
5. Chaque envoi effectué en réponse est signalé avec la phrase à relayer : « Message envoyé à <handle>. Pour qu'il le voie tout de suite, dis /inbox à son agent. »

## Règles

- Tout en français, aucun tiret quadratin, jamais de suppression (les messages se déplacent, ne s'effacent pas).
- Boîte vide : le dire simplement, vérifier au passage qu'aucune tâche TODO bloquée n'attend une réponse en souffrance (la signaler avec le last_seen du correspondant).
