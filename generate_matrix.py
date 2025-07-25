#!/usr/bin/env python3
"""
Generate a Markdown matrix of all Infinite Backrooms conversations.

- Reads the master index JSON (backrooms_recreation/original_conversations/_chronological_master.json)
- Outputs a Markdown table (backrooms_matrix.md) with columns:
    Filename | Scenario | Timestamp | CMS Date | Source URL
- Each row links to the source URL.
- Table is sorted chronologically.
- Usage: python3 generate_matrix.py
"""
import json
import os

MASTER_INDEX = "backrooms_recreation/original_conversations/_chronological_master.json"
OUTPUT_MD = "backrooms_matrix.md"

if not os.path.exists(MASTER_INDEX):
    print(f"Master index not found: {MASTER_INDEX}")
    exit(1)

with open(MASTER_INDEX, "r") as f:
    data = json.load(f)

# Header
headers = ["Filename", "Scenario", "Timestamp", "CMS Date", "Source URL"]
lines = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]

for entry in data:
    filename = entry.get("filename", "")
    scenario = filename.split("scenario_")[-1].replace(".txt", "") if "scenario_" in filename else ""
    timestamp = entry.get("timestamp", "")
    cms_date = entry.get("cms_date", "")
    url = entry.get("source_url", "")
    lines.append(f"| {filename} | {scenario} | {timestamp} | {cms_date} | [link]({url}) |")

with open(OUTPUT_MD, "w") as f:
    f.write("\n".join(lines))

print(f"Matrix written to {OUTPUT_MD}") 