#!/usr/bin/env python3
"""Manual Pinterest queue builder. Never schedules social posts or calls image API."""
import json
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parent.parent
base="https://whatsforeats.online/"
out=ROOT/"pinterest-command-center/manual-queue.json"
existing=json.loads(out.read_text(encoding="utf-8")) if out.exists() else {"pins":[]}
items=existing.get("pins",[])
def valid_slug(s):
 return isinstance(s,str) and s.endswith(".html") and ".." not in s and (ROOT/s).is_file()
for manifest_file in sorted((ROOT/"pinterest-research").glob("*/manifest.json")):
 date=manifest_file.parent.name
 if date<"2026-10-29":continue # Previous day's two failed manual pins are preserved.
 manifest=json.loads(manifest_file.read_text(encoding="utf-8"))
 if manifest.get("date")!=date:continue
 concepts=manifest.get("pin_concepts") or []
 if len(concepts)!=9 or sum(x.get("content_type")=="free_pdf" for x in concepts)<3:continue
 redo=ROOT/"pinterest-publishing-ledger"/f"{date}-redo.json"
 standard=ROOT/"pinterest-publishing-ledger"/f"{date}.json"
 chosen=redo if redo.is_file() else standard
 if not chosen.is_file():continue
 log=json.loads(chosen.read_text(encoding="utf-8"))
 entries=log.get("original_new_images") or []
 dirname=date+"-redo" if chosen==redo else date
 if len(entries)!=9:continue
 if not all((ROOT/"pinterest-daily-pins"/dirname/x["filename"]).is_file() for x in entries):
  print("Waiting for full nine images before publishing any queue updates for",date)
  continue
 if any(not valid_slug(c.get("destination_slug")) for c in concepts):
  print("One or more destination links not local/real",date);continue
 if any((ROOT/c.get("pdf_slug","")).is_file() is False for c in concepts if c.get("content_type")=="free_pdf"):
  print("Free printable missing, refusing incomplete manual queue",date);continue
 new=[]
 for c,pic in zip(concepts,entries):
  current=next((x for x in items if x.get("date")==date and x.get("destination_url")==base+c["destination_slug"]),None)
  entry=dict(current or {})
  entry.update(date=date,content_type=c.get("content_type","recipe"),image_url=base+"pinterest-daily-pins/"+dirname+"/"+pic["filename"],
      title=c["seo_title"],description=c["description"],destination_url=base+c["destination_slug"],
      pdf_slug=c.get("pdf_slug"),status="READY_FOR_MANUAL_POST",
      image_sha256=pic["image_sha256"],image_model=log.get("original_new_images",[{}])[0].get("image_model","gpt-image-2"),
      image_quality=pic.get("image_quality",log.get("quality","medium")),
      winning_style=pic.get("winning_style"),research_ref_ids=pic.get("reference_ids"),source_ledger=str(chosen.relative_to(ROOT)))
  if current and current.get("image_url")!=entry["image_url"]:
   entry["prior_original_image_url"]=current.get("prior_original_image_url") or current.get("image_url")
  new.append(entry)
 items=[x for x in items if x.get("date")!=date]+new
 print(f"Updated manual queue: {date} | {len(new)} images | 3+ free PDFs | variant {dirname}")
existing["pins"]=items
existing["mode"]="manual_only"
existing["instructions"]="Download the original pin image, then copy its SEO title, description and accurate destination into Pinterest manually. Never auto-post with Metricool or RSS."
existing["updated_at"]=datetime.now(timezone.utc).isoformat()
out.write_text(json.dumps(existing,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print("Manual queue total",len(items))
