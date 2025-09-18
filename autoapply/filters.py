from __future__ import annotations
import re
def _hits(text, terms):
    text_l = text.lower()
    return [t for t in terms if re.search(r'\b'+re.escape(t.lower())+r'\b', text_l)]
def passes(job, cfg):
    blob = ' '.join([job.get('title',''), job.get('location',''), job.get('description','')])
    inc = _hits(blob, cfg.filters.include_keywords)
    exc = _hits(blob, cfg.filters.exclude_keywords)
    if exc: return False, {'include_hits': inc}
    if cfg.filters.remote_only and 'remote' not in job.get('location','').lower():
        return False, {'include_hits': inc}
    title_l = job.get('title','').lower()
    if not cfg.filters.allow_internships and ('intern' in title_l or 'internship' in title_l):
        return False, {'include_hits': inc}
    return True, {'include_hits': inc}
