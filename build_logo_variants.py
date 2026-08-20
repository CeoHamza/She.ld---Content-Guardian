"""Generate sh*eld logo variations: girih star pattern clipped to the shield.

The 8-pointed star is the classic khatam -- the union of two squares, one
rotated 45 degrees. Outer points sit at k*45 deg on radius R; the inner
vertices fall where the squares' edges cross, at 22.5+k*45 deg on radius
R*sqrt((1-1/sqrt2)^2 + 1/2). With R = s/2 the stars in adjacent cells meet
point-to-point and the negative space between four of them forms the cross,
giving the standard star-and-cross tessellation.
"""
import math

TILE = 512.0
RX = TILE * 13 / 46.0                      # tile corner radius, from .logo CSS
S = TILE * 26 / 46.0                       # shield box, from .logo .mark svg
OFF = (TILE - S) / 2.0
SC = S / 24.0                              # 24-unit viewBox -> tile units

SHIELD_D = ("M12 2.2 3.8 5.4v6c0 4.6 3.2 7.9 8.2 9.4 5-1.5 8.2-4.8 8.2-9.4"
            "v-6L12 2.2Z")
CHECK_D = "M8.2 12.1 10.8 14.7 15.8 9.5"

R_INNER = math.sqrt((1 - 1 / math.sqrt(2)) ** 2 + 0.5)   # 0.76537

GOLD = "#dcb978"
GREEN_HI, GREEN_LO = "#4aa863", "#256437"   # tile gradient, unchanged
SHIELD_HI, SHIELD_LO = "#2a7346", "#17502c"  # deeper green behind the pattern


def star(cx, cy, R):
    pts = []
    for k in range(8):
        a = math.radians(k * 45)
        pts.append((cx + R * math.cos(a), cy + R * math.sin(a)))
        b = math.radians(k * 45 + 22.5)
        pts.append((cx + R * R_INNER * math.cos(b), cy + R * R_INNER * math.sin(b)))
    return pts


def poly(pts):
    return " ".join(f"{x:.2f},{y:.2f}" for x, y in pts)


def ngon(cx, cy, r, n=8, phase=0.0):
    return [(cx + r * math.cos(math.radians(phase + i * 360 / n)),
             cy + r * math.sin(math.radians(phase + i * 360 / n))) for i in range(n)]


def pattern(pid, s, sw, inner_octagon, cx=256.0, cy=250.0):
    """One seamless s-by-s girih tile: stars at the corners, cross at centre.

    cx/cy is the point a star is centred on, so the lattice comes out
    mirror-symmetric about the shield's vertical axis.
    """
    R = s / 2.0
    o = []
    for (cx, cy) in [(0, 0), (s, 0), (0, s), (s, s)]:
        o.append(f'<polygon points="{poly(star(cx, cy, R))}"/>')
        if inner_octagon:
            o.append(f'<polygon points="{poly(ngon(cx, cy, R * R_INNER * 0.52, 8, 22.5))}"/>')
    # centre diamond of the cross, plus the four struts that lock it to the
    # inner vertices of the diagonal stars
    d = s * 0.135
    o.append(f'<polygon points="{poly(ngon(s/2, s/2, d, 4, 45))}"/>')
    for ang in (45, 135, 225, 315):
        a = math.radians(ang)
        x1, y1 = s / 2 + d * math.cos(a), s / 2 + d * math.sin(a)
        sx, sy = (s / 2 + math.cos(a) * s / 2, s / 2 + math.sin(a) * s / 2)
        ix = sx - math.cos(a) * R * R_INNER
        iy = sy - math.sin(a) * R * R_INNER
        o.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{ix:.2f}" y2="{iy:.2f}"/>')
    body = "\n        ".join(o)
    return f'''<pattern id="{pid}" patternUnits="userSpaceOnUse"
        x="{cx % s:.4f}" y="{cy % s:.4f}" width="{s:.4f}" height="{s:.4f}">
      <g fill="none" stroke="{GOLD}" stroke-width="{sw:.4f}" stroke-linejoin="miter">
        {body}
      </g>
    </pattern>'''


def svg(key, s, sw, opacity, inner_octagon, tile=True):
    p = f"pat-{key}"
    tile_bg = (f'<rect width="{TILE}" height="{TILE}" rx="{RX:.1f}" fill="url(#tg-{key})"/>'
               if tile else "")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {TILE:.0f} {TILE:.0f}"
     role="img" aria-label="Shieldora shield logo">
  <defs>
    <linearGradient id="tg-{key}" x1="0.281" y1="-0.103" x2="0.719" y2="1.103">
      <stop offset="0" stop-color="{GREEN_HI}"/><stop offset="1" stop-color="{GREEN_LO}"/>
    </linearGradient>
    <linearGradient id="sg-{key}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{SHIELD_HI}"/><stop offset="1" stop-color="{SHIELD_LO}"/>
    </linearGradient>
    {pattern(p, s, sw, inner_octagon)}
    <clipPath id="clip-{key}">
      <path d="{SHIELD_D}" transform="translate({OFF:.2f} {OFF:.2f}) scale({SC:.4f})"/>
    </clipPath>
    <!-- knock a clean gap in the pattern around the check, so no gold line
         runs under it; far cleaner than a dark halo behind the stroke -->
    <mask id="knock-{key}">
      <rect width="{TILE}" height="{TILE}" fill="#fff"/>
      <path d="{CHECK_D}" transform="translate({OFF:.2f} {OFF:.2f}) scale({SC:.4f})"
            fill="none" stroke="#000" stroke-width="3.5"
            stroke-linecap="round" stroke-linejoin="round"/>
    </mask>
  </defs>
  {tile_bg}
  <g transform="translate({OFF:.2f} {OFF:.2f}) scale({SC:.4f})">
    <path d="{SHIELD_D}" fill="url(#sg-{key})"/>
  </g>
  <g clip-path="url(#clip-{key})" mask="url(#knock-{key})" opacity="{opacity}">
    <rect width="{TILE}" height="{TILE}" fill="url(#{p})"/>
  </g>
  <g transform="translate({OFF:.2f} {OFF:.2f}) scale({SC:.4f})" fill="none">
    <path d="{SHIELD_D}" stroke="#ffffff" stroke-opacity="0.5" stroke-width="1.1"/>
    <path d="{CHECK_D}" stroke="#ffffff" stroke-width="2.1"
          stroke-linecap="round" stroke-linejoin="round"/>
  </g>
</svg>'''


VARIANTS = [
    ("a", dict(s=40.0, sw=1.6, opacity=0.55, inner_octagon=True),
     "Fine", "Dense lattice, hairline gold. Most detail, softest contrast."),
    ("b", dict(s=58.0, sw=2.3, opacity=0.70, inner_octagon=True),
     "Balanced", "Mid-scale stars, clearly readable strapwork."),
    ("c", dict(s=76.0, sw=3.2, opacity=0.88, inner_octagon=True),
     "Bold", "Large stars, strongest gold. Survives small sizes best."),
]

if __name__ == "__main__":
    cards = []
    for key, kw, name, blurb in VARIANTS:
        markup = svg(key, **kw)
        with open(f"logo-girih-{key}.svg", "w", encoding="utf-8") as fh:
            fh.write(markup + "\n")
        sizes = "".join(
            f'<div class="sz"><div style="width:{px}px">{markup}</div>'
            f'<span>{px}px</span></div>' for px in (72, 44, 28))
        cards.append(f'''<section class="card">
  <h2>{name} <em>({key.upper()})</em></h2>
  <p>{blurb}</p>
  <div class="big">{markup}</div>
  <div class="row">{sizes}</div>
  <div class="light"><div class="lw">{markup}</div><span>on light</span></div>
</section>''')

    html = f'''<!doctype html>
<meta charset="utf-8">
<title>Shieldora logo variations</title>
<style>
  body {{ margin:0; padding:40px; background:#0c0d0f; color:#f4f5f6;
         font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; }}
  h1 {{ font-size:24px; margin:0 0 6px; letter-spacing:-.02em; }}
  .hint {{ color:#9aa1aa; margin:0 0 32px; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(300px,1fr)); gap:28px; }}
  .card {{ background:#131417; border:1px solid #23262b; border-radius:16px; padding:22px; }}
  .card h2 {{ font-size:18px; margin:0 0 4px; }}
  .card h2 em {{ color:#4fbf6c; font-style:normal; }}
  .card p {{ color:#9aa1aa; font-size:14px; margin:0 0 18px; min-height:40px; }}
  .big {{ width:100%; max-width:300px; margin:0 auto 20px; }}
  .big svg, .sz svg, .lw svg {{ display:block; width:100%; height:auto; }}
  .row {{ display:flex; align-items:flex-end; gap:20px; justify-content:center;
          padding:16px 0; border-top:1px solid #23262b; }}
  .sz {{ text-align:center; }}
  .sz span {{ display:block; margin-top:8px; font-size:11px; color:#9aa1aa; }}
  .light {{ margin-top:8px; background:#f4f5f6; border-radius:10px; padding:16px;
            display:flex; align-items:center; gap:14px; }}
  .light .lw {{ width:64px; flex:none; }}
  .light span {{ font-size:12px; color:#5a6068; }}
</style>
<h1>sh&bull;eld &mdash; girih pattern variations</h1>
<p class="hint">Same shield and checkmark throughout; only pattern scale, line
weight and gold opacity differ. Check the small sizes &mdash; that is where
density decides it.</p>
<div class="grid">
{"".join(cards)}
</div>
'''
    with open("logo-preview.html", "w", encoding="utf-8") as fh:
        fh.write(html)
    print("wrote logo-girih-{a,b,c}.svg + logo-preview.html")
