# AutoApply (Streamlit Web App) — Elmoncy Edition

Run a **web app** (no local storage) to find, score, tailor, and track job applications. 
Deployed on **Streamlit Cloud** with data persisted to **Google Sheets** and downloadable files in the browser.

## One‑click Deploy (Streamlit Cloud)
1) Create a **GitHub repo** and upload this folder (or use the ZIP below).
2) Go to https://share.streamlit.io/ → **Deploy an app** and point to your repo.
3) In Streamlit Cloud → **App settings → Secrets**, paste:
```toml
# Required only if you want Google Sheets sync / Telegram pings
GOOGLE_SHEETS_CREDS_JSON = "<<<paste the entire service account JSON here>>>"
TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""
```
4) Press **Deploy**. Open the app, adjust filters, click buttons.

## Local dev (optional)
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Files of note
- `streamlit_app.py` – the web UI
- `config.yaml` – defaults (also editable in the app)
- `data/skills.yaml` – scoring skills list
- `data/companies_*.txt` – company slugs for Greenhouse/Lever
- `autoapply/` – core logic
