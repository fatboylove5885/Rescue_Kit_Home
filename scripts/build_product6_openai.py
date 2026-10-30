"""Product 6. Artwork must come from OpenAI Images API; no fallback assets.
Run inside GitHub Actions using secrets.OPENAI_API_KEY. Build itself is offline.
Photos are illustrative AI artwork, not evidence of kitchen testing.
"""
import os,json,base64,hashlib,urllib.request,urllib.error,datetime,concurrent.futures,shutil
from pathlib import Path
ROOT=Path('product6-output'); ASSETS=ROOT/'assets';ROOT.mkdir(exist_ok=True);ASSETS.mkdir(exist_ok=True)
MODEL='gpt-image-2'; ENDPOINT='https://api.openai.com/v1/images/generations'
# Each recipe has its own newly generated photo. No crops from references are accepted.
RECIPES=[
 dict(id='01',name='Lemon chicken & rice bowls',food='lemon herb sliced chicken, fluffy rice, roasted broccoli and carrots, yogurt herb sauce in an abundant ceramic bowl',time='12 minutes',ing='2 cups cooked rice; 250 g / 9 oz cooked chicken; 2 cups cooked broccoli and carrots; 4 tbsp herb yogurt sauce; 1/2 lemon.',steps=['Put rice in a microwave-safe bowl with 2 tbsp water. Cover loosely and heat, stirring midway, until steaming hot throughout.','Warm chicken and vegetables separately with a splash of water. Check leftovers reach 74 C / 165 F in several places.','Divide between two bowls. Spoon on cold sauce and squeeze over lemon. Serve immediately.'],swap='Use canned white beans instead of chicken; heat them through. Change rice to fresh couscous.',allergy='Milk in yogurt. Check prepared chicken seasonings.'),
 dict(id='02',name='Smoky black bean tacos',food='three soft corn tortillas filled with smoky black beans, shredded purple cabbage, salsa and lime, ceramic plate, no avocado',time='15 minutes',ing='1 x 400 g / 15 oz can black beans, drained; 4 small tortillas; 1 cup shredded cabbage; 4 tbsp salsa; 1 tsp oil; 1/2 tsp cumin; 1/2 tsp smoked paprika; 1/2 lime.',steps=['Heat oil in a saucepan over medium heat. Add drained beans, spices and 3 tbsp water. Simmer 5 minutes, stirring; mash a few beans.','Warm tortillas in a dry pan, about 20 seconds per side, until flexible.','Divide beans and cabbage among tortillas. Finish with salsa and lime. Serve two tacos per person.'],swap='Use pinto beans or chickpeas. Put the filling over rice for a bowl.',allergy='Wheat in flour tortillas; choose appropriate corn tortillas if needed.'),
 dict(id='03',name='Pesto broccoli pasta',food='short rigatoni pasta coated in green pesto with broccoli florets and white beans, no pine nuts garnish, rustic bowl',time='20 minutes',ing='180 g / 6 oz dry pasta; 2 cups small broccoli florets; 1 can white beans, drained; 3 tbsp pesto; 1/2 lemon.',steps=['Boil pasta following its package time. Add broccoli for the last 3 minutes, checking tenderness.','Reserve 1/2 cup cooking water. Drain pasta and broccoli; return to the pan with beans, pesto and 2 tbsp reserved water.','Stir over low heat until beans are hot. Loosen with extra water as needed; add lemon to taste.'],swap='Use chopped spinach instead of broccoli; stir in at the end until wilted.',allergy='Wheat; pesto often contains milk and nuts. Choose an appropriate pesto.'),
 dict(id='04',name='Crunchy chicken flatbreads',food='open flatbreads with lemon chicken, thin cucumber, purple cabbage and white yogurt herb sauce, colorful lunch board',time='12 minutes',ing='2 large flatbreads; 250 g / 9 oz cooked chicken; 1/2 cucumber, sliced; 1 cup cabbage; 4 tbsp herb yogurt sauce.',steps=['Reheat chicken with 1 tbsp water in a covered dish to 74 C / 165 F throughout. Warm flatbreads according to package directions.','Spread each flatbread with 2 tbsp sauce. Add chicken, cucumber and cabbage.','Fold and eat immediately. Keep unused cold toppings separate from heated filling.'],swap='Use chickpeas or cooked tofu; change sauce to lemon tahini.',allergy='Wheat and milk; sesame if tahini is used.'),
 dict(id='05',name='Ginger egg fried rice',food='golden egg fried rice with diced carrots broccoli and scallions in a dark skillet, real individual grains, no meat',time='15 minutes',ing='2 cups safely chilled cooked rice; 2 eggs; 1 cup cooked diced vegetables; 2 tsp oil; 1 tsp grated ginger; 1 tbsp soy sauce; 1 sliced scallion.',steps=['Heat 1 tsp oil in a large pan. Beat eggs, add, and stir until fully set. Transfer to a clean plate.','Add remaining oil and ginger. Stir 30 seconds. Add rice, vegetables and 2 tbsp water; stir and heat until rice reaches 74 C / 165 F throughout.','Return eggs, add soy sauce and heat through. Add scallion. Serve immediately; do not cool and reheat again.'],swap='Use crumbled firm tofu instead of egg. Use certified gluten-free tamari where needed.',allergy='Egg, soy and usually wheat. Rice must follow page 9 storage rules.'),
 dict(id='06',name='Golden chickpea couscous',food='golden couscous with roasted carrots, chickpeas, parsley, lemon and creamy tahini drizzle in a terracotta bowl',time='15 minutes',ing='3/4 cup dry couscous; boiling water per packet; 1 can chickpeas, drained; 1 cup cooked carrots; 1/2 tsp cumin; 4 tbsp lemon tahini sauce.',steps=['Prepare couscous with the quantity of boiling water stated on the packet. Cover and stand as directed, then fluff.','Warm chickpeas and carrots in a saucepan with cumin and 3 tbsp water until piping hot.','Divide couscous into bowls, add chickpeas and carrots, then drizzle on sauce.'],swap='Use freshly cooked rice for a wheat-free base; check all other labels.',allergy='Wheat and sesame.'),
 dict(id='07',name='Fajita chicken remix',food='warm tortilla wraps beside skillet of sliced chicken and charred red bell peppers and onions, lime and salsa',time='20 minutes',ing='250 g / 9 oz cooked chicken; 2 sliced peppers; 1 sliced onion; 4 small tortillas; 2 tsp oil; 1 tsp smoked paprika; 4 tbsp salsa.',steps=['Heat oil in a wide pan. Cook peppers and onion over medium-high heat for 8-10 minutes, stirring until softened and lightly browned.','Add chicken, paprika and 3 tbsp water. Cover briefly, then stir until chicken reaches 74 C / 165 F throughout.','Warm tortillas. Fill with chicken and peppers; serve salsa separately.'],swap='Use a can of drained black beans instead of chicken.',allergy='Wheat in flour tortillas; check salsa and seasonings.'),
 dict(id='08',name='Loaded sweet potato boats',food='two split roasted orange sweet potatoes stuffed with black beans and corn topped with yogurt and scallions, no cheese',time='20 minutes',ing='2 medium sweet potatoes; 1 can black beans, drained; 1 cup frozen corn; 1/2 tsp cumin; 4 tbsp plain yogurt; 1 scallion.',steps=['Scrub and pierce potatoes several times. Microwave on a suitable plate 8-12 minutes, turning halfway, until completely tender; larger potatoes take longer.','Simmer beans, frozen corn, cumin and 4 tbsp water for 5-7 minutes until piping hot.','Split potatoes carefully; allow steam to escape. Fill with beans and corn, then finish with yogurt and scallion.'],swap='Use white potatoes or cooked lentils. Omit yogurt or use an appropriate dairy-free topping.',allergy='Milk in yogurt.'),
 dict(id='09',name='Creamy white bean soup',food='rustic tomato white bean and spinach soup in a cream bowl, partially blended velvety tomato broth, bread at side',time='20 minutes',ing='1 can white beans, drained; 1 x 400 g / 14 oz can crushed tomatoes; 300 ml / 1 1/4 cups stock; 2 cups spinach; 1 tsp Italian herbs; 1 tsp oil.',steps=['Combine tomatoes, beans, stock, herbs and oil in a saucepan. Bring to a simmer and cook gently for 12 minutes, stirring.','Mash some beans against the side with a spoon to thicken. Add spinach and stir until wilted.','Taste before adding salt because stock varies. Serve hot; add bread if wanted.'],swap='Use chickpeas and chopped cooked carrots. Add extra stock for a thinner soup.',allergy='Check stock for celery, wheat and other allergens. Bread is optional.'),
 dict(id='10',name='Crispy veggie quesadillas',food='golden crisp tortilla quesadilla wedges with melted cheese, roasted peppers and black beans visible, salsa dipping bowl',time='15 minutes',ing='4 medium tortillas; 1 cup chopped cooked vegetables; 1 cup black beans, drained; 100 g / 3.5 oz grated cheese; 4 tbsp salsa.',steps=['Divide vegetables, beans and cheese over two tortillas. Place the other tortillas on top.','Heat a dry nonstick pan over medium-low heat. Cook each quesadilla 3-4 minutes per side, turning carefully, until browned and filling is piping hot.','Rest 1 minute, cut into wedges and serve with salsa. Heat longer over low heat if the outside browns before the center is hot.'],swap='Use a cheese alternative that melts, or mash beans to help hold the filling.',allergy='Milk and often wheat.'),
 dict(id='11',name='Mediterranean grain salad',food='bright couscous salad with chickpeas cucumber tomatoes parsley and lemon dressing, no olives or feta, white ceramic platter',time='15 minutes',ing='2 cups safely chilled cooked couscous; 1 can chickpeas, drained; 1/2 cucumber; 2 tomatoes; 1 tbsp olive oil; 1 tbsp lemon juice; 2 tbsp parsley.',steps=['Keep couscous chilled while washing and chopping vegetables. Drain chickpeas thoroughly.','Whisk oil with lemon juice in a large bowl. Fold in couscous, vegetables, chickpeas and parsley.','Taste and season. Serve immediately or refrigerate promptly. Use the earliest use-by deadline of any component.'],swap='Use fresh cooked and safely cooled quinoa in place of couscous.',allergy='Wheat in couscous.'),
 dict(id='12',name='Saucy turkey & pepper skillet',food='saucy ground turkey with red peppers in paprika tomato sauce on rice, skillet closeup, scallion garnish',time='25 minutes',ing='300 g / 10.5 oz raw ground turkey; 1 sliced pepper; 1 tsp oil; 1 tsp smoked paprika; 200 ml / 3/4 cup tomato passata; 2 cups cooked rice.',steps=['Heat oil in a pan over medium heat. Add turkey and cook 6-8 minutes, breaking it into small pieces.','Add pepper and cook 4 minutes. Add paprika, passata and 3 tbsp water. Simmer 5-8 minutes; turkey must reach 74 C / 165 F.','Separately heat rice to 74 C / 165 F throughout, then divide into bowls and top with turkey sauce.'],swap='Use 1 can lentils, drained, in place of turkey and simmer until hot.',allergy='Check passata and seasonings; rice storage rules apply.')]
ART=[{'id':'cover','scene':'Full-bleed editorial overhead photograph: a generous table with several visually distinct mix-and-match dinners, lemon chicken rice bowl, chickpea couscous, tacos, vegetables and sauces in separate ceramic vessels. Warm oak, cream linen, sage and terracotta ceramics, joyful abundant contemporary cookbook styling. No text.','size':'1024x1536'}, {'id':'components','scene':'Premium overhead food photograph of separate meal-prep ingredients in open glass containers: cooked chicken, roasted broccoli and carrots, fluffy rice, black beans, shredded cabbage, yogurt herb sauce, lemon tahini sauce. Fresh herbs and linen, cream background. Never identical prepared lunch boxes. No text.','size':'1536x1024'}, {'id':'botanical','scene':'Hand painted gouache illustration of edible kitchen ingredients arranged in an airy horizontal garland: lemon halves, broccoli, carrot, red pepper, parsley, chickpeas, terracotta bowl and wooden spoon. Warm ivory paper background, rich forest green, tomato orange and golden yellow, sophisticated cheerful cookbook illustration. No letters, words, numbers, logos or diagrams.','size':'1536x1024'}]
for r in RECIPES:ART.append({'id':r['id'],'scene':'Dedicated food photograph for the recipe '+r['name']+': '+r['food']+'. Food and ingredients must match exactly. Single plated dish, appetizing edible texture, professional soft window light, close three-quarter or overhead angle, cream linen, warm wood, sage/terracotta ceramics, premium colorful cookbook editorial. No words or typography.','size':'1536x1024'})
STYLE='Original artwork created exclusively for the What\'s For Eats Mix & Match Meal Prep product. No stock image, no existing reference image, no watermark, no collage, no lettering. '
def sha(b):return hashlib.sha256(b).hexdigest()
def generate(a):
 path=ASSETS/(a['id']+'.png');meta=ASSETS/(a['id']+'.json');prompt=STYLE+a['scene']
 if path.exists() and meta.exists():
  m=json.loads(meta.read_text())
  if m['sha256']==sha(path.read_bytes()) and m['prompt']==prompt and m['model']==MODEL and m['endpoint']==ENDPOINT:return m
  raise RuntimeError('Provenance mismatch: '+a['id'])
 key=os.environ.get('OPENAI_API_KEY');assert key,'OPENAI_API_KEY missing; stopped. No substitute artwork allowed.'
 body={'model':MODEL,'prompt':prompt,'n':1,'quality':'medium','size':a['size'],'output_format':'png'}
 req=urllib.request.Request(ENDPOINT,data=json.dumps(body).encode(),headers={'Content-Type':'application/json','Authorization':'Bearer '+key})
 try:
  with urllib.request.urlopen(req,timeout=300) as response:
   data=json.load(response);request_id=response.headers.get('x-request-id')
 except urllib.error.HTTPError as e:
  # Never print the credential or arbitrary response bodies.
  raise RuntimeError('OpenAI image request failed: HTTP '+str(e.code)+'; stopped with no fallback.') from None
 raw=base64.b64decode(data['data'][0]['b64_json']);path.write_bytes(raw)
 m={'id':a['id'],'filename':path.name,'provider':'OpenAI','endpoint':ENDPOINT,'model':MODEL,'quality':'medium','prompt':prompt,'sha256':sha(raw),'request_id':request_id,'created':data.get('created'),'usage':data.get('usage'),'generated_for':'Product 6: Mix & Match Meal Prep','github_run_id':os.getenv('GITHUB_RUN_ID'),'github_commit':os.getenv('GITHUB_SHA')}
 meta.write_text(json.dumps(m,indent=2));print('OpenAI artwork completed:',a['id'],flush=True);return m
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:records=list(pool.map(generate,ART))
assert len(records)==15 and len({m['sha256'] for m in records})==15
for m in records:assert m['provider']=='OpenAI' and m['request_id'] and sha((ASSETS/m['filename']).read_bytes())==m['sha256']
(ROOT/'artwork-provenance.json').write_text(json.dumps({'passed':True,'asset_count':15,'assets':records},indent=2))
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from PIL import Image,ImageOps,ImageDraw
import fitz
for name,file in [('Body','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf'),('Display','DejaVuSerif-Bold.ttf')]:pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
W,H=612,792;cream='#FFF8E9';green='#164535';orange='#D9562D';gold='#F4BF57';ink='#243A31';palette=['#DCEADA','#FADACB','#E0EDF0','#E9E0EF']
out=ROOT/'Mix_and_Match_Meal_Prep_OpenAI_Edition.pdf';c=canvas.Canvas(str(out),pagesize=(W,H));c.setTitle('Mix & Match Meal Prep | The No-Boring-Leftovers System');c.setAuthor("What's For Eats")
placements=[];bounds=[]
def rect(x,y,w,h,color,r=12):
 c.setFillColor(HexColor(color));c.roundRect(x,y,w,h,r,fill=1,stroke=0)
def text(s,x,top,width=516,size=10,color=ink,font='Body'):
 p=Paragraph(s,ParagraphStyle('a',fontName=font,fontSize=size,leading=size*1.4,textColor=HexColor(color)))
 _,h=p.wrap(width,900);p.drawOn(c,x,top-h)
 bounds.append({'page':c.getPageNumber(),'text':s[:55],'x':x,'top':top,'bottom':top-h,'right':x+width})
 assert top-h>=63,('Text enters footer',c.getPageNumber(),s[:30],top-h)
 return top-h
def photo(a,x,y,w,h):
 assert a in {z['id'] for z in records},'Unverified image blocked'
 im=Image.open(ASSETS/(a+'.png'));im=ImageOps.fit(im,(round(w*2),round(h*2)),method=Image.Resampling.LANCZOS)
 from reportlab.lib.utils import ImageReader
 c.drawImage(ImageReader(im),x,y,w,h);placements.append({'page':c.getPageNumber(),'asset_id':a,'sha256':next(m['sha256'] for m in records if m['id']==a)})
def base(section,title,sub=None):
 c.setFillColor(HexColor(cream));c.rect(0,0,W,H,fill=1,stroke=0)
 rect(0,754,612,38,green,0);text("WHAT'S FOR EATS   /   MIX & MATCH MEAL PREP",34,778,544,8,'#FFFFFF','Bold')
 for j,col in enumerate([orange,gold,'#91B475']):rect(j*204,748,204,6,col,0)
 text(section.upper(),36,733,540,8,orange,'Bold')
 text(title,36,709,540,25,green,'Display')
 if sub:text(sub,36,660,540,9)
 rect(36,23,540,30,green,8)
 c.setFillColor(white);c.setFont('Body',7);c.drawString(48,35,'THE NO-BORING-LEFTOVERS SYSTEM');c.drawRightString(563,35,str(c.getPageNumber()))
 c.bookmarkPage('p'+str(c.getPageNumber()))
def card(title,body,top=628,h=120,col=palette[0],x=36,w=540):
 rect(x,top-h,w,h,col);text(title.upper(),x+14,top-13,w-28,9,green,'Bold');bottom=text(body,x+14,top-36,w-28,10)
 assert bottom>=top-h+10,('Card overflow',c.getPageNumber(),title)
def done():c.showPage()
def strip(y=76):photo('botanical',36,y,540,100)
# 1
base('A flexible kitchen, a calmer week','',None);photo('cover',0,56,612,692)
rect(28,492,556,223,green);text('MIX & MATCH',48,690,516,37,'#FFFFFF','Display');text('MEAL PREP',48,634,516,38,'#F4BF57','Display');text('The No-Boring-Leftovers System',48,571,510,18,'#FFFFFF','Bold');text('Prep useful ingredients. Build dinners you actually want.',48,530,510,11,'#FFFFFF')
rect(28,77,556,96,orange);text('12 dinner transformations + a realistic prep plan + reusable planning pages',47,151,520,17,'#FFFFFF','Bold');done()
# 2
base('Start here','Your dinner roadmap','For busy households who want flexible food, not five identical containers.')
entries=[('The method & your first prep session',3),('A safe plan for the whole week',8),('Sauces, portions & fresh finishes',10),('12 dedicated recipe cards',12),('Three-day worked example & grocery list',24),('Fix the usual problems',27),('Reusable worksheets',28),('Sources & artwork self-check',34)]
for i,(s,page) in enumerate(entries):
 y=627-i*58;rect(36,y-47,540,48,palette[i%4]);text(s,50,y-11,458,10,green,'Bold');text(str(page),530,y-11,30,11,orange,'Bold');c.linkRect('', 'p'+str(page),(36,y-47,576,y),relative=0,thickness=0)
text('Use the linked contents to jump. Photos are AI-generated illustrations of the meals; times and yields are estimates. See final-page testing notes.',36,135,540,9);done()
# 3
base('01 / Change the unit of prep','Prepare components, not copies')
photo('components',36,382,540,264)
card('The starting point','You have food in the fridge, but nothing that feels like dinner. The answer is a small set of compatible components - not more disconnected recipes.',362,120)
card('The finish line','By the end, choose three dinners, prep shared ingredients, label safe portions, and assemble different meals with a sauce, format or texture change.',227,120,palette[1]);done()
# 4
base('02 / Keep it small','The two-person starter plan','Scale by appetite and household size after one trial week.')
card('Choose a base','Cook rice for your next meal and freeze any later portions promptly. Or keep tortillas ready and cook couscous fresh on the night.',630,115)
card('Choose two anchors','Cook about 700 g / 1.5 lb raw boneless chicken, or prepare a plant-based alternative. Keep two cans of beans in the pantry to open when needed.',502,115,palette[1])
card('Choose two kinds of color','Roast broccoli and carrots together. Keep cabbage and cucumber raw and dry. Separate hot components from fresh toppings.',374,115,palette[2])
card('Choose two contrasting finishes','A cool herb yogurt sauce and bright lemon tahini sauce give the same ingredients two different identities. Make only what you can safely use.',246,115,palette[3]);done()
# 5
base('03 / Set up before the clock','A kitchen that makes prep easier')
photo('components',306,364,270,275)
card('Minimum useful equipment','One wide pan; one sheet pan; saucepan with lid; knife and board; food thermometer; shallow containers; labels; measuring spoons.',638,257,x=36,w=254)
card('Before you buy anything','Check your next three evenings. Circle the night you will be most tired. Choose familiar ingredients, check allergies, then inspect your fridge and pantry.',344,117,palette[1])
card('Your first-session rule','Stop at three dinners. A 60-minute session is a target for a practiced cook, not a guarantee. Start with 75-90 minutes if you are learning.',210,122,palette[2]);done()
# 6
base('04 / A coordinated session','The prep sprint','The example makes two chicken dinners plus pantry-ready tacos for two people.')
for i,(h,b) in enumerate([('0-10 / Start hot','Wash hands. Heat oven to 220 C / 425 F (200 C fan). Start rice according to its packet. Put out labeled shallow containers.'),('10-30 / Cook components','Cut broccoli and carrots into small even pieces. Toss with oil; roast 20-25 minutes, turning. Pan-cook thin chicken pieces; verify 74 C / 165 F.'),('30-45 / Build contrast','Use a clean board after raw chicken. Shred cabbage, wash cucumber and mix the two sauces on page 10.'),('45-60 / Portion and reset','Serve or cool components promptly. Freeze later rice portions on prep day. Label food and dates; wash equipment. Cooling continues safely beyond the timer.')]):card(h,b,635-i*135,121,palette[i])
done()
# 7
base('05 / Make dinner feel different','Change two of these three things')
photo('01',36,410,540,232)
for i,(h,b) in enumerate([('FORMAT','Bowl -> wrap -> skillet. Chicken and vegetables can become three different eating experiences.'),('FLAVOR','Lemon-herb -> smoky salsa -> sesame-ginger. Start with neutral components and season at assembly.'),('TEXTURE','Soft rice + crisp cabbage; warm beans + crunchy tortilla; creamy sauce + fresh cucumber.')]):card(h,b,391-i*101,90,palette[i])
text('Worked remix: Monday chicken bowl = rice + yogurt + roast vegetables. Tuesday flatbread = bread + lemon tahini + raw crunch. Same anchor, different dinner.',36,96,540,8);done()
# 8
base('06 / A seven-night plan','Prep is not seven days in the fridge','Later-week dinners use frozen portions, unopened pantry food, or fresh cooking.')
week=[('MON','Chicken bowls','Sunday chicken + vegetables. Rice cooked fresh or safely thawed.'),('TUE','Chicken flatbreads','Finish the refrigerated chicken; use fresh crunch.'),('WED','Black bean tacos','Open beans today. Warm tortillas and add cabbage.'),('THU','Pesto broccoli pasta','Cook pasta and broccoli fresh; open white beans.'),('FRI','Sweet potato boats','Cook potatoes fresh. Use unopened beans and frozen corn.'),('SAT','Turkey skillet','Cook fresh turkey, or thaw raw frozen turkey safely in fridge.'),('SUN','Soup + review','Use pantry beans and tomatoes; plan the next three dinners.')]
for i,(day,h,b) in enumerate(week):
 y=634-i*75;rect(36,y-66,540,67,palette[i%4]);text(day,48,y-14,47,9,orange,'Bold');text(h+'<br/>'+b,103,y-10,457,9)
done()
# 9
base('07 / Safety first','The label is part of the recipe')
for i,(h,b) in enumerate([('CHILL + SEPARATE','Keep fridge at 4 C / 40 F or below. Refrigerate perishables within 2 hours, or 1 hour above 32 C / 90 F. Use shallow containers; keep raw meat separate.'),('A CONSERVATIVE WORKBOOK RULE','Use refrigerated cooked components within 48 hours, or freeze promptly. USDA permits many cooked leftovers 3-4 days; this workbook uses a shorter default for mixed markets. Follow shorter labels/local rules.'),('RICE NEEDS EXTRA CARE','Cool cooked rice as quickly as possible, ideally within 1 hour. Refrigerate for no more than 1 day before reheating, or freeze promptly. Reheat only once; do not keep reheated leftovers.'),('HEAT THE FOOD, NOT JUST THE DISH','Check chicken, ground turkey and reheated leftovers reach 74 C / 165 F throughout. Stir microwave food and check multiple spots. Thaw in fridge, or follow safe microwave thawing and cook immediately.')]):card(h,b,637-i*136,123,palette[i])
text('Sources: FoodSafety.gov temperature chart; USDA reheating guidance; UK FSA rice and cooking guidance. Links on page 34. Smell cannot prove food is safe.',36,96,540,8);done()
# 10
base('08 / Make the same food taste new','Two sauces, two personalities')
photo('components',36,405,540,238)
card('HERB YOGURT / ABOUT 1/2 CUP','Mix 1/2 cup plain yogurt, 1 tbsp lemon juice and 1 tbsp finely chopped parsley or dill. Add a pinch of salt if wanted. For two bowls use 4 tbsp total. Contains milk.',383,135)
card('LEMON TAHINI / ABOUT 1/2 CUP','Whisk 3 tbsp tahini, 2 tbsp lemon juice and 2 tbsp water. Add extra water 1 tsp at a time until pourable. Taste before seasoning. Contains sesame.',232,135,palette[1]);done()
# 11
base('09 / Portion without guesswork','Shop from portions, then adjust')
card('For two typical adult dinners','Start with 2 cups cooked grain, about 250 g / 9 oz cooked chicken or 1 drained can beans, and 2 cups vegetables. These are practical starting amounts, not individualized nutrition targets.',635,130)
card('Scale with a multiplier','Four eaters instead of two? Multiply recipe ingredients by 2. One eater? Halve ingredients or portion and freeze suitable extras. Pan size and cooking time may need adjustment.',488,130,palette[1])
card('Measure the result once','Record what your household actually eats. If one rice portion remains, cook 1/2 cup less next time. Keep extra bread, beans or vegetables available if people are still hungry.',341,130,palette[2])
strip(84);done()
# 12-23 recipe cards
for i,r in enumerate(RECIPES):
 base('RECIPE '+r['id']+' / SERVES TWO',r['name'])
 photo(r['id'],36,429,540,224)
 rect(36,395,540,28,green);text(r['time']+'  |  From ready components where listed',49,416,514,8,'#FFFFFF','Bold')
 card('INGREDIENTS',r['ing'],384,118,palette[i%4])
 # Exact numbered instructions; enough space and bounded.
 text('<b>MAKE IT</b>',36,252,540,10,green)
 yy=231
 for n,s in enumerate(r['steps']):yy=text(str(n+1)+'. '+s,36,yy,540,9)-7
 assert yy>=113,('Recipe too long',r['id'],yy)
 text('<b>SWAP:</b> '+r['swap'],36,113,540,8)
 text('<b>ALLERGEN CHECK:</b> '+r['allergy'],36,84,540,7.2)
 done()
# 24
base('10 / A worked small start','Three dinners. One linked shop.','Example for two adults; check appetite, pack sizes and pantry stock.')
for i,(h,b) in enumerate([('DINNER 1 / CHICKEN BOWLS','Use half the cooked chicken, 2 cups rice, all 2 cups cooked vegetables, 4 tbsp herb yogurt sauce and half a lemon.'),('DINNER 2 / CHICKEN FLATBREADS','Use remaining chicken, 2 flatbreads, 1/2 cucumber, 1 cup cabbage and 4 tbsp herb yogurt sauce. Finish refrigerated chicken within 48 hours.'),('DINNER 3 / BLACK BEAN TACOS','Open 1 can black beans on the night. Add 4 small tortillas, 1 cup cabbage, salsa, cumin, paprika and lime. No cooked Sunday food needed.')]):card(h,b,633-i*157,141,palette[i])
text('Yield check: 500 g raw boneless chicken may yield roughly 350-400 g cooked, not the 500 g needed above. For these two recipes, buy about 700 g / 1.5 lb raw, then weigh and allocate 250 g cooked to each.',36,139,540,9);done()
# 25
base('11 / The example shopping list','Buy the gap, not the whole kitchen')
for i,(h,b) in enumerate([('PRODUCE','1 small broccoli + 2 carrots (aim for 2 cups cooked); 1/2 cucumber; cabbage for 2 shredded cups; 1 lemon; 1 lime; small bunch parsley or dill.'),('ANCHORS + BASES','About 700 g / 1.5 lb raw boneless chicken; 1 can black beans; dry rice sufficient for 2 cups cooked (check packet yield); 2 large flatbreads; 4 small tortillas.'),('CHILLED + JARS','1/2 cup plain yogurt; 4 tbsp salsa. Check use-by dates and storage instructions. Buy smaller packs when the rest has no planned use.'),('PANTRY CHECK','Oil; cumin; smoked paprika; salt if wanted. Optional: tahini for an alternative finish. Cross out what you own before shopping.')]):card(h,b,634-i*135,122,palette[i])
text('This list covers the three-dinner example only. The seven-night menu on page 8 requires additional ingredients from the relevant recipe cards.',36,96,540,8);done()
# 26
base('12 / Put names on containers','The fridge map that gets food eaten')
photo('components',36,406,540,237)
card('EXAMPLE LABEL / COOKED CHICKEN','Prepared Sunday 5 p.m. -> Monday bowls + Tuesday flatbreads. Refrigerate promptly; use within 48 hours under this workbook plan. Freeze promptly if Tuesday changes.',384,127)
card('THREE ZONES','EAT FIRST: ready components for the next 48 hours. KEEP SEPARATE: sauces and dry crunch. FROZEN BACKUP: later portions, labeled with name, date and intended meal. Store raw meat sealed below ready-to-eat food.',239,143,palette[1]);done()
# 27
base('13 / Troubleshooting','Fix friction before adding recipes')
for i,(h,b) in enumerate([('EVERYTHING TASTES THE SAME','Change two things: a new format, sauce or texture. Use the remix on page 7. Do not simply add more spice to every box.'),('VEGETABLES ARE WET','Dry washed produce. Roast without crowding. Store crunchy raw toppings separately; add sauce only at serving.'),('PREP TAKES TOO LONG','Halve the plan. Start with a grain, ready-to-use beans and one sauce. Buy frozen vegetables or pre-cut cabbage if useful.'),('PLANS CHANGE','Freeze suitable cooked portions promptly before their deadline. Keep unopened pantry meals as the backup; never extend a use-by date.'),('NOT ENOUGH FOOD','Record the shortfall. Increase only that component next week. Recipe portions are a starting point; appetite varies.')]):card(h,b,635-i*109,98,palette[i%4])
done()
# 28-32 worksheets
works=[('My component bank','Choose ingredients that can appear in at least two dinners.',['Component + amount','Dinner 1','Dinner 2','Use / freeze deadline']),('My prep sequence','Write cooking and cooling tasks; do not leave safety until the end.',['Time block','Task','Equipment','Done']),('My flexible dinner week','Mark fresh, refrigerated and frozen components explicitly.',['Day','Dinner','Source / thaw plan','Backup']),('My grocery gap check','Check shelves first. Write exact amounts and pack-size leftovers.',['Ingredient','Need / own','Buy amount','Extra goes to']),('My use-first tracker','Copy dates from labels. Freeze suitable food promptly when plans change.',['Food','Prepared / opened','Use / freeze by','Meal'])]
for wi,(h,sub,cols) in enumerate(works):
 base('PRINT + REUSE / '+str(wi+1),h,sub)
 rect(36,573,540,54,green)
 for j,t in enumerate(cols):text(t,46+j*135,610,115,8,'#FFFFFF','Bold')
 for i in range(7):
  y=510-i*60;rect(36,y,540,55,palette[i%4],5)
  c.setStrokeColor(HexColor('#A4B2A5'));c.setLineWidth(.5)
  for j in range(1,4):c.line(36+j*135,y+7,36+j*135,y+48)
 text('Small plan, clear labels, useful food. Photograph your completed page if that helps your household coordinate.',36,96,540,8);done()
# 33
base('14 / Make it yours','The four-week confidence check')
for i,(h,b) in enumerate([('WEEK 1 / THREE DINNERS','Complete the page 24 example or your own equivalent. Record prep time, leftover amounts and the dinner everyone liked best.'),('WEEK 2 / ONE REMIX','Keep the winning components. Change one meal format and one sauce. Avoid adding a whole new ingredient list.'),('WEEK 3 / A REAL BACKUP','Freeze a suitable portion promptly and schedule when to thaw it. Try an unopened pantry dinner on your busiest night.'),('WEEK 4 / KEEP THE WINNERS','Choose 6 favorite meal builds. Compare planned dinners with dinners eaten. Track unused food and extra shopping trips; improve one friction point.')]):card(h,b,634-i*135,121,palette[i])
text('Success means less decision effort and more food eaten - not perfect meal prep. This is a planning system, not a medical or nutrition prescription.',36,96,540,8);done()
# 34
base('Sources + honest production notes','Read, verify, then make it yours')
refs=[('Safe minimum temperatures','https://www.foodsafety.gov/food-safety-charts/safe-minimum-internal-temperatures'),('USDA: reheating leftovers','https://ask.fsis.usda.gov/article/How-do-I-reheat-leftovers-safely'),('UK FSA: rice and reheating','https://www.gov.uk/government/publications/home-food-fact-checker/home-food-fact-checker'),('UK FSA: cooking food','https://www.food.gov.uk/safety-hygiene/cooking-your-food')]
y=636
for i,(name,url) in enumerate(refs):
 rect(36,y-67,540,68,palette[i]);text(name,49,y-12,514,10,green,'Bold');text(url,49,y-37,514,7);c.linkURL(url,(36,y-67,576,y),relative=0);y-=78
card('ARTWORK SELF-CHECK','15 unique images were generated exclusively for this product through the OpenAI Images API. Every placement is mapped to a request record and SHA-256 hash in the accompanying provenance file. Photos are illustrative AI artwork.',310,113)
card('BEFORE COMMERCIAL RELEASE','Recipes have not been kitchen-tested. Test yields, timing and reheating with your equipment; check allergies, accessibility and local food rules. The 60-minute routine is a target, not a guaranteed result. No nutrition or savings claims are verified.',181,113,palette[1]);done()
c.save()
# Fail closed: every embedded visual must derive from the recorded OpenAI assets.
assert set(p['asset_id'] for p in placements)==set(a['id'] for a in ART)
assert all(63<=b['bottom']<=b['top']<=792 and b['right']<=612 for b in bounds)
doc=fitz.open(out);assert len(doc)==34
render=ROOT/'page-previews';render.mkdir(exist_ok=True)
thumbs=[]
for i,page in enumerate(doc):
 assert page.get_text().strip(),('No selectable body text',i+1)
 pix=page.get_pixmap(matrix=fitz.Matrix(1,1));pix.save(str(render/('page-%02d.png'%(i+1))))
 im=Image.open(render/('page-%02d.png'%(i+1))).convert('RGB');im.thumbnail((244,317));thumbs.append(im)
for start in range(0,len(thumbs),12):
 sheet=Image.new('RGB',(4*264,3*347),'#ddd8ce');draw=ImageDraw.Draw(sheet)
 for j,im in enumerate(thumbs[start:start+12]):x=(j%4)*264+10;y=(j//4)*347+20;sheet.paste(im,(x,y));draw.text((x,y-16),str(start+j+1),fill='black')
 sheet.save(ROOT/('contact-sheet-%d.jpg'%(start//12+1)),quality=90)
(ROOT/'self-check.json').write_text(json.dumps({'artwork_provenance_passed':True,'unique_openai_assets':15,'placement_count':len(placements),'pdf_pages':len(doc),'selectable_text_on_all_pages':True,'footer_bounds_passed':True,'all_assets_used':True,'human_visual_review':'Pending inspection of final rendered pages','recipe_kitchen_testing':'Not performed','placements':placements,'text_bounds':bounds},indent=2))
shutil.copy(__file__,ROOT/'build_product6_openai.py')
print('PDF complete: 34 pages; 15 verified OpenAI assets; visual review still required.',flush=True)
