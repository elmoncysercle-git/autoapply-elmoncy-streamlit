import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import os, io, datetime, pandas as pd, yaml, json
import streamlit as st

from pathlib import Path
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import os, io, datetime, pandas as pd, yaml, json
import streamlit as st
from autoapply.config import load_config, AppConfig
from autoapply.main import run_search, run_tailor
from autoapply.tracker import upsert_sheet

st.set_page_config(page_title="AutoApply — Elmoncy", page_icon="🧭", layout="wide")
st.title("AutoApply — Elmoncy Edition")

# Load config
with open("config.yaml","r") as f:
    cfg_dict = yaml.safe_load(f) or {}
cfg = load_config("config.yaml")

st.sidebar.header("Filters")
inc = st.sidebar.text_area("Include keywords (comma-separated)", ", ".join(cfg.filters.include_keywords))
exc = st.sidebar.text_area("Exclude keywords (comma-separated)", ", ".join(cfg.filters.exclude_keywords))
remote_only = st.sidebar.checkbox("Remote only", value=cfg.filters.remote_only)
seniority = st.sidebar.text_input("Seniority levels (comma-separated)", ", ".join(cfg.filters.seniority_levels))

if st.sidebar.button("Save Filters"):
    cfg_dict["filters"]["include_keywords"] = [s.strip() for s in inc.split(",") if s.strip()]
    cfg_dict["filters"]["exclude_keywords"] = [s.strip() for s in exc.split(",") if s.strip()]
    cfg_dict["filters"]["remote_only"] = bool(remote_only)
    cfg_dict["filters"]["seniority_levels"] = [s.strip() for s in seniority.split(",") if s.strip()]
    with open("config.yaml","w") as f:
        yaml.safe_dump(cfg_dict, f)
    st.sidebar.success("Filters saved to config.yaml")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔎 Search Jobs"):
        cfg = load_config("config.yaml")
        csv_path, rows = run_search(cfg)
        st.session_state["last_csv"] = csv_path
        st.success(f"Found {len(rows)} jobs. Saved to {csv_path}.")
        if rows:
            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True)
            st.download_button("Download CSV", data=df.to_csv(index=False).encode(), file_name=os.path.basename(csv_path), mime="text/csv")

with col2:
    if st.button("✍️ Generate Cover Letters"):
        cfg = load_config("config.yaml")
        csv_path = st.session_state.get("last_csv", os.path.join(cfg.general.out_dir, f"jobs_{datetime.date.today().isoformat()}.csv"))
        if not os.path.exists(csv_path):
            st.error("No CSV found. Run Search Jobs first.")
        else:
            df = pd.read_csv(csv_path)
            out_dir, files = run_tailor(cfg, df)
            st.success(f"Generated {len(files)} cover letters → {out_dir}")
            if files:
                # bundle into a zip in memory
                import zipfile
                mem = io.BytesIO()
                with zipfile.ZipFile(mem, "w", zipfile.ZIP_DEFLATED) as z:
                    for path in files:
                        z.write(path, os.path.basename(path))
                st.download_button("Download Cover Letters (zip)", data=mem.getvalue(), file_name="cover_letters.zip")

with col3:
    if st.button("📝 Push to Google Sheets"):
        try:
            cfg = load_config("config.yaml")
            csv_path = st.session_state.get("last_csv", os.path.join(cfg.general.out_dir, f"jobs_{datetime.date.today().isoformat()}.csv"))
            if not os.path.exists(csv_path):
                st.error("No CSV found. Run Search Jobs first.")
            else:
                df = pd.read_csv(csv_path); rows = df.to_dict(orient="records")
                if not cfg.tracker.google_sheets.enabled:
                    st.warning("Google Sheets integration is disabled in config.yaml")
                else:
                    # Reads creds from st.secrets['GOOGLE_SHEETS_CREDS_JSON'] if present
                    if "GOOGLE_SHEETS_CREDS_JSON" in st.secrets:
                        os.environ["GOOGLE_SHEETS_CREDS_JSON"] = st.secrets["GOOGLE_SHEETS_CREDS_JSON"]
                    upsert_sheet(rows, cfg.tracker.google_sheets.sheet_name, cfg.tracker.google_sheets.creds_json_path)
                    st.success(f"Pushed {len(rows)} rows to Google Sheet: {cfg.tracker.google_sheets.sheet_name}")
        except Exception as e:
            st.error(f"Google Sheets push failed: {e}")

st.divider()
st.subheader("Companies Lists")
c1, c2 = st.columns(2)
with c1:
    st.caption("Greenhouse company slugs (one per line)")
    gh_text = st.text_area("Greenhouse", open("data/companies_greenhouse.txt").read(), height=200)
with c2:
    st.caption("Lever company slugs (one per line)")
    lv_text = st.text_area("Lever", open("data/companies_lever.txt").read(), height=200)

if st.button("Save Company Lists"):
    with open("data/companies_greenhouse.txt","w") as f: f.write(gh_text.strip()+"\n")
    with open("data/companies_lever.txt","w") as f: f.write(lv_text.strip()+"\n")
    st.success("Company lists saved.")

st.divider()
st.subheader("Tailoring Assets")
colA, colB = st.columns(2)
with colA:
    st.caption("Résumé (markdown) used for context or downloads")
    resume_md = open("resume/base_resume.md").read()
    st.download_button("Download Résumé (md)", data=resume_md.encode(), file_name="resume.md")
with colB:
    st.caption("Cover letter template (Jinja2).")
    tpl = open("resume/cover_letter_template.md").read()
    st.download_button("Download Cover Letter Template", data=tpl.encode(), file_name="cover_letter_template.md")
