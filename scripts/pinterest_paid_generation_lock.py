#!/usr/bin/env python3
"""Before ANY OpenAI image call, create a durable paid-attempt lock.
If a batch fails partially, GitHub's future hourly retries cannot quietly
regenerate already-billed output. Do not override without explicit approval.
"""
import datetime as dt,json,os
from pathlib import Path
from zoneinfo import ZoneInfo
ROOT=Path(__file__).resolve().parent.parent
date=dt.datetime.now(ZoneInfo("America/Detroit")).date().isoformat()
manifest=ROOT/"pinterest-research"/date/"manifest.json"
output=ROOT/"pinterest-publishing-ledger"/(date+".json")
lock=ROOT/"pinterest-generation-attempts"/(date+".json")
if output.exists():
    j=json.loads(output.read_text())
    if len(j.get("original_new_images") or [])==9:
        print("Already completed: no new paid-generation lock needed.")
        raise SystemExit(0)
    raise SystemExit("BLOCKED: partial output receipt exists. Do not auto-retry paid image generation.")
if lock.exists():
    raise SystemExit("BLOCKED: previous paid attempt recorded; do not silently regenerate or charge again.")
if not manifest.is_file():
    raise SystemExit("No valid today's research yet; do not lock or call image API.")
research=json.loads(manifest.read_text())
concepts=research.get("pin_concepts") or []
assert research.get("date")==date and len(concepts)==9
assert sum(c.get("content_type")=="free_pdf" for c in concepts)>=3
assert os.environ.get("OPENAI_IMAGE_QUALITY")=="high" and os.environ.get("OPENAI_IMAGE_MODEL")=="gpt-image-2"
lock.parent.mkdir(parents=True,exist_ok=True)
lock.write_text(json.dumps({"date":date,"state":"paid_generation_reservation","approved_batches":1,
"model":"gpt-image-2","quality":"high","count":9,"estimated_output_usd":1.485,
"estimated_input_allowance_usd":0.12,"max_estimated_total_usd":2,
"reserved_at":dt.datetime.now(dt.timezone.utc).isoformat(),
"notice":"Fail-closed: if an image API call fails, no automatic second batch without user approval."},indent=2)+"\n")
print("Created pre-API, durable cost-and-retry lock:",lock)
