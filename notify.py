from __future__ import annotations
import os, requests
def maybe_notify(rows, chat_env="TELEGRAM_CHAT_ID", token_env="TELEGRAM_BOT_TOKEN"):
    token = os.getenv(token_env,""); chat = os.getenv(chat_env,"")
    if not token or not chat or not rows: return
    base = f"https://api.telegram.org/bot{token}/sendMessage"
    lines = [f"• {r.get('title')} @ {r.get('company')} — {r.get('location')}\n{r.get('url')} (score {r.get('score')})" for r in rows[:10]]
    requests.post(base, json={"chat_id": chat, "text": "New roles:\n" + "\n".join(lines)})
