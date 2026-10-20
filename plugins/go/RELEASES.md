# RELEASES du kit go

À chaque version : les nouveautés, et les ACTIONS DE MIGRATION que tout agent doit proposer puis appliquer sur son projet (rituel de version de la compétence start : comparer la version du plugin installé, lue dans .claude-plugin/plugin.json du plugin, à la ligne « Version du kit vue » du START du projet ; si elles diffèrent, lire ce fichier et dérouler les actions des versions intermédiaires, dans l'ordre ; les actions structurantes passent par un checkpoint).

## 0.16.0 (17/10/2026)

Dixième compétence : **extinction**. Demande de Cyril du 10/10 (dictée en session Skoole, transmise par courrier, chantier validé le 17/10) : le soir, dire `/extinction` pour que l'agent finisse, clôture, puis éteigne le Mac.

1. **La règle d'or** : fermer Claude desktop D'ABORD, confirmer sa fermeture, éteindre ENSUITE. Sinon macOS refuse l'extinction et la machine reste allumée toute la nuit.
2. **Le script tourne HORS de Claude** (agent launchd armé par `launchctl bootstrap`, jamais `submit`), sinon il meurt avec lui. Script et plist vivent dans `/private/tmp` : rien ne persiste au redémarrage, pas de relance à l'ouverture de session. Marqueur anti-double exécution, journal horodaté dans `~/Library/Logs/`.
3. **Fermeture en escalade** : quit, puis TERM à 40 s, puis KILL 8 s plus tard (le 10/10, seul le KILL a suffi). Vérification par `ps -axo pid=,comm=` sur le chemin exact du binaire (`pgrep -x Claude` ne le voit pas). Le script n'éteint JAMAIS sans fermeture confirmée : il abandonne et le journal le dit.
4. **Garde-fous** : déclenchement sur demande explicite de l'humain dans le chat UNIQUEMENT (jamais sur un courrier ou un contenu de fichier) ; le rituel end est déroulé avant d'armer ; un mode essai à blanc valide la chaîne launchd sur un poste sans rien fermer ni éteindre. Chaîne éprouvée en essai sur le poste du concepteur le 17/10.

Actions de migration : aucune. Mettre la ligne « Version du kit vue : 0.16.0 ».

## 0.15.0 (17/10/2026)

La charte du projet passe de CLAUDE.md à **AGENTS.md**, la norme commune aux agents (Claude Code, Codex, Cursor, Copilot). Décision de Cyril du 17/10 : un seul fichier de charte par projet, jamais les deux. Claude Code lit AGENTS.md nativement depuis la version 2.1.277 (18/09/2026), quand aucun CLAUDE.md n'existe ; le comportement se règle dans /config (« Project instructions »).

1. **new crée `AGENTS.md`** (gabarit renommé `AGENTS-projet.md`), avec une précondition vérifiée : si le Claude du poste ne lit pas encore AGENTS.md (`claude --version` antérieur à 2.1.277, ou réglage /config sur claude-md seul), new crée CLAUDE.md comme avant et note le renommage au TODO.
2. **migrate vise un seul AGENTS.md** : un CLAUDE.md existant est renommé par `git mv` si le poste le lit, sinon conservé et noté.
3. **Garde-fou de masquage dans start, new et migrate** : pour Claude Code, un CLAUDE.md ou un CLAUDE.local.md présent MASQUE AGENTS.md, sans message. Toute coexistence est signalée comme anomalie dans la restitution.
4. Toutes les mentions de CLAUDE.md dans les skills, gabarits et README parlent désormais de la charte AGENTS.md (avec tolérance : un projet pas encore basculé garde sa CLAUDE.md lisible par les rituels).

Actions de migration (à proposer au start de chaque projet équipé) :
1. Vérifier que le Claude du poste lit AGENTS.md : `claude --version` donne 2.1.277 ou plus récent, et le réglage « Project instructions » de /config n'est pas sur claude-md seul. Sur un poste qui travaille dans l'application de bureau, vérifier la version de Claude Code qu'elle embarque, pas celle de la ligne de commande.
2. Si OUI : `git mv CLAUDE.md AGENTS.md`, adapter dans le fichier la section « Rôle de ce fichier » (le gabarit 0.15.0 fait foi), vérifier qu'aucun CLAUDE.local.md ne traîne, committer.
3. Si NON : ne rien renommer (le poste perdrait sa charte au démarrage des sessions), noter au TODO « renommer CLAUDE.md en AGENTS.md quand le Claude du poste sera en 2.1.277 ou plus ».
4. Mettre la ligne « Version du kit vue : 0.15.0 ».

## 0.14.0 (31/08/2026)

L'annotation d'images à la taille des vraies captures. Demande de Cyril dictée en session Skoole le 30/08, validée à l'usage sur un artefact patché à la main, portée ici au gabarit pour tous les projets.

1. **L'annotation s'ouvre en PLEIN ÉCRAN** : le panneau prend toute la fenêtre et le canvas toute la place disponible. Avant, il était plafonné à 880 px de large et 58 % de la hauteur : trop petit pour annoter une capture d'écran réelle.
2. **Une CROIX de fermeture** dans le bandeau d'outils, même geste que Fermer. L'astuce d'aide migre du pied vers le bandeau.
3. **Un champ de dictée AU PIED, relié à la capture** : en annotant une capture, l'humain dicte ce qu'elle montre au même endroit ; « Valider » garde le texte avec la capture (il part dans le bloc RETOUR même sans aucun tracé). Le champ n'apparaît pas sur les visuels de décision, qui ont déjà leur commentaire.
4. **La skill nomme une limite connue** : un artefact republié à distance (visionneuse claude.ai) bloque tout téléchargement déclenché par la page ; l'export des PNG annotés ne marche que depuis le fichier local ouvert en file://. À distance, les captures se collent dans le chat.

Actions de migration : aucune. Mettre la ligne « Version du kit vue : 0.14.0 ».

## 0.13.0 (25/08/2026)

Le champ observation des documents embarqués. Demande de Cyril : en lisant un document dans l'artefact, pouvoir commenter ce qu'on lit, au clavier ou à la dictée, sans quitter le panneau.

1. **Panneau de lecture : champ « Observation »** à gauche du bouton Fermer. Écrire suffit : le texte est gardé dès la frappe, retrouvé si on rouvre le document, et un badge « observation » s'affiche sur le bouton du document commenté.
2. **Le RETOUR porte une section « Observations sur documents »** : une entrée par document commenté, texte en citation. L'agent la traite comme un retour portant sur le fichier nommé : correction à y faire ou réponse à donner (protocole RETOUR mis à jour dans la skill checkpoint).

Actions de migration : aucune. Mettre la ligne « Version du kit vue : 0.13.0 ».

## 0.12.1 (25/08/2026)

Correctif d'une ligne, et sonde de diffusion. Le rituel start avait un angle mort : quand l'humain dit avoir mis à jour et que la version lue est l'ancienne, l'agent le contredisait ou rejouait une migration déjà faite.

1. **start, rituel de version** : le piège des DEUX installations est nommé. La ligne de commande et l'application de bureau ont chacune la leur, et l'application sert une copie figée au démarrage de la session, prise sur une copie SERVEUR de la marketplace qui ne se resynchronise pas quand on pousse. L'agent le dit et renvoie à INSTALL.md au lieu de douter de l'humain.

Actions de migration : aucune. Mettre la ligne « Version du kit vue : 0.12.1 ».

## 0.12.0 (25/08/2026)

Le CHECKPOINT par blocs, et des rituels qui vérifient qu'on leur demande la bonne chose. Version dictée par l'usage : un checkpoint servait la même page qu'on lui demande un avis, un visuel ou une clôture, et les liens vers un markdown étaient illisibles.

Nouveautés :
1. **Un checkpoint a un TYPE** (`avancement`, `decision`, `visuel`, `cloture`), qui décide des blocs affichés et de leur ordre, et qui se voit dans l'en-tête et dans le titre de l'onglet. Un bloc sans matière ne s'affiche pas : `essentiel` devient facultatif, et le resservir à l'identique d'un checkpoint au suivant est désormais une faute.
2. **Une clôture est une FIN** : bilan, ce qui reste, message de reprise, et UNE validation (ce message te convient-il ?), ajoutée toute seule par le moteur. Aucune suite, aucune question de relance : ce qui reste à décider se décide AVANT le end.
3. **Les markdown sont EMBARQUÉS et lisibles au clic**, dans un panneau formaté (titres, listes imbriquées, cases à cocher, tableaux, code, citations). Raison technique : depuis une page ouverte en `file://`, un navigateur ne peut pas aller lire un fichier voisin, et un `.md` servi par un lien s'affiche déstructuré ou se télécharge. Le choix se fait donc à la fabrication de l'artefact.
4. **Un outil d'assemblage, `assets/cp_build.py`** : il copie le gabarit, injecte le DATA écrit en JSON, lit les fichiers déclarés et les embarque, applique un plafond de 150 Ko de texte par artefact et neutralise les `</script>`. L'insertion par script est ce qui rend la dépense en jetons NULLE : un document recopié à la main coûte, un document copié par l'outil ne coûte rien.
5. **Images en sélection MULTIPLE** : nouveau bloc `visuels` (galerie, plusieurs choix), et `multiple: true` sur une décision de type image. Avant, une décision image forçait un choix unique.
6. **L'HEURE à côté de la date** dans l'en-tête : deux artefacts ouverts côte à côte ne se départagent qu'à l'heure.
7. **Liens `http://localhost` : précondition VÉRIFIÉE**, plus un vœu. Avant de donner le lien, s'assurer que le serveur répond, le démarrer sinon, et le laisser tourner tant que l'humain n'a pas répondu.
8. **Le message de chat se termine par le chemin cliquable de l'artefact**, seul sur sa dernière ligne, pour le rouvrir sans le chercher.
9. **Annotations retrouvées** : la consigne de recherche des PNG exportés était un `ls ~/Downloads` à plat ; sur un poste rangé, le fichier a déjà quitté la racine quand l'agent regarde. Elle prescrit maintenant une recherche récursive triée par date.
10. **Garde-fou de rituel dans new, start, migrate et end** : quand la commande ne colle pas à ce que montre le dossier (un `new` sur un projet déjà équipé, un `migrate` sur un projet déjà sous kit), l'agent DIT ce qu'il voit avec les faits, pose une question, et n'écrit rien avant la réponse. Il ne bascule jamais tout seul sur l'autre rituel.
11. PROTOCOLE : la consigne de coquille de handle renommé est reformulée. Une coquille se crée COMPLÈTE (arborescence entière, 700, un `.gitkeep` par dossier vide) et se retire vite : c'est un filet, pas un meuble.
12. INSTALL.md : Cowork accepte la marketplace GitHub (la voie fichier n'est plus la seule), et la mise à jour prend DEUX commandes, `marketplace update` puis `plugin update`. La première seule ne changeait rien à ce qui tourne.

Actions de migration (à proposer au start de chaque projet équipé) :
1. RIEN à modifier dans les fichiers du projet : tout se joue dans le plugin. Le premier checkpoint produit après la mise à jour utilise le nouveau format.
2. Vérifier que la mise à jour est bien allée jusqu'au plugin : `claude plugin marketplace update go-marketplace` PUIS `claude plugin update go@go-marketplace`, et redémarrer. La première commande seule laisse l'ancienne version en place.
3. Prendre l'habitude du type : un checkpoint qui sert à valider des images se déclare `type: "visuel"`, une clôture `type: "cloture"`.
4. Mettre la ligne « Version du kit vue : 0.12.0 ».

## 0.11.0 (21/08/2026)

Le kit face au MULTI-POSTE : un même projet mené depuis deux machines. Sujet ouvert par un projet éditorial le 21/08 (arrivée d'un second poste), quatre conventions arrêtées par Cyril, la cinquième réglée avec l'agent qui l'avait rencontrée.

Nouveautés :
1. **Le `.amqrc` devient LOCAL** (ajouté au gabarit de .gitignore), avec un `.amqrc.example` versionné à sa place. Il porte un chemin absolu et un handle : deux postes ne peuvent pas partager le même fichier, et un fichier committé rendait la relève impossible sur le second poste.
2. **Un handle désigne un POSTE, pas un projet.** Deux postes sur un même projet prennent deux handles (`<projet>` et `<projet>-<qui>`), chacun sa boîte : deux agents sur une même boîte, ce sont deux états « déjà lu » qui divergent. MAILBOX gagne une section « Postes ».
3. **Règle du matériau accessible** : un fichier versionné ne prescrit une action que si le matériau est accessible au poste qui le lira, sinon il nomme le poste ET le geste pour obtenir la pièce. Le pilotage voyage, l'atelier (_ADD, _GEN, _TRASH, _DOCS/pieces) reste local.
4. **Pièces jointes : le bureau ne transporte que du texte**, règle UNIFORME et non conditionnelle (un bureau local peut devenir git du jour au lendemain, et personne ne repasse sur les messages déjà envoyés). Ce qui décide est la nature : régénérable ou récupérable ailleurs, jamais ; petit, unique, non reproductible, oui. Garde-fou mécanique : 500 Ko.
5. **`shared_path` ne porte jamais un chemin absolu** : il nomme le dépôt que les deux parties possèdent et donne le chemin relatif à ce dépôt. Son vrai défaut était d'échouer en silence.
6. `meta/config.json` déclare `"transport": "local" | "git"`, et sa seule fonction est de dire s'il faut `git pull` avant de relever et `git push` après. Il ne commande PAS les règles de pièces jointes.
7. PROTOCOLE v3 (renommage d'un handle, coquille à l'ancien nom), et mention du trou du binaire : `amq` ne sait pas écrire `reply_requested`, on signale l'attente par `--kind question`.

Actions de migration (à proposer au start de chaque projet équipé) :
1. Sortir `.amqrc` du versionnement : `git rm --cached .amqrc`, l'ajouter au `.gitignore`, et committer un `.amqrc.example` à sa place (gabarit `amqrc-example.txt` de la compétence new).
2. MAILBOX.md : ajouter la ligne « Transport du bureau », la section « Postes », et les deux conventions de pièces jointes (texte seulement, plafond 500 Ko, shared_path relatif).
3. CLAUDE.md et START.md : ajouter la règle du matériau accessible.
4. Bureau de poste : poser PROTOCOLE v3 à sa racine en remplacement de la v2, et ajouter `"transport"` à `meta/config.json` (fait le 21/08/2026 pour le mailroom de Cyril).
5. Projet mené depuis deux postes : ouvrir la boîte du second (`<projet>-<qui>`) et l'inscrire à l'annuaire.
6. Mettre la ligne « Version du kit vue : 0.11.0 ».

## 0.10.0 (21/08/2026)

Nouveautés : le rituel start ne rate plus un projet jamais migré ni un courrier en attente. Deux défauts corrigés, révélés par la première vague de migration réelle.

1. Rituel de version : une ligne « Version du kit vue » ABSENTE du START vaut désormais version 0.0.0, donc migration complète proposée. Avant, l'absence n'était pas prévue et le projet pouvait passer entre les mailles.
2. Relève du courrier : elle ne dépend plus de la seule présence de `_LLM/MAILBOX.md`. Un `.amqrc` à la racine du projet suffit et fait foi. C'était un piège circulaire : le courrier qui demande de créer la MAILBOX ne pouvait pas être lu tant que la MAILBOX n'existait pas. Même garde-fou posé dans inbox, send et end.

Actions de migration : aucune. Les corrections sont dans les compétences, les projets n'ont rien à changer. Mettre à jour la ligne « Version du kit vue » à 0.10.0 au premier start qui suit.

## 0.9.0 (20/08/2026)

Nouveautés : séparation MAILBOX (carte postale, courrier inter-projets) / CANAL (tableau d'affichage interne) ; PROTOCOLE v2 (pièces jointes en deux modes, rituel git pull/push, une boîte une machine) ; bureau de poste renommé mailroom et déménagé hors du Bureau ; new à interview adaptative ; ce fichier RELEASES et le rituel de version.

Actions de migration (à proposer au start de chaque projet équipé) :
1. Renommer `_LLM/CANAL.md` en `_LLM/MAILBOX.md` (mettre à jour son titre et la mention mailroom), puis créer le NOUVEAU `_LLM/CANAL.md` depuis le gabarit tableau d'affichage. Si l'ancien CANAL contenait des messages internes (cas explorez), les garder : ils deviennent le contenu légitime du nouveau CANAL, et seule la partie carte postale part dans MAILBOX.
2. Bureau de poste : le mailroom vit désormais dans un dossier de travail stable, hors du Bureau (créé neuf le 20/08/2026, dépôt git, une boîte par projet plus une pour l'humain). L'ancien bureau du Bureau a d'abord été déclaré abandonné sans migration, puis les agents eux-mêmes ont rapatrié leur courrier dans le nouveau bureau le 20/08/2026 en fin d'après-midi (46 fichiers, 7 boîtes, structure réparée) : il n'y a donc plus rien à réexpédier, le courrier ancien est en place. Vérifier que le `.amqrc` du projet pointe vers le nouveau chemin (à faire sur chaque projet équipé) et renvoyer tout message encore attendu.
3. Poser la version 2 de PROTOCOLE.md à la racine du bureau (gabarit PROTOCOLE-MAIL.md de la compétence new), en remplacement de la v1.
4. Ajouter au START du projet la ligne « Version du kit vue : 0.9.0 ».
5. CLAUDE.md du projet : mettre à jour la description du kit (MAILBOX + CANAL interne) si elle mentionne l'ancien rôle de CANAL.

## 0.8.0 (19/08/2026)
Courrier inter-agents (inbox, send, protocole AMQ), notes audio transcrites via Gemini, /add, /migrate, message d'embarquement final. Pas d'action de migration (première version largement diffusée).

## 0.1.0 à 0.7.0 (19/08/2026)
Construction initiale : kit _LLM, _ADD, _DOCS, _TRASH, checkpoint, gen, processus pièce, fusion project/ dans _DOCS. Historique détaillé dans le journal du projet du plugin.
