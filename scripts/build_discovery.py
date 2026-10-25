"""Maintain discovery metadata and the curated Pinterest feed. Run from any folder.
Install beautifulsoup4 first. Existing page prose/layout is preserved with scoped edits.
"""
from pathlib import Path
from html import escape
from urllib.parse import urljoin, urlencode, urlparse
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup
import json
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://whatsforeats.online/'
CHECKOUT = 'https://whop.com/life-shapers/the-5-47-p-m-rescue-kit-lazy-dinner-planner/'
CAMPAIGN = [
    {'slug':'what-to-make-for-dinner','title':'What should I make for dinner? Try this free dinner finder','description':'Too tired to decide what to cook? Choose your available time, effort and main ingredient to browse 12 practical dinner ideas with links to full recipes. Free to use, with no signup. Save it for your next busy evening.','image':'assets/pins/dinner-finder.jpg','board':'Easy Weeknight Dinners','intent':'what should I make for dinner','creative':'dinner-finder'},
    {'slug':'5-ingredient-dinners','title':'5-ingredient dinners for busy nights','description':'Keep dinner simple with seven flexible recipes, measured ingredients and step-by-step directions. Find black bean sweet potatoes, cheesy bean quesadillas, pasta and more. Read the free guide and choose one meal for tonight.','image':'assets/pins/five-ingredients.jpg','board':'Easy Weeknight Dinners','intent':'5 ingredient dinners','creative':'five-ingredients'},
    {'slug':'7-night-dinner-plan-for-picky-families','title':'A 7-night dinner plan for picky families','description':'Take some of the guessing out of dinner with a flexible seven-night plan. Explore tacos, pasta, breakfast for dinner and build-your-own plates, with practical serving ideas. Read the free plan and adapt it to your family.','image':'assets/pins/family-plan.jpg','board':'Family Meal Planning','intent':'meal plan for picky families','creative':'family-plan'},
]

def add_meta(text, soup, key, value, prop=False):
    attr = 'property' if prop else 'name'
    if soup.find('meta', attrs={attr:key}):
        return text
    return text.replace('</head>',f'<meta {attr}="{key}" content="{escape(value, quote=True)}">\n</head>',1)

def build():
    changed_images = 0
    for path in sorted(ROOT.glob('*.html')):
        text = path.read_text()
        # One consent-controlled loader replaces the formerly uneven inline GA setup.
        text = re.sub(r'<!-- Google tag \(gtag.js\) -->\s*<script async src="https://www.googletagmanager.com/gtag/js\?id=G-QM26ZNDC24"></script>\s*<script>.*?</script>', '', text, count=1, flags=re.S)
        soup = BeautifulSoup(text,'html.parser')
        canonical = soup.find('link',rel='canonical')
        if not canonical:
            continue
        url = canonical.get('href')
        title = soup.title.get_text(strip=True)
        desc_tag = soup.find('meta', attrs={'name':'description'})
        desc = desc_tag.get('content') if desc_tag else title
        # Render existing figure images in HTML so they load without JS, with no duplicates.
        for index, figure in enumerate(soup.select('figure[data-file]')):
            if figure.find('img'):
                continue
            src = figure.get('data-file')
            if not (ROOT/src).is_file():
                continue
            pattern = r'(<figure\b[^>]*data-file="'+re.escape(src)+r'"[^>]*>)(\s*)(</figure>)'
            loading = 'eager' if index == 0 else 'lazy'
            attrs = ' fetchpriority="high"' if index == 0 else ''
            img = f'<img src="{escape(src)}" alt="{escape(figure.get("data-alt", ""),quote=True)}" loading="{loading}" decoding="async"{attrs}>'
            text,n = re.subn(pattern,lambda m:m[1]+img+m[3],text,count=1)
            changed_images += n
        text = text.replace('var i=new Image();i.alt=f.dataset.alt||"";i.loading="lazy";', 'if(f.querySelector("img"))return;\n  var i=new Image();i.alt=f.dataset.alt||"";i.loading="lazy";') if 'if(f.querySelector("img"))return;' not in text else text
        # Working, crawlable CTA hrefs even if JavaScript is blocked.
        for a in soup.select('a.rk, a.vt'):
            old=str(a)
            target=BASE+'5-47-rescue-kit.html' if 'rk' in a.get('class',[]) else 'https://fatboylove5885.github.io/Cheap-Dinner-Home/'
            # Match only the opening tag, without reformatting adjacent content.
            pattern=r'<a\b(?=[^>]*class="[^"]*\b'+('rk' if 'rk' in a.get('class',[]) else 'vt')+r'\b)[^>]*>'
            text=re.sub(pattern,lambda m:re.sub(r'href="[^"]*"',f'href="{target}"',m[0]),text)
        if path.name=='5-47-rescue-kit.html':
            text = re.sub(r'(<a\b[^>]*class="cta"[^>]*href=")#(")',lambda m:m[1]+CHECKOUT+m[2],text)
        soup=BeautifulSoup(text,'html.parser')
        og=soup.find('meta',property='og:image')
        image=og.get('content') if og else BASE+'blog-1-hero.jpg'
        if path.name=='5-47-rescue-kit.html': image=BASE+'rescue-kit-fridge.jpg'
        if path.name=='what-to-make-for-dinner.html': image=BASE+'assets/pins/dinner-finder.jpg'
        for key,value,prop in [('og:url',url,True),('og:site_name',"What's for Eats",True),('og:title',title,True),('og:description',desc,True),('og:image',image,True),('og:type','website' if path.name in ['index.html','5-47-rescue-kit.html','what-to-make-for-dinner.html'] else 'article',True),('twitter:card','summary_large_image',False),('twitter:image',image,False),('robots','index,follow,max-image-preview:large',False)]:
            text=add_meta(text,soup,key,value,prop)
        if '/assets/site-growth.js' not in text:
            text=text.replace('</head>','<link rel="stylesheet" href="/assets/site-growth.css"><script src="/assets/site-growth.js" defer></script>\n</head>',1)
        if 'application/rss+xml' not in text:
            text=text.replace('</head>','<link rel="alternate" type="application/rss+xml" title="What\'s for Eats dinner ideas" href="https://whatsforeats.online/pinterest-feed.xml">\n</head>',1)
        if path.name not in ['what-to-make-for-dinner.html','5-47-rescue-kit.html','privacy.html','freebies.html'] and 'class="wfe-discover"' not in text:
            pin=next((p for p in CAMPAIGN if path.stem==p['slug']),None)
            pin_image=BASE+pin['image'] if pin else image
            pin_url='https://www.pinterest.com/pin/create/button/?'+urlencode({'url':url,'media':pin_image,'description':title})
            block=f'''<aside class="wfe-discover" aria-label="Find your next dinner"><h2>Still deciding what to make?</h2><p>Match a dinner to your time and energy, or plan the week with our free guides.</p><div class="wfe-discover-links"><a class="wfe-primary" href="/what-to-make-for-dinner.html">Try the free dinner finder</a><a href="/free-pdfs.html">Free meal-planning printables</a><a href="{escape(pin_url,quote=True)}" target="_blank" rel="noopener noreferrer">Save this guide to Pinterest</a></div></aside>'''
            # Early internal links on index pages; end-of-content discovery on full articles.
            if path.name in ['index.html','blogs.html','free-pdfs.html'] and '<h1' in text:
                text=re.sub(r'(</h1>)',lambda m:m[1]+block,text,count=1)
            elif '</main>' in text:
                text=text.replace('</main>',block+'</main>',1)
            else:
                text=text.replace('<footer',block+'<footer',1)
        # Use accurate Article URLs and images; retain existing recipe/FAQ content untouched.
        def enrich(match):
            try: data=json.loads(match[1])
            except json.JSONDecodeError: return match[0]
            nodes=data.get('@graph',[data]) if isinstance(data,dict) else data
            for node in nodes:
                if node.get('@type') in ['Article','BlogPosting']:
                    node['url']=url
                    node['mainEntityOfPage']={'@type':'WebPage','@id':url}
                    node.setdefault('image',[image])
                    if isinstance(node.get('isPartOf'),dict) and node['isPartOf'].get('url'):
                        node['isPartOf']['url']=urljoin(BASE,node['isPartOf']['url'])
            return '<script type="application/ld+json">'+json.dumps(data,ensure_ascii=False)+'</script>'
        text=re.sub(r'<script type="application/ld\+json">(.*?)</script>',enrich,text,flags=re.S)
        path.write_text(text)

    # Keep existing indexable entries and add the restored product and finder.
    ns='http://www.sitemaps.org/schemas/sitemap/0.9'
    ET.register_namespace('',ns)
    sitemap=ET.parse(ROOT/'sitemap.xml')
    for node in list(sitemap.getroot()):
        loc=node.find('{'+ns+'}loc')
        local=ROOT/urlparse(loc.text).path.lstrip('/')
        if local.is_file() and local.suffix=='.html':
            robots=BeautifulSoup(local.read_text(),'html.parser').find('meta',attrs={'name':'robots'})
            if robots and 'noindex' in robots.get('content',''):
                sitemap.getroot().remove(node)
    urls={e.text for e in sitemap.findall('.//{'+ns+'}loc')}
    for rel in ['5-47-rescue-kit.html','what-to-make-for-dinner.html']:
        url=BASE+rel
        if url not in urls:
            node=ET.SubElement(sitemap.getroot(),'{'+ns+'}url');ET.SubElement(node,'{'+ns+'}loc').text=url;urls.add(url)
    ET.indent(sitemap,space='  ')
    sitemap.write(ROOT/'sitemap.xml',encoding='utf-8',xml_declaration=True)
    media='http://search.yahoo.com/mrss/'
    atom='http://www.w3.org/2005/Atom'
    ET.register_namespace('media',media);ET.register_namespace('atom',atom)
    rss=ET.Element('rss',version='2.0');channel=ET.SubElement(rss,'channel')
    ET.SubElement(channel,'title').text="What's for Eats — practical dinner ideas"
    ET.SubElement(channel,'link').text=BASE
    ET.SubElement(channel,'description').text='Free dinner tools and guides for busy households.'
    ET.SubElement(channel,'language').text='en-us'
    ET.SubElement(channel,'{'+atom+'}link',href=BASE+'pinterest-feed.xml',rel='self',type='application/rss+xml')
    for index,pin in enumerate(CAMPAIGN):
        pin['url']=BASE+pin['slug']+'.html'
        pin['tracked_url']=pin['url']+'?'+urlencode({'utm_source':'pinterest','utm_medium':'organic_social','utm_campaign':'dinner_rescue_2026_10','utm_content':pin['creative']})
        pin['status']='ready_to_publish_not_scheduled'
        item=ET.SubElement(channel,'item')
        for tag,value in [('title',pin['title']),('link',pin['tracked_url']),('description',pin['description'])]: ET.SubElement(item,tag).text=value
        ET.SubElement(item,'guid',isPermaLink='false').text='wfe-dinner-rescue-2026-10-'+pin['creative']
        # Launch-feed publication dates, not claims that older articles were newly written.
        ET.SubElement(item,'pubDate').text=f'Sun, 25 Oct 2026 16:0{index}:00 GMT'
        ET.SubElement(item,'{'+media+'}content',url=BASE+pin['image'],medium='image',type='image/jpeg',width='1024',height='1536')
        ET.SubElement(item,'enclosure',url=BASE+pin['image'],type='image/jpeg',length=str((ROOT/pin['image']).stat().st_size))
    ET.indent(rss,space='  ');ET.ElementTree(rss).write(ROOT/'pinterest-feed.xml',encoding='utf-8',xml_declaration=True)
    (ROOT/'marketing/pinterest-launch.json').write_text(json.dumps(CAMPAIGN,indent=2,ensure_ascii=False)+'\n')
    print(f'Updated discovery metadata; added {changed_images} static image elements; sitemap has {len(urls)} URLs; RSS has {len(CAMPAIGN)} distinct campaign items.')

if __name__ == '__main__': build()
