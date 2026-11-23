"""Menu a tendina (hamburger) per telefono e tablet su landing e collezione.
Lancio: python tools/menu_mobile.py  (dalla radice del repo). Idempotente."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent

CSS = """
/* menu a tendina su telefono e tablet */
.za-menu{display:none}
.za-menu summary{list-style:none;display:flex;flex-direction:column;justify-content:center;gap:5px;width:48px;height:48px;padding:0 12px;box-sizing:border-box;border:1.5px solid rgba(235,207,147,.55);border-radius:8px;background:rgba(11,14,53,.6);cursor:pointer}
.za-menu summary::-webkit-details-marker{display:none}
.za-menu summary:focus-visible{outline:2px solid #E8B04B;outline-offset:2px}
.za-menu summary span{display:block;height:2px;border-radius:2px;background:#FFE7A0;transition:transform .25s ease,opacity .2s ease}
.za-menu[open] summary{border-color:#E8B04B}
.za-menu[open] summary span:nth-child(1){transform:translateY(7px) rotate(45deg)}
.za-menu[open] summary span:nth-child(2){opacity:0}
.za-menu[open] summary span:nth-child(3){transform:translateY(-7px) rotate(-45deg)}
.za-menu-panel{position:absolute;left:0;right:0;top:100%;display:flex;flex-direction:column;padding:8px 20px 22px;background:rgba(10,15,34,.97);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);border-bottom:2px solid #E8B04B;box-shadow:0 24px 40px rgba(0,0,0,.55)}
.za-menu-panel a{display:block;padding:16px 4px;border-bottom:1px solid rgba(235,207,147,.18);font:700 16px Cinzel,serif;letter-spacing:.14em;text-transform:uppercase;text-decoration:none;color:#EBCF93}
.za-menu-panel a[aria-current=page]{color:#FFE7A0}
.za-menu-panel a.za-menu-cta{margin-top:18px;padding:15px 4px;border:0;border-radius:8px;text-align:center;font-weight:800;color:#2A1405;background:linear-gradient(180deg,#FFF0B3 0%,#E8B04B 55%,#B07A22 100%);box-shadow:0 4px 12px rgba(0,0,0,.45)}
.za-menu-panel a.za-menu-login{padding:12px 4px 0;border:0;text-align:center;font:600 13px Nunito,sans-serif;letter-spacing:0;text-transform:none;color:#B9B6CF}
@media (prefers-reduced-motion: reduce){.za-menu summary span{transition:none}}
"""

def menu(rules, collezione, iscriviti, accedi, current=None, gioca="gioca.html"):
    cur = lambda n: ' aria-current="page"' if current == n else ''
    close = ' onclick="this.closest(\'details\').open=false"'
    return ('<details class="za-menu"><summary aria-label="Menu"><span></span><span></span><span></span></summary>'
            '<div class="za-menu-panel" role="navigation" aria-label="Menu">'
            f'<a href="{rules}"{cur("rules")}{close}>Regolamento</a>'
            f'<a href="{collezione}"{cur("coll")}{close}>Collezione</a>'
            f'<a href="{gioca}"{cur("play")}{close}>Gioca!</a>'
            f'<a class="za-menu-cta" href="{iscriviti}"{close}>Iscriviti</a>'
            f'<a class="za-menu-login" href="{accedi}"{close}>Hai già un account? Accedi</a>'
            '</div></details>')

# ---------- collezione.html ----------
p = ROOT / "collezione.html"; h = p.read_text(encoding="utf-8")
if "za-menu" not in h:
    h = h.replace("</style>", CSS + """@media (max-width:860px){
.za-menu{display:block}
header .brand .ghost,header>.ghost.cta{display:none!important}
header .brand>a:first-child img{height:48px!important}
header{padding:8px 16px}
}
</style>""", 1)
    h = h.replace('<a class="ghost cta" href="index.html#iscriviti">Iscriviti</a>\n</header>',
                  '<a class="ghost cta" href="index.html#iscriviti">Iscriviti</a>\n'
                  + menu("regolamento.html", "collezione.html", "index.html#iscriviti", "index.html", "coll") + "\n</header>", 1)
    assert h.count("za-menu-panel") >= 2
    p.write_text(h, encoding="utf-8"); print("collezione ok")

# ---------- index.html (pagina impacchettata) ----------
p = ROOT / "index.html"; L = p.read_text(encoding="utf-8").split("\n")
ti = next(i for i, l in enumerate(L) if '<script type="__bundler/template">' in l)
m = re.match(r'(\s*<script type="__bundler/template">)(.*)(</script>\s*)$', L[ti], re.S)
t = json.loads(m.group(2))
if "za-menu" not in t:
    t = t.replace("</style>\n</helmet>", CSS + """@media (max-width: 860px){
.za-menu{display:block}
.zl-rules,header nav{display:none!important}
header .zl-brand>a:first-child img{height:48px!important}
}
</style>
</helmet>""", 1)
    # niente onclick testuali nella landing: React li rifiuta (errore #231); il menu si chiude con uno script esterno
    t = t.replace("</header>", (menu("regolamento.html", "collezione.html", "#iscriviti", "#") + "\n</header>").replace(" onclick=\"this.closest('details').open=false\"", ""), 1)
    assert t.count("za-menu-panel") >= 2
    L[ti] = m.group(1) + json.dumps(t).replace("</", "<\\u002F") + m.group(3)
    p.write_text("\n".join(L), encoding="utf-8"); print("index ok")
