#!/usr/bin/env python3
"""Original printable dinner crossword. Outputs a real numbered crossword + key."""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/"pdfs"/"dinner-crossword-challenge.pdf"
OUT.parent.mkdir(parents=True,exist_ok=True)
# Row/column placements were generated with letter-crossing and neighbor checks.
WORDS=[
 ("CHICKEN",7,4,"Across","A popular roast protein for Sunday dinner."),
 ("GARLIC",2,7,"Down","A savory bulb often used with butter and herbs."),
 ("BEANS",6,9,"Down","Budget-friendly legumes for chili or tacos."),
 ("RICE",5,4,"Down","Small grains that are great beside stir-fry."),
 ("TACOS",10,5,"Across","Folded tortillas filled with savory goodness."),
 ("BROTH",4,6,"Across","Savory liquid used to make soup."),
 ("CHILI",10,7,"Down","Hearty, spicy stew often topped with cheese."),
 ("SALAD",13,5,"Across","A fresh bowl of greens or vegetables."),
 ("BAKE",8,1,"Across","Cook in an oven with dry heat.")
]
SIZE=15
grid=[["" for _ in range(SIZE)] for _ in range(SIZE)]
for w,r,c,orientation,_ in WORDS:
 dr,dc=(0,1) if orientation=="Across" else (1,0)
 for i,ch in enumerate(w):
  rr=r+i*dr;cc=c+i*dc
  assert grid[rr][cc] in ("",ch), (w,rr,cc)
  grid[rr][cc]=ch
minr=min(r for _,r,c,_,_ in WORDS);maxr=max(r+(len(w)-1 if o=="Down" else 0) for w,r,c,o,_ in WORDS)
minc=min(c for _,r,c,o,_ in WORDS);maxc=max(c+(len(w)-1 if o=="Across" else 0) for w,r,c,o,_ in WORDS)
starts=sorted({(r,c) for _,r,c,_,_ in WORDS})
nums={p:i+1 for i,p in enumerate(starts)}
across=sorted([(nums[(r,c)],clue,len(w)) for w,r,c,o,clue in WORDS if o=="Across"])
down=sorted([(nums[(r,c)],clue,len(w)) for w,r,c,o,clue in WORDS if o=="Down"])
GREEN=HexColor("#23533D");RUST=HexColor("#C45531");INK=HexColor("#252A26")
C=canvas.Canvas(str(OUT),pagesize=(612,792))
C.setTitle("Free Dinner Crossword Challenge | What's For Eats")
def header(title,desc):
 C.setFillColor(HexColor("#FBF5E9"));C.rect(0,0,612,792,fill=1,stroke=0)
 C.setFillColor(GREEN);C.roundRect(33,713,546,49,14,fill=1,stroke=0)
 C.setFillColor(HexColor("#FFFFFF"));C.setFont("Helvetica-Bold",12);C.drawString(53,730,"WHAT'S FOR EATS  •  FREE PRINTABLE")
 C.setFillColor(GREEN);C.setFont("Times-Bold",29);C.drawCentredString(306,676,title)
 C.setFont("Helvetica",10);C.setFillColor(INK);C.drawCentredString(306,655,desc)
def draw_grid(answer=False):
 cell=27;cols=maxc-minc+1;rows=maxr-minr+1
 x0=(612-cols*cell)//2;y0=630
 for r in range(minr,maxr+1):
  for col in range(minc,maxc+1):
   x=x0+(col-minc)*cell;y=y0-(r-minr+1)*cell
   ch=grid[r][col]
   C.setFillColor(HexColor("#FFFFFF") if ch else GREEN)
   C.setStrokeColor(HexColor("#556A61"))
   C.rect(x,y,cell,cell,fill=1,stroke=1)
   if ch:
    if (r,col) in nums:
     C.setFillColor(RUST);C.setFont("Helvetica-Bold",6);C.drawString(x+3,y+cell-8,str(nums[(r,col)]))
    if answer:
     C.setFillColor(INK);C.setFont("Helvetica-Bold",13);C.drawCentredString(x+cell/2,y+8,ch)
 return y0-rows*cell
def clues_block(x,y,title,entries):
 C.setFillColor(GREEN);C.setFont("Times-Bold",16);C.drawString(x,y,title)
 y-=20;C.setFont("Helvetica",8.4);C.setFillColor(INK)
 for n,clue,l in entries:
  # Text wrapped by simple two-line fixed width; avoid clipped printed puzzles.
  words=clue.split();lines=[""]
  for word in words:
   proposed=(lines[-1]+" "+word).strip()
   if C.stringWidth(proposed,"Helvetica",8.4)>214:
    lines.append(word)
   else:lines[-1]=proposed
  for line_i,line in enumerate(lines):
   C.drawString(x,y-11*line_i,(f"{n}. " if line_i==0 else "    ")+line if line_i==0 else "    "+line)
  y-=(len(lines)*11)+7
header("DINNER CROSSWORD","9 kitchen clues • free family fun • print and play")
y=draw_grid(False)
C.setFillColor(RUST);C.setFont("Helvetica-Bold",9)
C.drawCentredString(306,y-22,"Fill the white boxes. Every answer is a real dinner or kitchen word.")
clues_block(54,y-57,"Across",across)
clues_block(323,y-57,"Down",down)
C.setFillColor(HexColor("#6D6C63"));C.setFont("Helvetica",9);C.drawCentredString(306,28,"Find more free printables at whatsforeats.online/free-pdfs.html")
C.showPage()
header("ANSWER KEY","Check your answers after you finish the puzzle.")
draw_grid(True)
C.setFillColor(GREEN);C.setFont("Times-Bold",20);C.drawCentredString(306,235,"Well done, dinner detective!")
C.setFillColor(INK);C.setFont("Helvetica",11)
C.drawCentredString(306,207,"Try our free Cozy Dinner Bingo printable next.")
C.setFillColor(RUST);C.setFont("Helvetica-Bold",11)
C.drawCentredString(306,179,"What's For Eats Free Printable Library")
C.linkURL("https://whatsforeats.online/free-pdfs.html",(125,163,487,193),relative=0)
C.showPage();C.save()
assert OUT.stat().st_size>4000
print("Generated genuine kitchen crossword with",len(WORDS),"checked answers:",OUT,OUT.stat().st_size)
