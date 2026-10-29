#!/usr/bin/env python3
"""Produce publicly safe, dated Pinterest Command Center data from repo receipts."""
import os,json,datetime as dt,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
BASE="https://whatsforeats.online"
REPO="fatboylove5885/Rescue_Kit_Home"
GH="https://github.com/"+REPO
LIB="https://drive.google.com/drive/folders/1TzX-um3SpktjJ9jh1gP8F0cYbOHbcvHd"
def read(path):
 try:return json.loads((ROOT/path).read_text(encoding="utf-8"))
 except (ValueError,OSError):return {}
def refpath(p):return GH+"/blob/main/"+p
def event(date,title,description,severity="info",phase="system",at=None,url=None,source="Recorded artifact"):
 return dict(date=date,title=title,description=description,severity=severity,phase=phase,at=at,url=url,source=source)
def build_day(date):
 rp=f"pinterest-research/{date}/manifest.json";ip=f"pinterest-publishing-ledger/{date}.json";sp=f"pinterest-scheduling-ledger/{date}.json";vp=f"pinterest-status-snapshots/{date}.json";ap=f"pinterest-activity/{date}.json"
 m=read(rp);img=read(ip);sch=read(sp);snap=read(vp);act=read(ap)
 generated={v.get("destination_slug"):v for v in img.get("original_new_images",[]) if v.get("destination_slug")}
 receipts={v.get("recipe_slug"):v for v in sch.get("posts",[]) if v.get("recipe_slug")}
 observed={str(p.get("post_id")):p for p in snap.get("posts",[]) if p.get("post_id")}
 pins=[]
 for c in m.get("pin_concepts",[]):
  slug=c.get("destination_slug")
  if not slug:continue
  i=generated.get(slug,{}) ; r=receipts.get(slug,{})
  v=observed.get(str(r.get("post_id")),{})
  filename=i.get("filename"); image_path=f"pinterest-daily-pins/{date}/{filename}" if filename else None
  available=bool(image_path and (ROOT/image_path).is_file())
  state=str(v.get("status") or r.get("status") or ("IMAGE_READY" if available else "RESEARCHED")).upper()
  pins.append(dict(id=c.get("id"),date=date,title=c.get("seo_title") or c.get("headline"),headline=c.get("headline"),
   description=c.get("description"),link=BASE+"/"+slug,slug=slug,image_url=BASE+"/"+image_path if available else None,
   image_available=available,image_model=i.get("image_model"),image_sha256=i.get("image_sha256"),image_created_at=i.get("created_at"),
   scene=c.get("food_scene"),layout=c.get("layout"),content_type=c.get("content_type","recipe"),pdf_slug=c.get("pdf_slug"),reference_ids=c.get("research_ref_ids") or [],
   keywords=([c.get("primary_keyword")]+(c.get("secondary_keywords") or [])) if c.get("primary_keyword") else [],
   board=c.get("board_suggestion") or "Not recorded",provider_board_id=r.get("board_id"),
   status=state,status_source="Metricool snapshot" if v else ("Metricool receipt" if r else "GitHub artifact"),
   status_observed_at=snap.get("observed_at") if v else None,schedule_time=r.get("publish_at"),
   post_id=r.get("post_id"),auto_publish=r.get("auto_publish"),planner_url=r.get("planner_url"),
   media_url=r.get("media"),source_manifest_url=refpath(rp)))
 for r in act.get("historical_posts",[]):
  slug=r.get("recipe_slug")
  if not slug or any(p["slug"]==slug and p.get("post_id")==r.get("post_id") for p in pins):continue
  v=observed.get(str(r.get("post_id")),{})
  pins.append(dict(id=r.get("post_id"),date=date,title=r.get("pin_title"),headline=r.get("pin_title"),
   description=r.get("description"),link=r.get("link"),slug=slug,image_url=r.get("image_url"),
   image_available=bool(r.get("image_url")),image_model="Not recorded",image_sha256=None,image_created_at=None,
   scene="Source scene not fully logged",layout="Not recorded",content_type="recipe",pdf_slug=None,reference_ids=[],keywords=[],board="Quick Dinner Recipes",
   provider_board_id=r.get("board_id"),status=str(v.get("status") or r.get("status") or "UNKNOWN").upper(),
   status_source="Metricool snapshot" if v else "Historical receipt",
   status_observed_at=snap.get("observed_at") if v else r.get("observed_at"),schedule_time=r.get("publish_at"),
   post_id=r.get("post_id"),auto_publish=r.get("auto_publish"),planner_url=r.get("planner_url"),
   media_url=r.get("media_url"),source_manifest_url=None))
 # Manual queue is authoritative for user-ready assets; keep old provider receipts as history.
 manual=read("pinterest-command-center/manual-queue.json")
 manual_rows={p.get("destination_url"):p for p in manual.get("pins",[]) if p.get("date")==date}
 for p in pins:
  match=manual_rows.get(p.get("link"))
  if not match:continue
  p["image_url"]=match.get("image_url") or p.get("image_url")
  p["image_available"]=bool(p.get("image_url"))
  p["image_sha256"]=match.get("image_sha256") or p.get("image_sha256")
  p["image_model"]=match.get("image_model") or p.get("image_model")
  p["image_quality"]=match.get("image_quality")
  p["image_variant"]=match.get("image_variant")
  p["winning_style"]=match.get("winning_style")
  p["status"]=match.get("status","READY_FOR_MANUAL_POST")
  p["status_source"]="GitHub verified manual queue"
  p["manual_posting"]=True
  p["auto_publish"]=False
  p["schedule_time"]=None
 refs=[]
 for r in m.get("reference_images",[]):
  path=str(r.get("archive_file") or "")
  refs.append(dict(id=r.get("id"),date=date,type=r.get("type"),pin_url=r.get("pin_url"),
   file_name=path.rsplit("/",1)[-1] if path else None,archive_status=r.get("archive_status"),
   design_notes=r.get("visual_features"),metric_status=r.get("metric_status"),
   label=r.get("label") or "Observed visual reference, not a proven winner",private_library_url=LIB))
 ev=[]
 if m:ev.append(event(date,"Daily Pinterest research saved",f'{len(refs)} documented references and {len(m.get("pin_concepts",[]))} creative briefs.',"success","research",m.get("research_completed_at"),refpath(rp)))
 if generated:ev.append(event(date,"New original images created",f'{len(generated)} GPT Image source artifacts with individual hashes.',"success","generation",min(x.get("created_at") or date for x in generated.values()),refpath(ip)))
 if sch:ev.append(event(date,"Metricool scheduling receipt saved",f'{len(sch.get("posts",[]))} provider IDs. Scheduling is not proof of publication.',"success","scheduling",sch.get("verified_at"),refpath(sp)))
 if snap:
  counts={}
  for p in snap.get("posts",[]):
   key=p.get("status","UNKNOWN");counts[key]=counts.get(key,0)+1
  ev.append(event(date,"Metricool publishing status observed",", ".join(f"{k}: {v}" for k,v in counts.items()),"success" if counts.get("PUBLISHED") else "info","publishing",snap.get("observed_at"),refpath(vp)))
 for a in act.get("events",[]):ev.append(event(date,a.get("title","Activity"),a.get("description",""),a.get("severity","info"),a.get("phase","system"),a.get("at"),a.get("url"),a.get("source","Operations journal")))
 ev.sort(key=lambda e:e.get("at") or date,reverse=True)
 generated_count=sum(1 for p in pins if p.get("image_model")=="gpt-image-2" and p.get("image_available"))
 nsch=sum(1 for p in pins if p.get("post_id"))
 npub=sum(1 for p in pins if p.get("status")=="PUBLISHED")
 nr=sum(r.get("archive_status")=="saved_in_drive" for r in refs)
 warn=sum(e["severity"] in ("warning","error") for e in ev)
 free_pdf_count=sum(p.get("content_type")=="free_pdf" for p in pins)
 xp=20*bool(m)+10*nr+15*generated_count+15*nsch+20*npub
 missions=[
  dict(name="Research done",done=bool(m),details="Dated Pinterest manifest exists"),
  dict(name="Reference vault stocked",done=nr>=3,details="Three or more references archived privately"),
  dict(name="9 original food images",done=generated_count>=9,details="Nine distinct photos in repository"),
  dict(name="3 free printables",done=free_pdf_count>=3 if date>="2026-10-29" else True,details="At least 3 of the 9 daily posts feature real free PDFs"),
  dict(name="9 posts scheduled",done=nsch>=9,details="Nine provider post IDs accepted"),
  dict(name="9 posts published",done=npub>=9,details="Verified PUBLISHED on provider")]
 if date>="2026-10-29":
  manual_ready=sum(p.get("status")=="READY_FOR_MANUAL_POST" for p in pins)
  missions[-2]=dict(name="9 manual pins ready",done=manual_ready>=9,details="Nine copy-ready original images, SEO titles, descriptions and verified links")
  missions[-1]=dict(name="Manual posting by owner",done=False,details="Ready for the owner to post; no automatic Pinterest publishing")
 src=[("Research manifest",rp,m),("Image ledger",ip,img),("Scheduling receipt",sp,sch),("Provider status snapshot",vp,snap),("Operations history",ap,act)]
 return dict(date=date,status="manual_ready" if date>="2026-10-29" and sum(p.get("status")=="READY_FOR_MANUAL_POST" for p in pins)>=9 else "published" if npub>=9 else "scheduled" if nsch>=9 else "generated" if generated_count>=9 else "research" if m else "partial",
  totals=dict(concepts=len(m.get("pin_concepts",[])),references=len(refs),archived_refs=nr,original_images=generated_count,
  scheduled_receipts=nsch,published_verified=npub,free_pdf_pins=free_pdf_count,incidents=warn,xp=xp),missions=missions,
  pins=pins,references=refs,events=ev,audit_note=m.get("audit_note") or "No research manifest",
  evidence_sources=m.get("evidence_sources") or [],
  raw_sources=[dict(label=n,url=refpath(p),available=bool(obj)) for n,p,obj in src],
  status_snapshot_at=snap.get("observed_at"),reviewed_at=m.get("research_completed_at"))
def api(url):
 try:
  headers={"Accept":"application/vnd.github+json","User-Agent":"wfe-pinterest-command-center"}
  token=os.environ.get("GITHUB_TOKEN")
  if token:headers["Authorization"]="Bearer "+token
  with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=12) as r:return json.load(r)
 except Exception as e:print("Run-history endpoint unavailable:",str(e)[:100]);return {}
def main():
 dates=set()
 for path in ["pinterest-research/*/manifest.json","pinterest-publishing-ledger/*.json","pinterest-scheduling-ledger/*.json","pinterest-status-snapshots/*.json","pinterest-activity/*.json"]:
  for f in ROOT.glob(path):dates.add(f.parent.name if f.name=="manifest.json" else f.stem)
 days=[build_day(d) for d in sorted(dates,reverse=True) if len(d)==10 and d[4]=="-" and d[7]=="-"]
 summary={k:sum(d["totals"][k] for d in days) for k in ["concepts","references","archived_refs","original_images","scheduled_receipts","published_verified","free_pdf_pins","incidents","xp"]}
 summary.update(days_recorded=len(days),daily_target=9,latest_date=days[0]["date"] if days else None,daily_research_streak=0)
 for d in days:
  if d["missions"][0]["done"]:summary["daily_research_streak"]+=1
  else:break
 actions=api(f"https://api.github.com/repos/{REPO}/actions/runs?per_page=100")
 runs=[dict(id=x.get("id"),name=x.get("name"),event=x.get("event"),status=x.get("status"),conclusion=x.get("conclusion"),
   created_at=x.get("created_at"),updated_at=x.get("updated_at"),url=x.get("html_url"),attempt=x.get("run_attempt"))
   for x in actions.get("workflow_runs",[]) if any(word in str(x.get("name","")).lower() for word in ["pinterest","dashboard"])]
 catalog=read("pinterest-freebie-catalog.json")
 audit=read("pinterest-activity/free-pdf-product-promotion-audit.json")
 report=dict(schema_version=2,updated_at=dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
   site="What's For Eats — Pinterest Command Center",timezone="America/Detroit",visibility="PUBLIC_SITE_METADATA_ONLY",
   security_notice="Public dashboard. No API keys, user account emails, or private reference screenshots are embedded.",
   library_url=LIB,github_repo=GH,metricool_url="https://app.metricool.com/planner/calendar?blogId=4488790",
   pipeline=["Competitor Pinterest research","Private reference library archive","Daily 9-concept research manifest",
   "GPT Image 2 original photographs within $2 daily estimated budget","GitHub image receipts and manual-ready queue","Owner copies images, SEO text and links into Pinterest",
   "Historical Metricool provider status retained for past posts"],
   known_limits=[
    dict(title="Public website",detail="Any visitor can access operational metadata; raw private Drive assets and secrets are excluded."),
    dict(title="Status snapshot, not live feed",detail="Metricool statuses update only when a connected agent writes a verified snapshot."),
    dict(title="Manual posting only",detail="No Metricool or RSS auto-posting. Image generation requires validated $2 per-day budget."),
    dict(title="Image storage growth",detail="Nine new JPG images per day grow the same GitHub site by roughly 90-135 MB monthly; a CDN may be needed later."),
    dict(title="No invented metrics",detail="Pinterest clicks, saves and impressions remain unknown until trustworthy account records are connected.")],
   stats=summary,days=days,runs=runs[:55],
   free_pdf_strategy={"daily_minimum":3,"daily_total":9,"verified_inventory":len(catalog.get("items",[])),
    "verified_promoted_pdf_files":audit.get("count"),"source":"pinterest-freebie-catalog.json"})
 out=ROOT/"pinterest-command-center/data.json";out.parent.mkdir(parents=True,exist_ok=True)
 out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
 print(f"Command Center: {len(days)} days, {sum(len(d['pins']) for d in days)} posts, {len(runs)} runs")
if __name__=="__main__":main()
