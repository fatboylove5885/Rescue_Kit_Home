"""After deployment, notify IndexNow of indexable HTML URLs from the sitemap.
Requires only Python's standard library. No paid service or account credentials.
"""
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlparse
from xml.etree import ElementTree as ET
import json
import argparse

ROOT=Path(__file__).resolve().parents[1]
HOST='whatsforeats.online'
BASE='https://'+HOST+'/'
parser=argparse.ArgumentParser()
parser.add_argument('--submit',action='store_true',help='Submit once after verifying the deployed ownership file.')
args=parser.parse_args()
urls=[node.text for node in ET.parse(ROOT/'sitemap.xml').getroot().iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc') if node.text.endswith('.html') or node.text==BASE]
assert all(urlparse(url).hostname==HOST for url in urls)
print(f'{len(urls)} indexable HTML URLs prepared.')
if not args.submit:
    print('Dry run. Use --submit after deployment to notify participating search engines.')
    raise SystemExit(0)
key=(ROOT/'indexnow-key.txt').read_text().strip()
with urlopen(BASE+'indexnow-key.txt',timeout=30) as response:
    assert response.status==200 and response.read().decode().strip()==key, 'Ownership file is not deployed.'
payload={'host':HOST,'key':key,'keyLocation':BASE+'indexnow-key.txt','urlList':urls}
request=Request('https://api.indexnow.org/indexnow',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json; charset=utf-8'},method='POST')
with urlopen(request,timeout=30) as response:
    print('IndexNow HTTP status:',response.status)
    if response.status==200: print('URLs received. This does not guarantee crawling, indexing or rankings.')
    elif response.status==202: print('URLs received; key validation pending. This does not confirm indexing.')
