#!/usr/bin/env python3
"""Make all downloadable What's For Eats PDFs promote relevant paid tools.

Adds ONE tasteful, clearly labeled optional resource page AFTER existing pages.
Original PDF pages are preserved byte-for-byte in rendering; prior edits are
detected by metadata to keep workflow runs idempotent.
"""
from __future__ import annotations
import io, json, pathlib
from datetime import datetime, timezone
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import HexColor, Color

ROOT=pathlib.Path(__file__).resolve().parent.parent
PDF_DIR=ROOT/"pdfs"
OUT=ROOT/"pinterest-activity"/"free-pdf-product-promotion-audit.json"
PROMO_MARKER="/WFEProductPromoV1"
RESCUE="https://whatsforeats.online/5-47-rescue-kit.html"
VAULT="https://fatboylove5885.github.io/Cheap-Dinner-Home/"
PDFS=sorted(PDF_DIR.glob("*.pdf"))
assert len(PDFS)>=19, f"Expected >=19 existing free PDFs, discovered {len(PDFS)}."

def round_rect(c,x,y,w,h,col,radius=13):
    c.setFillColor(HexColor(col));c.roundRect(x,y,w,h,radius,stroke=0,fill=1)

def promo_page():
    b=io.BytesIO(); c=Canvas(b,pagesize=(612,792))
    c.setTitle("What's for Eats - A Little More Dinner Help")
    bg=HexColor("#FFF9EF");ink=HexColor("#17392E");rust=HexColor("#B84825")
    c.setFillColor(bg);c.rect(0,0,612,792,fill=1,stroke=0)
    c.setFillColor(ink);c.roundRect(39,40,534,713,20,stroke=1,fill=0)
    round_rect(c,39,695,534,59,"#194B39",15)
    c.setFillColor(HexColor("#FFFFFF"));c.setFont("Helvetica-Bold",12)
    c.drawString(65,721,"WHAT'S FOR EATS")
    c.setFont("Helvetica",9);c.drawRightString(546,722,"FREE PRINTABLE COMPANION")
    c.setFillColor(ink);c.setFont("Times-Bold",34)
    c.drawString(64,634,"Make tomorrow's dinner")
    c.drawString(64,594,"even easier.")
    c.setFont("Helvetica",11);c.setFillColor(HexColor("#554F42"))
    c.drawString(64,560,"Your free resource is yours to keep. If you'd like more help,")
    c.drawString(64,543,"these optional tools make real-life meal planning easier.")

    round_rect(c,61,358,490,158,"#EAF2E8",15)
    c.setFillColor(ink);c.setFont("Helvetica-Bold",10);c.drawString(83,485,"DINNER PLANNING MADE SIMPLE")
    c.setFont("Times-Bold",22);c.drawString(83,449,"The 5:47 P.M. Rescue Kit")
    c.setFont("Helvetica",10);c.drawString(83,427,"Find low-effort dinners based on how much energy you have,")
    c.drawString(83,411,"plus useful planning tools for busy evenings.")
    round_rect(c,82,370,260,30,"#B84825",9)
    c.setFillColor(HexColor("#FFFFFF"));c.setFont("Helvetica-Bold",10)
    c.drawCentredString(212,381,"EXPLORE THE RESCUE KIT")
    c.linkURL(RESCUE,(82,370,342,400),relative=0)

    round_rect(c,61,176,490,158,"#F6EEE4",15)
    c.setFillColor(ink);c.setFont("Helvetica-Bold",10);c.drawString(83,303,"SHOP SMARTER FOR FAMILY MEALS")
    c.setFont("Times-Bold",22);c.drawString(83,266,"The Cheap Dinner Vault")
    c.setFont("Helvetica",10);c.drawString(83,245,"Compare low-cost dinner ideas and practical meal-budget")
    c.drawString(83,230,"approaches to get more from your groceries.")
    round_rect(c,82,188,260,30,"#194B39",9)
    c.setFillColor(HexColor("#FFFFFF"));c.setFont("Helvetica-Bold",10)
    c.drawCentredString(212,199,"EXPLORE BUDGET DINNERS")
    c.linkURL(VAULT,(82,188,342,218),relative=0)
    c.setFillColor(HexColor("#62584A"));c.setFont("Helvetica",9)
    c.drawCentredString(306,126,"Both resources are optional. Your free printable does not require a purchase.")
    c.drawCentredString(306,107,"whatsforeats.online  •  Easy dinners for real life.")
    c.showPage();c.save();b.seek(0)
    return PdfReader(b).pages[0]

page=promo_page();audit=[]
for file in PDFS:
    before=PdfReader(str(file))
    previous_meta=dict(before.metadata or {})
    if previous_meta.get(PROMO_MARKER)=="true":
        audit.append({"pdf":file.name,"status":"already_promoted","page_count":len(before.pages)})
        continue
    original_pages=len(before.pages)
    writer=PdfWriter()
    for p in before.pages:writer.add_page(p)
    writer.add_page(page)
    meta={"/Title":str(previous_meta.get("/Title") or file.stem.replace("-"," ").title()),
          "/Creator":"What's For Eats","/Producer":"WFE Printables",
          PROMO_MARKER:"true","/WFEOriginalPages":str(original_pages)}
    writer.add_metadata(meta)
    tmp=file.with_name(file.stem+".updated.pdf")
    with tmp.open("wb") as dst:writer.write(dst)
    check=PdfReader(str(tmp))
    assert len(check.pages)==original_pages+1
    assert len(check.pages[-1].get("/Annots",[]))>=2, "Product links not found in appended page"
    assert "Make tomorrow" in (check.pages[-1].extract_text() or ""), "Promo page missing text"
    tmp.replace(file)
    audit.append({"pdf":file.name,"status":"appended","original_pages":original_pages,
                  "final_pages":len(check.pages),"paid_links":[RESCUE,VAULT]})
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(json.dumps({"updated_at":datetime.now(timezone.utc).isoformat(),
 "promotion_type":"Clearly labeled optional final-page companion, preserving every original printable page",
 "count":len(audit),"updated":sum(x["status"]=="appended" for x in audit),
 "skipped_existing":sum(x["status"]=="already_promoted" for x in audit),
 "files":audit},indent=2)+"\n",encoding="utf-8")
print("Verified free PDF promotions:",len(audit),"/",len(PDFS),
      "newly appended:",sum(x["status"]=="appended" for x in audit))
