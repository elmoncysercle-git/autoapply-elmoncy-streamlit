from __future__ import annotations
import os, datetime, pandas as pd
from .config import load_config
from . import filters as F
from . import scoring as S
from .tailor import render_cover, simple_reason
from .tracker import append_csv, upsert_sheet
from .notify import maybe_notify
from .sources import greenhouse, lever

def fetch_and_rank(cfg):
    jobs = []
    jobs += greenhouse.fetch_all(cfg.sources.greenhouse_companies_file, cfg.sources.max_per_company)
    jobs += lever.fetch_all(cfg.sources.lever_companies_file, cfg.sources.max_per_company)
    kept=[]
    for j in jobs:
        ok, hits = F.passes(j, cfg)
        if not ok: continue
        score, detail = S.score(j, hits, cfg)
        kept.append({**j, "score": score, "include_hits": ",".join(hits.get("include_hits",[])), "skill_hits": ",".join(detail.get("skill_hits",[]))})
    kept.sort(key=lambda r: r["score"], reverse=True)
    return kept

def run_search(cfg):
    rows = fetch_and_rank(cfg)
    out_dir = cfg.general.out_dir
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"jobs_{datetime.date.today().isoformat()}.csv")
    pd.DataFrame(rows).to_csv(path, index=False)
    if rows: append_csv(cfg.tracker.csv_path, rows)
    return path, rows

def run_tailor(cfg, df):
    out_dir = os.path.join(cfg.general.out_dir, "cover_letters")
    os.makedirs(out_dir, exist_ok=True)
    written = []
    for _, r in df.iterrows():
        ctx = {
            "company_name": r.get("company","") or None,
            "job_title": r.get("title","") or None,
            "matched_keywords": [k for k in str(r.get("include_hits","")).split(",") if k],
            "tools_hit": [k for k in str(r.get("skill_hits","")).split(",") if k],
            "reason": simple_reason(r.to_dict())
        }
        txt = render_cover(cfg.tailor.cover_template, ctx)
        fname = f"{(r.get('company','company') or 'company').replace('/','-')}_{(r.get('title','role') or 'role').replace('/','-')}.md"
        full = os.path.join(out_dir, fname)
        with open(full, "w") as f: f.write(txt)
        written.append(full)
    return out_dir, written
