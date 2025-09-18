from __future__ import annotations
from jinja2 import Template
def simple_reason(job):
    t = job.get('title','').lower(); d = job.get('description','').lower()
    if 'revenue' in t: return "the focus on revenue operations and reconciliations"
    if 'audit' in t: return "the emphasis on audit rigor and cross-functional collaboration"
    if 'netsuite' in d: return "your use of NetSuite and process improvement"
    return "your emphasis on accuracy, collaboration, and continuous improvement"
def render_cover(template_path: str, context: dict) -> str:
    with open(template_path,'r') as f:
        return Template(f.read()).render(**context)
