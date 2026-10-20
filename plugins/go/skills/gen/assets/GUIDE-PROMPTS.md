# Guide : parler à Gemini pour générer une image

## La structure d'un bon prompt (dans cet ordre)

1. Le sujet, précis : qui ou quoi, en train de faire quoi. "Un phare breton battu par une tempête" bat "un phare".
2. Le style : photo (préciser objectif et pellicule si voulu), illustration flat, aquarelle, 3D isométrique, pixel art, schéma technique...
3. La composition : cadrage (gros plan, plan large, vue de dessus), position du sujet, profondeur de champ.
4. La lumière et la palette : heure dorée, néon, lumière douce de studio ; 2 ou 3 couleurs dominantes.
5. Le texte à afficher, s'il y en a : le mettre entre guillemets et court ("le titre \"RADAR\" en haut à gauche"). Les modèles récents gèrent bien le texte court, mal les paragraphes.
6. Le format : passé au script via --ratio (1:1, 16:9, 9:16, 4:3, 3:4) plutôt que décrit dans le prompt.

## Ce qui marche

- Une seule idée forte par image ; les prompts fleuves diluent.
- Décrire ce qu'on VEUT, pas ce qu'on ne veut pas ("fond uni crème" plutôt que "pas de fond chargé").
- Le français fonctionne ; pour les styles très codifiés, les termes anglais consacrés aident (flat design, isometric, film grain).
- Itérer en changeant UNE chose à la fois ; pour retoucher une image existante : --input image.png et un prompt qui décrit uniquement la modification ("remplace le ciel par un ciel d'orage, ne touche à rien d'autre").

## Pièges connus

- Texte long ou accents dans l'image : vérifier le rendu, régénérer au besoin.
- Mains, foules, instruments : demander un cadrage qui les évite si le résultat déçoit.
- Cohérence de série (même personnage, même style sur 10 images) : réutiliser la première image en --input, ou fixer une charte dans _LLM/RULES.md.

## Exemples

- "Illustration flat design d'un radar stylisé balayant des icônes d'articles de presse, palette bleu nuit et orange, fond uni crème, composition centrée, style minimaliste" --ratio 16:9
- "Photo culinaire vue de dessus d'une tarte aux pommes rustique sur une table en bois clair, lumière naturelle de fin d'après-midi, torchon en lin beige, style magazine" --ratio 4:3
- Édition : --input logo.png + "place ce logo sur la poche d'un tee-shirt gris porté, photo en extérieur, flou d'arrière-plan"

## Le réflexe kit

Avant toute génération : lire _LLM/RULES.md. Si le projet a une charte d'images (le cahier des charges d'un site, des interdits, un style maison), elle prime sur ce guide.
