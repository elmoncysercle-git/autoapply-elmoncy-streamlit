from __future__ import annotations
import yaml
from pydantic import BaseModel
from typing import List, Dict

class General(BaseModel):
    timezone: str
    out_dir: str

class Sources(BaseModel):
    greenhouse_companies_file: str
    lever_companies_file: str
    max_per_company: int = 100

class Filters(BaseModel):
    include_keywords: List[str] = []
    exclude_keywords: List[str] = []
    locations_include: List[str] = []
    locations_exclude: List[str] = []
    remote_only: bool = False
    min_salary_usd: int = 0
    allow_internships: bool = False
    seniority_levels: List[str] = []

class Scoring(BaseModel):
    skills_file: str
    weight_keyword_hit: float = 3.0
    weight_skill_hit: float = 2.0
    weight_remote: float = 1.0

class Tailor(BaseModel):
    resume_base: str
    cover_template: str
    use_llm: bool = False

class GoogleSheets(BaseModel):
    enabled: bool = False
    sheet_name: str = "Job Tracker"
    creds_json_path: str = ""

class Tracker(BaseModel):
    csv_path: str
    google_sheets: GoogleSheets = GoogleSheets()

class TelegramCfg(BaseModel):
    enabled: bool = False
    chat_id_env: str = "TELEGRAM_CHAT_ID"
    token_env: str = "TELEGRAM_BOT_TOKEN"

class Notify(BaseModel):
    telegram: TelegramCfg = TelegramCfg()

class ApplyCfg(BaseModel):
    selenium_enabled: bool = False
    browser: str = "chrome"
    selectors: Dict[str, Dict[str, str]] = {}

class AppConfig(BaseModel):
    general: General
    sources: Sources
    filters: Filters
    scoring: Scoring
    tailor: Tailor
    tracker: Tracker
    notify: Notify
    apply: ApplyCfg

def load_config(path: str = "config.yaml") -> AppConfig:
    with open(path, "r") as f:
        data = yaml.safe_load(f) or {}
    return AppConfig(**data)
