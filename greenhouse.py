from __future__ import annotations
import requests, time
def companies_from_file(path):
    try:
        with open(path,'r') as f:
            return [l.strip() for l in f if l.strip() and not l.strip().startswith('#')]
    except FileNotFoundError: return []
def fetch_company(slug, max_items=100):
    url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
    try:
        r = requests.get(url, timeout=20); r.raise_for_status()
        data = r.json().get('jobs',[])
    except Exception: return []
    out=[]
    for j in data[:max_items]:
        out.append({
            "source":"greenhouse",
            "company": slug,
            "title": j.get("title",""),
            "location": j.get("location",{}).get("name",""),
            "url": j.get("absolute_url",""),
            "description": j.get("content","") or ""
        })
    return out
def fetch_all(path, max_items=100):
    out=[]
    for slug in companies_from_file(path):
        out.extend(fetch_company(slug, max_items)); time.sleep(0.3)
    return out
