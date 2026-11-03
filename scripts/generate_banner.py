#!/usr/bin/env python3
"""
generate_banner.py
------------------
Builds an animated, self-contained SVG hero banner for a GitHub profile README.

* Your cutout photo is embedded as base64, so GitHub shows it with no extra hosting.
* The photo drops in from the top, bounces once, then settles. The scene loops.
* Headline, terminal card, and typed tagline reveal in sequence.
* Only CSS animations are used, which GitHub renders for SVGs in <img> tags.

Usage
    python scripts/generate_banner.py
    python scripts/generate_banner.py --static   # no animation, for a quick preview
"""

from __future__ import annotations

import argparse
import base64
import random
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# --------------------------------------------------------------------------
# Profile content: edit this block, then re-run the script
# --------------------------------------------------------------------------


@dataclass
class Profile:
    handle: str = "rashid-ahmad199"
    roles: str = "CS Student  \u2022  Prompt Engineer  \u2022  Loop Engineer"
    headline: tuple[str, str, str] = ("Building.", "Learning.", "Growing.")
    title: str = "Aspiring AI Engineer"
    typed: str = "Code  \u2022  Solve  \u2022  Innovate"
    chips: tuple[str, ...] = (
        "Python",
        "Prompt Engineering",
        "Loop Engineering",
        "Web Coding",
    )
    location: str = "Peshawar, Pakistan"
    status: str = "Available for Collaboration"
    tagline: str = "Dream Big. Code Better."
    terminal: tuple[str, ...] = field(
        default_factory=lambda: (
            "class Rashid:",
            '    role  = "Aspiring AI Engineer"',
            '    stack = ["Python", "Prompts", "Web"]',
            "    learning = True",
        )
    )


# --------------------------------------------------------------------------
# Design tokens
# --------------------------------------------------------------------------

W, H = 1280, 640
CYCLE = 14  # seconds per loop

BG = "#04120f"
BG2 = "#082a22"
GREEN = "#2ee59d"
LIME = "#b6f36a"
TEXT = "#f2fbf7"
MUTED = "#8fb5a8"
FONT = "'Segoe UI', 'Inter', 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', 'Fira Code', Consolas, 'Courier New', monospace"


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def reveal(name: str, start: float, ramp: float = 5, rise: int = 28) -> str:
    """Keyframes that fade/slide an element in at `start` percent of the loop."""
    return (
        f"@keyframes {name}{{0%,{start}%{{opacity:0;transform:translateY({rise}px)}}"
        f"{start + ramp}%{{opacity:1;transform:translateY(0)}}100%{{opacity:1;transform:translateY(0)}}}}"
    )


def build_css(static: bool) -> str:
    if static:
        return ""
    k = []
    # Whole scene fades out at the end so the loop restarts cleanly.
    k.append(
        "@keyframes scene{0%{opacity:0}2%{opacity:1}93%{opacity:1}98%,100%{opacity:0}}"
    )
    # Photo: fall from above, land, bounce twice, settle.
    k.append(
        "@keyframes drop{"
        "0%{transform:translateY(-760px);opacity:0;animation-timing-function:cubic-bezier(.55,0,.9,.55)}"
        "3%{opacity:1}"
        "13%{transform:translateY(0);animation-timing-function:cubic-bezier(.2,.7,.4,1)}"
        "16.5%{transform:translateY(-30px);animation-timing-function:cubic-bezier(.55,0,.9,.55)}"
        "20%{transform:translateY(0);animation-timing-function:cubic-bezier(.2,.7,.4,1)}"
        "22%{transform:translateY(-9px);animation-timing-function:cubic-bezier(.55,0,.9,.55)}"
        "24%,100%{transform:translateY(0);opacity:1}}"
    )
    # Glow flash when the photo lands.
    k.append(
        "@keyframes impact{0%,12%{opacity:0;transform:scale(.6)}16%{opacity:.9;transform:scale(1.15)}"
        "30%{opacity:.35;transform:scale(1)}100%{opacity:.35;transform:scale(1)}}"
    )
    k.append("@keyframes pulse{0%,100%{opacity:.28}50%{opacity:.5}}")
    k.append("@keyframes spin{to{transform:rotate(360deg)}}")
    k.append("@keyframes spinr{to{transform:rotate(-360deg)}}")
    k.append("@keyframes gridmove{to{transform:translateY(48px)}}")
    k.append(
        "@keyframes float{0%,100%{transform:translateY(0);opacity:.15}50%{transform:translateY(-26px);opacity:.75}}"
    )
    k.append("@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}")
    k.append("@keyframes dot{0%,100%{opacity:1}50%{opacity:.25}}")
    k.append(
        "@keyframes sweep{0%,26%{transform:translateX(-120px);opacity:0}30%{opacity:.8}"
        "46%{transform:translateX(1400px);opacity:0}100%{transform:translateX(1400px);opacity:0}}"
    )
    k.append(
        "@keyframes type{0%,32%{transform:scaleX(0)}46%,100%{transform:scaleX(1)}}"
    )
    for name, start in [("r1", 6), ("r2", 9), ("r3", 12), ("r4", 17), ("r5", 22), ("r6", 50), ("r7", 54)]:
        k.append(reveal(name, start))
    for i in range(6):
        k.append(reveal(f"line{i}", 24 + i * 3.2, ramp=3, rise=0))

    rules = f"""
.scene{{animation:scene {CYCLE}s linear infinite}}
.photo{{animation:drop {CYCLE}s infinite}}
.impact{{transform-box:fill-box;transform-origin:center;animation:impact {CYCLE}s ease-out infinite}}
.halo{{animation:pulse 4s ease-in-out infinite}}
.ring1{{transform-box:fill-box;transform-origin:center;animation:spin 40s linear infinite}}
.ring2{{transform-box:fill-box;transform-origin:center;animation:spinr 60s linear infinite}}
.grid{{animation:gridmove 6s linear infinite}}
.beam{{animation:sweep {CYCLE}s ease-in-out infinite}}
.typebox{{transform-box:fill-box;transform-origin:left center;animation:type {CYCLE}s steps(24,end) infinite}}
.cursor{{animation:blink .9s steps(1) infinite}}
.dot{{animation:dot 1.6s ease-in-out infinite}}
.r1{{animation:r1 {CYCLE}s infinite}} .r2{{animation:r2 {CYCLE}s infinite}}
.r3{{animation:r3 {CYCLE}s infinite}} .r4{{animation:r4 {CYCLE}s infinite}}
.r5{{animation:r5 {CYCLE}s infinite}} .r6{{animation:r6 {CYCLE}s infinite}}
.r7{{animation:r7 {CYCLE}s infinite}}
.l0{{animation:line0 {CYCLE}s infinite}} .l1{{animation:line1 {CYCLE}s infinite}}
.l2{{animation:line2 {CYCLE}s infinite}} .l3{{animation:line3 {CYCLE}s infinite}}
.l4{{animation:line4 {CYCLE}s infinite}} .l5{{animation:line5 {CYCLE}s infinite}}
.p{{animation:float 7s ease-in-out infinite}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
"""
    return "\n".join(k) + rules


def highlight_python(line: str) -> str:
    """Tiny syntax highlighter for the terminal card (returns tspans)."""
    import re

    out, pos = [], 0
    token = re.compile(r'("[^"]*")|\b(class|def|return|True|False|None)\b|(\b\d+\b)')
    for m in token.finditer(line):
        out.append(f'<tspan fill="{TEXT}">{esc(line[pos:m.start()])}</tspan>')
        if m.group(1):
            out.append(f'<tspan fill="{LIME}">{esc(m.group(1))}</tspan>')
        elif m.group(2):
            out.append(f'<tspan fill="#7cc7ff">{esc(m.group(2))}</tspan>')
        else:
            out.append(f'<tspan fill="#ffb86b">{esc(m.group(3))}</tspan>')
        pos = m.end()
    out.append(f'<tspan fill="{TEXT}">{esc(line[pos:])}</tspan>')
    return "".join(out)


def build_svg(p: Profile, photo_path: Path, static: bool) -> str:
    photo_b64 = base64.b64encode(photo_path.read_bytes()).decode()
    mime = "image/webp" if photo_path.suffix.lower() == ".webp" else "image/png"

    # --- photo geometry (cutout is 550 x 1000) ---
    ph = 610
    pw = round(ph * 0.55)
    cx, cy = 1005, 330
    px, py = cx - pw // 2, 40

    # --- ambient particles ---
    rnd = random.Random(199)
    particles = []
    for _ in range(30):
        x, y = rnd.randint(30, W - 30), rnd.randint(30, H - 30)
        r = rnd.choice([1.4, 1.8, 2.4, 3])
        d = rnd.uniform(5, 10)
        delay = -rnd.uniform(0, 8)
        particles.append(
            f'<circle class="p" cx="{x}" cy="{y}" r="{r}" fill="{GREEN}" '
            f'style="animation-duration:{d:.1f}s;animation-delay:{delay:.1f}s"/>'
        )

    # --- chips ---
    chips, x = [], 60
    for label in p.chips:
        w = round(len(label) * 8.6 + 38)
        chips.append(
            f'<g><rect x="{x}" y="528" width="{w}" height="38" rx="19" fill="{GREEN}" fill-opacity=".08" '
            f'stroke="{GREEN}" stroke-opacity=".55"/>'
            f'<text x="{x + w / 2}" y="552" text-anchor="middle" font-family="{FONT}" font-size="15" '
            f'font-weight="600" fill="{TEXT}">{esc(label)}</text></g>'
        )
        x += w + 12

    # --- terminal card ---
    tx, ty, tw, th = 474, 300, 364, 176
    term_lines = []
    for i, line in enumerate(p.terminal):
        term_lines.append(
            f'<text class="l{i}" x="{tx + 20}" y="{ty + 62 + i * 26}" font-family="{MONO}" font-size="13.5" '
            f'xml:space="preserve">{highlight_python(line)}</text>'
        )

    def cls(name: str) -> str:
        return "" if static else f' class="{name}"'

    h1, h2, h3 = p.headline
    typed_w = round(len(p.typed) * 13.4)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{esc(p.handle)}: {esc(p.title)}">
<title>{esc(p.handle)} \u2013 {esc(p.title)}</title>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG}"/><stop offset=".55" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient>
  <linearGradient id="gtext" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{GREEN}"/><stop offset="1" stop-color="{LIME}"/></linearGradient>
  <radialGradient id="halo" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{GREEN}" stop-opacity=".55"/><stop offset=".6" stop-color="{GREEN}" stop-opacity=".12"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></radialGradient>
  <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG}" stop-opacity="0"/><stop offset="1" stop-color="{BG}" stop-opacity=".95"/></linearGradient>
  <linearGradient id="beam" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{GREEN}" stop-opacity="0"/><stop offset=".5" stop-color="{GREEN}" stop-opacity=".35"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></linearGradient>
  <pattern id="grid" width="48" height="48" patternUnits="userSpaceOnUse"><path d="M48 0H0V48" fill="none" stroke="{GREEN}" stroke-opacity=".07"/></pattern>
  <filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="26"/></clipPath>
  <clipPath id="typeclip"><rect{cls("typebox")} x="60" y="480" width="{typed_w}" height="48"/></clipPath>
  <style>{build_css(static)}</style>
</defs>

<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect y="-48" width="{W}" height="{H + 96}" fill="url(#grid)"{cls("grid")}/>
  {"".join(particles)}
  <rect x="0" y="0" width="120" height="{H}" fill="url(#beam)"{cls("beam")}/>

  <g{cls("scene")}>
    <!-- halo + orbit rings behind the photo -->
    <circle{cls("halo")} cx="{cx}" cy="{cy}" r="300" fill="url(#halo)"/>
    <circle{cls("impact")} cx="{cx}" cy="{cy + 40}" r="260" fill="url(#halo)"/>
    <circle{cls("ring1")} cx="{cx}" cy="{cy}" r="258" fill="none" stroke="{GREEN}" stroke-opacity=".55" stroke-width="1.6" stroke-dasharray="3 14" stroke-linecap="round"/>
    <circle{cls("ring2")} cx="{cx}" cy="{cy}" r="292" fill="none" stroke="{LIME}" stroke-opacity=".35" stroke-width="1" stroke-dasharray="70 22 6 22"/>

    <!-- code glyph -->
    <text{cls("halo")} x="640" y="250" font-family="{MONO}" font-size="150" font-weight="700" fill="{GREEN}" fill-opacity=".22" filter="url(#glow)">&lt;/&gt;</text>

    <!-- photo -->
    <g{cls("photo")}>
      <image x="{px}" y="{py}" width="{pw}" height="{ph}" preserveAspectRatio="xMidYMax meet" xlink:href="data:{mime};base64,{photo_b64}" href="data:{mime};base64,{photo_b64}"/>
    </g>
    <rect x="{px - 40}" y="{H - 110}" width="{pw + 80}" height="110" fill="url(#fade)"/>

    <!-- top bar -->
    <g{cls("r1")}>
      <circle cx="74" cy="52" r="14" fill="none" stroke="{TEXT}" stroke-width="2"/>
      <path d="M68 58c0-5 2-6 6-6s6 1 6 6M66 48l3 3M82 48l-3 3" fill="none" stroke="{TEXT}" stroke-width="2" stroke-linecap="round"/>
      <text x="100" y="58" font-family="{FONT}" font-size="22" font-weight="700" fill="{TEXT}">{esc(p.handle)}</text>
      <rect x="298" y="38" width="1.5" height="28" fill="{GREEN}" fill-opacity=".5"/>
      <text x="316" y="58" font-family="{FONT}" font-size="16" fill="{MUTED}" xml:space="preserve">{esc(p.roles)}</text>
    </g>

    <!-- headline -->
    <text{cls("r2")} x="60" y="178" font-family="{FONT}" font-size="86" font-weight="800" fill="{TEXT}" letter-spacing="-2">{esc(h1)}</text>
    <text{cls("r3")} x="60" y="262" font-family="{FONT}" font-size="86" font-weight="800" font-style="italic" fill="url(#gtext)" letter-spacing="-2" filter="url(#glow)">{esc(h2)}</text>
    <text{cls("r4")} x="60" y="346" font-family="{FONT}" font-size="86" font-weight="800" fill="{TEXT}" letter-spacing="-2">{esc(h3)}</text>

    <!-- title pill -->
    <g{cls("r5")}>
      <rect x="60" y="388" width="{round(len(p.title) * 15.5 + 78)}" height="54" rx="27" fill="url(#gtext)"/>
      <path d="M92 416l16-8 16 8-16 8z M98 420v8c6 6 18 6 24 0v-8" fill="{BG}"/>
      <text x="138" y="423" font-family="{FONT}" font-size="22" font-weight="700" fill="{BG}">{esc(p.title)}</text>
    </g>

    <!-- terminal card -->
    <g{cls("r5")}>
      <rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="14" fill="#03100c" fill-opacity=".82" stroke="{GREEN}" stroke-opacity=".5"/>
      <circle cx="{tx + 22}" cy="{ty + 22}" r="5" fill="#ff6b6b"/><circle cx="{tx + 40}" cy="{ty + 22}" r="5" fill="#ffd166"/><circle cx="{tx + 58}" cy="{ty + 22}" r="5" fill="{GREEN}"/>
      <text x="{tx + tw - 20}" y="{ty + 26}" text-anchor="end" font-family="{MONO}" font-size="12" fill="{MUTED}">rashid.py</text>
    </g>
    {"".join(term_lines)}

    <!-- typed tagline -->
    <g clip-path="url(#typeclip)">
      <text x="60" y="512" font-family="{FONT}" font-size="30" font-style="italic" fill="{MUTED}" xml:space="preserve">{esc(p.typed)}</text>
    </g>
    <rect{cls("cursor")} x="{60 + typed_w + 4}" y="486" width="3" height="32" fill="{GREEN}"/>

    <!-- skill chips -->
    <g{cls("r6")}>{"".join(chips)}</g>

    <!-- footer line -->
    <g{cls("r7")}>
      <circle{cls("dot")} cx="68" cy="606" r="5" fill="{GREEN}" filter="url(#glow)"/>
      <text x="84" y="611" font-family="{FONT}" font-size="15" fill="{TEXT}" xml:space="preserve">{esc(p.status)}  <tspan fill="{MUTED}">\u2022  {esc(p.location)}</tspan></text>
      <text x="{W - 40}" y="611" text-anchor="end" font-family="'Segoe Script','Brush Script MT','Snell Roundhand',cursive" font-size="22" font-style="italic" fill="{GREEN}">{esc(p.tagline)}</text>
    </g>
  </g>

  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="25" fill="none" stroke="{GREEN}" stroke-opacity=".35"/>
</g>
</svg>
"""
    return svg


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate the animated profile banner.")
    ap.add_argument("--photo", default=str(ROOT / "assets" / "rashid-cutout.webp"))
    ap.add_argument("--out", default=str(ROOT / "assets" / "banner.svg"))
    ap.add_argument("--static", action="store_true", help="skip animations (preview)")
    args = ap.parse_args()

    photo = Path(args.photo)
    if not photo.exists():
        raise SystemExit(f"Photo not found: {photo}")

    svg = build_svg(Profile(), photo, args.static)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(svg, encoding="utf-8")
    print(f"Wrote {out} ({out.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
