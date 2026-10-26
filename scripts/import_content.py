"""Import Naverah HTML export. Usage: python scripts/import_content.py SOURCE_DIRECTORY.
Requirements: beautifulsoup4, Pillow. Preserves source slugs, article bodies and property details.
"""
from pathlib import Path
from bs4 import BeautifulSoup,Comment
from PIL import Image,ImageOps
from urllib.parse import unquote
import re,json,hashlib,shutil,sys
root=Path(sys.argv[1]).resolve();out=Path(__file__).resolve().parents[1];media=out/'public/media';media.mkdir(parents=True,exist_ok=True)
assets={};missing=set()
def txt(x):return ' '.join(x.get_text(' ',strip=True).split()) if x else ''
def asset(src):
 if not src:return ''
 src=unquote(src).replace('\n','').replace('\r','').strip().split('?')[0].replace('\\','/');src=re.sub(r'^https?://(?:www\.)?naverahassets.com/','',src).removeprefix('../').lstrip('/')
 if src in assets:return assets[src]
 if src.startswith(('http:','https:','data:')):return src
 f=root/src
 if not f.is_file():missing.add(src);return ''
 name=re.sub('[^a-zA-Z0-9_-]','-',f.stem)[-80:]+'-'+hashlib.sha1(src.encode()).hexdigest()[:8];ext=f.suffix.lower();dest=name+('.webp' if ext in ['.png','.jpg','.jpeg','.webp','.avif'] else ext)
 if not (media/dest).exists():
  try:
   if dest.endswith('.webp'):
    im=ImageOps.exif_transpose(Image.open(f));im.thumbnail((1920,1920));im.save(media/dest,'WEBP',quality=86)
   else:shutil.copy2(f,media/dest)
  except:dest=name+ext;shutil.copy2(f,media/dest)
 assets[src]='/media/'+dest;return assets[src]
def clean(node):
 if not node:return ''
 s=BeautifulSoup(str(node),'html.parser')
 for x in s(['script','style','iframe','form','button']):x.decompose()
 for x in s.find_all(string=lambda t:isinstance(t,Comment)):x.extract()
 for x in s.find_all(True):
  attrs={k:v for k,v in x.attrs.items() if k in ['href','src','alt','colspan','rowspan','title']}
  if 'href' in attrs:
   h=re.sub(r'^https?://(?:www\.)?naverahassets.com','',attrs['href'])
   if h.startswith('javascript:'):attrs.pop('href')
   else:attrs['href']=h if h.startswith(('http','mailto:','tel:','#','/')) else '/'+h
  if x.name=='img':attrs.update(src=asset(attrs.get('src')),loading='lazy')
  x.attrs=attrs
 return str(s)
soups={f.name:BeautifulSoup(f.read_text(errors='ignore'),'html.parser') for f in root.glob('*.html')}
raw=soups['properties.html'].decode().split('const properties =',1)[1].split('];',1)[0]+']';raw=re.sub(r'//[^\n]*','',raw);raw=re.sub(r',\s*([}\]])',r'\1',raw);listings=json.loads(raw);lmap={p['url']:p for p in listings}
blogmeta={}
for c in soups['blog.html'].select('.blog-card-individual-item'):
 a=c.select_one('a[href]');im=c.select_one('img.blog-card-image')
 if a:blogmeta[a['href'].lstrip('/')]=dict(date=txt(c.select_one('.blog-card-info .body-text-default')),image=asset(im.get('src')) if im else '')
css='\n'.join(p.read_text(errors='ignore') for p in root.rglob('*.css'))
def bg(s):
 for x in s.select('[class*=bg-image]'):
  for cl in x.get('class',[]):
   m=re.search(r'\.'+re.escape(cl)+r'\s*\{[^}]*?background-image:\s*url\([\"\']?([^\"\')]+)',css)
   if m:
    a=asset(m[1])
    if a:return a
 return ''
articles=[];properties=[];pages={}
for fn,s in soups.items():
 meta=s.find('meta',attrs={'name':'description'});p=dict(slug=fn[:-5],url='/'+fn,title=txt(s.find('h1')),seoTitle=txt(s.title),description=meta.get('content','') if meta else '')
 rich=s.select_one('.w-richtext')
 if rich and fn!='property-details.html':
  p.update(body=clean(rich),**blogmeta.get(fn,dict(date='',image='')))
  if not p['image']:
   im=s.select_one('.blog-details-image,img[alt="Blog Image"]');p['image']=asset(im.get('src')) if im else ''
  articles.append(p)
 elif fn in lmap or fn=='property-details.html' or s.select_one('.pricing-section-parent'):
  p.update(lmap.get(fn,{}));p['url']='/'+fn;p['image']=asset(p.get('image',''));p['hero']=bg(s) or p['image'];p['location']=p.get('location',txt(s.select_one('h5')))
  about=s.select_one('.properties-details-section');p['about']=clean(about);p.update(sections=[],gallery=[],plans=[],prices=[],amenities=[],locationBody='',brochures=[])
  for sec in s.select('section'):
   cl=' '.join(sec.get('class',[]))
   if 'pricing-section-parent' in cl:
    for c in sec.select('.card,.card2'):p['prices'].append(dict(type=txt(c.select_one('.typology,.typology2')),price=txt(c.select_one('.price-details')),area=txt(c.select_one('.size-detail,.size-detail2'))))
   if 'gallery-section-parent' in cl:
    arr=p['plans'] if 'Floor Plan' in txt(sec) else p['gallery']
    for im in sec.select('img'):
     a=asset(im.get('src'))
     if a and a not in arr:arr.append(a)
   if 'properties-details-section' in cl and sec!=about:
    p['sections'].append(dict(title=txt(sec.find(['h2','h3','h4'])),html=clean(sec)))
    # Structured amenity items retain source captions and images.
    for im in sec.select('img'):
     a=asset(im.get('src'));parent=im.parent
     while parent and not txt(parent) and parent!=sec:parent=parent.parent
     caption=txt(parent) if parent else ''
     if a:p['amenities'].append(dict(image=a,title=caption if len(caption)<100 else im.get('alt','')))
   if 'location-section' in cl:p['locationBody']=clean(sec)
  p['brochures']=[dict(label=txt(a) or 'Download brochure',url=asset(a['href'])) for a in s.select('a[href]') if a['href'].lower().endswith('.pdf')]
  if not p['gallery']:p['gallery']=list(dict.fromkeys(asset(i.get('src')) for i in s.select('img') if 'property-details-images/' in i.get('src','') and asset(i.get('src'))))[:12]
  if not p['image']:p['image']=p['hero'] or (p['gallery'][0] if p['gallery'] else '')
  if not p.get('type'):
   body=txt(about).lower();p['type']='Plots' if 'plot' in body else 'Villas' if 'villa' in body else 'Apartments' if 'apartment' in body else 'Residential'
  properties.append(p)
 else:pages[fn[:-5]]=p
properties.sort(key=lambda p:next((i for i,q in enumerate(listings) if '/'+q['url']==p['url']),999));articles.sort(key=lambda p:next((i for i,q in enumerate(blogmeta) if '/'+q==p['url']),999))
s=soups['service.html'];services=[]
for b in s.select('.buy-property-main-content,.sell-property-content-block'):
 h=b.select_one('.section-tag-text');items=[txt(x) for x in b.select('.list-header-text')];im=b.select_one('img')
 if h and items:
  title=txt(h);slug=re.sub('[^a-z0-9]+','-',title.lower()).strip('-');fallback={'Home Loans & Financial Assistance':'services-images/homeloan_financialassitance.png','Legal & Documentation Support':'services-images/legal_support.png','Property Resale & Leasing':'services-images/resale_leasing.png'};services.append(dict(title=title,slug=slug,url='/services/'+slug,image=asset(im.get('src')) if im else asset(fallback.get(title)),points=items))
types=[]
for title in ['Apartments','Villas','Row Houses','Bungalows','Plots','Independent Homes','Farmhouses']:
 el=s.find(string=lambda t:t and t.strip()==title)
 if el:types.append(dict(title=title,description=txt(el.parent.parent)))
home=soups['index.html'];testimonials=[dict(quote=txt(x.select_one('h2')),name=txt(x.select_one('h3')),role=txt(x.select_one('p'))) for x in home.select('.default-testimonial-slide')]
a=soups['about.html'];founder=[txt(x) for x in a.select('p.letter-elabration-description')[:4]];about=[txt(p) for p in a.select('p') if 'Naverah Assets Private Limited — your trusted' in txt(p) or 'At Naverah Assets, we believe' in txt(p) or 'The Meaning Behind' in txt(p)];faqs=[]
for x in a.select('[class*=faq]'):
 if any('item' in c for c in x.get('class',[])):
  m=re.match(r'(.+?\?)(.*)',txt(x))
  if m and len(m[2].strip())>20 and not any(y['question']==m[1] for y in faqs):faqs.append(dict(question=m[1],answer=m[2].strip()))
team=[]
for name,role,img in [('Naveed Ahmed Shaikh','Founder & Managing Director','about-images/naveed-ahmed.jpg'),('Richard wayne','The deal closer','agent-images/67d677f87a8964eda8e2fbc8_Team Member 2.webp'),('George allen','The innovation agent','agent-images/67d677fec62f330473a41b1e_Team Member 3.webp')]:
 slug=re.sub('[^a-z0-9]+','-',name.lower());team.append(dict(name=name,role=role,slug=slug,url='/team/'+slug,image=asset(img),bio=founder if not team else []))
images={k:asset(v) for k,v in dict(logo='images/naverah-logo-main.png',about='about-images/abouts-us-img-1.png',mission='about-images/our_mission.png',vision='about-images/our_vision.png',values='about-images/our_values.png',founder='about-images/naveed-ahmed.jpg').items()}
data=dict(pages=pages,articles=articles,properties=properties,services=services,propertyTypes=types,testimonials=testimonials,team=team,about=about,faqs=faqs,images=images)
(out/'src/data/content.json').write_text(json.dumps(data,ensure_ascii=False,indent=2));(out/'src/data/asset-map.json').write_text(json.dumps(assets,indent=2));(out/'src/data/migration.json').write_text(json.dumps(dict(sourcePageCount=len(soups),articles=len(articles),properties=len(properties),pages=len(pages),sourceFiles=sorted(soups),missingSourceAssets=sorted(missing)),indent=2));print(dict(articles=len(articles),properties=len(properties),services=len(services),assets=len(assets),missing=len(missing)))
