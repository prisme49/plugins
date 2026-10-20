---
name: gen
description: "Génère une image depuis un prompt via l'API Gemini (modèles image type Nano Banana) et la range dans _GEN/ avec son prompt tracé. Déclencher quand l'utilisateur dit « /gen », « gen », « génère une image », « generate », « fais-moi un visuel », « crée une illustration », ou demande une image dans un projet équipé du kit go."
---

# gen : générer une image

Claude ne génère pas d'images nativement : cette compétence le fait via l'API Gemini de Google, avec la clé de l'utilisateur. Elle produit l'image, la range, et trace le prompt.

## Règles permanentes

- Tout en français. Aucun tiret quadratin.
- Ne JAMAIS afficher la valeur de GEMINI_API_KEY (ni d'aucun secret) : seuls les noms de variables se citent.
- `_GEN/` (racine, hors Git) accueille les images générées ; créé au premier usage avec son INDEX.md.
- Jamais d'image imitant une personne réelle identifiable ni de logo de marque tierce, sauf demande explicite de l'humain.

## Procédure

1. La clé : vérifier que `GEMINI_API_KEY` est renseignée dans `.env.local` (lire uniquement le NOM et la présence d'une valeur, jamais la valeur). Absente : expliquer qu'il faut créer une clé sur aistudio.google.com/apikey et la coller dans `.env.local` (ligne GEMINI_API_KEY=...), puis s'arrêter là.
2. Les règles du projet : lire `_LLM/RULES.md`. Si une charte de génération d'images y vit (styles imposés, interdits, formats, ton), elle s'applique à chaque génération sans qu'on ait à la répéter.
3. Le prompt : construire un prompt solide à partir du brief de l'humain en suivant `assets/GUIDE-PROMPTS.md` (sujet précis, style, composition, lumière, texte entre guillemets, format). Enrichir un brief maigre sans le trahir ; montrer le prompt final si l'humain le demande.
4. Générer : exécuter le script embarqué (zéro dépendance, Python standard) :

```
python3 <dossier de cette compétence>/assets/gen_image.py \
  --prompt "..." \
  --out _GEN/AAAA-MM-JJ-<slug>.png \
  [--model auto] [--ratio 16:9] [--input chemin/image.png]
```

   - Le script lit GEMINI_API_KEY depuis l'environnement ou le .env.local du projet.
   - `--model auto` (défaut) interroge l'API et choisit le modèle image le plus récent disponible ; la variable `GEMINI_IMAGE_MODEL` dans .env.local force un modèle précis.
   - `--input` permet l'édition : partir d'une image existante et la modifier selon le prompt.
5. Tracer : ajouter une ligne à `_GEN/INDEX.md` : | date | fichier | modèle | prompt |. Créer le dossier et l'index au premier usage (en-tête : "# _GEN : images générées. Hors Git. Une ligne par image.").
6. Montrer : afficher l'image à l'humain. Pour un choix entre variantes ou une validation avant usage, passer par un checkpoint de type image (avec la tuile À refaire).

## Notes

- Ce même script fonctionne dans tous les projets équipés du kit : il vit dans le plugin, pas dans le projet.
- Coût : la génération d'images Gemini est facturée sur la clé de l'utilisateur ; en cas d'usage intensif, le signaler.
- Pas de vidéo dans cette version : si l'humain demande une vidéo, le dire honnêtement et proposer une piste (Veo via la même clé, non couvert par le script actuel).
