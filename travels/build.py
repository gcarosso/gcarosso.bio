#!/usr/bin/env python3
"""Rebuild travels/index.html from photos.json (trips, counts, names) and captions.txt (your words).
Run from the site folder:  python3 travels/build.py"""
import json,re,html,os
HERE=os.path.dirname(os.path.abspath(__file__))
P=json.load(open(os.path.join(HERE,'photos.json'),encoding='utf-8'))
MEDIA='https://media.gcarosso.bio'
caps={}
for line in open(os.path.join(HERE,'captions.txt'),encoding='utf-8'):
    line=line.rstrip()
    if not line or line.startswith('#'): continue
    m=re.match(r'([a-z0-9-]+)\s+(\d+):\s*(.*)$',line)
    if m and m.group(3).strip(): caps[(m.group(1),int(m.group(2)))]=m.group(3).strip()
# order.txt: per-trip display order of photo ids and clip names, and the cover photo
order={}
cur=None
for line in open(os.path.join(HERE,'order.txt'),encoding='utf-8'):
    line=line.strip()
    m=re.match(r'##\s.*\[([a-z0-9-]+)\]$',line)
    if m: cur=m.group(1); order[cur]={}; continue
    if not cur or not line or line.startswith('#'): continue
    key,_,val=line.partition(':'); order[cur][key.strip()]=val.split()
cards=''; ov=''
for t in P['trips']:
    k,n,N=t['key'],t['name'],t['count']
    o=order.get(k,{}); photo_ids=[int(x) for x in o.get('photos',[str(i) for i in range(1,N+1)])]
    clipmap={c['name']:c for c in t.get('clips',[])}; clip_names=[c for c in o.get('clips',list(clipmap)) if c in clipmap]
    cover=int(o.get('cover',['1'])[0]); items=[('p',i) for i in photo_ids]+[('v',c) for c in clip_names]; T=len(items)
    nc=len(clip_names); cards+=f'    <a class="trip" href="#{k}"><img src="img/{k}/{cover:02d}.jpg" alt="" loading="lazy"><span class="tn">{html.escape(n)}</span><span class="tc">{len(photo_ids)} photos'+(f' · {nc} video'+('s' if nc>1 else '') if nc else '')+'</span></a>\n'
    slides=''
    for pos,(kind,ref) in enumerate(items,1):
        prev=pos-1 if pos>1 else T; nxt=pos+1 if pos<T else 1
        if kind=='p':
            cap=caps.get((k,ref),''); text=html.escape(n)+f' · {pos} / {T}'+(' — '+html.escape(cap) if cap else '')
            media=f'<img src="img/{k}/{ref:02d}.jpg" alt="{html.escape(cap)}" loading="lazy">'
        else:
            cap=clipmap[ref].get('caption',''); text=html.escape(n)+f' · {pos} / {T}'+(' — '+html.escape(cap) if cap else '')+' · video'
            media=f'<video controls preload="none" playsinline poster="img/{k}/{ref}.jpg"><source src="{MEDIA}/travels/{k}/{ref}.mp4" type="video/mp4"></video>'
        slides+=f'      <figure class="slide" id="{k}-{pos}"><a class="nav prev" href="#{k}-{prev}" aria-label="previous">‹</a>{media}<a class="nav next" href="#{k}-{nxt}" aria-label="next">›</a><figcaption>{text}</figcaption></figure>\n'
    ov+=f'  <section class="gallery" id="{k}">\n    <a class="close" href="#travels" aria-label="close">×</a>\n    <div class="strip">\n{slides}    </div>\n  </section>\n'
p=os.path.join(HERE,'index.html'); s=open(p,encoding='utf-8').read()
main=f'<main id="travels">\n\n  <h1>Travels</h1>\n  <p class="sub">Assorted adventures &amp; swashbucklings.</p>\n\n  <div class="trips">\n{cards}  </div>\n\n{ov}</main>'
s=re.sub(r'<main id="travels">.*?</main>',main,s,count=1,flags=re.S); open(p,'w',encoding='utf-8').write(s)
print(f"travels/index.html rebuilt: {len(P['trips'])} trips, {sum(t['count'] for t in P['trips'])} photos, {len(caps)} captions")
