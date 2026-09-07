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
cards=''; ov=''
for t in P['trips']:
    k,n,N=t['key'],t['name'],t['count']
    nc=len(t.get('clips',[])); cards+=f'    <a class="trip" href="#{k}"><img src="img/{k}/cover.jpg" alt="" loading="lazy"><span class="tn">{html.escape(n)}</span><span class="tc">{N} photos'+(f' · {nc} video'+('s' if nc>1 else '') if nc else '')+'</span></a>\n'
    slides=''
    for i in range(1,N+1):
        T=N+len(t.get('clips',[])); prev=i-1 if i>1 else T; nxt=i+1 if i<T else 1
        cap=caps.get((k,i),''); text=html.escape(n)+f' · {i} / {T}'+(' — '+html.escape(cap) if cap else '')
        slides+=f'      <figure class="slide" id="{k}-{i}"><a class="nav prev" href="#{k}-{prev}" aria-label="previous">‹</a><img src="img/{k}/{i:02d}.jpg" alt="{html.escape(cap)}" loading="lazy"><a class="nav next" href="#{k}-{nxt}" aria-label="next">›</a><figcaption>{text}</figcaption></figure>\n'
    # video clips after the photos: hosted on R2 at MEDIA, poster in the repo, browser's own player
    for j,c in enumerate(t.get('clips',[]),1):
        i=N+j; prev=i-1; nxt=i+1 if i<N+len(t['clips']) else 1
        cap=caps.get((k,i),'') or c.get('caption',''); text=html.escape(n)+f' · {i} / {N+len(t["clips"])}'+(' — '+html.escape(cap) if cap else '')+' · video'
        slides+=f'      <figure class="slide" id="{k}-{i}"><a class="nav prev" href="#{k}-{prev}" aria-label="previous">‹</a><video controls preload="none" playsinline poster="img/{k}/{c["name"]}.jpg"><source src="{MEDIA}/travels/{k}/{c["name"]}.mp4" type="video/mp4"></video><a class="nav next" href="#{k}-{nxt}" aria-label="next">›</a><figcaption>{text}</figcaption></figure>\n'
    ov+=f'  <section class="gallery" id="{k}">\n    <a class="close" href="#travels" aria-label="close">×</a>\n    <div class="strip">\n{slides}    </div>\n  </section>\n'
p=os.path.join(HERE,'index.html'); s=open(p,encoding='utf-8').read()
main=f'<main id="travels">\n\n  <h1>Travels</h1>\n  <p class="sub">Assorted adventures &amp; swashbucklings.</p>\n\n  <div class="trips">\n{cards}  </div>\n\n{ov}</main>'
s=re.sub(r'<main id="travels">.*?</main>',main,s,count=1,flags=re.S); open(p,'w',encoding='utf-8').write(s)
print(f"travels/index.html rebuilt: {len(P['trips'])} trips, {sum(t['count'] for t in P['trips'])} photos, {len(caps)} captions")
