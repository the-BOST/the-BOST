#!/usr/bin/env python3
"""Generate assets/cyber-terminal.svg: a rounded neon terminal with assets/banner.webp as animated background."""
import base64
from pathlib import Path

W, H = 840, 280
ROOT = Path(__file__).resolve().parent.parent
BG = ROOT / "assets" / "banner.webp"
OUT = ROOT / "assets" / "cyber-terminal.svg"

# GitHub blocks external resources inside SVGs, so the background is inlined.
bg_uri = "data:image/webp;base64," + base64.b64encode(BG.read_bytes()).decode()

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <linearGradient id="neon" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ff2a6d"/>
      <stop offset="50%" stop-color="#7b2ff7"/>
      <stop offset="100%" stop-color="#00f7ff"/>
    </linearGradient>
    <clipPath id="screen"><rect x="2" y="36" width="{W - 4}" height="{H - 38}" rx="14"/></clipPath>
    <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="2" fill="#000" opacity="0.25"/>
    </pattern>
  </defs>
  <style>
    text {{ font-family: 'Fira Code', 'JetBrains Mono', Consolas, monospace; }}
    .title {{ font-size: 64px; font-weight: 700; letter-spacing: 4px; }}
    .g1 {{ animation: g1 2.8s infinite steps(1); }}
    .g2 {{ animation: g2 2.8s infinite steps(1); }}
    @keyframes g1 {{ 0%,88%,100% {{ transform: translate(0,0); }} 90% {{ transform: translate(-5px,2px); }} 94% {{ transform: translate(4px,-2px); }} }}
    @keyframes g2 {{ 0%,88%,100% {{ transform: translate(0,0); }} 90% {{ transform: translate(5px,-2px); }} 94% {{ transform: translate(-4px,2px); }} }}
    .sub {{ font-size: 18px; fill: #d1f7ff; }}
    .cur {{ animation: blink 1s infinite steps(1); }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    .flick {{ animation: flick 4s infinite; }}
    @keyframes flick {{ 0%,100% {{ opacity: 1; }} 47% {{ opacity: 1; }} 48% {{ opacity: .4; }} 49% {{ opacity: 1; }} }}
  </style>

  <rect x="2" y="2" width="{W - 4}" height="{H - 4}" rx="16" fill="#0d0221" stroke="url(#neon)" stroke-width="3"/>
  <rect x="2" y="2" width="{W - 4}" height="34" rx="16" fill="#1a0b3a"/>
  <rect x="2" y="20" width="{W - 4}" height="16" fill="#1a0b3a"/>
  <circle cx="26" cy="19" r="6" fill="#ff2a6d"/>
  <circle cx="46" cy="19" r="6" fill="#f9c80e"/>
  <circle cx="66" cy="19" r="6" fill="#00f7ff"/>
  <text x="{W / 2}" y="24" text-anchor="middle" font-size="13" fill="#d1f7ff" opacity=".7">root@the-BOST: ~/</text>

  <g clip-path="url(#screen)">
    <image x="2" y="36" width="{W - 4}" height="{H - 38}" preserveAspectRatio="xMidYMid slice" href="{bg_uri}" xlink:href="{bg_uri}"/>
    <rect x="2" y="36" width="{W - 4}" height="{H - 38}" fill="#0d0221" opacity=".35"/>
    <rect x="2" y="36" width="{W - 4}" height="{H - 38}" fill="url(#scan)"/>
  </g>

  <g class="flick" text-anchor="middle">
    <text class="title g1" x="{W / 2}" y="160" fill="#ff2a6d" opacity=".8">the-BOST</text>
    <text class="title g2" x="{W / 2}" y="160" fill="#00f7ff" opacity=".8">the-BOST</text>
    <text class="title" x="{W / 2}" y="160" fill="#ffffff">the-BOST</text>
    <text class="sub" x="{W / 2}" y="210">&gt; ACCESS GRANTED<tspan class="cur" fill="#00f7ff">_</tspan></text>
  </g>
</svg>
"""

OUT.write_text(svg, encoding="utf-8")
print(f"wrote {OUT}")
