#!/usr/bin/env python3
"""Render sample PDF appendix for visual QA; confirm all 20 PDFs are linked."""
import json
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parent.parent
AUDIT=ROOT/"pinterest-activity"/"free-pdf-product-promotion-audit.json"
data=json.loads(AUDIT.read_text(encoding="utf8"))
assert data["count"]>=20
for info in data["files"]:
 assert len(info.get("paid_links",[]))==2 or info.get("status")=="already_promoted"
 p=ROOT/"pdfs"/info["pdf"]
 with fitz.open(str(p)) as document:
  page=document[-1]
  assert len(page.get_links())>=2, p
  assert "Make tomorrow's dinner" in page.get_text(),p
sample=ROOT/"pdfs"/"cozy-dinner-bingo.pdf"
with fitz.open(str(sample)) as document:
 pix=document[-1].get_pixmap(matrix=fitz.Matrix(1.35,1.35),alpha=False)
 dest=ROOT/"pinterest-activity"/"pdf-promotion-visual-check.png"
 pix.save(str(dest))
 print("PDF visual QA saved:",dest.name,pix.width,pix.height)
