"""Genera collezione.html: tutte le carte, gli dei, i dorsi e i pacchetti di Zodiax Arena.
Lancio: python tools/build_collezione.py  (dalla radice del repo)"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PL = ["Sole", "Luna", "Marte", "Giove", "Saturno", "Mercurio", "Venere"]
SG = ["Ariete", "Toro", "Gemelli", "Cancro", "Leone", "Vergine", "Bilancia", "Scorpione",
      "Sagittario", "Capricorno", "Acquario", "Pesci"]
GLYPH = dict(zip(SG, "♈♉♊♋♌♍♎♏♐♑♒♓"))
ELEM = {"Fuoco": ["Ariete", "Leone", "Sagittario"], "Terra": ["Toro", "Vergine", "Capricorno"],
        "Aria": ["Gemelli", "Bilancia", "Acquario"], "Acqua": ["Cancro", "Scorpione", "Pesci"]}
EL_OF = {s: e for e, ss in ELEM.items() for s in ss}

def card_src(p, s):
    n = PL.index(p) * 12 + SG.index(s) + 1
    return f"img/za-{n:03d}-{p.lower()}-{s.lower()}.webp"

def asc_src(s):
    return f"img/za-asc-{SG.index(s) + 1:02d}-ascendente-{s.lower()}.webp"

def zoom_src(src):
    # anteprima ad alta risoluzione: carte e dorsi in img/hd (1000x1400); i pacchetti restano come sono
    if "/pacchetti/" in src: return src
    return "img/hd/" + src.split("/")[-1]

def tilt_img(src, alt, cls="", extra=""):
    return (f'<button class="tilt {cls}" type="button" data-zoom="{zoom_src(src)}" aria-label="Ingrandisci {alt}"{extra}>'
            f'<span class="tilt-in"><img src="{src}" alt="{alt}" loading="lazy" decoding="async"></span></button>')

def grid(items):
    return '<ul class="grid">' + "".join(
        f'<li>{tilt_img(src, alt)}<span class="cap">{cap}</span></li>' for src, alt, cap in items) + "</ul>"

# ---------- schede per rarita ----------
RAR = [
    ("asc", "Ascendenti", "Ultra-rare", "ultra", [("Ascendenti", [(asc_src(s), f"Ascendente {s}", f"{GLYPH[s]}︎ {s}") for s in SG])],
     "Non combattono: danno +1 ATK alle carte del loro segno nel mazzo."),
    ("leg", "Leggendarie", "Leggendarie", "leg", [("Sole", [(card_src("Sole", s), f"Sole in {s}", f"{GLYPH[s]}︎ {s}") for s in SG])],
     "Il Sole è la carta più forte del mazzo: alla registrazione ricevi quello del tuo segno."),
    ("epi", "Epiche", "Epiche", "epi", [(p, [(card_src(p, s), f"{p} in {s}", f"{GLYPH[s]}︎ {s}") for s in SG]) for p in ("Marte", "Luna")],
     "Marte attacca, la Luna difende."),
    ("rar", "Rare", "Rare", "rar", [(p, [(card_src(p, s), f"{p} in {s}", f"{GLYPH[s]}︎ {s}") for s in SG]) for p in ("Giove", "Saturno")],
     "Giove spinge l'attacco, Saturno regge i colpi."),
    ("com", "Comuni", "Comuni", "com", [(p, [(card_src(p, s), f"{p} in {s}", f"{GLYPH[s]}︎ {s}") for s in SG]) for p in ("Mercurio", "Venere")],
     "Le più facili da trovare: il segno conta più del pianeta."),
]
n_tot = sum(len(g[1]) for r in RAR for g in r[4])

tabs = "".join(
    f'<button role="tab" id="tab-{k}" aria-controls="pan-{k}" aria-selected="{str(i == 0).lower()}" tabindex="{0 if i == 0 else -1}" class="r-{c}">'
    f'{label}<span class="n">{sum(len(g[1]) for g in groups)}</span></button>'
    for i, (k, label, _, c, groups, _) in enumerate(RAR))
panels = "".join(
    f'<div role="tabpanel" id="pan-{k}" aria-labelledby="tab-{k}" class="panel r-{c}"{"" if i == 0 else " hidden"}>'
    f'<p class="lead">{note}</p>'
    + "".join(f'<h3 class="sub"><span>{name}</span><em>{rname}</em></h3>' + grid(items) for name, items in groups)
    + "</div>"
    for i, (k, label, rname, c, groups, note) in enumerate(RAR))

# ---------- dei ----------
GODS = [("Efesto", "Fuoco", "+2 ATK alle tue creature di Fuoco"), ("Poseidone", "Acqua", "+3 DEF alle tue creature d'Acqua"),
        ("Demetra", "Terra", "+1 ATK e +1 DEF alle tue creature di Terra"), ("Era", "Aria", "+1 ATK e +1 DEF alle tue creature d'Aria")]
gods = '<ul class="gods">' + "".join(
    f'<li class="el-{e.lower()}">{tilt_img(f"img/za-dio-{g.lower()}.webp", f"Carta di {g}")}'
    f'<span class="gname"><img src="img/elementi/{e.lower()}.webp" alt="" width="28" height="28">{g}</span><span class="gtxt">{t}</span></li>'
    for g, e, t in GODS) + "</ul>"

# ---------- dorsi ----------
backs = "".join(
    f'<div class="belem el-{e.lower()}"><h3 class="sub"><span><img src="img/elementi/{e.lower()}.webp" alt="" width="30" height="30">{e}</span></h3>'
    + '<ul class="backs">' + "".join(
        f'<li>{tilt_img(f"img/dorsi/dorso-{s.lower()}.webp", f"Dorso {s}")}<span class="cap">{GLYPH[s]}︎ {s}</span></li>' for s in ss)
    + "</ul></div>"
    for e, ss in ELEM.items())

# ---------- pacchetti ----------
PACKS = [("costellazione", "Costellazione", 5, 100, [("3", "C"), ("1", "R"), ("1", "S")], "Carte della Casa I. Il pacchetto di tutti i giorni."),
         ("zenit", "Zenit", 10, 300, [("3", "C"), ("3", "R"), ("4", "S")], "Carte della Casa I, con più Stelle: aperture più ricche."),
         ("nuova-casa", "Nuova Casa", 8, 200, [("4", "C"), ("2", "R"), ("2", "S")], "Carte dell'ultima Casa uscita."),
         ("archivio-celeste", "Archivio Celeste", 20, 400, [("12", "C"), ("4", "R"), ("4", "S")], "Carte di una Casa precedente, a tua scelta."),
         ("luna-piena", "Luna Piena", 12, 600, [("6", "C"), ("3", "R"), ("1", "E"), ("1", "S"), ("1", "A")], "Con un Ascendente garantito.")]
packs = '<ul class="packs">' + "".join(
    f'<li>{tilt_img(f"img/pacchetti/{k}.webp", f"Pacchetto {n}", "pack")}'
    f'<h3>{n}</h3><p class="meta">{c} carte · {cr} crediti</p>'
    f'<p class="mix" aria-label="Contenuto">' + " ".join(f'<span class="s-{t.lower()}">{q}&nbsp;{t}</span>' for q, t in mix) + "</p>"
    f'<p class="desc">{d}</p></li>'
    for k, n, c, cr, mix, d in PACKS) + "</ul>"

HTML = f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Collezione · Zodiax Arena</title>
<meta name="description" content="Tutte le carte di Zodiax Arena: {n_tot} carte dello zodiaco, gli dèi, i dorsi personalizzati e i pacchetti.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;800;900&family=Cinzel+Decorative:wght@700;900&family=Nunito:wght@400;600;700;800&display=swap">
<style>
:root{{--bg:#10172B;--bg2:#0B0E35;--deep:#07060F;--gold:#E8B04B;--gold-l:#FFE7A0;--gold-s:#EBCF93;--ink:#2A1405;--text:#F3EBDD;--muted:#B9B6CF;
--com:#CFCFDA;--rar:#7FA8FF;--epi:#D9B8FF;--leg:#FFE38A;--ult:#7AF0FF;--fuoco:#F2604A;--acqua:#6E95F0;--terra:#B7C66A;--aria:#D9CBE0;color-scheme:dark}}
*{{box-sizing:border-box}}
html{{scroll-behavior:smooth;scroll-padding-top:84px}}
body{{margin:0;background:var(--bg);color:var(--text);font:16px/1.55 Nunito,system-ui,sans-serif;-webkit-font-smoothing:antialiased}}
img{{max-width:100%}}
a{{color:var(--gold-l)}}
h1,h2,h3{{font-family:Cinzel,serif;margin:0;line-height:1.1;text-wrap:balance}}
:focus-visible{{outline:2px solid var(--gold);outline-offset:3px}}
.wrap{{max-width:1180px;margin:0 auto;padding:0 32px}}

/* intestazione: come la landing */
header{{position:fixed;top:0;left:0;right:0;z-index:20;display:flex;align-items:center;justify-content:space-between;gap:12px;padding:8px 32px;
background:linear-gradient(180deg,rgba(18,24,48,.88),rgba(10,15,34,.84));-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);border-bottom:2px solid var(--gold);box-shadow:0 -6px 0 -5px rgba(217,185,124,.45) inset}}
.brand{{display:flex;align-items:center;gap:14px}}
.brand>a:first-child{{flex:none}}
.brand>a:first-child img{{height:52px;width:auto;display:block}}
.ghost{{display:inline-flex;align-items:center;min-height:44px;padding:0 18px;border:1.5px solid rgba(235,207,147,.55);border-radius:6px;font:700 14px Cinzel,serif;letter-spacing:.14em;text-transform:uppercase;text-decoration:none;color:var(--gold-s);white-space:nowrap;transition:background .2s}}
.ghost:hover{{background:rgba(235,207,147,.14)}}
.ghost[aria-current=page]{{background:rgba(235,207,147,.16);border-color:var(--gold);color:var(--gold-l)}}
.ghost.cta{{border-color:var(--gold-s);color:var(--gold-l)}}

/* hero */
.hero{{position:relative;padding:112px 0 40px;overflow:hidden;background:radial-gradient(ellipse 70% 60% at 50% 62%,rgba(255,214,107,.16),rgba(255,214,107,0) 70%),linear-gradient(180deg,#0A0F22 0%,var(--bg) 100%)}}
.hero::before{{content:"";position:absolute;inset:0;background-image:radial-gradient(1.2px 1.2px at 12% 22%,#F3EBDD 50%,transparent),radial-gradient(1px 1px at 28% 12%,#FFE7A0 50%,transparent),radial-gradient(1.4px 1.4px at 71% 18%,#F3EBDD 50%,transparent),radial-gradient(1px 1px at 86% 30%,#FFE7A0 50%,transparent),radial-gradient(1.2px 1.2px at 52% 8%,#F3EBDD 50%,transparent),radial-gradient(1px 1px at 92% 64%,#F3EBDD 50%,transparent),radial-gradient(1px 1px at 6% 70%,#FFE7A0 50%,transparent);opacity:.7}}
.hero h1{{position:relative;z-index:3;text-align:center;font-family:'Cinzel Decorative',Cinzel,serif;font-weight:900;font-size:clamp(34px,5.4vw,68px);color:#FFF8EC;text-shadow:0 3px 0 #05070F,0 0 30px rgba(6,9,22,.9);padding:0 16px}}
.hero .kick{{position:relative;z-index:3;text-align:center;margin:14px 0 0;font:600 clamp(15px,1.6vw,19px) Cinzel,serif;letter-spacing:.06em;color:var(--gold-l)}}
.stage{{position:relative;height:540px;max-width:1180px;margin:8px auto 0}}
.god{{position:absolute;bottom:0;z-index:1;pointer-events:none;filter:drop-shadow(0 18px 28px rgba(0,0,0,.6))}}
.god img{{display:block;height:100%;width:auto}}
.god.g1{{left:2%;height:500px}} .god.g2{{left:19%;height:430px;bottom:34px;z-index:0;opacity:.92}}
.god.g3{{right:19%;height:430px;bottom:34px;z-index:0;opacity:.92}} .god.g4{{right:2%;height:500px}}
.god.g2 img,.god.g3 img{{filter:brightness(.82)}}
.trio{{position:absolute;left:50%;bottom:24px;z-index:3;width:0;height:0}}
.trio .tilt{{position:absolute;bottom:0}}
.trio .t1{{width:180px;left:-250px;transform:rotate(-9deg);transform-origin:50% 100%}}
.trio .t2{{width:212px;left:-106px;bottom:22px}}
.trio .t3{{width:180px;left:70px;transform:rotate(9deg);transform-origin:50% 100%}}
.float{{animation:float 7s ease-in-out infinite}}
@keyframes float{{0%,100%{{translate:0 0}}50%{{translate:0 -10px}}}}
.hero .cue{{position:relative;z-index:3;display:flex;justify-content:center;gap:10px;flex-wrap:wrap;margin:26px auto 0;padding:0 16px}}
.hero .cue a{{font:700 13px Nunito,sans-serif;letter-spacing:.12em;text-transform:uppercase;text-decoration:none;color:var(--gold-s);border:1px solid rgba(235,207,147,.35);border-radius:99px;padding:9px 14px;background:rgba(11,14,53,.6)}}
.hero .cue a:hover{{border-color:var(--gold);color:var(--gold-l)}}

/* sezioni */
section{{position:relative;padding:80px 0}}
.sec-head{{text-align:center;margin-bottom:32px}}
.sec-head .eyebrow{{display:block;font:800 12px Nunito,sans-serif;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-bottom:10px}}
.sec-head h2{{font-size:clamp(28px,3.4vw,44px);color:#FFF8EC}}
.sec-head p{{max-width:620px;margin:12px auto 0;color:var(--muted)}}
#carte{{background:linear-gradient(180deg,var(--bg) 0%,var(--bg2) 100%)}}
#dei{{background:var(--bg2)}}
#dorsi{{background:linear-gradient(180deg,var(--bg2) 0%,var(--bg) 100%)}}
#pacchetti{{background:var(--bg)}}

/* schede rarita */
.tabs{{position:sticky;top:70px;z-index:10;display:flex;gap:8px;justify-content:center;flex-wrap:wrap;padding:10px 0;margin-bottom:8px;background:linear-gradient(180deg,rgba(16,23,43,.96),rgba(16,23,43,.9));-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)}}
.tabs button{{--c:var(--gold-s);display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 16px;border-radius:99px;border:1.5px solid rgba(235,207,147,.3);background:rgba(11,14,53,.7);color:var(--text);font:700 14px Cinzel,serif;letter-spacing:.06em;cursor:pointer;transition:border-color .2s,background .2s}}
.tabs button .n{{font:800 12px Nunito,sans-serif;color:var(--c);border:1px solid currentColor;border-radius:99px;padding:1px 7px;letter-spacing:0}}
.tabs button[aria-selected=true]{{border-color:var(--c);background:rgba(42,49,88,.9);color:#FFF8EC;box-shadow:0 0 18px -6px var(--c)}}
.r-ultra{{--c:var(--ult)}} .r-leg{{--c:var(--leg)}} .r-epi{{--c:var(--epi)}} .r-rar{{--c:var(--rar)}} .r-com{{--c:var(--com)}}
.panel .lead{{text-align:center;color:var(--muted);margin:8px 0 26px}}
.sub{{display:flex;align-items:center;gap:14px;margin:36px 0 18px;font-size:20px;color:#FFF8EC}}
.sub::after{{content:"";flex:1;height:1px;background:linear-gradient(90deg,rgba(232,176,75,.5),rgba(232,176,75,0))}}
.sub span{{display:inline-flex;align-items:center;gap:10px}}
.sub em{{font:800 12px Nunito,sans-serif;font-style:normal;letter-spacing:.16em;text-transform:uppercase;color:var(--c,var(--gold))}}
.grid{{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:22px 18px}}
.grid li,.backs li{{display:flex;flex-direction:column;align-items:center;gap:8px}}
.cap{{font:700 13px Nunito,sans-serif;color:var(--muted);text-align:center}}

/* tilt 3D */
.tilt{{--rx:0deg;--ry:0deg;--gx:50%;--gy:50%;--ga:0;display:block;width:100%;padding:0;border:0;background:none;cursor:pointer;perspective:900px;touch-action:pan-y;-webkit-tap-highlight-color:transparent}}
.tilt-in{{position:relative;display:block;border-radius:5.4%/3.9%;transform:rotateX(var(--rx)) rotateY(var(--ry)) scale(var(--s,1));transform-style:preserve-3d;transition:transform .45s cubic-bezier(.2,.7,.2,1),box-shadow .45s;box-shadow:0 10px 24px rgba(0,0,0,.5)}}
.tilt-in img{{display:block;width:100%;height:auto;border-radius:inherit}}
.tilt-in::after{{content:"";position:absolute;inset:0;border-radius:inherit;pointer-events:none;opacity:var(--ga);transition:opacity .3s;mix-blend-mode:soft-light;
background:radial-gradient(circle at var(--gx) var(--gy),rgba(255,255,255,.75) 0%,rgba(255,255,255,.15) 30%,rgba(255,255,255,0) 60%)}}
.tilt.on .tilt-in{{--s:1.05;transition:transform .08s linear,box-shadow .3s;box-shadow:0 26px 44px rgba(0,0,0,.6),0 0 30px -8px rgba(255,214,107,.45)}}
.tilt.pack .tilt-in{{border-radius:2%;box-shadow:none;filter:drop-shadow(0 14px 22px rgba(0,0,0,.55))}}
.tilt.pack .tilt-in img{{border-radius:0}}
.tilt.pack.on .tilt-in{{box-shadow:none;filter:drop-shadow(0 26px 34px rgba(0,0,0,.6))}}
.tilt.pack .tilt-in::after{{border-radius:2%}}

/* dei */
.gods{{list-style:none;margin:0 auto;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:28px;max-width:1040px}}
.gods li{{display:flex;flex-direction:column;align-items:center;gap:6px;text-align:center}}
.gname{{display:inline-flex;align-items:center;gap:8px;margin-top:10px;font:800 20px Cinzel,serif;letter-spacing:.08em;color:#FFF8EC}}
.gtxt{{font-size:14px;color:var(--muted);max-width:220px}}
.el-fuoco .gname{{color:var(--fuoco)}} .el-acqua .gname{{color:var(--acqua)}} .el-terra .gname{{color:var(--terra)}} .el-aria .gname{{color:var(--aria)}}
.ade{{margin-top:72px;padding:56px 32px;border-radius:24px;background:radial-gradient(ellipse 60% 70% at 30% 50%,rgba(181,63,42,.22),rgba(181,63,42,0) 70%),var(--deep);border:1px solid rgba(232,176,75,.25);box-shadow:inset 0 0 80px rgba(0,0,0,.7)}}
.ade-in{{display:grid;grid-template-columns:260px 1fr;gap:48px;align-items:center;max-width:860px;margin:0 auto}}
.lock{{display:inline-flex;align-items:center;gap:8px;font:800 12px Nunito,sans-serif;letter-spacing:.18em;text-transform:uppercase;color:#FF9C86;border:1px solid rgba(255,156,134,.5);border-radius:99px;padding:6px 12px}}
.ade h3{{margin:16px 0 10px;font-size:clamp(28px,3vw,40px);color:#FFF8EC}}
.ade p{{margin:0 0 10px;color:var(--muted)}}

/* dorsi */
.std{{display:grid;grid-template-columns:320px 1fr;gap:48px;align-items:center;max-width:860px;margin:0 auto 24px}}
.std h3{{font-size:28px;color:#FFF8EC;margin-bottom:10px}} .std p{{margin:0 0 10px;color:var(--muted)}}
.belems{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px 40px}}
.backs{{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}}
.el-fuoco .sub span{{color:var(--fuoco)}} .el-terra .sub span{{color:var(--terra)}} .el-aria .sub span{{color:var(--aria)}} .el-acqua .sub span{{color:var(--acqua)}}

/* pacchetti */
.packs{{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:28px}}
.packs li{{display:flex;flex-direction:column;align-items:center;text-align:center;gap:4px}}
.packs h3{{margin-top:16px;font-size:20px;color:#FFF8EC}}
.packs .meta{{margin:0;font:700 14px Nunito,sans-serif;color:var(--gold-l)}}
.mix{{display:flex;flex-wrap:wrap;justify-content:center;gap:6px;margin:8px 0 4px}}
.mix span{{font:800 13px Nunito,sans-serif;padding:3px 9px;border-radius:99px;border:1px solid currentColor;background:rgba(11,14,53,.8)}}
.s-c{{color:var(--com)}} .s-r{{color:var(--rar)}} .s-e{{color:var(--epi)}} .s-s{{color:var(--leg)}} .s-a{{color:var(--ult)}}
.packs .desc{{margin:0;font-size:14px;color:var(--muted)}}
.legend{{display:flex;flex-wrap:wrap;justify-content:center;gap:8px 18px;margin:36px auto 0;font-size:14px;color:var(--muted);max-width:820px;text-align:center}}
.legend b{{font-weight:800}}

footer{{padding:36px 32px 48px;text-align:center;color:var(--muted);font-size:14px;border-top:1px solid rgba(232,176,75,.25)}}
footer nav{{display:flex;gap:20px;justify-content:center;margin-bottom:10px}}
footer a{{color:var(--gold-s);text-decoration:none;font:700 13px Cinzel,serif;letter-spacing:.12em;text-transform:uppercase}}

/* ingrandimento */
.lb{{position:fixed;inset:0;z-index:50;display:flex;align-items:center;justify-content:center;padding:24px;background:rgba(5,7,15,.92);animation:fade .2s both}}
.lb[hidden]{{display:none}}
.lb .tilt{{width:min(92vw,800px,calc((100vh - 120px) * .714));width:min(92vw,800px,calc((100dvh - 120px) * .714));touch-action:none;cursor:default}}
.lb .tilt.wide{{width:min(92vw,800px,calc((100vh - 120px) * .64));width:min(92vw,800px,calc((100dvh - 120px) * .64))}}
.flipper{{position:relative;display:block;transform-style:preserve-3d;transform:rotateY(var(--flip,0deg));transition:transform .65s cubic-bezier(.3,.7,.2,1)}}
.flipper .face{{display:block;backface-visibility:hidden;-webkit-backface-visibility:hidden;border-radius:inherit}}
.flipper .face img{{display:block;width:100%;height:auto;border-radius:inherit}}
.flipper .face.back{{position:absolute;inset:0;transform:rotateY(180deg)}}
.flipper .face.back img{{height:100%}}
.lb .tilt:not(.can-flip) .face.back{{display:none}}
.lb .tilt.can-flip{{cursor:grab}}
.lbhint{{position:absolute;left:0;right:0;bottom:calc(24px + env(safe-area-inset-bottom,0px));margin:0;text-align:center;font:700 13px Nunito,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--gold-s);pointer-events:none}}
.lbhint span{{display:inline-block;animation:nudge 1.8s ease-in-out infinite}}
@keyframes nudge{{0%,100%{{transform:translateX(0)}}50%{{transform:translateX(6px)}}}}
@media (prefers-reduced-motion:reduce){{.flipper{{transition:none}}.lbhint span{{animation:none}}}}
.lbx{{position:absolute;top:16px;right:16px;width:48px;height:48px;border-radius:50%;border:1.5px solid var(--gold);background:var(--bg2);color:var(--gold-l);font-size:22px;cursor:pointer}}
@keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}

@media (max-width:980px){{
.grid{{grid-template-columns:repeat(4,minmax(0,1fr))}}
.packs{{grid-template-columns:repeat(3,minmax(0,1fr))}}
.gods{{grid-template-columns:repeat(2,minmax(0,1fr));max-width:560px}}
.stage{{height:440px}} .god.g1,.god.g4{{height:400px}} .god.g2,.god.g3{{height:340px}}
.trio .t1{{width:140px;left:-196px}} .trio .t2{{width:166px;left:-83px}} .trio .t3{{width:140px;left:56px}}
}}
@media (max-width:700px){{
.wrap{{padding:0 16px}}
header{{padding:6px 12px}}
.brand{{gap:8px}} .brand>a:first-child img{{height:38px}}
.ghost{{min-height:40px;padding:0 10px;font-size:11px;letter-spacing:.06em}}
.hero{{padding-top:92px}}
.stage{{height:300px;margin-top:0}}
.god.g1{{left:-8%;height:270px}} .god.g4{{right:-8%;height:270px}}
.god.g2{{left:10%;height:220px;bottom:40px}} .god.g3{{right:10%;height:220px;bottom:40px}}
.trio{{bottom:16px}}
.trio .t1{{width:100px;left:-136px}} .trio .t2{{width:118px;left:-59px;bottom:14px}} .trio .t3{{width:100px;left:36px}}
section{{padding:56px 0}}
.tabs{{top:56px;justify-content:flex-start;flex-wrap:nowrap;overflow-x:auto;margin:0 -16px 8px;padding:10px 16px;scrollbar-width:none}}
.tabs button{{flex:none;font-size:13px;padding:0 12px}}
.grid{{grid-template-columns:repeat(3,minmax(0,1fr));gap:16px 10px}}
.cap{{font-size:12px}}
.gods{{gap:24px 14px}} .gname{{font-size:17px}} .gtxt{{font-size:13px}}
.ade{{margin-top:56px;padding:36px 20px}} .ade-in{{grid-template-columns:1fr;gap:24px;justify-items:center;text-align:center}} .ade-in .tilt{{max-width:230px}}
.std{{grid-template-columns:1fr;gap:20px;text-align:center;justify-items:center}} .std .tilt{{max-width:250px}}
.belems{{grid-template-columns:1fr}}
.backs{{gap:10px}}
.packs{{grid-template-columns:repeat(2,minmax(0,1fr));gap:28px 14px}}
.packs h3{{font-size:17px}}
}}
@media (max-width:380px){{.ghost.cta{{display:none}}}}
@media (prefers-reduced-motion:reduce){{.float{{animation:none}}.tilt-in{{transition:none}}html{{scroll-behavior:auto}}}}
</style>
</head>
<body>
<header>
<div class="brand">
<a href="index.html" aria-label="Zodiax Arena, torna alla home"><img src="img/za-logo-compatto.webp" alt="Zodiax Arena"></a>
<a class="ghost" href="regolamento.html">Regolamento</a>
<a class="ghost" href="collezione.html" aria-current="page">Collezione</a>
</div>
<a class="ghost cta" href="index.html#iscriviti">Iscriviti</a>
</header>

<main>
<section class="hero" aria-labelledby="titolo">
<h1 id="titolo">Tutte le carte dello zodiaco</h1>
<p class="kick">{n_tot} carte · 5 dèi · 13 dorsi · 5 pacchetti</p>
<div class="stage" aria-hidden="true">
<div class="god g1 float" style="animation-delay:-1s"><img src="img/dei/efesto-scontornato.webp" alt=""></div>
<div class="god g2 float" style="animation-delay:-3.5s"><img src="img/dei/demetra-scontornato.webp" alt=""></div>
<div class="god g3 float" style="animation-delay:-2.2s"><img src="img/dei/era-scontornato.webp" alt=""></div>
<div class="god g4 float" style="animation-delay:-4.6s"><img src="img/dei/poseidone-scontornato.webp" alt=""></div>
<div class="trio">
<span class="tilt t1" data-free><span class="tilt-in"><img src="{card_src('Luna', 'Acquario')}" alt=""></span></span>
<span class="tilt t3" data-free><span class="tilt-in"><img src="{asc_src('Cancro')}" alt=""></span></span>
<span class="tilt t2" data-free><span class="tilt-in"><img src="{card_src('Sole', 'Capricorno')}" alt=""></span></span>
</div>
</div>
</section>

<section id="carte" aria-labelledby="h-carte">
<div class="wrap">
<div class="sec-head"><h2 id="h-carte">Le carte</h2>
<p>Ogni carta è un pianeta in un segno: 7 pianeti per 12 segni, più i 12 Ascendenti.</p></div>
<div class="tabs" role="tablist" aria-label="Rarità">{tabs}</div>
{panels}
</div>
</section>

<section id="dei" aria-labelledby="h-dei">
<div class="wrap">
<div class="sec-head"><h2 id="h-dei">Gli dèi</h2>
<p>Quattro dèi si contendono il trono di Zeus. Quello che scegli definisce la tua <strong>fazione</strong> e potenzia le creature del suo elemento, in tutti i tuoi mazzi.</p></div>
{gods}
<div class="ade">
<div class="ade-in">
{tilt_img("img/za-dio-ade.webp", "Carta di Ade")}
<div>
<span class="lock"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>Da sbloccare · fase 2</span>
<h3>Ade, signore dei morti</h3>
<p>Il quinto dio non ha un elemento: regna su chi cade. +1 PV per ogni creatura avversaria che muore, fino ai tuoi PV iniziali.</p>
<p>Arriva con la fase 2 del gioco. Per ora aspetta nell'ombra.</p>
</div>
</div>
</div>
</div>
</section>

<section id="dorsi" aria-labelledby="h-dorsi">
<div class="wrap">
<div class="sec-head"><h2 id="h-dorsi">I dorsi</h2></div>
<div class="std">
{tilt_img("img/dorsi/dorso-standard.webp", "Dorso standard")}
<div><h3>Dorso standard</h3><p>Il dorso di tutte le carte: blu notte, motivo shippō e il sole al centro.</p>
<p>I dorsi dei segni sono <strong>cosmetici</strong>: si comprano con i crediti e non cambiano nulla in partita.</p></div>
</div>
<div class="belems">{backs}</div>
</div>
</section>

<section id="pacchetti" aria-labelledby="h-pacchetti">
<div class="wrap">
<div class="sec-head"><h2 id="h-pacchetti">I pacchetti</h2></div>
{packs}
<p class="legend"><span><b class="s-c">C</b> Comune</span><span><b class="s-r">R</b> Rara</span><span><b class="s-e">E</b> Epica</span><span><b class="s-s">S</b> Stella: lo slot che può contenere le carte più rare</span><span><b class="s-a">A</b> Ascendente</span></p>
</div>
</section>
</main>

<footer>
<nav aria-label="Pagine"><a href="index.html">Home</a><a href="regolamento.html">Regolamento</a><a href="collezione.html" aria-current="page">Collezione</a></nav>
Zodiax Arena · gioco di carte collezionabili tra astrologia e mitologia greca
</footer>

<div class="lb" id="lb" hidden role="dialog" aria-modal="true" aria-label="Carta ingrandita">
<button class="lbx" type="button" aria-label="Chiudi">✕</button>
<span class="tilt" id="lbCard" data-free><span class="tilt-in"><span class="flipper"><span class="face front"><img src="" alt=""></span><span class="face back"><img src="img/hd/dorso-standard.webp" alt="Dorso standard"></span></span></span></span>
<p class="lbhint" id="lbHint" hidden><span>‹ Scorri per girare la carta ›</span></p>
</div>

<script>
(() => {{
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const MAX = 14;
  // inclinazione 3D: segue il mouse o il dito, la luce segue il punto toccato
  function bind(el) {{
    let down = null;
    const set = (e) => {{
      const r = el.getBoundingClientRect();
      const x = Math.min(Math.max((e.clientX - r.left) / r.width, 0), 1);
      const y = Math.min(Math.max((e.clientY - r.top) / r.height, 0), 1);
      el.style.setProperty('--ry', ((x - .5) * 2 * MAX).toFixed(2) + 'deg');
      el.style.setProperty('--rx', ((.5 - y) * 2 * MAX).toFixed(2) + 'deg');
      el.style.setProperty('--gx', (x * 100).toFixed(1) + '%');
      el.style.setProperty('--gy', (y * 100).toFixed(1) + '%');
      el.style.setProperty('--ga', '1');
    }};
    const reset = () => {{
      el.classList.remove('on');
      ['--rx', '--ry'].forEach(p => el.style.setProperty(p, '0deg'));
      el.style.setProperty('--ga', '0');
    }};
    el.addEventListener('pointerenter', e => {{ if (e.pointerType === 'mouse' && !still) {{ el.classList.add('on'); set(e); }} }});
    el.addEventListener('pointerdown', e => {{
      down = {{ x: e.clientX, y: e.clientY, t: Date.now() }};
      if (e.pointerType !== 'mouse' && !still) {{ el.classList.add('on'); set(e); }}
    }});
    el.addEventListener('pointermove', e => {{ if (el.classList.contains('on')) set(e); }});
    el.addEventListener('pointerleave', e => {{ if (e.pointerType === 'mouse') reset(); }});
    el.addEventListener('pointercancel', reset);
    el.addEventListener('pointerup', e => {{
      if (e.pointerType !== 'mouse') reset();
      const tap = down && Math.hypot(e.clientX - down.x, e.clientY - down.y) < 10 && Date.now() - down.t < 400;
      down = null;
      if (tap && el.dataset.zoom) open(el.dataset.zoom, el.querySelector('img').alt, el.classList.contains('pack'), el);
    }});
  }}
  document.querySelectorAll('.tilt').forEach(bind);

  // ingrandimento
  const lb = document.getElementById('lb'), lbCard = document.getElementById('lbCard'), lbImg = lbCard.querySelector('img');
  let last = null;
  const lbHint = document.getElementById('lbHint');
  let flip = 0;
  const setFlip = d => {{ flip += d; lbCard.style.setProperty('--flip', flip + 'deg'); if (lbHint) lbHint.hidden = true; }};
  let keepY = 0;
  function open(src, alt, wide, trigger) {{
    last = trigger || document.activeElement; keepY = window.scrollY;
    lbImg.src = src; lbImg.alt = alt;
    lbCard.classList.toggle('pack', wide); lbCard.classList.toggle('wide', wide);
    // solo le carte di fronte (segni, Ascendenti, dei) si girano: dorsi e pacchetti no
    const canFlip = !/(dorso-|\\/pacchetti\\/)/.test(src);
    lbCard.classList.toggle('can-flip', canFlip); lbHint.hidden = !canFlip;
    flip = 0; lbCard.style.transition = 'none'; lbCard.style.setProperty('--flip', '0deg');
    requestAnimationFrame(() => {{ lbCard.style.transition = ''; }});
    lb.hidden = false; lb.querySelector('.lbx').focus({{ preventScroll: true }});
  }}
  // swipe orizzontale (dito o mouse): la carta gira di 180 gradi nella direzione del gesto
  let sw = null;
  lbCard.addEventListener('pointerdown', e => {{ if (lbCard.classList.contains('can-flip')) sw = {{ x: e.clientX, y: e.clientY }}; }});
  lbCard.addEventListener('pointerup', e => {{
    if (!sw) return;
    const dx = e.clientX - sw.x, dy = e.clientY - sw.y; sw = null;
    if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy) * 1.2) setFlip(dx > 0 ? 180 : -180);
  }});
  lbCard.addEventListener('pointercancel', () => {{ sw = null; }});
  document.addEventListener('keydown', e => {{
    if (lb.hidden || !lbCard.classList.contains('can-flip')) return;
    if (e.key === 'ArrowRight') setFlip(180); else if (e.key === 'ArrowLeft') setFlip(-180);
  }});
  function close() {{ lb.hidden = true; lbImg.src = ''; if (last) last.focus({{ preventScroll: true }}); window.scrollTo(0, keepY); }}
  lb.addEventListener('click', e => {{ if (e.target === lb || e.target.closest('.lbx')) close(); }});
  document.addEventListener('keydown', e => {{ if (e.key === 'Escape' && !lb.hidden) close(); }});
  document.querySelectorAll('.tilt[data-zoom]').forEach(b => b.addEventListener('keydown', e => {{
    if (e.key === 'Enter' || e.key === ' ') {{ e.preventDefault(); open(b.dataset.zoom, b.querySelector('img').alt, b.classList.contains('pack'), b); }}
  }}));

  // schede per rarità
  const tabs = [...document.querySelectorAll('[role=tab]')];
  function pick(t, focus) {{
    tabs.forEach(x => {{
      const on = x === t;
      x.setAttribute('aria-selected', on); x.tabIndex = on ? 0 : -1;
      document.getElementById(x.getAttribute('aria-controls')).hidden = !on;
    }});
    if (focus) t.focus();
  }}
  tabs.forEach((t, i) => {{
    t.addEventListener('click', () => pick(t));
    t.addEventListener('keydown', e => {{
      const d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
      if (d) {{ e.preventDefault(); pick(tabs[(i + d + tabs.length) % tabs.length], true); }}
    }});
  }});
}})();
</script>
</body>
</html>
"""

(ROOT / "collezione.html").write_text(HTML, encoding="utf-8")
print("collezione.html", len(HTML), "caratteri,", n_tot, "carte")
