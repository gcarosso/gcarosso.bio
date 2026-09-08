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
    m=re.match(r'([a-z0-9-]+)\s+([A-Za-z0-9-]+):\s*(.*)$',line)
    if m and m.group(3).strip():
        ref=m.group(2); caps[(m.group(1),int(ref) if ref.isdigit() else ref)]=m.group(3).strip()
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
            cap=caps.get((k,ref)) or clipmap[ref].get('caption',''); text=html.escape(n)+f' · {pos} / {T}'+(' — '+html.escape(cap) if cap else '')+' · video'
            media=f'<video controls preload="none" playsinline poster="img/{k}/{ref}.jpg"><source src="{MEDIA}/travels/{k}/{ref}.mp4" type="video/mp4"></video><button class="play" type="button" aria-label="Play"></button>'
        slides+=f'      <figure class="slide{" video" if kind=="v" else ""}" id="{k}-{pos}"><a class="nav prev" href="#{k}-{prev}" aria-label="previous">‹</a>{media}<a class="nav next" href="#{k}-{nxt}" aria-label="next">›</a><figcaption>{text}</figcaption></figure>\n'
    ov+=f'  <section class="gallery" id="{k}">\n    <a class="close" href="#travels" aria-label="close">×</a>\n    <div class="strip">\n{slides}    </div>\n  </section>\n'
# ---- contact sheet for ordering: travels/contact.html (noindex; every item with its key, in current order) ----
sheet=''
for t in P['trips']:
    k=t['key']; n=t['name']; N=t['count']; o=order.get(k,{}); clipmap={c['name']:c for c in t.get('clips',[])}
    if 'order' in o: items=[('p',int(x)) if x.isdigit() else ('v',x) for x in o['order'] if x.isdigit() or x in clipmap]
    else: items=[('p',i) for i in range(1,N+1)]+[('v',c) for c in clipmap]
    cv=o.get('cover',['1'])[0]; shown={r for _,r in items}
    hidden=[('p',i) for i in range(1,N+1) if i not in shown and os.path.exists(os.path.join(HERE,'img',k,f'{i:02d}.jpg'))]+[('v',c) for c in clipmap if c not in shown]
    def cell(kind,ref,pos=None,dim=False):
        src=f'img/{k}/{ref:02d}.jpg' if kind=='p' else f'img/{k}/{ref}.jpg'
        key=str(ref); cap=caps.get((k,ref),'') or (clipmap[ref].get('caption','') if kind=='v' else '')
        tag=('<b>cover</b> ' if key==cv else '')+(f'<span class="pos">{pos}</span> ' if pos else '')+html.escape(key)+(' &#9654;' if kind=='v' else '')
        return f'<figure{" class=dim" if dim else ""}><img src="{src}" loading="lazy"><figcaption>{tag}'+(f'<i>{html.escape(cap)}</i>' if cap else '')+'</figcaption></figure>'
    cells=''.join(cell(kd,r,i) for i,(kd,r) in enumerate(items,1))
    hid=''.join(cell(kd,r,dim=True) for kd,r in hidden)
    sheet+=f'<section><h2>{html.escape(n)} <code>[{k}]</code> <span class="cnt">{len(items)} shown'+(f', {len(hidden)} hidden' if hidden else '')+'</span></h2>\n<pre>cover: '+html.escape(cv)+'\norder: '+html.escape(' '.join(str(r) for _,r in items))+f'</pre>\n<div class="grid">{cells}</div>\n'+(f'<div class="grid hidden"><span class="lbl">not in order.txt</span>{hid}</div>\n' if hidden else '')+'</section>\n'
SHEET_HEAD='<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex">\n<title>Travels contact sheet</title>\n<style>\n' \
 'body{background:#000;color:#ddd;font:14px/1.4 "Helvetica Neue",Helvetica,Arial,sans-serif;margin:0;padding:24px}\n' \
 'h1{font-size:20px;margin:0 0 4px}p.hint{color:#888;margin:0 0 28px}\n' \
 'h2{font-size:16px;margin:32px 0 6px;color:#fff}h2 code{color:#FF6A1A;font-weight:400;font-size:13px}h2 .cnt{color:#888;font-weight:400;font-size:13px;margin-left:8px}\n' \
 'pre{margin:0 0 10px;padding:8px 10px;background:#111;border:1px solid #222;color:#bbb;font-size:12px;white-space:pre-wrap;word-break:break-all;user-select:all}\n' \
 '.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px}\n' \
 '.grid.hidden{margin-top:10px;padding-top:10px;border-top:1px dashed #333}.grid .lbl{grid-column:1/-1;color:#777;font-size:12px}\n' \
 'figure{margin:0}figure img{width:100%;aspect-ratio:4/3;object-fit:cover;display:block;background:#111;border-radius:3px}\n' \
 'figure.dim img{opacity:.35}\n' \
 'figcaption{font-size:12px;color:#aaa;margin-top:4px;word-break:break-all}figcaption .pos{display:inline-block;min-width:18px;padding:0 4px;border-radius:3px;background:#FF6A1A;color:#000;font-weight:700;text-align:center}\n' \
 'figcaption b{color:#fff}figcaption i{display:block;color:#777;font-style:normal}\n' \
 '</style></head><body>\n<h1>Travels contact sheet</h1>\n' \
 '<p class="hint">Every item in its current order, with the key to use in order.txt (photo number, or clip name marked &#9654;). Orange badge = position. Dimmed = in the album but not shown. Edit travels/order.txt and captions.txt, then run python3 travels/build.py.</p>\n'
open(os.path.join(HERE,'contact.html'),'w',encoding='utf-8').write(SHEET_HEAD+sheet+'</body></html>\n')

# ---- keep captions.txt in step with the site: one line per shown item, in display order, existing text preserved ----
cap_lines=['# Travels captions — one line per photo or video: "trip number: caption" or "trip clipname: caption". Leave a line blank for no caption.',
 '# Photo numbers are file names (img/<trip>/03.jpg is 3) and stay fixed when you reorder; clip names are the ones used in order.txt.',
 '# Lines follow the display order and are regenerated by build.py (your text is kept). After editing, run:  python3 travels/build.py   then commit and push.','']
for t in P['trips']:
    k=t['key']; o=order.get(k,{}); clipmap={c['name']:c for c in t.get('clips',[])}
    if 'order' in o: items=[('p',int(x)) if x.isdigit() else ('v',x) for x in o['order'] if x.isdigit() or x in clipmap]
    else: items=[('p',i) for i in range(1,t['count']+1)]+[('v',c) for c in clipmap]
    cap_lines.append('## '+t['name'])
    for kind,ref in items: cap_lines.append(f'{k} {ref}: '+caps.get((k,ref),''))
    cap_lines.append('')
open(os.path.join(HERE,'captions.txt'),'w',encoding='utf-8').write('\n'.join(cap_lines).rstrip(' \n')+'\n')
print("travels/captions.txt rewritten")

print("travels/contact.html rebuilt")

p=os.path.join(HERE,'index.html'); s=open(p,encoding='utf-8').read()
SCRIPT='''  <script>
  // The site's one script, confined to this page: whichever video slide is on screen plays (muted, as browsers
  // require) and the rest pause; the play mark is a real button; a card's cover clip plays on hover.
  (function(){
    var vids=[].slice.call(document.querySelectorAll('.slide video'));
    function stop(v){ v.pause(); v.closest('.slide').classList.remove('playing'); }
    function start(v){ v.muted=true; v.setAttribute('data-autoplay','1'); var p=v.play(); if(p&&p.catch) p.catch(function(){}); }
    function galleryOpen(el){ var g=el.closest('.gallery'); return g && getComputedStyle(g).display!=='none'; }
    var io=new IntersectionObserver(function(entries){
      entries.forEach(function(e){ var v=e.target.querySelector('video'); if(!v) return;
        if(e.isIntersecting && e.intersectionRatio>=0.6 && galleryOpen(e.target)) start(v); else stop(v); });
    },{threshold:[0,0.6]});
    vids.forEach(function(v){ io.observe(v.closest('.slide'));
      v.addEventListener('play',function(){ v.closest('.slide').classList.add('playing'); });
      v.addEventListener('pause',function(){ v.closest('.slide').classList.remove('playing'); });
      v.addEventListener('ended',function(){ v.closest('.slide').classList.remove('playing'); }); });
    document.querySelectorAll('.slide .play').forEach(function(btn){ btn.addEventListener('click',function(){ var v=btn.parentNode.querySelector('video'); v.muted=false; v.play(); }); });
    function resync(){ vids.forEach(function(v){ var s=v.closest('.slide'); if(!galleryOpen(s)) stop(v); }); io.disconnect(); vids.forEach(function(v){ io.observe(v.closest('.slide')); }); }
    window.addEventListener('hashchange',function(){ setTimeout(resync,50); });
    document.addEventListener('visibilitychange',function(){ if(!document.hidden) resync(); });
    var noHover=window.matchMedia('(hover: none)').matches;
    document.querySelectorAll('.trip video.hover').forEach(function(v){
      var a=v.closest('.trip'); v.muted=true;
      if(noHover){
        // phones and tablets: no hover, so the cover clip plays by itself while the card is on screen
        new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting&&e.intersectionRatio>=0.5){ var p=v.play(); if(p&&p.catch) p.catch(function(){}); } else { v.pause(); } }); },{threshold:[0,0.5]}).observe(a);
      } else {
        a.addEventListener('mouseenter',function(){ var p=v.play(); if(p&&p.catch) p.catch(function(){}); });
        a.addEventListener('mouseleave',function(){ v.pause(); v.currentTime=0; });
      }
    });
  })();
  </script>
'''
main=f'<main id="travels">\n\n  <h1>Travels</h1>\n  <p class="sub">Assorted swashbucklings.</p>\n\n  <div class="trips">\n{cards}  </div>\n\n{ov}'+SCRIPT+'</main>'
s=re.sub(r'<main id="travels">.*?</main>',main,s,count=1,flags=re.S); open(p,'w',encoding='utf-8').write(s)
print(f"travels/index.html rebuilt: {len(P['trips'])} trips, {sum(t['count'] for t in P['trips'])} photos, {len(caps)} captions")
