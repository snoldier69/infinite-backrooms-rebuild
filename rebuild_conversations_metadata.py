#!/usr/bin/env python3
"""
Rebuild conversations_metadata.json with system_prompts, context, roles, num_turns, and all metadata fields, matching the UniversalBackrooms template format (student, spirituality, etc).
- For each .txt in backrooms_recreation/original_conversations:
  - Extract system prompts and context for each actor, matching order and format of templates.
  - Extract roles (actor names), num_turns, timestamp, cms_date, filename, models, temperature.
  - If {lm1_actor} or {lm2_actor} placeholders are present, extract and include.
  - Use .html as fallback for missing blocks.
- Output conversations_metadata.json with all fields, matching template structure.
"""
import os
import re
import json
from datetime import datetime

CONVO_DIR = 'backrooms_recreation/original_conversations'
OUT_PATH = 'backrooms_recreation/metadata/conversations_metadata.json'

# Helper: extract blocks between <Actor#TAG> and next <...>
def extract_blocks(content, tagtype):
    pattern = re.compile(r'<([^>#]+)#' + tagtype + r'>\s*', re.IGNORECASE)
    matches = list(pattern.finditer(content))
    blocks = []
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i+1].start() if i+1 < len(matches) else len(content)
        block = content[start:end].strip()
        actor = m.group(1).strip()
        blocks.append((actor, block))
    return blocks

# Helper: extract {lm1_actor}, {lm2_actor} placeholders
lm_actor_pattern = re.compile(r'\{(lm[12]_actor)\}', re.IGNORECASE)
def extract_lm_actors(content):
    return list(set(lm_actor_pattern.findall(content)))

def extract_metadata(txt_path, html_path=None):
    with open(txt_path, encoding='utf-8') as f:
        content = f.read()
    # If html exists, read for fallback
    html_content = ''
    if html_path and os.path.exists(html_path):
        with open(html_path, encoding='utf-8') as f:
            html_content = f.read()
    # Extract actors, models, temp
    actors = []
    models = []
    temperature = []
    actors_match = re.search(r'actors:\s*(.+)', content)
    if actors_match:
        actors = [a.strip() for a in actors_match.group(1).split(',')]
    models_match = re.search(r'models:\s*(.+)', content)
    if models_match:
        models = [m.strip() for m in models_match.group(1).split(',')]
    temp_match = re.search(r'temp:\s*(.+)', content)
    if temp_match:
        temperature = [float(t.strip()) for t in temp_match.group(1).split(',')]
    # Extract system prompts and context for each actor
    sys_blocks = extract_blocks(content, 'SYSTEM')
    ctx_blocks = extract_blocks(content, 'CONTEXT')
    # Fallback to html if missing
    if html_content:
        if not sys_blocks:
            sys_blocks = extract_blocks(html_content, 'SYSTEM')
        if not ctx_blocks:
            ctx_blocks = extract_blocks(html_content, 'CONTEXT')
    # Map by actor order in actors list
    system_prompts = [''] * len(actors)
    contexts = [[] for _ in actors]
    for i, actor in enumerate(actors):
        # Find first matching block for this actor (case-insensitive, allow partial match)
        for a, block in sys_blocks:
            if a.lower() in actor.lower() or actor.lower() in a.lower():
                system_prompts[i] = block.strip()
                break
        for a, block in ctx_blocks:
            if a.lower() in actor.lower() or actor.lower() in a.lower():
                try:
                    ctx = json.loads(block)
                    if isinstance(ctx, list):
                        contexts[i] = ctx
                except Exception:
                    pass
                break
    # Extract conversation turns (all <Actor> ... blocks not #SYSTEM/#CONTEXT)
    turn_pattern = re.compile(r'<([^>#]+)>\s*(.*?)(?=<[^>]+>|$)', re.DOTALL)
    conversation_turns = []
    for m in turn_pattern.finditer(content):
        actor = m.group(1).strip()
        if '#SYSTEM' in actor or '#CONTEXT' in actor:
            continue
        text = m.group(2).strip()
        if text:
            conversation_turns.append({'actor': actor, 'content': text})
    # Extract timestamp from filename
    base = os.path.basename(txt_path)
    timestamp = None
    m = re.match(r'conversation_(\d+)_scenario_', base)
    if m:
        timestamp = int(m.group(1))
    # Extract cms_date from html if present
    cms_date = None
    if html_content:
        m = re.search(r'Last Published: ([^<\n]+)', html_content)
        if m:
            try:
                cms_date = m.group(1).strip()
            except Exception:
                pass
    # Extract lm1_actor, lm2_actor placeholders
    lm_actors = extract_lm_actors(content)
    # Build roles (same as actors)
    roles = actors[:]
    # Compose metadata entry
    meta = {
        'timestamp': timestamp,
        'cms_date': cms_date,
        'filename': base,
        'system_prompts': system_prompts,
        'contexts': contexts,
        'roles': roles,
        'models': models,
        'actors': actors,
        'temperature': temperature,
        'num_turns': len(conversation_turns)
    }
    if lm_actors:
        meta['lm_actors'] = lm_actors
    return meta

def main():
    all_meta = []
    for fname in os.listdir(CONVO_DIR):
        if fname.endswith('.txt'):
            txt_path = os.path.join(CONVO_DIR, fname)
            html_path = txt_path.replace('.txt', '.html')
            meta = extract_metadata(txt_path, html_path)
            all_meta.append(meta)
    # Sort by cms_date (if present), then timestamp
    def sortkey(m):
        if m['cms_date']:
            try:
                dt = datetime.strptime(m['cms_date'][:24], '%a %b %d %Y %H:%M:%S')
                return (dt, m['timestamp'] or 0)
            except Exception:
                pass
        return (datetime.min, m['timestamp'] or 0)
    all_meta.sort(key=sortkey)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(all_meta, f, indent=2)
    print(f"Wrote {len(all_meta)} entries to {OUT_PATH}")

if __name__ == '__main__':
    main() 