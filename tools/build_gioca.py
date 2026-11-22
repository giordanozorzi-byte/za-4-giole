"""Genera gioca.html dalla prova di gioco (tools/src/prova.html, l'artefatto "Zodiax Arena · Prova"),
con la navbar e lo stile del sito. Lancio: python tools/build_gioca.py  (dalla radice del repo)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from menu_mobile import CSS as MENU_CSS, menu

ROOT = Path(__file__).resolve().parent.parent
h = (ROOT / "tools" / "src" / "prova.html").read_text(encoding="utf-8")

def rep(a, b):
    global h
    assert h.count(a) == 1, (a[:70], h.count(a)); h = h.replace(a, b)

GOLD = "background:linear-gradient(180deg,#FFF0B3 0%,#E8B04B 55%,#B07A22 100%);color:var(--ink-gold);border-color:#B07A22;box-shadow:0 4px 12px rgba(0,0,0,.45)"

rep("<title>Zodiax Arena · Prova</title>", "<title>Gioca! · Zodiax Arena</title>\n<meta name=\"description\" content=\"Componi due mazzi e prova una sfida di Zodiax Arena, round per round.\">")
rep("--sky:#1D2238; --sky-2:#07060F; --panel:#0B0E35; --panel-2:#2A3158; --line:#3A4374;",
    "--sky:#10172B; --sky-2:#07060F; --panel:#0B0E35; --panel-2:#1B2350; --line:#343C6B; --nav-h:70px; --gold-s:#EBCF93;")
rep("--text:#FFF8EC; --muted:#A8A3CF;", "--text:#F3EBDD; --muted:#B9B6CF;")
rep("html,body{margin:0;background:var(--sky);color:var(--text);font-family:var(--f-body);font-size:16px;line-height:1.45;overflow-x:clip}",
    "html,body{margin:0;color:var(--text);font-family:var(--f-body);font-size:16px;line-height:1.45;overflow-x:clip}\n"
    "body{min-height:100vh;padding-top:var(--nav-h);background:radial-gradient(ellipse 900px 420px at 50% 0%,rgba(255,214,107,.08),rgba(255,214,107,0) 70%),linear-gradient(180deg,var(--sky) 0%,var(--panel) 100%) fixed}")
rep("h1,h2,h3{font-family:var(--f-display);font-weight:700;margin:0;letter-spacing:.01em}",
    "h1,h2,h3{font-family:var(--f-display);font-weight:700;margin:0;letter-spacing:.01em;color:#FFF8EC}")

# barra della pagina sotto la navbar
rep(".top{position:sticky;top:0;z-index:10;background:var(--sky);padding-top:env(safe-area-inset-top,0px);border-bottom:1px solid var(--panel-2)}",
    ".top{position:sticky;top:var(--nav-h);z-index:19;background:linear-gradient(rgba(16,23,43,.97) 80%,rgba(16,23,43,0));-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)}")
rep(".top h1{font-size:1.05rem;color:var(--gold);flex:1}", ".top h1{font-size:1.15rem;color:var(--gold);flex:1;letter-spacing:.04em}")
rep(".pill{border:1px solid var(--line);background:var(--panel);border-radius:10px;padding:6px 10px;font-size:.82rem;font-weight:700}",
    ".pill{border:1.5px solid rgba(235,207,147,.55);background:var(--panel);border-radius:6px;padding:7px 12px;color:var(--gold-s);font:700 .78rem var(--f-display);letter-spacing:.1em;text-transform:uppercase}")
rep('<header class="top"><div class="wrap"><h1 id="title">Componi i mazzi</h1><button class="pill" id="backBtn" hidden>Mazzi</button></div></header>',
    '<header class="zn-head">\n<div class="zn-brand">\n'
    '<a href="index.html" aria-label="Zodiax Arena, torna alla home"><img src="img/za-logo-compatto.webp" alt="Zodiax Arena"></a>\n'
    '<a class="zn-ghost" href="regolamento.html">Regolamento</a>\n<a class="zn-ghost" href="collezione.html">Collezione</a>\n'
    '<a class="zn-ghost" href="gioca.html" aria-current="page">Gioca!</a>\n</div>\n'
    '<a class="zn-ghost zn-cta" href="index.html#iscriviti">Iscriviti</a>\n'
    + menu("regolamento.html", "collezione.html", "index.html#iscriviti", "index.html", "play") + "\n</header>\n"
    '<div class="top"><div class="wrap"><h1 id="title">Componi i mazzi</h1><button class="pill" id="backBtn" hidden>‹ Mazzi</button></div></div>')

# schede, dei e bottoni come il resto del sito
rep(".tabs button{padding:10px;border-radius:12px;border:1px solid var(--line);background:var(--panel);font-weight:800;",
    ".tabs button{padding:10px;border-radius:8px;border:1.5px solid rgba(235,207,147,.3);background:var(--panel);font:700 1rem var(--f-display);letter-spacing:.06em;")
rep(".tabs button[aria-selected=true]{border-color:var(--gold);background:var(--panel-2);color:var(--gold)}",
    ".tabs button[aria-selected=true]{border-color:var(--gold);background:var(--panel-2);color:#FFE7A0;box-shadow:0 0 18px -6px var(--gold)}")
rep(".sec h2{font-size:.78rem;font-family:var(--f-body);font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}",
    ".sec h2{font-size:.78rem;font-family:var(--f-body);font-weight:800;letter-spacing:.16em;text-transform:uppercase;color:var(--gold)}")
rep(".btn{flex:1;padding:13px 12px;border-radius:14px;border:1px solid var(--line);background:var(--panel);font-weight:800}",
    ".btn{flex:1;padding:13px 12px;border-radius:8px;border:1.5px solid rgba(235,207,147,.55);background:var(--panel);color:var(--gold-s);font:700 .86rem var(--f-display);letter-spacing:.1em;text-transform:uppercase}")
rep(".btn.primary{background:var(--indaco);border-color:var(--gold);color:var(--text)}", f".btn.primary{{{GOLD};font-weight:800}}")
rep(".btn.gold{background:linear-gradient(180deg,#FFE7A0,#E8B04B 55%,#9C6A1C);color:var(--ink-gold);border-color:#FFE7A0;font-family:var(--f-display);letter-spacing:.06em}",
    f".btn.gold{{{GOLD};font-weight:800;font-size:.95rem;letter-spacing:.12em}}")
rep(".dock{position:sticky;bottom:0;z-index:10;background:linear-gradient(#1D223800,var(--sky) 25%);",
    ".dock{position:sticky;bottom:0;z-index:10;background:linear-gradient(rgba(11,14,53,0),rgba(11,14,53,.96) 30%);")
rep(".who{font-family:var(--f-display);font-weight:700;font-size:.95rem;color:var(--gold)}",
    ".who{font-family:var(--f-display);font-weight:700;font-size:.95rem;color:#FFE7A0;letter-spacing:.04em}")

NAV = """
/* navbar comune a landing, regolamento, collezione e gioca */
.zn-head{position:fixed;top:0;left:0;right:0;z-index:30;display:flex;align-items:center;justify-content:space-between;gap:12px;padding:8px 32px;
background:linear-gradient(180deg,rgba(18,24,48,.9),rgba(10,15,34,.86));-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);border-bottom:2px solid #E8B04B;box-shadow:0 -6px 0 -5px rgba(217,185,124,.45) inset}
.zn-brand{display:flex;align-items:center;gap:14px}
.zn-brand>a:first-child{flex:none}
.zn-brand>a:first-child img{height:52px;width:auto;display:block}
.zn-ghost{display:inline-flex;align-items:center;min-height:44px;padding:0 18px;border:1.5px solid rgba(235,207,147,.55);border-radius:6px;font:700 14px Cinzel,serif;letter-spacing:.14em;text-transform:uppercase;text-decoration:none;color:#EBCF93;white-space:nowrap;transition:background .2s}
.zn-ghost:hover{background:rgba(235,207,147,.14)}
.zn-ghost[aria-current=page]{background:rgba(235,207,147,.16);border-color:#E8B04B;color:#FFE7A0}
.zn-ghost.zn-cta{border-color:#EBCF93;color:#FFE7A0}
""" + MENU_CSS + """@media (max-width:860px){
.za-menu{display:block}
.zn-brand .zn-ghost,.zn-head>.zn-cta{display:none!important}
.zn-brand>a:first-child img{height:48px}
.zn-head{padding:8px 16px}
:root{--nav-h:66px}
}

/* desktop: composizione larga, arena con le creature affiancate e la cronaca a lato */
@media (min-width:1024px){
.wrap{max-width:1180px;padding:0 32px}
.top .wrap{padding-block:14px}
#setup{display:grid;grid-template-columns:minmax(0,1fr) 340px;column-gap:40px;align-items:start}
#setup>.tabs{grid-column:1/-1;max-width:520px}
#setup>.sec:has(#gods){grid-column:2;grid-row:2}
#setup>.sec:has(#deck){grid-column:1;grid-row:2/span 2}
#setup>.row{grid-column:2;grid-row:3;align-self:start}
#setup>.dock{grid-column:1/-1}
.deck{grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
.gods{grid-template-columns:repeat(2,1fr);gap:10px}
.god{flex-direction:row;justify-content:flex-start;gap:10px;padding:8px 10px;font-size:.9rem;text-align:left}
.god span{display:block}
.dock .btn.gold{max-width:420px;display:block;margin-left:auto}
.pick{grid-template-columns:repeat(6,1fr)}
.sheet{align-items:center}
.sheet>div{width:min(860px,100%);border-radius:20px}
.arena{display:grid;grid-template-columns:minmax(0,1fr) auto minmax(0,1fr) 340px;grid-template-rows:auto 1fr;column-gap:28px;row-gap:12px;align-items:start;padding-top:20px}
.side,.side.me{grid-template-columns:1fr;justify-items:center;text-align:center}
.side.me{grid-column:1;grid-row:1/span 2}
.vs{grid-column:2;grid-row:1/span 2;flex-direction:column;align-self:center;padding:0 4px}
.vs::before,.vs::after{width:1px;height:80px;flex:none}
.side.opp{grid-column:3;grid-row:1/span 2}
.side.me .info,.side .info{order:0;align-items:center;text-align:center}
.side.me .stats,.side.me .chips{justify-content:center}
.slotc{max-width:260px}
.pips{margin:0 auto}
#log{grid-column:4;grid-row:1}
details.hist{grid-column:4;grid-row:2}
#game>.dock .row{max-width:520px;margin-left:auto}
}
"""
rep("@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}.dmg.show{opacity:1}}",
    NAV + "@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}.dmg.show{opacity:1}}")

(ROOT / "gioca.html").write_text(h, encoding="utf-8")
print("gioca.html", len(h))
