from __future__ import annotations
import yaml
def skills_from(path):
    with open(path,'r') as f:
        y = yaml.safe_load(f) or {}
    return [s.lower() for s in (y.get('skills') or [])]
def score(job, hits, cfg):
    skills = skills_from(cfg.scoring.skills_file)
    text = (job.get('title','') + ' ' + job.get('description','')).lower()
    skill_hits = [s for s in skills if s in text]
    remote_bonus = cfg.scoring.weight_remote if 'remote' in job.get('location','').lower() else 0.0
    score = cfg.scoring.weight_keyword_hit*len(hits.get('include_hits',[])) + cfg.scoring.weight_skill_hit*len(skill_hits) + remote_bonus
    return round(score,2), {'skill_hits': skill_hits}
