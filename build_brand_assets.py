"""Emit the shipping brand assets from the chosen girih variant (B).

Single source of geometry: build_logo_variants.py. Everything here is derived
from it so the mark in the page, the favicon and the OG image cannot drift.
"""
import build_logo_variants as G

# --- chosen variant --------------------------------------------------------
VAR = dict(s=58.0, sw=2.3, opacity=0.70, inner_octagon=True)

# The mark is authored in the shield's own 24-unit box (matching the existing
# inline <svg viewBox="0 0 24 24"> in index.html), so the pattern cell and
# stroke must be converted out of 512-tile units.
U = VAR["s"] / G.SC          # cell size in shield units
SWU = VAR["sw"] / G.SC       # stroke weight in shield units
CY = 11.5                    # shield path spans y 2.2..20.8 -> centre 11.5


def mark24(uid, with_pattern=True):
    """Shield + girih + check in a 0 0 24 24 box. No tile: the CSS draws that."""
    pat = G.pattern(f"gp-{uid}", U, SWU, VAR["inner_octagon"], cx=12.0, cy=CY)
    pattern_layer = f'''
  <g clip-path="url(#gc-{uid})" mask="url(#gm-{uid})" opacity="{VAR["opacity"]}">
    <rect x="0" y="0" width="24" height="24" fill="url(#gp-{uid})"/>
  </g>''' if with_pattern else ""
    defs_pattern = f'''
    {pat}
    <clipPath id="gc-{uid}"><path d="{G.SHIELD_D}"/></clipPath>
    <mask id="gm-{uid}">
      <rect x="0" y="0" width="24" height="24" fill="#fff"/>
      <path d="{G.CHECK_D}" fill="none" stroke="#000" stroke-width="3.5"
        stroke-linecap="round" stroke-linejoin="round"/>
    </mask>''' if with_pattern else ""
    return f'''<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="gs-{uid}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{G.SHIELD_HI}"/>
      <stop offset="1" stop-color="{G.SHIELD_LO}"/>
    </linearGradient>{defs_pattern}
  </defs>
  <path d="{G.SHIELD_D}" fill="url(#gs-{uid})"/>{pattern_layer}
  <path d="{G.SHIELD_D}" stroke="#ffffff" stroke-opacity="0.5" stroke-width="1.1"/>
  <path d="{G.CHECK_D}" stroke="#ffffff" stroke-width="2.1"
    stroke-linecap="round" stroke-linejoin="round"/>
</svg>'''


def favicon():
    """Plain shield on the green tile -- no girih. At 16-32px the gold lines
    only add noise, so the favicon carries the silhouette alone."""
    t, sh = 64.0, 64.0 * 26 / 46
    off, sc = (64.0 - sh) / 2, sh / 24
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"
     role="img" aria-label="sh-eld shield logo">
  <defs>
    <linearGradient id="ft" x1="0.281" y1="-0.103" x2="0.719" y2="1.103">
      <stop offset="0" stop-color="{G.GREEN_HI}"/>
      <stop offset="1" stop-color="{G.GREEN_LO}"/>
    </linearGradient>
    <linearGradient id="fs" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{G.SHIELD_HI}"/>
      <stop offset="1" stop-color="{G.SHIELD_LO}"/>
    </linearGradient>
  </defs>
  <rect width="64" height="64" rx="{64 * 13 / 46:.2f}" fill="url(#ft)"/>
  <g transform="translate({off:.2f} {off:.2f}) scale({sc:.4f})" fill="none">
    <path d="{G.SHIELD_D}" fill="url(#fs)"/>
    <path d="{G.SHIELD_D}" stroke="#ffffff" stroke-opacity="0.5" stroke-width="1.1"/>
    <path d="{G.CHECK_D}" stroke="#ffffff" stroke-width="2.1"
      stroke-linecap="round" stroke-linejoin="round"/>
  </g>
</svg>'''


def lockup_page(mark_px, bg, pad_x=0, pad_y=0, canvas=None):
    """The .logo lockup from index.html, reproduced for offscreen rendering."""
    gap, fs, rad = mark_px * 14 / 46, mark_px * 26 / 46, mark_px * 13 / 46
    frame = (f"width:{canvas[0]}px;height:{canvas[1]}px;"
             if canvas else f"padding:{pad_y}px {pad_x}px;width:max-content;")
    return f'''<!doctype html><meta charset="utf-8"><style>
  html,body{{margin:0;background:{bg};}}
  .stage{{{frame}display:flex;align-items:center;justify-content:center;}}
  .logo{{display:flex;align-items:center;gap:{gap:.2f}px;}}
  .mark{{width:{mark_px}px;height:{mark_px}px;border-radius:{rad:.2f}px;
    background:linear-gradient(160deg,{G.GREEN_HI},{G.GREEN_LO});
    display:flex;align-items:center;justify-content:center;
    box-shadow:0 {mark_px*6/46:.1f}px {mark_px*16/46:.1f}px rgba(43,112,64,.45),
      inset 0 {max(1,mark_px/46):.1f}px 0 rgba(255,255,255,.18);}}
  .mark svg{{width:{mark_px*26/46:.2f}px;height:{mark_px*26/46:.2f}px;display:block;}}
  .wordmark{{font:800 {fs:.2f}px -apple-system,BlinkMacSystemFont,"Segoe UI",
    Roboto,Helvetica,Arial,sans-serif;letter-spacing:-.03em;color:#f4f5f6;}}
  .dot{{display:inline-block;width:.21em;height:.21em;border-radius:50%;
    background:#4fbf6c;vertical-align:.48em;margin:0 .07em;}}
</style><div class="stage"><div class="logo">
  <span class="mark">{mark24("og")}</span>
  <span class="wordmark">sh<span class="dot"></span>eld</span>
</div></div>'''


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    with open("favicon.svg", "w", encoding="utf-8") as fh:
        fh.write(favicon() + "\n")
    with open(f"{out}/mark24.svg", "w", encoding="utf-8") as fh:
        fh.write(mark24("m"))
    with open(f"{out}/og.html", "w", encoding="utf-8") as fh:
        fh.write(lockup_page(210, "#000000", canvas=(1200, 630)))
    with open(f"{out}/lockup.html", "w", encoding="utf-8") as fh:
        fh.write(lockup_page(512, "transparent", pad_x=110, pad_y=110))
    print("wrote favicon.svg, mark24.svg, og.html, lockup.html")
