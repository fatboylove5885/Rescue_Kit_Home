#!/usr/bin/env python3
"""Reference-driven, isolated creative experiment. Two MEDIUM images only.
Visual direction is derived from the privately inspected Pinterest reference library.
No third-party reference images, source photography, RSS entries or scheduler actions
are copied into the test outputs.
"""
import base64, hashlib, io, json, os, pathlib, urllib.request, urllib.error
from PIL import Image, ImageOps, ImageDraw, ImageFont
ROOT=pathlib.Path(__file__).resolve().parent.parent
DEST=ROOT/"pinterest-creative-lab"/"2026-10-27"/"reference-driven"
MODEL="gpt-image-2"
QUALITY="medium"
TESTS=[
 {
 "id":"A",
 "name":"fast-dinner-hero",
 "article":"15-minute-dinners-for-busy-weeknights.html",
 "headline":["15-MINUTE","DINNERS"],
 "tagline":"Big flavor. Barely any prep.",
 "cta":"GET THE EASY RECIPES",
 "inspiration":[
 {"id":"competitor-quick-dinners-20261027","file":"reobserved-20-minute-dinner.jpg","principle":"The thumbnail shows two close-up savory meals, warm food textures, obvious 20-minute benefit, highly contrasting headline band. Borrow an immediately legible FAST DINNER proposition and crop tightly into irresistible food; do not reproduce the original image or yellow central band."},
 {"id":"competitor-hero-meal-20261027","file":"reobserved-single-meal-hero.jpg","principle":"Single-pan, believable plated chicken, clearly readable heading above imagery. Borrow the single-hero food focus with a tidy type hierarchy; create a different meal and visual angle."}
 ],
 "photo_prompt":"""A breathtakingly realistic premium contemporary American food-magazine photograph for a quick weeknight dinner pin, portrait orientation 1024x1536. HERO DISH: gorgeous sizzling garlic-lime shrimp fajita skillet with shiny succulent seared shrimp, char-kissed yellow and red bell peppers, thin caramelized onions, fresh cilantro and lime halves, with a naturally folded warm tortilla just at the edge. Camera at appetizing three-quarter angle, skillet prominently fills the frame, visible fine oil sheen, pepper blistering, actual shrimp texture and steam, dramatic soft late-afternoon side lighting with luxurious warm highlights, authentic cozy home-kitchen table, off-white linen corner and handmade ceramic salsa bowl subtly in background. Food looks cooked and genuinely edible, deliciously abundant, magazine-level controlled art direction and color separation; rust red, deep leafy green, beautiful golden shrimp against dark skillet. Full-bleed continuous single photo, focused crisp hero food, tasteful depth of field, no collage, no split panels, no text, no logo, no visual borders, no graphic overlays, no watermark. Leave only extreme upper 15% slightly less busy because brand headline is professionally composited later. Make an unmistakably original arrangement and new photograph, not a reconstruction of any Pinterest source."""
 },
 {
 "id":"B",
 "name":"family-dinner-variety",
 "article":"weekly-meal-plan-for-busy-families.html",
 "headline":["7 EASY FAMILY","DINNERS"],
 "tagline":"One less thing to think about.",
 "cta":"GET THE 7-NIGHT PLAN",
 "inspiration":[
 {"id":"competitor-dinner-collage-20261027","file":"reobserved-family-dinner-collage.jpg","principle":"Multiple distinctly appetizing dinners offer immediate variety and a bold multi-recipe value promise. Borrow variety of meal textures and a bold central value proposition, but not the white diamond, photo quadrants or composition."},
 {"id":"competitor-hero-meal-20261027","file":"reobserved-single-meal-hero.jpg","principle":"Grounded family food with familiar chicken, vegetables and dinnerware. Borrow approachable authentic home dinner appeal rather than staged luxury."}
 ],
 "photo_prompt":"""Original ultra-realistic food-editorial photograph, portrait 1024x1536, shot as ONE CONTINUOUS physical overhead table scene for a premium family dinner meal-plan Pinterest graphic. On a rich natural light-oak home dining table, arrange THREE beautiful DISTINCT finished weeknight meals in ceramic serving dishes: (1) in the main foreground a glossy golden roast chicken-thigh and herb-potato one-pan platter with a few roasted green vegetables, (2) upper left a smaller ceramic bowl of creamy tomato-basil rigatoni with scattered fresh parmesan, (3) upper right a family-style bowl of vibrant seasoned beef taco rice with black beans, corn and tomatoes. These are ACTUAL food dishes placed on a single table with natural realistic shadows and angles, not separate pasted photographs. Bright appetizing ingredient colors, deeply detailed browned chicken, real pasta sauce sheen, inviting edible textures, sophisticated editorial styling, occasional wrinkled linen napkin, simple fork and sprinkle of fresh herbs. This should stop a scrolling viewer because there is abundant real food variety and harmonious warm colors. Capture like a top food publication, even premium soft daylight across the whole scene, relatively sharp dishes, no people. DO NOT use a collage, quadrants, white diamond, split panels, dividers, disconnected photos, graphic illustrations, visible headlines, typography, logos, watermarks, or fake food. Keep top 15% of vertical frame uncluttered for separate overlay lettering. Distinct from competitor source composition and individual dishes."""
 }
]
CREAM=(251,247,238);GREEN=(20,67,44);RUST=(190,61,26);INK=(39,39,31)
def font(size,serif=False):
 locs=(["/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf","/usr/share/fonts/truetype/liberation2/LiberationSerif-Bold.ttf"] if serif else ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf","/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"])
 return ImageFont.truetype(next(x for x in locs if pathlib.Path(x).exists()),size)
def generate(test):
 prompt=test["photo_prompt"]+"\n\nResearch-derived high-level art-direction priorities: "+" | ".join(x["principle"] for x in test["inspiration"])+". Use them as conceptual guidance, not copy instructions."
 payload=json.dumps({"model":MODEL,"prompt":prompt,"n":1,"quality":QUALITY,"size":"1024x1536","output_format":"jpeg"}).encode()
 req=urllib.request.Request("https://api.openai.com/v1/images/generations",data=payload,headers={"Content-Type":"application/json","Authorization":"Bearer "+os.environ["OPENAI_API_KEY"]},method="POST")
 try:
  with urllib.request.urlopen(req,timeout=200) as response:data=json.load(response)
 except urllib.error.HTTPError as exc:
  msg=exc.read().decode("utf8","replace")[:420].replace(os.environ["OPENAI_API_KEY"],"[REDACTED]")
  raise RuntimeError(f"Images API HTTP {exc.code}: {msg}") from None
 raw=base64.b64decode(data["data"][0]["b64_json"])
 with Image.open(io.BytesIO(raw)) as photo:return photo.convert("RGB"),hashlib.sha256(raw).hexdigest()
def compose(photo,test):
 width,height=1000,1500
 card=ImageOps.fit(photo,(width,height),method=Image.Resampling.LANCZOS)
 d=ImageDraw.Draw(card,"RGBA")
 # October 26 visual language: huge editorial titles, vivid hero meal and restrained footer.
 d.rectangle((0,0,1000,322),fill=(251,247,238,248))
 d.rectangle((0,1332,1000,1500),fill=(251,247,238,242))
 d.line((68,34,213,34),fill=RUST+(255,),width=3)
 d.line((787,34,932,34),fill=RUST+(255,),width=3)
 d.text((500,43),"W H A T ' S   F O R   E A T S",fill=INK,font=font(23),anchor="mt")
 first=test["headline"][0]
 fsize=84 if len(first)<=12 else 62
 d.text((500,91),first,fill=GREEN,font=font(fsize,True),anchor="mt",stroke_width=0)
 d.text((500,174),test["headline"][1],fill=RUST,font=font(110,True),anchor="mt")
 d.text((500,299),test["tagline"],fill=INK,font=font(25,True),anchor="mm")
 d.rounded_rectangle((105,1350,895,1443),radius=47,fill=RUST)
 d.text((500,1396),test["cta"],fill=(255,255,255),font=font(34),anchor="mm")
 d.text((500,1476),"whatsforeats.online",fill=INK,font=font(20),anchor="mm")
 out=DEST/(test["id"]+"-"+test["name"]+"-medium.jpg")
 card.save(out,"JPEG",quality=92,optimize=True)
 return out
def main():
 if not os.environ.get("OPENAI_API_KEY"):raise RuntimeError("OPENAI_API_KEY unavailable")
 DEST.mkdir(parents=True,exist_ok=True)
 report={"test_date":"2026-10-27","status":"complete","model":MODEL,"quality":QUALITY,"isolated":True,"scheduled":False,"published":False,
 "description":"Two different images inspired by actual private reference-library images visually reviewed on October 27. API uses derived design directions, not the competitor image pixels. Every photograph and composited layout is independently original.","tests":[]}
 for t in TESTS:
  im,sha=generate(t)
  path=compose(im,t)
  report["tests"].append({"id":t["id"],"name":t["name"],"source_reference_ids":[x["id"] for x in t["inspiration"]],
   "source_reference_files":[x["file"] for x in t["inspiration"]],
   "derived_design_principles":[x["principle"] for x in t["inspiration"]],
   "new_original_photo":True,"title":" ".join(t["headline"]),"destination_slug":t["article"],
   "filename":path.name,"output_size_bytes":path.stat().st_size,"source_image_sha256":sha})
 (DEST/"research-to-creative-report.json").write_text(json.dumps(report,indent=2),encoding="utf8")
 print("REFERENCE-LED CREATIVE TEST COMPLETE: 2 new Medium outputs; no scheduled/published pins.")
if __name__=="__main__":main()
