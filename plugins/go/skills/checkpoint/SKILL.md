---
name: checkpoint
description: "Restitution synthétique et prise de décision rapide via un artefact HTML interactif (points de décision cliquables avec recommandations, comparaison et annotation d'images, captures d'écran collées, suites proposées, clôture de session, message CANAL). Utiliser pour TOUTE restitution à l'humain : fin de tâche, point d'étape, avancement, choix à valider, comparaison de versions ou de visuels, fin de session. Déclencher dès que l'utilisateur dit « checkpoint », « fais le point », « où en est-on », « restitution », « point de décision », « qu'est-ce que tu recommandes », « montre-moi les options », « valide avec moi », ou dès qu'un résumé de travail serait produit : cette skill REMPLACE tout long résumé en prose. Déclencher aussi quand l'utilisateur colle un bloc commençant par « ## RETOUR CHECKPOINT » : il faut alors le parser et l'appliquer (section Protocole RETOUR)."
---

# checkpoint : communication modèle -> humain

L'humain pilote plusieurs agents en parallèle. Il n'a ni le temps ni l'envie de lire
de longs résumés : il veut comprendre l'en-cours en 30 secondes et trancher en
2 minutes. Cette skill est le canal unique de restitution : un artefact HTML
interactif, et un bloc de retour qu'il colle dans le chat pour que l'agent
applique ses décisions.

Règle absolue : quand cette skill s'applique, ne jamais produire de résumé en
prose. Le message de chat qui accompagne l'artefact fait 3 lignes maximum
(quoi, combien de décisions, quoi faire). Tout le reste vit dans l'artefact.

Instruction permanente de l'humain, valable ici comme partout : aucun tiret
quadratin dans les textes générés (utiliser deux points, parenthèses ou
virgules).

## Quand déclencher

- Fin d'une tâche ou d'un lot de travail, même petit.
- Point d'étape demandé (« fais le point », « où en est-on »).
- Un ou plusieurs choix à soumettre : options techniques, visuels, textes,
  noms, priorités.
- Une image ou un visuel produit à faire valider (avant/après, variantes).
- Fin de session : proposer la clôture (kit _LLM/) et, si utile, un message
  vers un autre agent (CANAL).
- Pas de décision en jeu mais un cap à donner : proposer des suites.
- L'utilisateur colle un bloc « ## RETOUR CHECKPOINT » : le traiter
  (voir Protocole RETOUR), sans régénérer d'artefact sauf nouveau point.

## Le TYPE d'abord : un checkpoint sert à ce qu'on lui demande

`DATA.type` décide des blocs affichés et de leur ordre. Le type se voit dans
l'en-tête et dans le titre de l'onglet. Choisir avant d'écrire quoi que ce soit :

| type | à quoi il sert | blocs |
| --- | --- | --- |
| `avancement` | point d'étape, fin de lot, cap à donner (défaut) | essentiel, décisions, visuels, documents, captures, suites, remarques, session |
| `decision` | uniquement des choix à trancher | essentiel, décisions, documents, captures, suites, remarques |
| `visuel` | uniquement valider des images | visuels (sélection multiple), décisions, documents, captures, remarques |
| `cloture` | fin de session : un end est une FIN | bilan, ce qui reste, message de reprise, une validation, documents, captures, remarques, session |

Règles de type, non négociables :

- Une CLÔTURE ne propose PAS de suites et ne pose pas de questions de relance :
  elle rend compte, montre le message de reprise, et demande une seule chose,
  est-ce que cette reprise convient. Ce qui reste à décider se décide AVANT.
  Le moteur ajoute cette validation tout seul dès que `reprise` est renseigné.
- Un checkpoint de type `visuel` ne contient que les visuels : pas d'essentiel,
  pas de suites, pas de bilan.
- `essentiel` est FACULTATIF partout : ne le mettre que s'il apprend quelque
  chose. Répéter le même essentiel d'un checkpoint à l'autre est un défaut.

## Procédure de production

1. Écrire un fichier `data.json` : l'objet DATA, en JSON (mêmes champs que le
   schéma ci-dessous). Les documents à faire lire se déclarent par un CHEMIN.
2. Assembler avec l'outil fourni, jamais à la main :
   `python3 <skill>/assets/cp_build.py data.json _LLM/checkpoints/CP-AAAAMMJJ-HHMM.html`
   L'outil copie le gabarit, y injecte DATA, lit les fichiers déclarés et les
   embarque, applique le plafond et neutralise les `</script>`.
   Ne jamais toucher au moteur (CSS et JS sous la ligne MOTEUR).
3. Présenter selon l'environnement :
   - claude.ai / Cowork : fichier `.html` dans le dossier de sorties,
     présenté comme artefact.
   - Claude Code : `_LLM/checkpoints/CP-AAAAMMJJ-HHMM.html` à la racine du
     projet (créer `_LLM/checkpoints/` au besoin), puis `open <fichier>`.
4. Message de chat : 3 lignes maximum, par exemple :
   « Point de décision prêt : 3 choix à trancher, 1 visuel à valider.
   Réponds dans l'artefact puis Copier le retour et colle le bloc ici. »
5. La DERNIÈRE ligne du message est le chemin cliquable de l'artefact, seul sur
   sa ligne. L'humain le rouvre d'un clic sans le chercher dans l'historique.

## Règles de contenu (non négociables)

- `essentiel` : 5 puces maximum, environ 90 caractères chacune, factuelles.
  C'est l'en-cours, pas le journal de la session.
- 6 décisions maximum par artefact. Au-delà : scinder, ou reporter les
  décisions secondaires en `suites`.
- 1 décision = 1 question courte + `detail` d'une phrase si nécessaire.
- Toujours une option `reco: true` par décision (recommandation ferme),
  avec la justification en une phrase dans `desc`. Si deux recommandations
  coexistent, utiliser `badge: "Recommandation A"` et `badge: "Recommandation B"`.
- Images : TOUJOURS en data URL base64 intégrée dans le HTML (jamais d'URL
  http externe, sinon annotation et export impossibles). JPEG qualité ~0.8,
  viser moins de 300 Ko par image, 6 images maximum par artefact. Pour un
  remplacement, mettre l'ancienne et la nouvelle côte à côte (labels
  « Avant » / « Après »).
- Toute décision qui porte sur quelque chose de lisible donne de quoi le lire
  (champ `liens`). Sans ça, l'humain valide à l'aveugle. Trois formes, dans cet
  ordre de préférence :
  1. Un MARKDOWN, une fiche, un fichier de configuration : le déclarer dans
     `documents` et y renvoyer par `{ label: "...", doc: "<id>" }`. Le texte est
     embarqué dans l'artefact et s'ouvre en panneau formaté, tableaux compris.
     Ne JAMAIS donner un `file://` vers un `.md` : le navigateur l'affiche
     déstructuré ou le télécharge, et depuis une page `file://` il ne peut pas
     aller lire le fichier lui-même (requête bloquée). Le choix se fait donc à
     la fabrication, pas au clic.
  2. Une PAGE servie, quand la validation porte sur ce que verra le lecteur :
     `http://localhost:<port>/...`. Précondition VÉRIFIÉE, pas espérée : avant
     de donner le lien, s'assurer que le serveur répond (le démarrer sinon), et
     le laisser tourner tant que l'humain n'a pas répondu. Un lien vers un
     serveur éteint est un lien mort. L'adresse et le port se décident dans la
     charte du projet (AGENTS.md), pas ici.
  3. Une URL externe, telle quelle.
  Des liens de portée générale (site, dépôt, tableau de bord) vont dans `liens`
  au niveau racine de DATA, sous le contexte.
- Documents embarqués : l'insertion se fait par `cp_build.py`, qui COPIE le
  fichier. Ne jamais recopier le contenu d'un document dans la réponse ni dans
  le JSON à la main : recopié, il coûte des jetons ; copié par l'outil, il n'en
  coûte aucun. Plafond de 150 Ko de texte embarqué par artefact, appliqué par
  l'outil (au delà, il tronque et le dit). Le panneau de lecture porte un
  champ « Observation » à gauche de Fermer : ce que l'humain y écrit ou y
  dicte est gardé dès la frappe (badge « observation » sur le bouton du
  document, texte retrouvé si on rouvre) et revient dans le bloc RETOUR,
  section « Observations sur documents ».
- Quand plusieurs réponses peuvent coexister, type `multi`, pas `choix` :
  un `choix` force une réponse unique et frustre l'humain. Cela vaut aussi pour
  les IMAGES : une décision `image` accepte `multiple: true`, et le bloc
  `visuels` est toujours en sélection multiple. Ne pas obliger l'humain à
  retenir un seul visuel quand il en valide trois sur cinq.
- Pas de décision à prendre ? Mettre `decisions: []` et soigner `suites` :
  2 à 4 continuations concrètes, la meilleure en `reco: true`.
- `suites.mode` : `multi` par défaut ; `ordre` dès que l'enchaînement
  compte (l'humain numérote les suites dans l'ordre de ses clics : 1, 2, 3) ;
  `single` seulement si les suites s'excluent vraiment. L'humain peut
  changer de mode dans l'artefact et ajouter ses propres suites (SP1,
  SP2...) : ne pas s'en étonner dans le RETOUR.
- Fin de session probable ? `type: "cloture"` (il met `session.cloture` tout
  seul). Coordination utile avec un autre agent ? `session.canal: { cible,
  message }` prérempli.
- `heure` est TOUJOURS renseigné, à côté de `date` : deux artefacts ouverts
  côte à côte ne se départagent qu'à l'heure.
- Tous les textes en français, ton direct, zéro remplissage.

## Schéma DATA

```js
const DATA = {
  type: "avancement",                      // avancement | decision | visuel | cloture
  titre: "Projet : objet du point",        // court
  agent: "claude-code : skoole",           // qui parle
  date: "24/08/2026",
  heure: "23h40",                          // obligatoire : départage deux artefacts ouverts
  contexte: "1 phrase de cadrage maximum", // optionnel
  liens: [                                 // optionnel, portée générale
    { label: "Le site en local", url: "http://localhost:4321/" },
    { label: "Lire le TODO", doc: "todo" } // doc : ouvre un document embarqué
  ],
  documents: [                             // déclarés par CHEMIN, embarqués par cp_build.py
    { id: "todo", label: "TODO du projet", fichier: "_LLM/TODO.md" }
  ],
  essentiel: [                             // FACULTATIF, 5 max
    { texte: "...", statut: "fait" }       // fait | encours | bloque | info
  ],
  decisions: [                             // 6 max, ids D1, D2, ...
    { id: "D1", type: "choix",             // options exclusives
      question: "...", detail: "...",
      liens: [ { label: "Lire la fiche", doc: "todo" } ],
      options: [
        { id: "A", label: "...", desc: "pourquoi", reco: true },
        { id: "B", label: "...", desc: "..." }
      ] },
    { id: "D2", type: "image",             // variantes visuelles
      multiple: true,                      // plusieurs validables d'un coup
      question: "...",
      options: [
        { id: "A", label: "Avant", image: "data:image/jpeg;base64,..." },
        { id: "B", label: "Après", image: "data:image/jpeg;base64,...", reco: true }
      ],
      refaire: true },                     // ajoute la tuile « À refaire »
    { id: "D3", type: "validation", question: "..." },   // oui / à modifier
    { id: "D4", type: "texte", question: "..." },        // réponse libre (dictée)
    { id: "D5", type: "multi", question: "...", options: [] }
  ],
  visuels: [                               // type "visuel" : galerie, sélection MULTIPLE
    { id: "V1", label: "Variante A", image: "data:image/jpeg;base64,...", desc: "...", reco: true }
  ],
  // --- blocs de CLÔTURE (type: "cloture") ---
  bilan:   [ { texte: "ce qui a été fait", statut: "fait" } ],
  reste:   [ { texte: "ce qui reste, consigné au TODO", statut: "info" } ],
  reprise: "Markdown du message de reprise proposé pour la prochaine session",
  // ou, mieux, le vrai START copié par l'outil, sans le réécrire :
  // reprise_fichier: "_LLM/START.md",
  // --- fin des blocs de clôture ---
  suites: {                                // JAMAIS rendu sur une clôture
    mode: "multi",                         // multi | single | ordre
    propositions: [ { id: "S1", label: "...", desc: "...", reco: true } ]
  },
  session: { cloture: false, canal: null }
};
```

Chaque décision, quel que soit son type, offre d'office : un champ de
commentaire libre (l'humain peut dicter à la voix), un bouton « En rediscuter » et un
bouton « Plus tard ». Les liens s'ouvrent dans un nouvel onglet (l'artefact garde les réponses
déjà saisies). L'humain peut aussi coller ou déposer des captures
d'écran dans la section Captures, agrandir toute image en plein écran pour
juger les détails (bouton d'agrandissement, clic pour la taille réelle,
fond clair ou sombre), les annoter en PLEIN ÉCRAN (tracé, cercle, flèche,
texte, croix de fermeture ; sur une capture, un champ au pied du panneau
permet de dicter ce qu'elle montre, gardé avec la capture au Valider) et
exporter le PNG annoté, et dispose en fin d'artefact d'un champ Remarques
pour toute consigne libre (remarques, idées, choses à faire). Limite connue :
un artefact republié à DISTANCE (visionneuse claude.ai) bloque tout
téléchargement déclenché par la page, liens download et data: compris ;
l'export des PNG annotés ne marche donc que depuis le fichier local
`_LLM/checkpoints/*.html` ouvert en file://. Quand l'humain est à distance,
les captures se collent dans le CHAT ; au poste, le fichier local fait tout. L'artefact
est TOUJOURS en thème sombre et en mise en page standard (décision de Cyril du
13/11/2026) : plus de bascule clair / sombre ni aéré / compact, et un champ
`affichage` dans DATA est sans effet. Si aucun type ne convient, utiliser `choix` avec des options sur
mesure : ne jamais inventer d'autre structure.

## Protocole RETOUR (à parser quand l'utilisateur le colle)

Le bouton « Copier le retour » génère ce format exact :

```
## RETOUR CHECKPOINT : <titre> : <jj/mm/aaaa hh:mm>

### D1 : <question>
- Statut : Répondu | À rediscuter | Plus tard | En attente
- Décision : <label de l'option>            (absent si aucune ; « À refaire » possible)
- Réponse : <texte libre>                   (type texte uniquement)
- Commentaire : <texte libre>               (autres types, si renseigné)
- Annotation : CP-D1-A-annote.png (PNG exporté depuis l'artefact, joint à ce message)

### Visuels retenus                     (bloc visuels, sélection multiple)
- V1 : <label>

### Captures jointes
- C1 (CP-cap-C1.png, exportée depuis l'artefact : à joindre à ce message) : <commentaire>

### Observations sur documents          (section absente si vide)
- <label> (<chemin du document>) :
> <texte de l'humain, lignes préfixées par > >

### Suites retenues                     (ou « Suites retenues (dans cet ordre) »)
- S1 : <label>                            (mode ordre : « 1. S3 : <label> », « 2. S1 : ... »)
- SP1 : <label> (ajoutée par vous)        (suite écrite par l'humain dans l'artefact)

### Remarques
<texte libre : remarques, idées, choses à faire>      (section absente si vide)

### Session
- Clôture demandée : oui (...) | non
- Message CANAL : oui : destinataire <nom>
> <message, lignes préfixées par > >
```

Compatibilité : accepter aussi l'ancien en-tête « ## RETOUR POINT DE DECISION » et les fichiers PD-*.png (artefacts produits avant le renommage de la skill).

Ordre de traitement par l'agent, dans cet ordre exact :

1. « À rediscuter » d'abord : pour chacun, poser 1 à 2 questions ciblées ou
   reformuler des options, avant toute exécution.
2. Appliquer les décisions « Répondu », en tenant compte des commentaires.
   Les « Observations sur documents » se traitent au même rang : chacune
   porte sur le FICHIER nommé (correction à y faire, réponse à la question
   posée, désaccord) ; appliquer ou répondre, et le dire dans la synthèse.
   « À refaire » sur un visuel : refaire en corrigeant précisément ce que
   montre l'annotation ou le commentaire, puis soumettre un nouveau point
   de décision avec l'ancienne et la nouvelle version côte à côte.
3. « Plus tard » : consigner dans `_LLM/TODO.md` (section « Mis de côté »,
   avec la date et l'identifiant Dx). Ne pas relancer le sujet.
4. « En attente » : ne rien décider à la place de l'humain ; redemander
   uniquement si la décision bloque la suite.
5. Annotations et captures : le copier-coller ne transporte que du texte,
   les images n'arrivent jamais avec le bloc. Les fichiers listés (CP-*.png)
   sont téléchargés par l'artefact dans le dossier Téléchargements.
   En Claude Code : aller les lire soi-même AVANT de les demander, par une
   recherche RÉCURSIVE dans le dossier Téléchargements, triée par date, et
   jamais par un simple `ls ~/Downloads` : sur un poste rangé (règle de tri,
   dossier d'archive, action Finder), le fichier a déjà quitté la racine
   quelques secondes après son arrivée, et l'agent conclut à tort qu'il n'a
   rien reçu. La commande qui marche :
   `find ~/Downloads -iname 'CP-*.png' -o -iname 'PD-*.png'`, puis trier par
   date de modification et prendre les plus récents. En chat : demander de
   glisser les fichiers depuis Téléchargements dans le message. Ne jamais
   agir sur une image non vue.
5bis. « Visuels retenus » : traiter comme une décision répondue. Aucun visuel
   retenu et des annotations exportées : c'est un « à refaire », aller lire les
   PNG avant de reprendre le travail.
6. Suites retenues : dérouler la première suite, puis les autres dans
   l'ordre listé (en mode ordre, l'ordre est celui voulu par l'humain, ne pas
   le réorganiser). Une suite « (ajoutée par vous) » est une consigne de
   l'humain à part entière : la traiter au même titre que les autres.
7. Remarques : ce sont des consignes libres de l'humain. Ce qui relève du
   travail en cours : l'appliquer ou l'intégrer au plan. Ce qui est hors
   périmètre ou pour plus tard : le consigner dans `_LLM/TODO.md` avec la
   date. Ne jamais ignorer cette section.
8. Session :
   - Clôture : mettre à jour `_LLM/JOURNAL.md` et `_LLM/TODO.md` selon le kit
     du projet, puis préparer le message de reprise pour la prochaine
     session (START).
   - CANAL : rédiger le message pour l'agent destinataire et le déposer par
     le canal du projet, que l'agent connaît (contrat `CANAL.md`, dossier
     partagé ou autre dispositif en place). Sans canal connu, fournir le
     message prêt à transmettre.

## Snippet à coller dans la charte (AGENTS.md) de chaque projet

```markdown
## Restitution et décisions (obligatoire)
- Toute restitution (fin de tâche, point d'étape, choix à valider, fin de
  session) passe par la skill `checkpoint` : artefact HTML interactif.
- Jamais de long résumé en prose ; message de chat : 3 lignes maximum.
- Quand un bloc « ## RETOUR CHECKPOINT » est collé, le parser et
  l'appliquer selon la skill (rediscuter d'abord, plus tard dans TODO).
- Aucun tiret quadratin dans les textes générés.
```

## Ne pas faire

- Ne pas produire de résumé en prose en parallèle de l'artefact.
- Ne pas modifier le moteur du template (CSS, JS) : seulement DATA.
- Ne pas dépasser 6 décisions ni 5 puces d'essentiel.
- Ne pas omettre la recommandation ferme sur une décision.
- Ne pas mettre d'images par URL externe.
- Ne pas demander de valider un texte sans donner le lien pour le lire.
- Ne pas donner un lien `file://` vers un markdown : le déclarer dans `documents`.
- Ne pas recopier à la main le contenu d'un document : `cp_build.py` le copie.
- Ne pas donner un lien `http://localhost` sans avoir vérifié que le serveur répond.
- Ne pas mettre de suites ni de questions de relance dans une clôture.
- Ne pas resservir le même `essentiel` d'un checkpoint au suivant.
- Ne pas oublier le chemin de l'artefact en dernière ligne du message.
- Ne pas mettre un `choix` là où plusieurs réponses peuvent coexister.
- Ne pas trancher soi-même un point « En attente » ou « À rediscuter ».
- Ne pas utiliser de tiret quadratin.
