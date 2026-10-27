#!/usr/bin/env python3
"""Build public, privacy-safe Pinterest Command Center data from verified repo records.

GH Actions automatically runs this job hourly. It never publishes GitHub/Metricool
credentials or private image files. Provider statuses are snapshots from verified
Metricool receipts and are NOT live Pinterest API telemetry.
"""
from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict
import json, os, urllib.request, urllib.error

ROOT=Path(__file__).resolve().parent.parent
DASH=ROOT/"pinterest-command-center"
REPO=os.environ.get("GITHUB_REPOSITORY","fatboylove5885/Rescue_Kit_Home")
SITE="https://whatsforeats.online/"
GITHUB="https://github.com/"+REPO+"/blob/main/"
RUNS_URL="https://api.github.com/repos/"+REPO+"/actions/runs?per_page=100"
MANIFESTS=ROOT/"pinterest-research"
PUBLISHING=ROOT/"pinterest-publishing-ledger"
SCHEDULING=ROOT/"pinterest-scheduling-ledger"
IMAGES=ROOT/"pinterest-daily-pins"
FIRST_DAYS={"2026-10-26","2026-10-27"}

def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (ValueError,OSError):
        return {}

def repo_file(path):
    return GITHUB+str(path).replace("\\","/")

def action_runs():
    token=os.environ.get("GITHUB_TOKEN")
    if not token:return []
    req=urllib.request.Request(RUNS_URL,headers={
        "Authorization":"Bearer "+token,
        "Accept":"application/vnd.github+json",
        "X-GitHub-Api-Version":"2022-11-28",
        "User-Agent":"WhatsForEats-CommandCenter"})
    try:
        with urllib.request.urlopen(req,timeout=18) as response:
            raw=json.load(response)
        return [r for r in raw.get("workflow_runs",[]) if "pinterest" in (r.get("name","").lower())][:100]
    except (urllib.error.HTTPError,urllib.error.URLError,TimeoutError) as e:
        print("Workflow run metadata not updated:",type(e).__name__)
        return []

HISTORY={
"2026-10-26":{
"events":[
 {"at":"2026-10-26T12:00:00","title":"Original Pinterest visual research archived","detail":"Three competitor visual crops and five existing brand-style examples saved privately in Google Drive. Nine article-matched briefs recorded; reference metrics not publicly verified.","level":"success"},
 {"at":"2026-10-26T18:00:00","title":"Evening Pinterest queue begins","detail":"Four unique photo-led pins scheduled for 6:00, 6:30, 7:00 and 7:30 PM Eastern, each with the correct landing article.","level":"success"},
 {"at":"2026-10-26T19:30:00","title":"Four evening posts subsequently confirmed published","detail":"Metricool provider returned PUBLISHED for all four. The earlier five preferred time slots were not verified as scheduled.","level":"success"}],
"incidents":[{"title":"Earlier five scheduled slots not completed","cause":"The day's earlier planned times had already passed when the evening recovery began.","action":"Four future evening posts were scheduled and later confirmed published; no backdating or false claims.","resolved":False}]
},
"2026-10-27":{
"events":[
 {"at":"2026-10-27T07:00:00","title":"Daily research task ran but required attention","detail":"ChatGPT research task reported requires_user_action and paused without publishing a complete result; later re-enabled.","level":"failure"},
 {"at":"2026-10-27T07:40:00","title":"Research recovery manifest committed","detail":"Three previously observed competitor images copied into today's private folder; nine new article-specific briefs saved. References honestly labeled re-observed.","level":"success","url":GITHUB+"pinterest-research/2026-10-27/manifest.json"},
 {"at":"2026-10-27T12:16:00","title":"First API-generation recovery test failed","detail":"Image endpoint returned HTTP 429. Diagnostic error handling was added.","level":"failure","url":"https://github.com/"+REPO+"/actions/runs/40539238332"},
 {"at":"2026-10-27T12:19:00","title":"API quota cause confirmed","detail":"Second test identified insufficient_quota / credit_balance_exhausted. No original images generated on this attempt.","level":"failure","url":"https://github.com/"+REPO+"/actions/runs/40539791866"},
 {"at":"2026-10-27T12:40:00","title":"API credits replenished; new creative run succeeds","detail":"All nine GPT Image 2 Medium food images generated and committed. Image-generation and GitHub deployment both succeeded.","level":"success","url":"https://github.com/"+REPO+"/actions/runs/40539791866"},
 {"at":"2026-10-27T13:00:00","title":"Nine images accepted by Metricool auto-publishing queue","detail":"Nine distinct uploaded media files and correct article links, all returned Pinterest PENDING + autoPublish true. Permanent posting ID receipt committed.","level":"success","url":GITHUB+"pinterest-scheduling-ledger/2026-10-27.json"},
 {"at":"2026-10-27T13:02:00","title":"Duplicate-post prevention added","detail":"GitHub photo pipeline now hands off to Metricool without adding the same assets to RSS. Already-added Oct 27 RSS items removed to reduce duplicate imports.","level":"success"}],
"incidents":[
 {"title":"7 AM research task interrupted","cause":"Automation required user attention with empty run result; underlying trigger not identified.","action":"Task re-enabled and same-day nine-concept research manifest manually recovered; future steps instructed to report actionable failures.","resolved":True},
 {"title":"OpenAI image-generation HTTP 429","cause":"API account returned insufficient_quota / credit_balance_exhausted. The secret was present; there were no paid credits.","action":"Diagnostic code added; user replenished API balance; subsequent nine-image generation completed successfully.","resolved":True,"url":"https://github.com/"+REPO+"/actions/runs/40539791866"},
 {"title":"8:15 AM generation did not deliver pins","cause":"No successful scheduled run observed at the expected time; the exact missed-trigger reason remains unverified.","action":"A push-triggered recovery run generated all nine images after quota was restored, with additional hourly fallback schedule.","resolved":True},
 {"title":"RSS / Metricool duplicate-import exposure","cause":"Nine images were temporarily present in both the RSS feed and the Metricool queue; Pinterest could have imported items before their removal.","action":"Newly generated images now default to Metricool-only handoff; duplicate Oct 27 RSS entries removed. Earlier external imports cannot be conclusively ruled out.","resolved":False}
]}
}

def clean_references(m):
    results=[]
    for r in m.get("reference_images",[]):
        u=r.get("pin_url") or ""
        results.append({
            "id":str(r.get("id","")),
            "type":str(r.get("type","unverified")),
            "title":str(r.get("label") or r.get("id") or "Pinterest reference").replace("_"," ")[:120],
            "pin_url":u if u.startswith("https://www.pinterest.com/") or u.startswith("https://pinterest.com/") else "",
            "visual_features":str(r.get("visual_features",""))[:800],
            "archive_status":r.get("archive_status","unverified"),
            "metric_status":r.get("metric_status","not_verified")
        })
    return results

def cleaned_evidence(m):
    return [dict(type=str(s.get("type","source"))[:150],note=str(s.get("note",""))[:800],url=s.get("url",""))
            for s in m.get("evidence_sources",[]) if str(s.get("url","")).startswith("https://")]

def collect_day(date, runindex):
    m=read_json(MANIFESTS/date/"manifest.json")
    gen=read_json(PUBLISHING/(date+".json"))
    sched=read_json(SCHEDULING/(date+".json"))
    receipts=sched.get("posts") or []
    by_slug={x.get("recipe_slug"):x for x in receipts if x.get("recipe_slug")}
    generated={x.get("destination_slug"):x for x in gen.get("original_new_images",[]) if x.get("destination_slug")}
    concept_by_slug={x.get("destination_slug"):x for x in m.get("pin_concepts",[]) if x.get("destination_slug")}
    pins=[]
    for slug,c in concept_by_slug.items():
        p=by_slug.get(slug,{})
        g=generated.get(slug,{})
        name=g.get("filename") or p.get("asset_filename")
        path=IMAGES/date/name if name else None
        exists=bool(path and path.is_file())
        accepted=bool(p.get("post_id"))
        status=p.get("status","").upper() if accepted else ("READY" if exists else "PLANNED")
        if status not in ("PUBLISHED","PENDING","SCHEDULED","FAILED","READY","PLANNED","BLOCKED"):status="UNKNOWN"
        pins.append({
            "id":str(p.get("post_id") or c.get("id") or slug),
            "slug":slug,
            "title":str(p.get("pin_title") or c.get("seo_title") or c.get("headline") or slug),
            "description":str(c.get("description") or "")[:600],
            "generated":exists,
            "status":status,
            "image_url":(SITE+"pinterest-daily-pins/"+date+"/"+name) if exists else (p.get("media") or ""),
            "destination":str(p.get("link") or (SITE+slug)),
            "planner_url":str(p.get("planner_url") or ""),
            "schedule_at":str(p.get("publish_at") or ""),
            "media_provider_uploaded":bool(p.get("media")),
            "auto_publish":bool(p.get("auto_publish")),
            "reference_ids":c.get("research_ref_ids") or [],
            "prompt_subject":str(c.get("food_scene",""))[:800],
            "primary_keyword":str(c.get("primary_keyword","")),
            "board_id":str(p.get("board_id","")),
            "provider_post_id":str(p.get("post_id","")),
            "model":g.get("image_model") or ("original hosted image" if exists else ""),
        })
    for slug,p in by_slug.items():
        if slug in concept_by_slug:continue
        filename=p.get("asset_filename")
        exists=bool(filename and (IMAGES/date/filename).is_file())
        pins.append({
            "id":str(p.get("post_id") or slug),"slug":slug,
            "title":str(p.get("pin_title") or slug),"description":"Published historical post; no matching manifest creative brief found.",
            "generated":exists,"status":str(p.get("status") or "UNKNOWN").upper(),
            "image_url":(SITE+"pinterest-daily-pins/"+date+"/"+filename) if exists else str(p.get("media") or ""),
            "destination":str(p.get("link") or (SITE+slug)),
            "planner_url":str(p.get("planner_url") or ""),"schedule_at":str(p.get("publish_at") or ""),
            "media_provider_uploaded":bool(p.get("media")),"auto_publish":bool(p.get("auto_publish")),
            "reference_ids":[],"prompt_subject":"","primary_keyword":"","board_id":str(p.get("board_id","")),
            "provider_post_id":str(p.get("post_id","")),"model":"original hosted image" if exists else ""
        })
    events=list(HISTORY.get(date,{}).get("events",[]))
    incidents=list(HISTORY.get(date,{}).get("incidents",[]))
    if m.get("research_completed_at"):
        events.append({"at":m["research_completed_at"],"title":"Pinterest research manifest saved","detail":f"{len(m.get('reference_images',[]))} visual references and {len(m.get('pin_concepts',[]))} creative briefs recorded.","level":"success","url":repo_file("pinterest-research/"+date+"/manifest.json")})
    for r in runindex.get(date,[]):
        status=(r.get("conclusion") or r.get("status") or "unknown").lower()
        started=(r.get("run_started_at") or r.get("created_at") or "")
        # GitHub emits UTC: use strict ISO and convert to local date/time text for consistent sorting.
        try:
            dt=datetime.fromisoformat(started.replace("Z","+00:00"))
            from zoneinfo import ZoneInfo
            at=dt.astimezone(ZoneInfo("America/Detroit")).replace(tzinfo=None).isoformat(timespec="seconds")
        except (ValueError,TypeError):
            at=date+"T00:00:00"
        events.append({"at":at,"title":"GitHub image publisher — "+status,
            "detail":"GitHub Actions run "+str(r.get("id"))+", trigger "+str(r.get("event") or "unknown")+". Job completion alone does not prove Pinterest published.",
            "level":"failure" if status=="failure" else ("success" if status=="success" else "info"),
            "url":r.get("html_url","")})
        if status=="failure" and date not in HISTORY:
            incidents.append({"title":"Publisher job failed","cause":"See the recorded GitHub Actions run for its exact error; no private logs are embedded on this public dashboard.","action":"Recovery guard must inspect and retry safe steps.","resolved":False,"url":r.get("html_url","")})
    events=sorted(events,key=lambda x:x.get("at",""),reverse=True)
    files=[]
    for label,path,desc in [
        ("Daily research manifest",MANIFESTS/date/"manifest.json","Raw research notes, visuals provenance and nine concepts"),
        ("Image generation ledger",PUBLISHING/(date+".json"),"Original image fingerprints, asset filenames and generation result"),
        ("Scheduling receipt",SCHEDULING/(date+".json"),"Metricool post IDs, accepted schedule, destination links and last provider status")
    ]:
        if path.is_file():
            files.append({"label":label,"path":str(path.relative_to(ROOT)),"detail":desc,"url":repo_file(path.relative_to(ROOT))})
    if (IMAGES/date).is_dir():
        files.append({"label":"Image output folder","path":"pinterest-daily-pins/"+date,"detail":"All confirmed generated food pin graphics","url":"https://github.com/"+REPO+"/tree/main/pinterest-daily-pins/"+date})
    return {
        "date":date,
        "planned_count":len(m.get("pin_concepts",[])),
        "research_completed_at":m.get("research_completed_at"),
        "audit_note":str(m.get("audit_note") or "No research memo archived.")[:1600],
        "research_status":str(m.get("status") or "not_verified"),
        "references":clean_references(m),
        "evidence_sources":cleaned_evidence(m),
        "pins":pins,
        "events":events,
        "incidents":incidents,
        "files":files,
        "generation_status":gen.get("status","none"),
        "scheduling_status":sched.get("status","none"),
        "provider_receipt_as_of":sched.get("verified_at",""),
        "provider_note":sched.get("notes",""),
        "metrics_status":"not_connected_or_unverified",
    }

def main():
    dates=set(FIRST_DAYS)
    for p in (MANIFESTS,PUBLISHING,SCHEDULING,IMAGES):
        if not p.exists():continue
        for f in p.iterdir():
            if f.is_dir() and len(f.name)==10 and f.name[:4].isdigit():dates.add(f.name)
            if f.is_file() and f.suffix==".json" and len(f.stem)==10:dates.add(f.stem)
    runs=action_runs()
    bydate=defaultdict(list)
    from zoneinfo import ZoneInfo
    for r in runs:
        try:
            iso=r.get("run_started_at") or r.get("created_at") or ""
            dt=datetime.fromisoformat(iso.replace("Z","+00:00"))
            date=dt.astimezone(ZoneInfo("America/Detroit")).date().isoformat()
            if date in dates:bydate[date].append(r)
        except (ValueError,TypeError):continue
    out={
        "schema_version":2,
        "site":"What's For Eats",
        "dashboard":"Pinterest Command Center",
        "built_at":datetime.now(timezone.utc).isoformat(),
        "timezone":"America/Detroit",
        "source":"GitHub repository research/image/scheduling ledgers plus public GitHub Actions run metadata; provider receipt snapshots are NOT live Pinterest telemetry",
        "privacy":"PUBLIC DATASET: no secrets or private reference images",
        "days":[collect_day(day,bydate) for day in sorted(dates,reverse=True)]
    }
    DASH.mkdir(exist_ok=True)
    file=DASH/"data.json"
    output=json.dumps(out,indent=2,ensure_ascii=False)+"\n"
    file.write_text(output,encoding="utf-8")
    print("Built",file,"for",len(out["days"]),"days,",sum(len(x["pins"]) for x in out["days"]),"tracked pins,",len(output),"bytes")
    for d in out["days"]:
        print(d["date"],"concepts",d["planned_count"],"pins",len(d["pins"]),"published",sum(p["status"]=="PUBLISHED" for p in d["pins"]),"queued",sum(p["status"]=="PENDING" for p in d["pins"]))

if __name__=="__main__":
    main()
