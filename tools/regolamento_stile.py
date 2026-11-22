"""Allinea regolamento.html a landing e collezione: navbar comune con menu a tendina,
barra dei capitoli sotto la navbar (senza bottone Capitoli), colori e bottoni come la landing.
Lancio: python tools/regolamento_stile.py  (dalla radice del repo). Idempotente."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from menu_mobile import CSS as MENU_CSS, menu

ROOT = Path(__file__).resolve().parent.parent
p = ROOT / "regolamento.html"; h = p.read_text(encoding="utf-8")
if "zn-head" in h:
    sys.exit("già aggiornato")

def rep(a, b):
    global h
    assert h.count(a) == 1, (a[:70], h.count(a)); h = h.replace(a, b)

# colori come landing e collezione
rep("--sky:#1D2238; --sky-2:#07060F; --panel:#0B0E35; --panel-2:#2A3158; --line:#3A4374; --line-soft:#2A3158;",
    "--sky:#10172B; --sky-2:#07060F; --panel:#0B0E35; --panel-2:#1B2350; --line:#343C6B; --line-soft:#232A55;")
rep("--text:#FFF8EC; --muted:#A8A3CF; --faint:#A8A3CF;", "--text:#F3EBDD; --muted:#B9B6CF; --faint:#B9B6CF; --gold-s:#EBCF93;\n  --nav-h:70px; --bar-h:64px;")
rep("body{color:var(--text);font-family:var(--f-body);font-size:16px;line-height:1.5;margin:0;background:var(--sky);font-variant-numeric:tabular-nums}",
    "body{color:var(--text);font-family:var(--f-body);font-size:16px;line-height:1.5;margin:0;min-height:100vh;padding-top:var(--nav-h);font-variant-numeric:tabular-nums;"
    "background:radial-gradient(ellipse 900px 420px at 50% 0%,rgba(255,214,107,.08),rgba(255,214,107,0) 70%),linear-gradient(180deg,var(--sky) 0%,var(--panel) 100%) fixed}")
rep("h1,h2,h3{font-family:var(--f-display);font-weight:700;margin:0;text-wrap:balance;letter-spacing:.01em}",
    "h1,h2,h3{font-family:var(--f-display);font-weight:700;margin:0;text-wrap:balance;letter-spacing:.01em;color:#FFF8EC}")

# barra dei capitoli: sotto la navbar, senza Home, Collezione e Capitoli
rep(".top{position:sticky;top:env(safe-area-inset-top,0px);z-index:20;background:linear-gradient(var(--sky) 78%,#1D223800)}",
    ".top{position:sticky;top:var(--nav-h);z-index:19;background:linear-gradient(rgba(16,23,43,.97) 80%,rgba(16,23,43,0));-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)}")
rep(".brand{font-family:var(--f-display);", ".brand{font-family:var(--f-display);font-weight:700;letter-spacing:.04em;")
rep("""<header class="top">
  <div class="wrap">
    <div class="top-row">
      <a class="home-btn" href="index.html" aria-label="Torna alla home di Zodiax Arena">‹ Home</a>
      <a class="home-btn" href="collezione.html">Collezione</a>
      <span class="brand" id="chTitle">Regolamento per i giocatori</span>
      <span class="part" id="partLbl">Parte 1</span>
      <button class="menu-btn" id="menuBtn" aria-haspopup="dialog">Capitoli</button>
    </div>
    <div class="prog" id="prog" aria-hidden="true"></div>
  </div>
</header>""",
"""<header class="zn-head">
<div class="zn-brand">
<a href="index.html" aria-label="Zodiax Arena, torna alla home"><img src="img/za-logo-compatto.webp" alt="Zodiax Arena"></a>
<a class="zn-ghost" href="regolamento.html" aria-current="page">Regolamento</a>
<a class="zn-ghost" href="collezione.html">Collezione</a>
</div>
<a class="zn-ghost zn-cta" href="index.html#iscriviti">Iscriviti</a>
""" + menu("regolamento.html", "collezione.html", "index.html#iscriviti", "index.html", "rules") + """
</header>

<div class="top">
  <div class="wrap">
    <div class="top-row">
      <span class="brand" id="chTitle">Regolamento per i giocatori</span>
      <span class="part" id="partLbl">Parte 1</span>
    </div>
    <div class="prog" id="prog" aria-hidden="true"></div>
  </div>
</div>""")
rep("$('menuBtn').onclick=()=>{", "if($('menuBtn'))$('menuBtn').onclick=()=>{")

# bottoni come la landing: oro pieno per andare avanti, bordo oro per tornare indietro
rep(".stepnav button{flex:1;padding:12px;border-radius:12px;border:1px solid var(--line);background:var(--panel-2);font-weight:700}",
    ".stepnav button{flex:1;padding:12px;border-radius:8px;border:1.5px solid rgba(235,207,147,.55);background:var(--panel);color:var(--gold-s);font:700 14px var(--f-display);letter-spacing:.1em;text-transform:uppercase}")
GOLD = "background:linear-gradient(180deg,#FFF0B3 0%,#E8B04B 55%,#B07A22 100%);color:var(--ink-gold);border-color:#B07A22;box-shadow:0 4px 12px rgba(0,0,0,.45)"
rep(".stepnav .go{background:var(--indaco);color:var(--text);border-color:var(--gold);flex:2}", f".stepnav .go{{{GOLD};flex:2;font-weight:800}}")
rep(".cta{padding:12px 18px;border-radius:999px;border:1px solid var(--gold);background:var(--indaco);color:var(--text);font-weight:800;letter-spacing:.06em}",
    f".cta{{padding:14px 26px;border-radius:8px;border:1px solid #B07A22;{GOLD};font:800 15px var(--f-display);letter-spacing:.1em;text-transform:uppercase}}")
rep(".bottom{position:fixed;left:0;right:0;bottom:0;z-index:20;background:linear-gradient(#1D223800,var(--sky) 30%)}",
    ".bottom{position:fixed;left:0;right:0;bottom:0;z-index:20;background:linear-gradient(rgba(11,14,53,0),rgba(11,14,53,.96) 34%)}")
rep(".bottom button{flex:1;padding:13px 10px;border-radius:14px;border:1px solid var(--line);background:var(--panel);font-weight:800}",
    ".bottom button{flex:1;padding:14px 10px;border-radius:8px;border:1.5px solid rgba(235,207,147,.55);background:var(--panel);color:var(--gold-s);font:700 14px var(--f-display);letter-spacing:.12em;text-transform:uppercase}")
rep(".bottom .next{flex:2;background:var(--panel-2);border-color:var(--gold);color:var(--gold)}", f".bottom .next{{flex:2;{GOLD};font-weight:800}}")

# elementi fissi che stavano sotto la vecchia barra
rep("position:sticky;top:calc(env(safe-area-inset-top,0px) + 70px);", "position:sticky;top:calc(var(--nav-h) + var(--bar-h));")
rep(".stoc{display:flex;flex-direction:column;gap:4px;grid-column:1;grid-row:1/span 20;position:sticky;top:100px;padding-top:20px}",
    ".stoc{display:flex;flex-direction:column;gap:4px;grid-column:1;grid-row:1/span 20;position:sticky;top:calc(var(--nav-h) + var(--bar-h) + 16px);padding-top:20px}")
rep(".split>.col.sticky{position:sticky;top:100px}", ".split>.col.sticky{position:sticky;top:calc(var(--nav-h) + var(--bar-h) + 16px)}")

# navbar comune
NAV = """
/* navbar comune a landing, regolamento e collezione */
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
"""
rep("</style>\n\n<header class=\"zn-head\">", NAV + "</style>\n\n<header class=\"zn-head\">")
p.write_text(h, encoding="utf-8"); print("regolamento ok")
