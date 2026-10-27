#!/usr/bin/env python3
"""Isolated creative A/B test. Never touches daily Pins, RSS or scheduling."""
import base64,datetime as dt,io,json,os,pathlib,urllib.request,urllib.error
from PIL import Image,ImageDraw,ImageFont,ImageOps
ROOT=pathlib.Path(__file__).resolve().parent.parent
OUT=ROOT/'pinterest-creative-lab'/'2026-10-27'
OUT.mkdir(parents=True,exist_ok=True)
QUALITY=[('A-medium-editorial','medium'),('B-high-editorial','high')]
PROMPT=("Create one photorealistic food editorial advertising photograph, PORTRAIT 1024 x 1536, no text, no lettering, no graphics. "
"A genuinely mouth-watering freshly baked stuffed sweet potato with spicy browned lean beef, golden molten cheddar, black beans, salsa, parsley and lightly caramelized edges, "
"served in a rustic handmade ivory ceramic plate. A little bowl of fresh salsa and soft folded striped linen nearby. "
"Golden hour natural sidelight, detailed realistic roasted potato skin and melting cheese, shallow depth of field but whole hero dish razor sharp. "
"The food fills much of the frame, beautifully plated, believable home-cooking not plastic, irresistible textures, vibrant reds, amber and dark greens, rich contrast. "
"Vertical polished recipe-magazine product photography with breathing room ONLY at extreme top edge for separately placed typography. "
"Not a collage, not a montage, no side-by-side dishes, no seams, no split panels, no whitespace dividers, no watermarks. "
"Evokes cozy comfort food, generous portions, homemade richness, and editorial visual precision.")
def f(size,serif=False):
 p=('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf' if serif else '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')
 return ImageFont.truetype(p,size)
def image_request(quality):
 data=json.dumps({'model':'gpt-image-2','size':'1024x1536','quality':quality,'output_format':'jpeg','prompt':PROMPT}).encode()
 req=urllib.request.Request('https://api.openai.com/v1/images/generations',data=data,headers={'Content-Type':'application/json','Authorization':'Bearer '+os.environ['OPENAI_API_KEY']},method='POST')
 try:
  with urllib.request.urlopen(req,timeout=200) as r:j=json.load(r)
 except urllib.error.HTTPError as e:
  txt=e.read().decode('utf8','replace')[:300]
  raise RuntimeError(f'Image API HTTP {e.code}; provider detail: {txt.replace(os.environ["OPENAI_API_KEY"],"[redacted]")}') from None
 x=j['data'][0]['b64_json']
 return Image.open(io.BytesIO(base64.b64decode(x))).convert('RGB')
def compose(img,name):
 W,H=1000,1500
 photo=ImageOps.fit(img,(W,H),method=Image.Resampling.LANCZOS)
 d=ImageDraw.Draw(photo,'RGBA')
 d.rectangle((0,0,1000,320),fill=(253,247,237,244))
 d.rectangle((0,1320,1000,1500),fill=(253,247,237,233))
 d.line((75,40,205,40),fill=(192,66,34),width=3);d.line((795,40,925,40),fill=(192,66,34),width=3)
 d.text((500,38),"W H A T ' S   F O R   E A T S",font=f(23),anchor='mt',fill=(40,47,38))
 d.text((500,93),"5-INGREDIENT",font=f(87,True),anchor='mt',fill=(22,68,42))
 d.text((500,187),"DINNERS",font=f(112,True),anchor='mt',fill=(190,63,29))
 d.text((500,296),"Simple meals for busy nights",font=f(27,True),anchor='mm',fill=(36,43,35))
 d.rounded_rectangle((119,1351,881,1445),radius=47,fill=(193,65,30))
 d.text((500,1397),"GET THE FREE RECIPES",font=f(35),fill=(255,255,255),anchor='mm')
 d.text((500,1475),"whatsforeats.online",font=f(21),fill=(35,42,35),anchor='mm')
 photo.save(OUT/(name+'.jpg'),'JPEG',quality=92,optimize=True)
 return OUT/(name+'.jpg')
def main():
 assert os.environ.get('OPENAI_API_KEY'),'Missing secret OPENAI_API_KEY'
 report={'date':'2026-10-27','purpose':'Independent original premium visual creative experiment; no publication and no production changes.','model':'gpt-image-2','prompt':PROMPT,'tests':[],'status':'complete','notes':'A and B differ only in API image quality (medium versus high). Same original prompt and same layout. Results are meant for visual review, not automatically selected as winners.'}
 for name,q in QUALITY:
  img=image_request(q)
  namepath=compose(img,name)
  report['tests'].append({'name':name,'quality':q,'file':namepath.name,'size_bytes':namepath.stat().st_size})
 (OUT/'test-results.json').write_text(json.dumps(report,indent=2))
 print('CREATIVE LAB SUCCESS:',len(report['tests']),'original outputs in',OUT,'No Pinterest publishing.')
if __name__=='__main__':main()
