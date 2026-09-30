import json, os
R=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
T=open(os.path.join(R,'blog/pilates-apparatus-stroje/index.html'),encoding='utf-8').read()
def cut(a,z,incl=True):
    i=T.index(a); j=T.index(z,i)+(len(z) if incl else 0)
    return T[i:j]
URL="https://fitpilates.cz/blog/jak-cistit-podlozku-a-reformer/"
TITLE="Jak vyčistit podložku na jógu a reformer po cvičení"
DESC="Jak vyčistit podložku na jógu a pilates a jak čistit reformer: postup krok za krokem, citlivé materiály a rozdíl mezi čištěním a dezinfekcí. Od lektora z praxe."
OG="https://fitpilates.cz/images/gallery/gallery-24-allegro-detail-full.jpg"
D="2026-09-30T18:00:00+02:00"
faq=[]
import re,html
body=open(os.path.join(R,'scripts/_cleanee/body.html'),encoding='utf-8').read()
for q,a in re.findall(r'<summary>(.*?)</summary>\s*<p>(.*?)</p>',body,re.S):
    faq.append({"@type":"Question","name":html.unescape(q),"acceptedAnswer":{"@type":"Answer","text":html.unescape(re.sub('<.*?>','',a))}})
text=re.sub(r'<script.*?</script>|<[^>]+>',' ',body); wc=len(text.split())
bp={"@context":"https://schema.org","@type":"BlogPosting","headline":"Jak vyčistit podložku a reformer po cvičení","description":DESC,
 "image":[OG,"https://fitpilates.cz/images/gallery/gallery-21-stefan-feet-full.jpg"],"datePublished":D,"dateModified":D,
 "author":{"@type":"Person","name":"Štefan Bitto","jobTitle":"Lektor pilates a osobní trenér","url":"https://fitpilates.cz/o-stefanovi/",
   "sameAs":["https://fitpilates.cz/o-stefanovi/","https://www.instagram.com/stefanbitto","https://www.facebook.com/share/1Hs5UmhdH9/"]},
 "publisher":{"@type":"Organization","name":"Fit Pilates","url":"https://fitpilates.cz/","logo":{"@type":"ImageObject","url":"https://fitpilates.cz/images/logo-dark.png"}},
 "mainEntityOfPage":{"@type":"WebPage","@id":URL},"inLanguage":"cs-CZ","wordCount":wc,"articleSection":"Pilates",
 "about":[{"@type":"Thing","name":"Čištění podložky na jógu a pilates"},{"@type":"Thing","name":"Údržba pilates reformeru"}]}
bc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
 {"@type":"ListItem","position":1,"name":"Domů","item":"https://fitpilates.cz/"},
 {"@type":"ListItem","position":2,"name":"Blog","item":"https://fitpilates.cz/blog/"},
 {"@type":"ListItem","position":3,"name":"Jak vyčistit podložku a reformer","item":URL}]}
fq={"@context":"https://schema.org","@type":"FAQPage","mainEntity":faq}
def ld(o,label): return f'  <!-- Schema.org: {label} -->\n  <script type="application/ld+json">\n{json.dumps(o,ensure_ascii=False,indent=2)}\n  </script>\n'
css="""  <style>
    .toc { background: var(--cream); border-left: 3px solid var(--gold); padding: 24px 28px; margin: 0 0 40px; border-radius: 0 8px 8px 0; }
    .toc-title { font-family: 'Cormorant Garamond', serif; font-size: 1.1rem; font-weight: 600; color: var(--black); margin-bottom: 12px; text-transform: uppercase; letter-spacing: .08em; }
    .toc ul { list-style: none; margin: 0; padding: 0; }
    .toc li { padding: 6px 0; font-size: .95rem; }
    .toc li::before { content: '→'; color: var(--gold); margin-right: 10px; }
    .toc a { color: var(--charcoal); text-decoration: none; transition: color .2s; }
    .toc a:hover { color: var(--gold); }
    .author-box { background: var(--charcoal); color: var(--white); padding: 32px; border-radius: 12px; margin: 40px 0; display: grid; grid-template-columns: 120px 1fr; gap: 24px; align-items: center; }
    .author-box img { width: 120px; height: 120px; border-radius: 50%; object-fit: cover; }
    .author-box h4 { font-family: 'Cormorant Garamond', serif; font-size: 1.4rem; color: var(--white); margin-bottom: 4px; }
    .author-box .author-role { color: var(--gold); font-size: .9rem; margin-bottom: 8px; }
    .author-box p { color: rgba(255,255,255,.75); font-size: .92rem; line-height: 1.55; margin: 0; }
    .author-box a { color: var(--gold); border-bottom: none !important; }
    .quote-block { font-family: 'Cormorant Garamond', serif; font-size: 1.4rem; font-style: italic; color: var(--charcoal); border-left: 3px solid var(--gold); padding: 16px 0 16px 24px; margin: 32px 0; line-height: 1.5; }
    .quote-block cite { display: block; font-size: .9rem; font-style: normal; color: var(--grey); margin-top: 8px; font-family: 'Inter', sans-serif; }
    .progression { display: flex; flex-direction: column; gap: 16px; margin: 32px 0; counter-reset: prog-step; }
    .prog-step { background: var(--white); border: 1px solid var(--border); border-radius: 10px; padding: 20px 24px; position: relative; padding-left: 64px; }
    .prog-step::before { counter-increment: prog-step; content: counter(prog-step); position: absolute; left: 16px; top: 18px; width: 36px; height: 36px; background: var(--gold); color: var(--white); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-family: 'Cormorant Garamond', serif; font-size: 1.1rem; }
    .prog-step h4 { font-family: 'Cormorant Garamond', serif; font-size: 1.2rem; color: var(--black); margin-bottom: 4px; }
    .prog-step p { font-size: .92rem; line-height: 1.6; margin: 0; color: var(--charcoal); }
    .coop-note { font-size: .88rem; color: var(--grey); border: 1px solid var(--border); border-radius: 999px; display: inline-block; padding: 6px 16px; margin-bottom: 24px !important; }
    .coop-box { background: var(--cream); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; margin: 36px 0; position: relative; }
    .coop-box img { width: 100%; height: auto; display: block; }
    .coop-body { padding: 24px 28px 8px; }
    .coop-body p { font-size: .98rem; }
    .coop-box .quote-block { font-size: 1.2rem; margin: 20px 0; }
    .coop-label { position: absolute; top: 12px; left: 12px; z-index: 2; background: var(--charcoal); color: var(--white); font-size: 11px; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; padding: 5px 12px; border-radius: 999px; }
    .coop-box--text .coop-label { position: static; display: inline-block; margin: 20px 0 0 28px; }
    .biocid-note { font-size: .88rem !important; color: var(--charcoal); background: var(--white); border-left: 3px solid var(--charcoal); padding: 10px 14px; border-radius: 0 6px 6px 0; }
    @media (max-width: 768px) {
      .author-box { grid-template-columns: 1fr; text-align: center; }
      .author-box img { margin: 0 auto; width: 96px; height: 96px; }
      .coop-body { padding: 20px 20px 4px; }
      .coop-box--text .coop-label { margin-left: 20px; }
    }
  </style>
"""
head=f"""<!DOCTYPE html>
<html lang="cs">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <title>{TITLE}</title>
  <meta name="description" content="{DESC}">
  <meta name="author" content="Štefan Bitto">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta name="theme-color" content="#1a1b1e">

  <!-- Canonical -->
  <link rel="canonical" href="{URL}">

  <!-- Favicon -->
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
  <link rel="manifest" href="/manifest.json">

  <!-- Open Graph -->
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Fit Pilates">
  <meta property="og:locale" content="cs_CZ">
  <meta property="og:url" content="{URL}">
  <meta property="og:title" content="Jak vyčistit podložku a reformer po cvičení">
  <meta property="og:description" content="Postup krok za krokem pro podložku na jógu i pilates a pro reformer – z praxe privátního studia v Praze 10.">
  <meta property="og:image" content="{OG}">
  <meta property="og:image:alt" content="Reformery Balanced Body Allegro ve Fit Pilates Praha 10">
  <meta property="og:image:width" content="1600">
  <meta property="og:image:height" content="907">
  <meta property="article:published_time" content="{D}">
  <meta property="article:modified_time" content="{D}">
  <meta property="article:author" content="Štefan Bitto">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Jak vyčistit podložku a reformer po cvičení">
  <meta name="twitter:description" content="Postup krok za krokem pro podložku na jógu i pilates a pro reformer – z praxe privátního studia v Praze 10.">
  <meta name="twitter:image" content="{OG}">

  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400;1,600&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">

"""
crit=cut('<style id="critical-css">','</style>')
ana=cut('<!-- Microsoft Clarity -->','</head>',False)
nav=cut('<!-- NAV-START -->','<!-- NAV-END -->')
foot=cut('<!-- FOOTER-START -->','</html>')
out=head+ld(bp,"BlogPosting")+"\n"+ld(bc,"BreadcrumbList")+"\n"+ld(fq,"FAQPage")+"\n"+crit+'\n  <link rel="stylesheet" href="/assets/css/site.css?v=08092026-mahagon">\n\n'+css+ana+"</head>\n<body>\n\n"+nav+"\n\n\n"+body+"\n\n<!-- FOOTER -->\n"+foot+"\n"
import os
os.makedirs(os.path.join(R,'blog/jak-cistit-podlozku-a-reformer'),exist_ok=True)
open(os.path.join(R,'blog/jak-cistit-podlozku-a-reformer/index.html'),'w',encoding='utf-8').write(out)
print(len(DESC),len(TITLE),wc,len(faq),len(out))
