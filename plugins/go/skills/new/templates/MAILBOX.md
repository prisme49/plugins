# MAILBOX : carte d'identité postale de ce projet

Le courrier inter-agents passe par un bureau de poste de fichiers (protocole AMQ, format Maildir), le mailroom. Ce fichier est la carte SIM du projet : qui je suis, où est la poste, avec qui je corresponds. (Anciennement nommé CANAL ; CANAL existe toujours mais sert au tableau d'affichage INTERNE du projet.)

## Identité
- Bureau de poste (racine) : (à renseigner, ex : /Users/<compte>/Desktop/_claude_code/mailroom ; le fichier `.amqrc` LOCAL à la racine du projet fait foi, il n'est pas versionné)
- Transport du bureau : (local ou git ; en git, `git pull` avant toute relève et `git push` après tout envoi)
- Mon handle : (à renseigner, ex : skoole)
- Statut : canal non configuré tant que les deux lignes ci-dessus sont vides.

## Postes
Un handle désigne un POSTE (une session sur une machine), pas un projet. Tant que ce projet est mené depuis une seule machine, il n'a qu'un handle. Dès qu'un second poste apparaît, il prend son propre handle `<projet>-<qui>` et sa propre boîte : deux agents sur une même boîte, ce sont deux états « déjà lu » qui divergent.
(un poste par ligne : handle, qui le tient, quelle machine)

## Annuaire
(un correspondant par ligne : handle, projet, rôle)

## Conventions de ce projet
- Relève : à chaque start, et à la demande via la compétence inbox. On relève APRÈS avoir terminé l'action en cours et vidé ses propres envois, jamais au milieu d'une tâche.
- Envoi : via la compétence send ou pendant le travail ; TOUJOURS prévenir l'humain qu'un message est parti, avec la phrase à relayer : « Message envoyé à <handle>. Pour qu'il le voie tout de suite, dis /inbox à son agent. »
- Question bloquante : en-tête `reply_requested: true` + tâche TODO « bloqué : en attente de réponse <msg_id> ». On ne travaille JAMAIS sur une question dont la réponse n'est pas arrivée.
- Pièces jointes : le bureau ne transporte que du TEXTE. Ce qui est régénérable ou récupérable ailleurs ne s'envoie jamais (on envoie la fiche et le geste pour l'obtenir) ; ce qui est petit, unique et non reproductible peut voyager, plafond 500 Ko. Sur un bureau partagé par git, une pièce envoyée pèse pour toujours dans tous les clones.
- `shared_path` ne porte jamais un chemin absolu : nommer le dépôt que les deux parties possèdent et donner le chemin relatif à ce dépôt.
- Protocole complet (format des messages, new/cur, reçus, envoi sans binaire) : PROTOCOLE.md à la racine du bureau de poste.
