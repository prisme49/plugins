# go

Kit de pilotage de projet par sessions IA. Il donne à tout projet (Cowork, Claude Code ou mixte) une structure que n'importe quel agent peut reprendre : une trace complète de l'état, des décisions et du travail en cours.

## Les 10 compétences

| Compétence | Rôle |
|---|---|
| new | Initialise la structure complète (_LLM, _ADD, _DOCS, _TRASH, project/, AGENTS.md, .env.local, gitignore) et affiche le message d'embarquement |
| start | Rituel de début de session : lecture du kit, traitement de _ADD, audit de cohérence entre l'état déclaré et l'état réel, restitution (où on en est, propositions, points douteux ou contradictoires) AVANT toute modification |
| end | Rituel de clôture : JOURNAL, TODO, réécriture de START comme message de reprise autoportant, point de décision de clôture |
| checkpoint | Restitution et prise de décision via un artefact HTML interactif (recommandations fermes, retour copiable que l'humain colle dans le chat) |
| gen | Génère une image via l'API Gemini (clé de l'utilisateur dans .env.local), la range dans _GEN/ avec son prompt, applique la charte d'images de _LLM/RULES.md |
| add | Traite la boîte _ADD/ : fiches (note + texte intégral), transcription mot à mot des notes audio via Gemini, index régénéré |
| inbox | Relève le courrier inter-agents (mailroom AMQ, remote git pris en charge) : lit, accuse réception, répond, débloque les tâches |
| send | Envoie un message à un autre agent, marque la tâche bloquée si réponse attendue, et prévient l'humain |
| migrate | Fait entrer un projet EXISTANT dans le kit : inventaire, plan détaillé, appliqué seulement après acceptation, sans toucher à l'application |
| extinction | Clôture la session (rituel end) puis éteint le Mac : un agent launchd hors de Claude ferme Claude desktop, confirme la fermeture, et n'éteint qu'ensuite. Sur demande explicite de l'humain uniquement |

## La structure installée par new

```
AGENTS.md      # charte du projet, lue en premier (norme commune Claude Code, Codex, Cursor, Copilot)
.env.local     # secrets, gabarit de variables vides (hors Git) ; l'agent ne lit que les noms, jamais les valeurs
_ADD/          # boîte de dépôt de l'humain (hors Git)
_DOCS/         # TOUTE la documentation : fiches des pièces (note + texte intégral) et docs rédigées + INDEX.md généré ; originaux dans pieces/ (hors Git)
_GEN/          # images générées (/gen), hors Git
_TRASH/        # rien n'est supprimé, tout y est déplacé ; seul l'humain vide (hors Git)
_LLM/          # START, TODO, JOURNAL, MAILBOX, CANAL, RULES, checkpoints/
```

## Principes non négociables

1. L'agent propose, l'humain décide (points de décision avec recommandations fermes).
2. Rien n'est supprimé, tout passe par _TRASH.
3. Chaque session commence par start (audit inclus) et se termine par end : ce qui n'est pas écrit dans le kit est perdu avec le contexte.
4. Tout en français, aucun tiret quadratin.

## Utilisation type

1. Nouveau projet : ouvrir le dossier, lancer `new`, répondre aux 2 ou 3 questions.
2. Chaque session : `start` pour reprendre, travailler, `end` pour clôturer.
3. Déposer des documents à tout moment dans _ADD/ : ils seront traités au prochain start.

## Notes d'installation

- Si une version autonome de la compétence checkpoint est déjà installée sur le compte, la désactiver pour éviter les doublons : celle du plugin devient la seule source de vérité.
- La personnalisation par projet se fait dans la section « Personnalisation » de l'AGENTS.md créé ; la personnalisation du plugin lui-même se fait via la compétence de customisation de plugins de Cowork.
