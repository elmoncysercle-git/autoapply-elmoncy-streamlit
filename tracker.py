from __future__ import annotations
import os, json
import pandas as pd
def ensure_dir(path): os.makedirs(os.path.dirname(path), exist_ok=True)
def append_csv(path, rows):
    if not rows: return
    ensure_dir(path)
    df = pd.DataFrame(rows)
    if not os.path.exists(path): df.to_csv(path, index=False)
    else: df.to_csv(path, mode='a', header=False, index=False)
def _client(creds_json_path: str = ""):
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    env = os.getenv("GOOGLE_SHEETS_CREDS_JSON","")
    if env.strip().startswith("{"):
        info = json.loads(env)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(info, scopes)
    elif creds_json_path and os.path.exists(creds_json_path):
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_json_path, scopes)
    else:
        raise RuntimeError("Google Sheets credentials not found.")
    return gspread.authorize(creds)
def upsert_sheet(rows, sheet_name, creds_json_path=""):
    if not rows: return
    gc = _client(creds_json_path)
    try: sh = gc.open(sheet_name)
    except Exception: sh = gc.create(sheet_name)
    ws = sh.sheet1
    headers = list(rows[0].keys())
    try:
        existing = ws.get_all_values()
        if not existing: ws.clear(); ws.append_row(headers)
    except Exception:
        ws.clear(); ws.append_row(headers)
    for r in rows: ws.append_row([r.get(h,"") for h in headers])
