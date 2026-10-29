#!/usr/bin/env python3
"""Add one clearly optional, clickable paid-product page to every public PDF.
Idempotent: will not append the advertisement twice. Original pages preserved.
"""
from pathlib import Path
from io import BytesIO
import os
import tempfile
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

ROOT=Path(__file__).resolve().parent.parent
PDFS=ROOT/"pdfs"
MARKER="WFE OPTIONAL DINNER TOOLS - PRODUCT BONUS"
RESCUE="https://whatsforeats.online/5-47-rescue-kit.html"
VAULT="https://fatboylove5885.github.io/Cheap-Dinner-Home/"

def product_page():
    buf=BytesIO()
    c=canvas.Canvas(buf,pagesize=(612,792),pageCompression=1)
    dark=HexColor("#213b2f"); rust=HexColor("#bb4e2d")
    cream=HexColor("#fff9ef"); charcoal=HexColor("#332923")
    c.setFillColor(cream);c.rect(0,0,612,792,fill=1,stroke=0)
    c.setFillColor(dark);c.roundRect(39,665,534,87,17,fill=1,stroke=0)
    c.setFillColor(HexColor("#ffffff"));c.setFont("Helvetica-Bold",11)
    c.drawString(60,727,"WHAT'S FOR EATS  /  OPTIONAL DINNER HELP")
    c.setFont("Helvetica-Bold",20);c.drawString(60,694,"Love this free resource?")
    c.setFont("Helvetica",12);c.drawString(60,675,"Here's how to make weeknight dinners easier.")
    c.setFillColor(charcoal);c.setFont("Helvetica",11)
    c.drawString(45,622,"Your free guide is yours to keep - no purchase is required.")
    c.drawString(45,604,"If you'd like more structured dinner help, explore these optional tools.")

    cards=[
      (474,"THE 5:47 P.M. RESCUE KIT",
       ["A practical dinner-planning shortcut for busy evenings.",
        "Plan simple meals without starting from scratch."],
       "EXPLORE THE RESCUE KIT",RESCUE),
      (266,"THE CHEAP DINNER VAULT",
       ["Browse budget-minded dinner tools and meal-planning ideas.",
        "Built for stretching the grocery budget further."],
       "SEE THE CHEAP DINNER VAULT",VAULT)
    ]
    for y,title,lines,cta,url in cards:
        c.setFillColor(HexColor("#ffffff"));c.setStrokeColor(HexColor("#e1d2bb"))
        c.roundRect(42,y-91,528,171,13,fill=1,stroke=1)
        c.setFillColor(dark);c.setFont("Helvetica-Bold",15)
        c.drawString(62,y+45,title)
        c.setFillColor(charcoal);c.setFont("Helvetica",11)
        for i,line in enumerate(lines):c.drawString(62,y+18-i*17,line)
        c.setFillColor(rust);c.roundRect(62,y-72,264,38,11,fill=1,stroke=0)
        c.setFillColor(HexColor("#ffffff"));c.setFont("Helvetica-Bold",10)
        c.drawCentredString(194,y-57,cta)
        c.linkURL(url,(62,y-72,326,y-34),relative=0,thickness=0)
        c.setFillColor(HexColor("#496454"));c.setFont("Helvetica",9)
        c.drawString(62,y-87,"Tap the button to view details before purchasing.")

    c.setStrokeColor(HexColor("#dbcbb4"));c.line(45,115,568,115)
    c.setFillColor(charcoal);c.setFont("Helvetica-Bold",9)
    c.drawString(45,92,"Free guide first. Paid extras are always optional.")
    c.setFont("Helvetica",8)
    c.drawString(45,74,"These links may lead to products for sale on our website or partner checkout.")
    c.setFont("Helvetica",6);c.setFillColor(HexColor("#6c6459"))
    c.drawString(45,41,MARKER)
    c.save();buf.seek(0)
    return PdfReader(buf).pages[0]

def main():
    pdfs=sorted(PDFS.glob("*.pdf"))
    if not pdfs:raise RuntimeError("No actual PDF files to update")
    promo=product_page()
    edited=0;skipped=0;issues=[]
    for path in pdfs:
        try:
            reader=PdfReader(str(path))
            if reader.is_encrypted:raise RuntimeError("Encrypted PDF cannot be safely modified")
            if any(MARKER in (page.extract_text() or "") for page in reader.pages[-2:]):
                skipped+=1;continue
            writer=PdfWriter()
            writer.append(str(path))
            writer.add_page(promo)
            writer.add_metadata({**{k:str(v) for k,v in (reader.metadata or {}).items() if v is not None},
                                 "/WFE_Promo":"optional-products-v1"})
            fd,tmp=tempfile.mkstemp(suffix=".pdf",dir=PDFS)
            os.close(fd)
            try:
                with open(tmp,"wb") as f:writer.write(f)
                proof=PdfReader(tmp)
                assert len(proof.pages)==len(reader.pages)+1
                assert MARKER in (proof.pages[-1].extract_text() or "")
                assert len(proof.pages[-1].get("/Annots",[]))>=2
                os.replace(tmp,path)
            finally:
                if os.path.exists(tmp):os.unlink(tmp)
            edited+=1
        except Exception as exc:
            issues.append((path.name,str(exc)))
    print(f"PDF PRODUCT LINKS: total={len(pdfs)} updated={edited} already_current={skipped} failures={len(issues)}")
    for name,error in issues:print(f"ERROR {name}: {error}")
    if issues:raise SystemExit(1)
if __name__=="__main__":main()
