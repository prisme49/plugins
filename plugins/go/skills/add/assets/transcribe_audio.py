#!/usr/bin/env python3
"""Transcription audio intégrale via l'API Gemini (kit go). Zéro dépendance : Python standard.

Usage :
  python3 transcribe_audio.py --input note.m4a --out /tmp/transcription.md [--model auto] [--consigne "..."]
Clé lue dans GEMINI_API_KEY (environnement, sinon .env.local du dossier courant), jamais affichée.
Audio < 19 Mo : envoi inline. Au-delà : upload via la Files API puis référence.
Modèle : GEMINI_AUDIO_MODEL si défini, sinon le meilleur modèle gemini pro disponible.
"""
import argparse, base64, json, mimetypes, os, re, sys, time, urllib.request

API = "https://generativelanguage.googleapis.com/v1beta"
UPLOAD = "https://generativelanguage.googleapis.com/upload/v1beta/files"
FALLBACK_MODEL = "gemini-3.1-pro-preview"
MIMES = {".mp3": "audio/mpeg", ".wav": "audio/wav", ".ogg": "audio/ogg", ".m4a": "audio/mp4",
         ".webm": "audio/webm", ".flac": "audio/flac", ".aac": "audio/aac"}

SYSTEME = """Tu es un assistant de transcription. Transcris fidèlement cet enregistrement audio en français.
Consignes : transcris TOUT ce qui est dit, mot à mot, hésitations et répétitions comprises ; identifie les
changements de locuteur (**Locuteur 1 :**, **Locuteur 2 :**, ou le prénom s'il est identifiable) ; ponctuation
naturelle du français oral ; [inaudible] pour les passages peu clairs, [pause] pour les pauses significatives ;
saut de ligne aux changements de sujet. Ne résume pas, ne reformule pas, ne corrige pas l'oral."""


def env_var(name):
    v = os.environ.get(name, "").strip()
    if not v and os.path.exists(".env.local"):
        for line in open(".env.local", encoding="utf-8", errors="ignore"):
            m = re.match(rf"\s*{name}\s*=\s*(.+)\s*$", line)
            if m:
                v = m.group(1).strip().strip('"').strip("'")
    return v


def http(url, payload=None, headers=None, raw=None, method=None):
    data = raw if raw is not None else (json.dumps(payload).encode() if payload is not None else None)
    h = {"Content-Type": "application/json"}
    h.update(headers or {})
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    with urllib.request.urlopen(req, timeout=600) as r:
        return r.headers, r.read()


def pick_model(key):
    forced = env_var("GEMINI_AUDIO_MODEL")
    if forced:
        return forced
    try:
        _, body = http(f"{API}/models?pageSize=200&key={key}")
        names = [m["name"].split("/")[-1] for m in json.loads(body).get("models", [])
                 if "generateContent" in m.get("supportedGenerationMethods", [])
                 and "pro" in m["name"] and "image" not in m["name"] and "veo" not in m["name"] and "tts" not in m["name"]]
        if names:
            names.sort()
            return names[-1]
    except Exception as e:
        print(f"(liste des modèles indisponible : {e}, repli sur {FALLBACK_MODEL})", file=sys.stderr)
    return FALLBACK_MODEL


def upload_file(key, path, mime):
    size = os.path.getsize(path)
    h, _ = http(f"{UPLOAD}?key={key}",
                payload={"file": {"display_name": os.path.basename(path)}},
                headers={"X-Goog-Upload-Protocol": "resumable", "X-Goog-Upload-Command": "start",
                         "X-Goog-Upload-Header-Content-Length": str(size),
                         "X-Goog-Upload-Header-Content-Type": mime})
    url = h.get("X-Goog-Upload-URL")
    _, body = http(url, raw=open(path, "rb").read(),
                   headers={"Content-Type": mime, "X-Goog-Upload-Offset": "0",
                            "X-Goog-Upload-Command": "upload, finalize"})
    f = json.loads(body)["file"]
    for _ in range(60):  # attendre l'état ACTIVE
        if f.get("state") == "ACTIVE":
            return f["uri"]
        time.sleep(2)
        _, body = http(f"{API}/{f['name']}?key={key}")
        f = json.loads(body)
    sys.exit("Le fichier uploadé n'est jamais passé ACTIVE côté Gemini.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="auto")
    ap.add_argument("--consigne", default="Réalise une retranscription fidèle et complète de cet audio.")
    a = ap.parse_args()

    key = env_var("GEMINI_API_KEY")
    if not key:
        sys.exit("GEMINI_API_KEY introuvable : ajoutez-la dans .env.local (clé sur aistudio.google.com/apikey).")
    mime = MIMES.get(os.path.splitext(a.input)[1].lower())
    if not mime:
        sys.exit("Format non supporté. Formats acceptés : " + ", ".join(MIMES))
    model = pick_model(key) if a.model == "auto" else a.model

    if os.path.getsize(a.input) < 19 * 1024 * 1024:
        audio_part = {"inline_data": {"mime_type": mime,
                                      "data": base64.b64encode(open(a.input, "rb").read()).decode()}}
    else:
        audio_part = {"file_data": {"file_uri": upload_file(key, a.input, mime), "mime_type": mime}}

    payload = {"systemInstruction": {"parts": [{"text": SYSTEME}]},
               "contents": [{"role": "user", "parts": [audio_part, {"text": a.consigne}]}],
               "generationConfig": {"mediaResolution": "MEDIA_RESOLUTION_HIGH"}}

    def call(p):
        _, body = http(f"{API}/models/{model}:generateContent?key={key}", payload=p)
        return json.loads(body)

    try:
        out = call(payload)
    except urllib.error.HTTPError as e:
        msg = e.read().decode(errors="ignore")[:400]
        if "mediaResolution" in msg or "media_resolution" in msg:
            payload["generationConfig"].pop("mediaResolution", None)
            out = call(payload)
        else:
            sys.exit(f"Erreur API ({e.code}) avec le modèle {model} : {msg}")

    parts = out.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    text = "".join(p.get("text", "") for p in parts).strip()
    if not text:
        sys.exit("Transcription vide : vérifier la qualité de l'audio ou le quota de la clé.")
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    open(a.out, "w", encoding="utf-8").write(text + "\n")
    print(f"transcription écrite : {a.out} (modèle : {model}, {len(text)} caractères)")


if __name__ == "__main__":
    main()
