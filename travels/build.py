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
    cv=o.get('cover',['1'])[0]; cover_src=f'img/{k}/{int(cv):02d}.jpg' if cv.isdigit() else f'img/{k}/{cv}.jpg'
    if 'order' in o: items=[('p',int(x)) if x.isdigit() else ('v',x) for x in o['order'] if x.isdigit() or x in clipmap]
    else: items=[('p',i) for i in photo_ids]+[('v',c) for c in clip_names]
    photo_ids=[r for kind,r in items if kind=='p']; clip_names=[r for kind,r in items if kind=='v']; T=len(items)
    nc=len(clip_names); hv=t.get('hover_clip')
    cover_el=(f'<video class="hover" muted loop playsinline preload="none" poster="{cover_src}"><source src="{MEDIA}/travels/{k}/{hv}.mp4" type="video/mp4"></video>' if hv else f'<img src="{cover_src}" alt="" loading="lazy">')
    cards+=f'    <a class="trip" href="#{k}">{cover_el}<span class="tn">{html.escape(n)}</span><span class="tc">'+' · '.join(x for x in [(f'{len(photo_ids)} photo'+('s' if len(photo_ids)!=1 else '') if photo_ids else ''),(f'{nc} video'+('s' if nc>1 else '') if nc else '')] if x)+'</span></a>\n'
    slides=''
    for pos,(kind,ref) in enumerate(items,1):
        prev=pos-1 if pos>1 else T; nxt=pos+1 if pos<T else 1
        if kind=='p':
            cap=caps.get((k,ref),''); text=html.escape(n)+f' · {pos} / {T}'+(' — '+html.escape(cap) if cap else '')
            media=f'<img src="img/{k}/{ref:02d}.jpg" alt="{html.escape(cap)}" loading="lazy">'
        else:
            cap=clipmap[ref].get('caption',''); text=html.escape(n)+f' · {pos} / {T}'+(' — '+html.escape(cap) if cap else '')+' · video'
            media=f'<video controls preload="none" playsinline poster="img/{k}/{ref}.jpg"><source src="{MEDIA}/travels/{k}/{ref}.mp4" type="video/mp4"></video>'
        slides+=f'      <figure class="slide{" video" if kind=="v" else ""}" id="{k}-{pos}"><a class="nav prev" href="#{k}-{prev}" aria-label="previous">‹</a>{media}<a class="nav next" href="#{k}-{nxt}" aria-label="next">›</a><figcaption>{text}</figcaption></figure>\n'
    ov+=f'  <section class="gallery" id="{k}">\n    <a class="close" href="#travels" aria-label="close">×</a>\n    <div class="strip">\n{slides}    </div>\n  </section>\n'
p=os.path.join(HERE,'index.html'); s=open(p,encoding='utf-8').read()
SCRIPT='''  <script>
  // The site's one script, confined to this page: play the open slide's clip (muted, as browsers require),
  // pause the others, and let a card's cover clip play on hover.
  (function(){
    var vids=document.querySelectorAll('.slide video');
    function sync(){
      var open=document.querySelector('.slide:target');
      vids.forEach(function(v){
        var fig=v.closest('.slide');
        if(fig===open){ v.muted=true; v.play().then(function(){fig.classList.add('playing');}).catch(function(){}); }
        else { v.pause(); fig.classList.remove('playing'); }
      });
    }
    vids.forEach(function(v){ v.addEventListener('pause',function(){v.closest('.slide').classList.remove('playing');}); v.addEventListener('play',function(){v.closest('.slide').classList.add('playing');}); });
    window.addEventListener('hashchange',sync); sync();
    document.querySelectorAll('.trip video.hover').forEach(function(v){
      var a=v.closest('.trip');
      a.addEventListener('mouseenter',function(){ v.play().catch(function(){}); });
      a.addEventListener('mouseleave',function(){ v.pause(); v.currentTime=0; });
    });
  })();
  </script>
'''
main=f'<main id="travels">\n\n  <h1>Travels</h1>\n  <p class="sub">Assorted swashbucklings.</p>\n\n  <div class="trips">\n{cards}  </div>\n\n{ov}'+SCRIPT+'</main>'
s=re.sub(r'<main id="travels">.*?</main>',main,s,count=1,flags=re.S); open(p,'w',encoding='utf-8').write(s)
print(f"travels/index.html rebuilt: {len(P['trips'])} trips, {sum(t['count'] for t in P['trips'])} photos, {len(caps)} captions")
