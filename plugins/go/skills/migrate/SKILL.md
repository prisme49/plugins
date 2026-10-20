---
name: migrate
description: "Fait entrer un projet EXISTANT dans le kit go sans rien casser : inventaire complet du dépôt, plan de migration détaillé (quels dossiers créés, quels fichiers déplacés où, ce que devient la charte existante, AGENTS.md ou CLAUDE.md), soumis à l'humain par checkpoint, appliqué SEULEMENT après acceptation. Déclencher quand l'utilisateur dit « /migrate », « migre ce projet », « fais passer ce projet au kit », « installe go sur un projet existant », ou quand start ou new détectent un projet riche sans kit."
---

# migrate : adopter le kit sans casser l'existant

Un projet en route a déjà son organisation, ses habitudes, parfois sa propre charte (AGENTS.md ou CLAUDE.md) et son application en développement. La migration se PROPOSE, elle ne s'impose jamais.

## Garde-fou : est-ce bien `migrate` qu'il fallait ?

AVANT l'inventaire, regarder le dossier courant :

| Ce qu'on voit | Ce que c'est | La question à poser |
| --- | --- | --- |
| `_LLM/START.md` existe | Le projet est DÉJÀ sous kit | « Ce projet est déjà migré (version du kit vue : <x>, START du <date>). `migrate` rejouerait une adoption sur une structure en place. Tu voulais `start` ? » |
| Un dossier vide ou quasi vide | Rien à faire entrer | « Il n'y a que <n> fichiers ici : il n'y a rien à migrer, `new` pose la structure directement. On fait `new` ? » |
| `_LLM/` partiel (des fichiers du kit manquent) | Migration interrompue | « Le kit est là mais incomplet : il manque <liste>. Je reprends la migration là où elle s'est arrêtée, ou tu préfères un plan complet ? » |

> **Principe du garde-fou** : quand ce qui est demandé ne colle pas à ce que
> montre le dossier, on ne corrige pas tout seul et on n'exécute pas quand même.
> On dit ce qu'on VOIT, avec les faits (dates, nombre de fichiers, dernier
> commit), on pose UNE question, et on attend. Aucune modification avant la
> réponse. C'est l'humain qui décide du rituel, pas l'agent.

## Principes non négociables

1. La migration ne touche QUE l'organisation : jamais le code, jamais l'application, jamais les données de production, jamais les fichiers de build ou de déploiement. Le doute profite au fichier : on ne le déplace pas.
2. Rien n'est appliqué avant l'acceptation explicite du plan par l'humain (checkpoint).
3. Rien n'est supprimé : uniquement des créations et des déplacements ; l'ancien qui n'a plus de place va dans _TRASH/.
4. Si le projet est un dépôt Git : commit de sauvegarde AVANT d'appliquer quoi que ce soit (retour arrière garanti).

## Procédure

### Phase 1 : inventaire (lecture seule)
- Parcourir tout le dépôt : arborescence, tailles, ce qui ressemble à du code, de la documentation, des pièces, des notes, des secrets, du généré.
- Lire la charte existante s'il y en a une (AGENTS.md, CLAUDE.md, CLAUDE.local.md), les README, tout fichier de conventions ou de suivi (TODO, notes de session, anciens journaux).
- Identifier ce qui correspond déjà aux rôles du kit : où vit l'état, où vit l'historique, où vivent les règles, où vivent les documents.

### Phase 2 : le plan de migration (document, pas action)
Écrire un plan DÉTAILLÉ dans `_LLM/checkpoints/` ou en corps de checkpoint, qui liste :
- les dossiers créés (_LLM, _ADD, _DOCS, _TRASH, .env.local...) ;
- chaque déplacement, fichier par fichier ou famille par famille : quoi, d'où, vers où, pourquoi ;
- ce que devient la charte existante : redécoupée, pas remplacée (le permanent reste dans la charte, les consignes de travail partent dans _LLM/RULES.md, l'historique dans _LLM/JOURNAL.md, l'état courant dans _LLM/START.md). La cible est UN SEUL `AGENTS.md` : un CLAUDE.md existant est renommé (`git mv CLAUDE.md AGENTS.md`) SI le Claude du poste le lit nativement (`claude --version` donne 2.1.277 ou plus récent, réglage « Project instructions » de /config pas sur claude-md seul), sinon il reste CLAUDE.md et le renommage est noté au TODO. Un CLAUDE.local.md résiduel est signalé : il masquerait l'AGENTS.md sans message ;
- ce qui n'est PAS touché (l'application, les builds, les configs de déploiement), listé explicitement ;
- le courrier, si le projet en a déjà : un `.amqrc` versionné doit passer en LOCAL (ajouté au .gitignore, déversé de l'index par `git rm --cached`) et un `.amqrc.example` prendre sa place dans le dépôt. Il porte un chemin absolu et un handle : deux postes ne peuvent pas partager le même fichier ;
- les points douteux, avec une recommandation ferme pour chacun.
Soumettre par checkpoint : accepter, amender, ou refuser.

### Phase 3 : appliquer (seulement après acceptation)
- Commit de sauvegarde, puis exécuter le plan tel qu'accepté, rien de plus.
- Régénérer _DOCS/INDEX.md si des pièces ont été rangées, écrire l'entrée JOURNAL de migration, rédiger le START de reprise.
- Vérifier : l'application démarre ou se construit comme avant (si vérifiable), rien n'a disparu (tout écart est dans _TRASH).

### Si l'humain refuse ou reporte
Le projet peut utiliser le kit PARTIELLEMENT (checkpoint, gen, send/inbox fonctionnent sans la structure complète). Dans ce cas, inscrire en tête de la charte du projet (AGENTS.md ou CLAUDE.md ; la créer minimale au besoin) la mention :
« Kit go : migration NON enclenchée le <date>. Organisation historique en vigueur ; utiliser /migrate pour la proposer à nouveau. »
Ainsi, tout agent qui arrive sait à quoi s'en tenir et ne mélange pas les deux mondes.
