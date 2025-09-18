from __future__ import annotations
import requests, time
def companies_from_file(path):
    try:
        with open(path,'r') as f:
            return [l.strip() for l in f if l.strip() and not l.strip().startswith('#')]
    except FileNotFoundError: return []
def fetch_company(slug, max_items=100):
    url = f"https://api.lever.co/v0/postings/{slug}?mode=json"
    try:
        r = requests.get(url, timeout=20); r.raise_for_status()
        data = r.json()
    except Exception: return []
    out=[]
    for j in data[:max_items]:
        out.append({
            "source":"lever",
            "company": j.get("company", slug),
            "title": j.get("text",""),
            "location": (j.get("categories") or {}).get("location",""),
            "url": j.get("hostedUrl") or j.get("applyUrl",""),
            "description": j.get("descriptionPlain","") or j.get("description","")
        })
    return out
def fetch_all(path, max_items=100):
    out=[]
    for slug in companies_from_file(path):
        out.extend(fetch_company(slug, max_items)); time.sleep(0.3)
    return out
