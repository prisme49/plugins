#!/usr/bin/env python3
"""Génération d'image via l'API Gemini (kit go). Zéro dépendance : Python standard.

Usage :
  python3 gen_image.py --prompt "un phare breton sous l'orage, photo" --out _GEN/2026-08-19-phare.png
Options :
  --model auto|<nom>   auto (défaut) : choisit le modèle image le plus récent disponible.
                       Peut être forcé par la variable GEMINI_IMAGE_MODEL (.env.local).
  --ratio 16:9         format d'image si le modèle le supporte (1:1, 16:9, 9:16, 4:3, 3:4...).
  --input chemin.png   image de départ pour une édition (le prompt décrit la modification).
La clé est lue dans GEMINI_API_KEY (environnement, sinon .env.local du dossier courant).
La clé n'est jamais affichée.
"""
import argparse, base64, json, mimetypes, os, re, sys, urllib.request

API = "https://generativelanguage.googleapis.com/v1beta"
FALLBACK_MODEL = "gemini-2.5-flash-image"  # mis à jour par --model auto quand l'API répond


def load_key():
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key and os.path.exists(".env.local"):
        for line in open(".env.local", encoding="utf-8", errors="ignore"):
            m = re.match(r"\s*GEMINI_API_KEY\s*=\s*(.+)\s*$", line)
            if m:
                key = m.group(1).strip().strip('"').strip("'")
                break
    if not key:
        sys.exit("GEMINI_API_KEY introuvable : ajoutez-la dans .env.local (clé sur aistudio.google.com/apikey).")
    return key


def http_json(url, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read().decode())


def pick_model(key):
    forced = os.environ.get("GEMINI_IMAGE_MODEL", "").strip()
    if not forced and os.path.exists(".env.local"):
        for line in open(".env.local", encoding="utf-8", errors="ignore"):
            m = re.match(r"\s*GEMINI_IMAGE_MODEL\s*=\s*(.+)\s*$", line)
            if m:
                forced = m.group(1).strip()
    if forced:
        return forced
    try:
        out = http_json(f"{API}/models?pageSize=200&key={key}")
        names = [m["name"].split("/")[-1] for m in out.get("models", [])
                 if "image" in m["name"] and "generateContent" in m.get("supportedGenerationMethods", [])]
        names = [n for n in names if "veo" not in n]
        if names:
            names.sort()  # les noms Gemini croissent avec la version : le dernier est le plus récent
            return names[-1]
    except Exception as e:
        print(f"(liste des modèles indisponible : {e}, repli sur {FALLBACK_MODEL})", file=sys.stderr)
    return FALLBACK_MODEL


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="auto")
    ap.add_argument("--ratio", default=None)
    ap.add_argument("--input", default=None)
    a = ap.parse_args()

    key = load_key()
    model = pick_model(key) if a.model == "auto" else a.model

    parts = [{"text": a.prompt}]
    if a.input:
        mime = mimetypes.guess_type(a.input)[0] or "image/png"
        parts.append({"inline_data": {"mime_type": mime,
                                      "data": base64.b64encode(open(a.input, "rb").read()).decode()}})
    payload = {"contents": [{"parts": parts}],
               "generationConfig": {"responseModalities": ["IMAGE", "TEXT"]}}
    if a.ratio:
        payload["generationConfig"]["imageConfig"] = {"aspectRatio": a.ratio}

    try:
        out = http_json(f"{API}/models/{model}:generateContent?key={key}", payload)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="ignore")[:400]
        if a.ratio and "imageConfig" in body:
            payload["generationConfig"].pop("imageConfig", None)  # modèle sans réglage de format : nouvel essai
            out = http_json(f"{API}/models/{model}:generateContent?key={key}", payload)
        else:
            sys.exit(f"Erreur API ({e.code}) avec le modèle {model} : {body}")

    for part in out.get("candidates", [{}])[0].get("content", {}).get("parts", []):
        blob = part.get("inlineData") or part.get("inline_data")
        if blob and blob.get("data"):
            os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
            open(a.out, "wb").write(base64.b64decode(blob["data"]))
            print(f"image écrite : {a.out} (modèle : {model})")
            return
    texts = [p.get("text", "") for p in out.get("candidates", [{}])[0].get("content", {}).get("parts", [])]
    sys.exit("Pas d'image dans la réponse. Message du modèle : " + " ".join(t for t in texts if t)[:400])


if __name__ == "__main__":
    main()
