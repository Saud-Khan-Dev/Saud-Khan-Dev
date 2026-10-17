#!/usr/bin/env python3
"""Generates the profile's SVG assets (light + dark) into ../assets.

Run:  python3 tools/generate_assets.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"

THEMES = {
    "dark": dict(
        bg="#0A0A0C", body="#111114", bar="#1A1A1E", stroke="#FFFFFF", stroke_op="0.09",
        text="#F5F5F7", text2="#A1A1A6", text3="#6E6E73", grid="#FFFFFF", grid_op="0.05",
        blue="#0A84FF", cyan="#64D2FF", mint="#66D4CF", aurora_op="0.42", node_fill="#0A0A0C",
    ),
    "light": dict(
        bg="#FBFBFD", body="#FFFFFF", bar="#F2F2F5", stroke="#000000", stroke_op="0.08",
        text="#1D1D1F", text2="#515154", text3="#86868B", grid="#000000", grid_op="0.05",
        blue="#0071E3", cyan="#0AA5D8", mint="#00A39A", aurora_op="0.28", node_fill="#FBFBFD",
    ),
}

SANS = "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
MONO = "'SF Mono', ui-monospace, Menlo, Monaco, Consolas, 'Liberation Mono', 'DejaVu Sans Mono', monospace"

REDUCED = "@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }"


# ----------------------------------------------------------------------------- hero
def hero(t):
    # Service-architecture motif: client -> gateway -> services -> data
    nodes = {
        "client": (800, 220), "gateway": (905, 220),
        "identity": (1015, 132), "orders": (1015, 220), "catalog": (1015, 308),
        "sql": (1118, 132), "events": (1118, 220), "cache": (1118, 308),
    }
    edges = [
        ("client", "gateway"),
        ("gateway", "identity"), ("gateway", "orders"), ("gateway", "catalog"),
        ("identity", "sql"), ("orders", "events"), ("catalog", "cache"),
    ]

    def path(a, b):
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        mx = (x1 + x2) / 2
        return f"M{x1} {y1} C{mx} {y1} {mx} {y2} {x2} {y2}"

    edge_svg, flow_svg = [], []
    for i, (a, b) in enumerate(edges):
        d = path(a, b)
        edge_svg.append(f'<path d="{d}" class="edge"/>')
        # Pulses start on the client edge, then fan out
        delay = 0 if i == 0 else (0.9 if i < 4 else 1.8)
        flow_svg.append(f'<path d="{d}" pathLength="100" class="flow" style="animation-delay:{delay + (i % 3) * 0.15:.2f}s"/>')

    node_svg = []
    for name, (x, y) in nodes.items():
        r = 7 if name == "gateway" else 5
        cls = "node gw" if name == "gateway" else "node"
        node_svg.append(f'<circle cx="{x}" cy="{y}" r="{r}" class="{cls}"/>')
        node_svg.append(f'<text x="{x}" y="{y + 26}" class="label">{name}</text>')

    TERM_W = len("saud@arch ~ ❯ architect · build · refine") * 10.2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 440" width="1200" height="440" role="img" aria-labelledby="title desc">
  <title id="title">Saud Khan — Software Engineer · Software Architect</title>
  <desc id="desc">Scalable systems. Clean architecture. Considered details. An animated diagram shows requests flowing from a client through an API gateway to services and data stores.</desc>
  <defs>
    <clipPath id="card"><rect width="1200" height="440" rx="28"/></clipPath>
    <filter id="blur" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="72"/></filter>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0H0V40" fill="none" stroke="{t['grid']}" stroke-opacity="{t['grid_op']}" stroke-width="1"/>
    </pattern>
    <radialGradient id="fade" cx="80%" cy="50%" r="62%">
      <stop offset="0" stop-color="#fff" stop-opacity="1"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </radialGradient>
    <mask id="gridmask"><rect width="1200" height="440" fill="url(#fade)"/></mask>
    <linearGradient id="eyebrow" x1="0" x2="1">
      <stop offset="0" stop-color="{t['blue']}"/>
      <stop offset="0.6" stop-color="{t['cyan']}"/>
      <stop offset="1" stop-color="{t['mint']}"/>
    </linearGradient>
  </defs>
  <style>
    .eyebrow {{ font: 600 17px {MONO}; letter-spacing: 3px; }}
    .name    {{ font: 700 104px {SANS}; letter-spacing: -4px; fill: {t['text']}; }}
    .tag     {{ font: 400 31px {SANS}; letter-spacing: -0.5px; fill: {t['text2']}; }}
    .term    {{ font: 500 17px {MONO}; fill: {t['text3']}; }}
    .term .cmd {{ fill: {t['text2']}; }}
    .term .ok  {{ fill: {t['mint']}; }}
    .label   {{ font: 500 13px {MONO}; fill: {t['text3']}; text-anchor: middle; }}
    .edge    {{ fill: none; stroke: {t['text3']}; stroke-opacity: 0.45; stroke-width: 1.2; }}
    .flow    {{ fill: none; stroke: {t['cyan']}; stroke-width: 2.4; stroke-linecap: round;
               stroke-dasharray: 7 93; stroke-dashoffset: 100; opacity: 0;
               animation: flow 3.6s cubic-bezier(.45,0,.25,1) infinite; }}
    .node    {{ fill: {t['node_fill']}; stroke: {t['cyan']}; stroke-width: 1.6; }}
    .node.gw {{ stroke: {t['blue']}; stroke-width: 2; animation: pulse 3.6s ease-in-out infinite; }}
    .a1 {{ animation: drift1 18s ease-in-out infinite alternate; }}
    .a2 {{ animation: drift2 22s ease-in-out infinite alternate; }}
    .a3 {{ animation: drift3 26s ease-in-out infinite alternate; }}
    .cursor {{ fill: {t['cyan']}; animation: blink 1.1s steps(1) infinite; }}
    @keyframes flow  {{ 0% {{ stroke-dashoffset: 100; opacity: 0; }} 8% {{ opacity: 1; }} 55% {{ stroke-dashoffset: 0; opacity: 1; }} 62%, 100% {{ stroke-dashoffset: 0; opacity: 0; }} }}
    @keyframes pulse {{ 0%, 100% {{ stroke-opacity: 1; }} 50% {{ stroke-opacity: 0.45; }} }}
    @keyframes drift1 {{ to {{ transform: translate(-90px, 40px); }} }}
    @keyframes drift2 {{ to {{ transform: translate(-60px, -50px); }} }}
    @keyframes drift3 {{ to {{ transform: translate(80px, -30px); }} }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    {REDUCED}
  </style>
  <g clip-path="url(#card)">
    <rect width="1200" height="440" fill="{t['bg']}"/>
    <g filter="url(#blur)" opacity="{t['aurora_op']}">
      <circle class="a1" cx="900" cy="110" r="165" fill="{t['blue']}"/>
      <circle class="a2" cx="1080" cy="340" r="150" fill="{t['cyan']}"/>
      <circle class="a3" cx="700" cy="380" r="120" fill="{t['mint']}"/>
    </g>
    <rect width="1200" height="440" fill="url(#grid)" mask="url(#gridmask)"/>

    <g>
      {chr(10).join("      " + e for e in edge_svg).strip()}
      {chr(10).join("      " + f for f in flow_svg).strip()}
      {chr(10).join("      " + n for n in node_svg).strip()}
    </g>

    <text x="80" y="140" class="eyebrow" fill="url(#eyebrow)">SOFTWARE ENGINEER · SOFTWARE ARCHITECT</text>
    <text x="73" y="240" class="name">Saud Khan</text>
    <text x="80" y="296" class="tag">Scalable systems. Clean architecture.</text>
    <text x="80" y="337" class="tag">Considered details.</text>
    <text x="80" y="396" class="term" textLength="{TERM_W:.1f}" lengthAdjust="spacingAndGlyphs"><tspan class="ok">saud@arch</tspan> ~ ❯ <tspan class="cmd">architect · build · refine</tspan></text>
    <rect x="{80 + TERM_W + 6:.1f}" y="382" width="10" height="19" rx="1.5" class="cursor"/>
  </g>
  <rect x="0.5" y="0.5" width="1199" height="439" rx="27.5" fill="none" stroke="{t['stroke']}" stroke-opacity="{t['stroke_op']}"/>
</svg>
'''


# ----------------------------------------------------------------------------- terminal typing
LINES = [
    "building scalable .NET applications",
    "exploring distributed systems & microservices",
    "designing clean software architectures",
    "exploring Rust, AI and machine learning",
    "crafting thoughtful frontend experiences",
    "working with Linux and open-source tools",
]


def terminal(t):
    W, H = 760, 132
    fs, cw = 17, 10.2                     # font size and fixed glyph advance (textLength keeps it exact)
    prompt = "saud@arch ~ ❯ "
    px, base = 28, 92
    tx = px + len(prompt) * cw            # where typed text starts
    slot, T = 4.0, 4.0 * len(LINES)

    def pct(s):
        return f"{min(max(s / T * 100, 0), 100):.3f}%"

    css, groups = [], []
    for i, line in enumerate(LINES):
        n = len(line)
        w = n * cw
        s = i * slot
        typing = min(1.9, n * 0.045)
        erase = 0.45
        hold = slot - typing - erase - 0.25
        css.append(
            f"@keyframes show{i} {{ 0% {{ opacity: {1 if i == 0 else 0}; }} "
            + (f"{pct(s)} {{ opacity: 1; }} " if i else "")
            + f"{pct(s + slot - 0.12)} {{ opacity: 0; }} 100% {{ opacity: 0; }} }}"
        )
        css.append(
            f"@keyframes type{i} {{ 0% {{ transform: translateX(0); }} "
            f"{pct(s)} {{ transform: translateX(0); animation-timing-function: steps({n}, end); }} "
            f"{pct(s + typing)} {{ transform: translateX({w:.1f}px); }} "
            f"{pct(s + typing + hold)} {{ transform: translateX({w:.1f}px); animation-timing-function: steps({n}, end); }} "
            f"{pct(s + typing + hold + erase)} {{ transform: translateX(0); }} 100% {{ transform: translateX(0); }} }}"
        )
        css.append(f".l{i} {{ animation: show{i} {T}s step-end infinite; }}")
        css.append(f".l{i} .rev {{ animation: type{i} {T}s linear infinite; }}")
        groups.append(f'''    <g class="line l{i}">
      <text x="{tx:.1f}" y="{base}" class="typed" textLength="{w:.1f}" lengthAdjust="spacingAndGlyphs">{escape(line)}</text>
      <g class="rev">
        <rect x="{tx:.1f}" y="{base - 20}" width="{W}" height="28" fill="{t['body']}"/>
        <rect x="{tx + 1:.1f}" y="{base - 15}" width="9" height="18" rx="1.5" class="cursor"/>
      </g>
    </g>''')

    w0 = len(LINES[0]) * cw
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="title desc">
  <title id="title">What I'm working on</title>
  <desc id="desc">A terminal that types: {escape("; ".join(LINES))}.</desc>
  <defs>
    <clipPath id="win"><rect x="0" y="0" width="{W}" height="{H}" rx="16"/></clipPath>
    <clipPath id="screen"><rect x="1" y="38" width="{W - 2}" height="{H - 39}"/></clipPath>
  </defs>
  <style>
    .typed, .prompt {{ font: 500 {fs}px {MONO}; }}
    .typed {{ fill: {t['text']}; }}
    .p-user {{ fill: {t['mint']}; }} .p-path {{ fill: {t['blue']}; }} .p-sym {{ fill: {t['text2']}; }}
    .title {{ font: 500 12px {MONO}; fill: {t['text3']}; text-anchor: middle; }}
    .cursor {{ fill: {t['cyan']}; animation: blink 1.1s steps(1) infinite; }}
    .line {{ opacity: 0; }}
    .l0 {{ opacity: 1; }}
    .l0 .rev {{ transform: translateX({w0:.1f}px); }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    {chr(10).join("    " + c for c in css).strip()}
    @media (prefers-reduced-motion: reduce) {{
      * {{ animation: none !important; }}
      .l0 {{ opacity: 1; }} .l0 .rev {{ transform: translateX({w0:.1f}px); }}
    }}
  </style>
  <g clip-path="url(#win)">
    <rect width="{W}" height="{H}" fill="{t['body']}"/>
    <rect width="{W}" height="38" fill="{t['bar']}"/>
    <rect y="37.5" width="{W}" height="1" fill="{t['stroke']}" fill-opacity="{t['stroke_op']}"/>
    <circle cx="22" cy="19" r="6" fill="#FF5F57"/>
    <circle cx="42" cy="19" r="6" fill="#FEBC2E"/>
    <circle cx="62" cy="19" r="6" fill="#28C840"/>
    <text x="{W / 2}" y="23" class="title">saud@arch — zsh</text>
    <text x="{px}" y="{base}" class="prompt" textLength="{len(prompt) * cw - cw:.1f}" lengthAdjust="spacingAndGlyphs"><tspan class="p-user">saud@arch</tspan><tspan class="p-path"> ~</tspan><tspan class="p-sym"> ❯</tspan></text>
    <g clip-path="url(#screen)">
{chr(10).join(groups)}
    </g>
  </g>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="15.5" fill="none" stroke="{t['stroke']}" stroke-opacity="{t['stroke_op']}"/>
</svg>
'''


# ----------------------------------------------------------------------------- divider
def divider(t):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 24" width="1200" height="24" role="presentation" aria-hidden="true">
  <defs>
    <linearGradient id="hair" x1="0" x2="1">
      <stop offset="0" stop-color="{t['text3']}" stop-opacity="0"/>
      <stop offset="0.5" stop-color="{t['text3']}" stop-opacity="0.55"/>
      <stop offset="1" stop-color="{t['text3']}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="shine" x1="0" x2="1">
      <stop offset="0" stop-color="{t['cyan']}" stop-opacity="0"/>
      <stop offset="0.5" stop-color="{t['cyan']}" stop-opacity="0.9"/>
      <stop offset="1" stop-color="{t['cyan']}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <style>
    .shine {{ animation: sweep 7s cubic-bezier(.45,0,.25,1) infinite; }}
    @keyframes sweep {{ 0% {{ transform: translateX(-260px); }} 60%, 100% {{ transform: translateX(1200px); }} }}
    {REDUCED}
    @media (prefers-reduced-motion: reduce) {{ .shine {{ display: none; }} }}
  </style>
  <rect x="0" y="11.5" width="1200" height="1" fill="url(#hair)"/>
  <rect class="shine" x="0" y="11" width="240" height="2" rx="1" fill="url(#shine)"/>
</svg>
'''


# ----------------------------------------------------------------------------- footer
def footer(t):
    CMD_W = len('saud@arch ~ ❯ git commit -m "thanks for stopping by"') * 9.0
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120" width="1200" height="120" role="img" aria-labelledby="title">
  <title id="title">Designed and engineered by Saud Khan</title>
  <style>
    .cmd  {{ font: 500 15px {MONO}; fill: {t['text3']}; text-anchor: middle; }}
    .cmd .u {{ fill: {t['mint']}; }} .cmd .c {{ fill: {t['text2']}; }}
    .sig  {{ font: 500 15px {SANS}; letter-spacing: 0.2px; fill: {t['text3']}; text-anchor: middle; }}
    .cursor {{ fill: {t['cyan']}; animation: blink 1.1s steps(1) infinite; }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    {REDUCED}
  </style>
  <text x="{600 - 8:.1f}" y="48" class="cmd" textLength="{CMD_W:.1f}" lengthAdjust="spacingAndGlyphs"><tspan class="u">saud@arch</tspan> ~ ❯ <tspan class="c">git commit -m "thanks for stopping by"</tspan></text>
  <rect x="{600 - 8 + CMD_W / 2 + 6:.1f}" y="35" width="9" height="17" rx="1.5" class="cursor"/>
  <text x="600" y="88" class="sig">Designed &amp; engineered by Saud Khan</text>
</svg>
'''


def main():
    OUT.mkdir(exist_ok=True)
    for theme, t in THEMES.items():
        for name, fn in [("hero", hero), ("terminal", terminal), ("divider", divider), ("footer", footer)]:
            path = OUT / f"{name}-{theme}.svg"
            path.write_text(fn(t))
            print("wrote", path.relative_to(OUT.parent))


if __name__ == "__main__":
    main()
