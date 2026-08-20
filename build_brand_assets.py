"""Emit the shipping brand assets for Shieldora.

Single source of geometry: build_logo_variants.py. The page mark, favicon and
OG image are all generated here so they cannot drift apart.

The mark is a plain shield: green tile, deeper green shield, a single gold
rule on the outline, white checkmark. No pattern inside the shield.
"""
import build_logo_variants as G

XF = f"translate({G.OFF:.2f} {G.OFF:.2f}) scale({G.SC:.4f})"


def mark(uid="", tile=True):
    """Full 512 tile. uid namespaces the defs so the SVG can be inlined next
    to other SVGs on a page without id collisions."""
    p = f"{uid}-" if uid else ""
    tile_bg = f'<rect width="512" height="512" rx="{G.RX:.1f}" fill="url(#{p}tg)"/>' if tile else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" role="img" aria-label="Shieldora logo"><defs><linearGradient id="{p}tg" x1="0.281" y1="-0.103" x2="0.719" y2="1.103">
    <stop offset="0" stop-color="{G.GREEN_HI}"/><stop offset="1" stop-color="{G.GREEN_LO}"/>
  </linearGradient>
  <linearGradient id="{p}sg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{G.SHIELD_HI}"/><stop offset="1" stop-color="{G.SHIELD_LO}"/>
  </linearGradient></defs>{tile_bg}
  <g transform="{XF}"><path d="{G.SHIELD_D}" fill="url(#{p}sg)"/></g>
  <g transform="{XF}" fill="none">
    <path d="{G.SHIELD_D}" stroke="{G.GOLD}" stroke-opacity="0.95" stroke-width="1.3"/>
    <path d="{G.CHECK_D}" stroke="#ffffff" stroke-width="2.1" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  </g></svg>'''


def favicon():
    """Same plain shield as the page mark, sized for a 64px tile."""
    sh = 64.0 * 26 / 46
    off, sc = (64.0 - sh) / 2, sh / 24
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"
     role="img" aria-label="Shieldora shield logo">
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
    <path d="{G.SHIELD_D}" stroke="{G.GOLD}" stroke-opacity="0.95" stroke-width="1.3"/>
    <path d="{G.CHECK_D}" stroke="#ffffff" stroke-width="2.1"
      stroke-linecap="round" stroke-linejoin="round"/>
  </g>
</svg>'''


def lockup_page(mark_px, bg, pad_x=0, pad_y=0, canvas=None):
    """The .logo lockup from index.html, reproduced for offscreen rendering.
    The SVG paints the tile itself now, so the span only carries the glow."""
    gap, fs, rad = mark_px * 14 / 46, mark_px * 26 / 46, mark_px * 13 / 46
    frame = (f"width:{canvas[0]}px;height:{canvas[1]}px;"
             if canvas else f"padding:{pad_y}px {pad_x}px;width:max-content;")
    return f'''<!doctype html><meta charset="utf-8"><style>
  html,body{{margin:0;background:{bg};}}
  .stage{{{frame}display:flex;align-items:center;justify-content:center;}}
  .logo{{display:flex;align-items:center;gap:{gap:.2f}px;}}
  .mark{{width:{mark_px}px;height:{mark_px}px;border-radius:{rad:.2f}px;
    box-shadow:0 {mark_px*6/46:.1f}px {mark_px*16/46:.1f}px rgba(43,112,64,.45);}}
  .mark svg{{width:100%;height:100%;display:block;}}
  .wordmark{{font:800 {fs:.2f}px -apple-system,BlinkMacSystemFont,"Segoe UI",
    Roboto,Helvetica,Arial,sans-serif;letter-spacing:-.03em;color:#f4f5f6;}}
</style><div class="stage"><div class="logo">
  <span class="mark">{mark("og")}</span>
  <span class="wordmark">Shieldora</span>
</div></div>'''


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    with open("logo-mark.svg", "w", encoding="utf-8") as fh:
        fh.write(mark() + "\n")
    with open("favicon.svg", "w", encoding="utf-8") as fh:
        fh.write(favicon() + "\n")
    with open(f"{out}/mark-inline.svg", "w", encoding="utf-8") as fh:
        fh.write(mark("bm"))
    with open(f"{out}/og.html", "w", encoding="utf-8") as fh:
        fh.write(lockup_page(210, "#000000", canvas=(1200, 630)))
    with open(f"{out}/lockup.html", "w", encoding="utf-8") as fh:
        fh.write(lockup_page(512, "transparent", pad_x=300, pad_y=260))
    print("wrote logo-mark.svg, favicon.svg, mark-inline.svg, og.html, lockup.html")
