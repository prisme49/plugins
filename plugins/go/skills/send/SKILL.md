---
name: send
description: "Envoie un message à un autre agent via le bureau de poste AMQ du projet (_LLM/MAILBOX.md) : compose au bon format, dépose dans l'inbox du destinataire, copie en outbox, marque la tâche bloquée si une réponse est attendue, et prévient l'humain. Déclencher quand l'utilisateur dit « /send », « envoie un message à », « dis à l'agent X que », « demande à skoole », ou quand le travail exige de poser une question à un autre agent."
---

# send : écrire à un autre agent

## Procédure

1. Lire `_LLM/MAILBOX.md` : racine du bureau, handle, annuaire. MAILBOX absente mais `.amqrc` présent à la racine du projet : le .amqrc fait foi, on envoie quand même. Canal vraiment non configuré (ni l'un ni l'autre) : proposer de le configurer d'abord.
2. Composer le message au format de PROTOCOLE.md : en-tête ---json (schema, id horodaté unique, from, to, thread p2p/<a>__<b>, subject court, created UTC, refs si réponse, `reply_requested: true` si une réponse est nécessaire pour continuer) puis corps markdown. Écrire un VRAI message : contexte, demande précise, ce qu'on attend en retour et pour quand ; le destinataire n'a pas notre session en tête.
3. Déposer : fichier dans `agents/<destinataire>/inbox/new/`, copie dans `agents/<soi>/outbox/sent/`, presence.json mis à jour ; pièce jointe en mode COPIE dans `attachments/<id>/` (ou `shared_path` si co-édition explicite, voir PROTOCOLE v2). Avec le binaire : `amq send` ou `amq reply`. Bureau avec remote git : pull avant, commit et push après.
4. Si `reply_requested` : créer ou basculer la tâche TODO concernée en « bloqué : en attente de réponse <msg_id> ». Cette tâche ne sera PAS travaillée tant que la réponse n'est pas relevée : on attend, on n'invente pas.
5. PRÉVENIR L'HUMAIN, toujours, avec la phrase à relayer : « Message envoyé à <handle> (sujet : ...). Pour qu'il le voie tout de suite, dis /inbox à son agent. » C'est l'humain qui fait le facteur entre les sessions.

## Règles

- Tout en français, aucun tiret quadratin.
- Jamais de secret dans un message (les correspondants ont leurs propres .env.local).
- Un message = un fichier : on n'édite jamais un message déjà envoyé, on en envoie un nouveau.
- Pas de spam : regrouper ce qui peut l'être, un fil par sujet (thread).
