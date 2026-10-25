"""Check crawlable discovery pages, metadata, feed targets and original content preservation."""
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote
from xml.etree import ElementTree as ET
import json

ROOT=Path(__file__).resolve().parents[1]
errors=[]
pages={p.relative_to(ROOT).as_posix():BeautifulSoup(p.read_text(),'html.parser') for p in ROOT.rglob('*.html') if '.git' not in p.parts}
def local_url(url, current):
    parsed=urlparse(url)
    if parsed.scheme and parsed.scheme not in ['http','https']: return None
    if parsed.netloc and parsed.netloc!='whatsforeats.online': return None
    path=unquote(parsed.path)
    if path.startswith('/'): file=path.lstrip('/') or 'index.html'
    elif path: file=(Path(current).parent/path).as_posix()
    else: file=current
    return file, unquote(parsed.fragment)

for name,soup in pages.items():
    if '/' not in name:
        canonical=soup.select('link[rel=canonical]')
        if len(canonical)!=1: errors.append(f'{name}: expected one canonical')
        if len(soup.select('h1'))!=1: errors.append(f'{name}: expected one H1')
        if len(soup.select('script[src="/assets/site-growth.js"]'))!=1: errors.append(f'{name}: analytics loader missing/duplicated')
        if 'googletagmanager.com/gtag/js' in str(soup): errors.append(f'{name}: ungated analytics remains')
    for script in soup.select('script[type="application/ld+json"]'):
        try: json.loads(script.get_text())
        except ValueError: errors.append(f'{name}: invalid JSON-LD')
    for tag in soup.select('a[href],img[src],script[src],link[href]'):
        value=tag.get('href') or tag.get('src')
        result=local_url(value,name)
        if not result: continue
        file,fragment=result
        if not (ROOT/file).is_file(): errors.append(f'{name}: missing target {value}')
        # Audit fragments for newly built links. Existing legacy article hashes are outside scope.
        if name=='what-to-make-for-dinner.html' and fragment and file in pages and not pages[file].find(id=fragment): errors.append(f'{name}: missing anchor {value}')
    if name in ['index.html','easy-weeknight-dinner-recipes.html']:
        for figure in soup.select('figure[data-file]'):
            if len(figure.select('img'))!=1: errors.append(f'{name}: figure must have one static image')
    if name=='5-47-rescue-kit.html':
        for link in soup.select('a.cta'):
            if urlparse(link.get('href')).hostname!='whop.com': errors.append('Product checkout needs JS')

root=ET.parse(ROOT/'sitemap.xml').getroot()
locs=[x.text for x in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
assert len(locs)==len(set(locs)), 'Duplicate sitemap URL'
for url in locs:
    file,_=local_url(url,'index.html')
    if not (ROOT/file).is_file(): errors.append('Sitemap missing file '+url)
    if file in pages:
        robots=pages[file].find('meta',attrs={'name':'robots'})
        if robots and 'noindex' in robots.get('content',''): errors.append('Noindex page in sitemap '+url)
for file in ['what-to-make-for-dinner.html','5-47-rescue-kit.html']:
    if 'https://whatsforeats.online/'+file not in locs: errors.append('Sitemap omits '+file)
feed=ET.parse(ROOT/'pinterest-feed.xml').getroot()
items=feed.findall('channel/item')
assert len(items)==3
guids=set()
for item in items:
    guid=item.findtext('guid');assert guid not in guids;guids.add(guid)
    assert len(item.findtext('title'))<=100 and len(item.findtext('description'))<=500
    for url in [item.findtext('link'),item.find('enclosure').get('url')]:
        file,_=local_url(url,'index.html')
        assert (ROOT/file).is_file(),url
assert len(pages['what-to-make-for-dinner.html'].select('.dinner-card'))==12
if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: {len(pages)} HTML pages, {len(locs)} sitemap URLs, 12 recipe destinations and 3 Pinterest feed items. No missing local targets or invalid JSON-LD.')
