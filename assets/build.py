#!/usr/bin/env python3
"""Generates every animated SVG used by README.md.

    python3 assets/build.py

Edit the data blocks below (projects, client work, career) and re-run.
Palette and font mirror the portfolio (aravindshajan6.github.io/react-portfolio).
"""
import math
import random
import textwrap
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).parent
random.seed(6)

BG, ELEV, ELEV2, BORDER = "#0a0a0f", "#121218", "#1a1a22", "#26262e"
TEXT, DIM, ACCENT, ACCENT2, OK = "#ededf2", "#8a8a94", "#7c6cff", "#ff8c42", "#4ade80"
FONT = ("'JetBrains Mono','SF Mono',SFMono-Regular,Menlo,Consolas,"
        "'DejaVu Sans Mono','Liberation Mono',monospace")
EM = 0.6  # monospace advance width, in em


# ── helpers ────────────────────────────────────────────────────────────────

def svg(w, h, title, body, style=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">\n'
            f'<title>{escape(title)}</title>\n'
            f'<style>text{{font-family:{FONT}}}{style}</style>\n{body}\n</svg>\n')


def discrete(attr, frames, T, begin="0s", loop=True):
    """Step an attribute through (seconds, value) frames; first frame at t=0."""
    kt = ";".join(f"{t / T:.4f}" for t, _ in frames)
    vals = ";".join(str(v) for _, v in frames)
    tail = 'repeatCount="indefinite"' if loop else 'fill="freeze"'
    return (f'<animate attributeName="{attr}" calcMode="discrete" dur="{T}s" '
            f'begin="{begin}" keyTimes="{kt}" values="{vals}" {tail}/>')


def appear(t, T, begin="0s", loop=True):
    return discrete("opacity", [(0, 0), (t, 1)], T, begin, loop)


def tspans(parts):
    """[(text, color, bold?)] -> <tspan>s"""
    out = []
    for p in parts:
        s, color = p[0], p[1]
        bold = ' font-weight="700"' if len(p) > 2 and p[2] else ""
        out.append(f'<tspan fill="{color}"{bold}>{escape(s)}</tspan>')
    return "".join(out)


def window(w, h, title, clip_id):
    """Terminal window chrome; returns (open markup, close markup)."""
    dots = "".join(f'<circle cx="{22 + i * 18}" cy="19" r="5.5" fill="{c}"/>'
                   for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840")))
    return (f'<defs><clipPath id="{clip_id}"><rect width="{w}" height="{h}" rx="14"/></clipPath></defs>'
            f'<g clip-path="url(#{clip_id})">'
            f'<rect width="{w}" height="{h}" fill="{BG}"/>'
            f'<rect width="{w}" height="38" fill="{ELEV}"/>'
            f'<line x1="0" y1="38" x2="{w}" y2="38" stroke="{BORDER}"/>{dots}'
            f'<text x="{w / 2}" y="24" text-anchor="middle" font-size="12.5" fill="{DIM}">{escape(title)}</text>',
            f'</g><rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="14" fill="none" stroke="{BORDER}"/>')


# ── hero ───────────────────────────────────────────────────────────────────

def cube_frames(cx, cy, scale, n, ay_fn, ax_fn, size=1.0, D=4.2):
    verts = [(x, y, z) for x in (-size, size) for y in (-size, size) for z in (-size, size)]
    frames = []
    for k in range(n + 1):
        ay, ax = ay_fn(k / n), ax_fn(k / n)
        pts = []
        for x, y, z in verts:
            x, z = x * math.cos(ay) + z * math.sin(ay), -x * math.sin(ay) + z * math.cos(ay)
            y, z = y * math.cos(ax) - z * math.sin(ax), y * math.sin(ax) + z * math.cos(ax)
            f = D / (D + z)
            pts.append((cx + x * scale * f, cy + y * scale * f))
        frames.append(pts)
    return frames


CUBE_EDGES = [(a, b) for a in range(8) for b in range(a + 1, 8) if bin(a ^ b).count("1") == 1]


def edges_d(pts, edges):
    return " ".join(f"M{pts[a][0]:.1f} {pts[a][1]:.1f}L{pts[b][0]:.1f} {pts[b][1]:.1f}" for a, b in edges)


def build_hero():
    W, H = 840, 300
    tau = 2 * math.pi
    body = []
    body.append(f'''<defs>
<clipPath id="card"><rect width="{W}" height="{H}" rx="18"/></clipPath>
<radialGradient id="glow" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{ACCENT}" stop-opacity=".45"/><stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/></radialGradient>
<linearGradient id="floorfade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff" stop-opacity="1"/></linearGradient>
<mask id="floormask"><rect y="222" width="{W}" height="{H - 222}" fill="url(#floorfade)"/></mask>
<filter id="blur" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3"/></filter>
<clipPath id="band1"><rect x="0" y="86" width="{W}" height="12"/></clipPath>
<clipPath id="band2"><rect x="0" y="106" width="{W}" height="9"/></clipPath>
</defs>
<g clip-path="url(#card)">
<rect width="{W}" height="{H}" fill="{BG}"/>''')

    # stars
    stars = []
    for _ in range(46):
        x, y = random.uniform(10, W - 10), random.uniform(46, 225)
        r = random.choice((0.6, 0.8, 1, 1.3))
        stars.append(f'<circle class="tw" cx="{x:.0f}" cy="{y:.0f}" r="{r}" '
                     f'style="animation-delay:{random.uniform(0, 4):.2f}s;animation-duration:{random.uniform(2.5, 5):.1f}s"/>')
    body.append(f'<g fill="{TEXT}">{"".join(stars)}</g>')

    # synthwave floor: converging verticals + horizontals rushing toward the viewer
    floor = [f'<line x1="{420 + i * 9}" y1="222" x2="{420 + i * 64}" y2="{H}"/>' for i in range(-14, 15)]
    for k in range(6):
        floor.append(f'<line x1="0" x2="{W}" y1="222" y2="222">'
                     f'<animate attributeName="y1" values="222;{H + 8}" dur="3s" begin="{-k * 0.5}s" repeatCount="indefinite" calcMode="spline" keyTimes="0;1" keySplines=".6 0 1 .5"/>'
                     f'<animate attributeName="y2" values="222;{H + 8}" dur="3s" begin="{-k * 0.5}s" repeatCount="indefinite" calcMode="spline" keyTimes="0;1" keySplines=".6 0 1 .5"/></line>')
    body.append(f'<g mask="url(#floormask)" stroke="{ACCENT}" stroke-width="1" opacity=".55">{"".join(floor)}</g>')
    body.append(f'<line x1="0" y1="222" x2="{W}" y2="222" stroke="{ACCENT}" stroke-opacity=".5"/>')

    # rotating hyper-cube (outer + counter-rotating inner + connectors)
    cx, cy, n, T = 690, 126, 120, 20
    outer = cube_frames(cx, cy, 46, n, lambda t: tau * t, lambda t: 0.5 + 0.25 * math.sin(tau * t))
    inner = cube_frames(cx, cy, 23, n, lambda t: -tau * t, lambda t: -0.4 + 0.3 * math.cos(tau * t))
    conn = [[(o[i], inn[i]) for i in range(8)] for o, inn in zip(outer, inner)]

    def anim_d(frames):
        return f'<animate attributeName="d" dur="{T}s" repeatCount="indefinite" values="{";".join(frames)}"/>'

    d_out = [edges_d(p, CUBE_EDGES) for p in outer]
    d_in = [edges_d(p, CUBE_EDGES) for p in inner]
    d_conn = [" ".join(f"M{a[0]:.1f} {a[1]:.1f}L{b[0]:.1f} {b[1]:.1f}" for a, b in c) for c in conn]
    d_dots = [" ".join(f"M{x:.1f} {y:.1f}h.01" for x, y in p) for p in outer]
    body.append(f'<ellipse class="pulse" cx="{cx}" cy="{cy}" rx="100" ry="92" fill="url(#glow)"/>')
    body.append(f'<g fill="none" stroke-linecap="round">'
                f'<path d="{d_out[0]}" stroke="{ACCENT}" stroke-width="6" opacity=".35" filter="url(#blur)">{anim_d(d_out)}</path>'
                f'<path d="{d_conn[0]}" stroke="{ACCENT}" stroke-width="1" opacity=".45">{anim_d(d_conn)}</path>'
                f'<path d="{d_out[0]}" stroke="{ACCENT}" stroke-width="1.8">{anim_d(d_out)}</path>'
                f'<path d="{d_in[0]}" stroke="{ACCENT2}" stroke-width="1.6">{anim_d(d_in)}</path>'
                f'<path d="{d_dots[0]}" stroke="{TEXT}" stroke-width="5">{anim_d(d_dots)}</path></g>')

    # top bar
    boot = "[ BOOTING PROFILE v3.0 ]"
    body.append(f'<clipPath id="bootclip"><rect x="44" y="20" height="22" width="0">'
                + discrete("width", [(0, 0)] + [(0.1 + i * 0.03, (i + 1) * 12 * EM) for i in range(len(boot) - 1)]
                           + [(0.1 + (len(boot) - 1) * 0.03, 600)], 1.2, loop=False)
                + f'</rect></clipPath>'
                f'<text x="44" y="36" font-size="12" letter-spacing="1" fill="{DIM}" clip-path="url(#bootclip)">{boot}</text>')
    body.append(f'<g transform="translate({W - 44} 0)"><circle class="led" cx="-196" cy="32" r="4" fill="{OK}"/>'
                f'<text x="0" y="36" text-anchor="end" font-size="12" fill="{DIM}">status: <tspan fill="{OK}">available_for_hire</tspan></text></g>')

    # name: decrypt intro, then chromatic glitch forever
    name, nx, ny, fs = "ARAVIND SHAJAN", 44, 124, 54
    glyphs = "!<>-_/[]{}=+*^?#$%&01ΞΛΣ"
    steps, dt, t0 = 13, 0.07, 0.35
    frames = []
    for f in range(steps):
        locked = round(len(name) * f / steps)
        parts = [(c, TEXT) if (i < locked or c == " ") else (random.choice(glyphs), ACCENT)
                 for i, c in enumerate(name)]
        frames.append(f'<text x="{nx}" y="{ny}" font-size="{fs}" font-weight="800" letter-spacing="1" opacity="0">'
                      f'{tspans(parts)}<set attributeName="opacity" to="1" begin="{t0 + f * dt:.2f}s" dur="{dt}s"/></text>')
    body.append("".join(frames))
    t_final = t0 + steps * dt
    txt = f'x="{nx}" y="{ny}" font-size="{fs}" font-weight="800" letter-spacing="1"'
    body.append(f'<g opacity="0"><set attributeName="opacity" to="1" begin="{t_final:.2f}s"/>'
                f'<text class="ga" {txt} fill="{ACCENT}" opacity=".85">{name}</text>'
                f'<text class="gb" {txt} fill="{ACCENT2}" opacity=".7">{name}</text>'
                f'<text class="nm" {txt} fill="{TEXT}">{name}</text>'
                f'<g class="s1" clip-path="url(#band1)"><rect x="30" y="80" width="560" height="40" fill="{BG}"/><text {txt} fill="{TEXT}">{name}</text></g>'
                f'<g class="s2" clip-path="url(#band2)"><rect x="30" y="80" width="560" height="40" fill="{BG}"/><text {txt} fill="{ACCENT}">{name}</text></g>'
                f'</g>')

    # role line: type → hold → delete, cycling
    roles = ["full stack developer", "python automation · playwright · fastapi",
             "MERN apps that actually ship", "three.js + anime.js enjoyer"]
    rx, ry, rs, slot = 44, 168, 18, 4.0
    cw = rs * EM
    T = slot * len(roles)
    begin = f"{t_final + 0.2:.2f}s"
    body.append(f'<text x="{rx}" y="{ry}" font-size="{rs}" fill="{OK}" font-weight="700">➜</text>')
    px = rx + 2 * cw
    for k, role in enumerate(roles):
        s0, n_ = k * slot, len(role)
        type_dt = min(0.07, 1.4 / n_)
        fr = [(0, 0)]
        fr += [(s0 + 0.05 + i * type_dt, round((i + 1) * cw, 1)) for i in range(n_)]
        del_start = s0 + slot - 0.75
        del_dt = 0.55 / n_
        fr += [(del_start + i * del_dt, round((n_ - i - 1) * cw, 1)) for i in range(n_)]
        cur = [(0, -99)] + [(t, px + w) for t, w in fr[1:]] + [(s0 + slot - 0.01, -99)]
        body.append(f'<clipPath id="role{k}"><rect x="{px}" y="{ry - rs}" height="{rs * 1.5}" width="0">'
                    f'{discrete("width", fr, T, begin)}</rect></clipPath>'
                    f'<text x="{px}" y="{ry}" font-size="{rs}" fill="{TEXT}" clip-path="url(#role{k})">{escape(role)}</text>'
                    f'<rect class="blink" x="-99" y="{ry - rs + 3}" width="{cw * 0.9:.1f}" height="{rs + 2}" fill="{ACCENT}">'
                    f'{discrete("x", cur, T, begin)}</rect>')

    body.append(f'<text x="44" y="200" font-size="12.5" fill="{DIM}">kerala, india <tspan fill="{ACCENT}">/</tspan> '
                f'shipping since 2023 <tspan fill="{ACCENT}">/</tspan> en · hi · ml</text>')
    body.append(f'</g><rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{BORDER}"/>')

    glitch = "5s {d}s infinite steps(1,end)".format(d=round(t_final + 1, 2))
    style = f"""
.tw{{animation:tw 3s ease-in-out infinite;opacity:.2}}
@keyframes tw{{50%{{opacity:.9}}}}
.pulse{{animation:pulse 4s ease-in-out infinite;transform-origin:{cx}px {cy}px}}
@keyframes pulse{{50%{{opacity:.55;transform:scale(1.12)}}}}
.led{{animation:led 1.6s ease-in-out infinite}}
@keyframes led{{50%{{opacity:.25}}}}
.blink{{animation:blink 1s steps(1,end) infinite}}
@keyframes blink{{50%{{opacity:0}}}}
.ga{{transform:translate(-2px,0);animation:ga {glitch}}}
.gb{{transform:translate(2px,0);animation:gb {glitch}}}
.nm{{animation:nm {glitch}}}
.s1,.s2{{opacity:0}}
.s1{{animation:s1 {glitch}}}
.s2{{animation:s2 {glitch}}}
@keyframes ga{{0%,90%,100%{{transform:translate(-2px,0)}}91%{{transform:translate(-9px,2px)}}93%{{transform:translate(6px,-2px)}}95%{{transform:translate(-5px,1px)}}97%{{transform:translate(3px,0)}}}}
@keyframes gb{{0%,90%,100%{{transform:translate(2px,0)}}91%{{transform:translate(8px,-1px)}}93%{{transform:translate(-7px,2px)}}95%{{transform:translate(4px,-1px)}}97%{{transform:translate(-3px,0)}}}}
@keyframes nm{{0%,90%,100%{{opacity:1}}92%{{opacity:.55}}94%{{opacity:1}}96%{{opacity:.75}}}}
@keyframes s1{{0%,90%,98%,100%{{opacity:0;transform:none}}91%{{opacity:1;transform:translate(16px,0)}}94%{{opacity:1;transform:translate(-12px,0)}}}}
@keyframes s2{{0%,92%,99%,100%{{opacity:0;transform:none}}93%{{opacity:1;transform:translate(-18px,0)}}96%{{opacity:1;transform:translate(10px,0)}}}}
"""
    return svg(W, H, "Aravind Shajan — full stack developer", "\n".join(body), style)


# ── terminal ───────────────────────────────────────────────────────────────

def build_terminal():
    W, H, T = 840, 352, 18
    fs, lh, x0, y0 = 14.5, 25, 26, 72
    cw = fs * EM
    body = []
    head, tail = window(W, H, "aravind@github: ~ — zsh", "twin")
    body.append(head)

    prompt = [("➜ ", OK, True), ("~ ", ACCENT, True)]
    prompt_w = 4 * cw
    uid = iter(range(1000))

    def line_y(i):
        return y0 + i * lh

    def cmd(i, t_show, t_type, command, cursor_until):
        k = next(uid)
        y = line_y(i)
        n = len(command)
        dt = 0.075
        xs = x0 + prompt_w
        fr = [(0, 0)] + [(t_type + j * dt, round((j + 1) * cw, 1)) for j in range(n - 1)] + [(t_type + (n - 1) * dt, 900)]
        cur = [(0, -99), (t_show, xs)] + [(t_type + j * dt, round(xs + (j + 1) * cw, 1)) for j in range(n)] + [(cursor_until, -99)]
        return (f'<text x="{x0}" y="{y}" font-size="{fs}" opacity="0">{tspans(prompt)}{appear(t_show, T)}</text>'
                f'<clipPath id="c{k}"><rect x="{xs}" y="{y - fs}" height="{fs * 1.6}" width="0">{discrete("width", fr, T)}</rect></clipPath>'
                f'<text x="{xs}" y="{y}" font-size="{fs}" fill="{TEXT}" clip-path="url(#c{k})">{escape(command)}</text>'
                f'<rect class="blink" x="-99" y="{y - fs + 2}" width="{cw:.1f}" height="{fs + 3}" fill="{ACCENT}">{discrete("x", cur, T)}</rect>')

    def out(i, t, parts, indent=2):
        return (f'<text x="{x0 + indent * cw:.1f}" y="{line_y(i)}" font-size="{fs}" opacity="0">'
                f'{tspans(parts)}{appear(t, T)}</text>')

    def dots(i, t, label, result, color):
        k = next(uid)
        y = line_y(i)
        xs = x0 + 2 * cw
        base = (len(label) + 3) * cw
        n = 8
        fr = [(0, 0), (t, round(base, 1))] + [(t + 0.12 + j * 0.1, round(base + (j + 1) * cw, 1)) for j in range(n)] + [(t + 0.12 + n * 0.1 + 0.15, 900)]
        parts = [("✔ ", OK), (label + " ", TEXT), ("." * n + " ", DIM), (result, color, True)]
        return (f'<clipPath id="c{k}"><rect x="{xs}" y="{y - fs}" height="{fs * 1.6}" width="0">{discrete("width", fr, T)}</rect></clipPath>'
                f'<text x="{xs}" y="{y}" font-size="{fs}" clip-path="url(#c{k})">{tspans(parts)}</text>'), xs + (len(label) + 2 + n + 1 + len(result)) * cw

    body.append(cmd(0, 0.3, 0.55, "whoami", 1.2))
    body.append(out(1, 1.35, [("aravind shajan", TEXT, True), (" — full stack developer @ synctric · kerala, india", DIM)]))
    body.append(cmd(2, 1.8, 2.0, "cat now.txt", 2.95))
    body.append(out(3, 3.15, [("› ", ACCENT), ("shipping client products: react up front, fastapi + node behind", DIM)]))
    body.append(out(4, 3.35, [("› ", ACCENT), ("side quest: ", DIM), ("pytch", ACCENT2, True), (" — turf booking + matchmaking for kochi", DIM)]))
    body.append(cmd(5, 3.9, 4.1, "sudo hire aravind", 5.5))

    # password line types its dots
    k = next(uid)
    y = line_y(6)
    xs = x0 + 2 * cw
    label = "[sudo] password for recruiter: "
    fr = [(0, 0), (5.8, round(len(label) * cw, 1))] + [(6.0 + j * 0.08, round((len(label) + j + 1) * cw, 1)) for j in range(8)] + [(6.7, 900)]
    body.append(f'<clipPath id="c{k}"><rect x="{xs}" y="{y - fs}" height="{fs * 1.6}" width="0">{discrete("width", fr, T)}</rect></clipPath>'
                f'<text x="{xs}" y="{y}" font-size="{fs}" clip-path="url(#c{k})">{tspans([(label, DIM), ("•" * 8, ACCENT)])}</text>')

    body.append(out(7, 7.1, [("✔ ", OK), ("Authentication successful.", TEXT)]))
    d1, _ = dots(8, 7.5, "Checking availability", "Available", OK)
    body.append(d1)
    t_ok = 10.0
    d2, end_x = dots(9, t_ok - 1.2, "Approving hire request", "APPROVED", ACCENT2)
    body.append(d2)

    # confetti out of APPROVED
    ox, oy = end_x - 4 * cw, line_y(9) - 5
    bits = []
    colors = (ACCENT, ACCENT2, OK, TEXT, "#febc2e")
    for _ in range(34):
        ang = random.uniform(-math.pi * 0.95, -math.pi * 0.05)
        sp = random.uniform(60, 190)
        dx, dy = math.cos(ang) * sp, math.sin(ang) * sp
        fall = random.uniform(70, 140)
        rot = random.choice((-1, 1)) * random.randint(180, 720)
        a, b, c = t_ok / T, (t_ok + 0.35) / T, (t_ok + 1.6) / T
        bits.append(
            f'<g transform="translate({ox:.1f} {oy:.1f})"><g opacity="0">'
            f'<animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" keyTimes="0;{a:.4f};{a + 0.001:.4f};{(t_ok + 1.0) / T:.4f};{c:.4f};1" values="0;0;1;1;0;0"/>'
            f'<animateTransform attributeName="transform" type="translate" dur="{T}s" repeatCount="indefinite" calcMode="spline" '
            f'keyTimes="0;{a:.4f};{b:.4f};{c:.4f};1" keySplines="0 0 1 1;.15 .7 .35 1;.5 0 .9 .6;0 0 1 1" '
            f'values="0 0;0 0;{dx:.1f} {dy:.1f};{dx * 1.35:.1f} {dy + fall:.1f};{dx * 1.35:.1f} {dy + fall:.1f}"/>'
            f'<rect x="-3" y="-1.5" width="6" height="3" rx="1" fill="{random.choice(colors)}">'
            f'<animateTransform attributeName="transform" type="rotate" dur="{T}s" repeatCount="indefinite" '
            f'keyTimes="0;{a:.4f};{c:.4f};1" values="0;0;{rot};{rot}"/></rect></g></g>')
    body.append("".join(bits))

    # final prompt with idle cursor
    y = line_y(10)
    body.append(f'<g opacity="0">{appear(10.9, T)}<text x="{x0}" y="{y}" font-size="{fs}">{tspans(prompt)}</text>'
                f'<rect class="blink" x="{x0 + prompt_w}" y="{y - fs + 2}" width="{cw:.1f}" height="{fs + 3}" fill="{ACCENT}"/></g>')
    body.append(tail)
    style = """
.blink{animation:blink 1s steps(1,end) infinite}
@keyframes blink{50%{opacity:0}}
"""
    return svg(W, H, "Terminal: whoami, cat now.txt, sudo hire aravind — APPROVED", "\n".join(body), style)


# ── project cards ──────────────────────────────────────────────────────────

PROJECTS = [
    dict(slug="auctioneer", title="Auctioneer", url="auctioneer.sapper.top",
         desc="Live auction house — real-time Socket.IO bidding, eBay-style proxy bids, hidden reserves, anti-snipe soft close and a double-entry ledger.",
         stack=["Next.js 16", "Socket.IO", "Postgres", "Three.js"]),
    dict(slug="valodex", title="Valodex", url="valodex.sapper.top",
         desc="A Valorant codex — every agent, weapon, map, skin and rank from live game data, plus a time-to-kill calculator, in Three.js scenes.",
         stack=["Next.js 16", "R3F", "Drizzle", "Postgres"]),
    dict(slug="sportscast", title="Sportscast", url="sportscast.sapper.top",
         desc="Live football scores, fixtures, match stats, a 3D formation pitch and an RSS news hub from BBC, Guardian, ESPN and Sky.",
         stack=["React 19", "anime.js", "Express 5", "MongoDB"]),
    dict(slug="nova-commerce", title="Nova Commerce", url="ecommerce-dashboard-a3ap.onrender.com",
         desc="E-commerce analytics — cohort retention, RFM segments, Holt forecasting, a live order feed and a 3D order globe.",
         stack=["React 19", "Three.js", "Recharts", "MongoDB"]),
    dict(slug="elecstore", title="Elecstore", url="elecstore-web.onrender.com",
         desc="Tech storefront — search, saved items, Razorpay checkout, coupons, order history and an admin area with a sales dashboard.",
         stack=["React", "Redux", "Razorpay", "Docker"]),
    dict(slug="steaminc", title="Steaminc", url="steaminc.onrender.com",
         desc="Finds where any movie is legally streaming in your region — and plays public-domain films straight from the Internet Archive.",
         stack=["Node.js", "TMDB API", "Archive.org", "Docker"]),
]


def build_card(i, p, total):
    W, H = 410, 222
    body = [f'<defs><filter id="g" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="2.5"/></filter>'
            f'<linearGradient id="sheen" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{ACCENT}" stop-opacity=".10"/>'
            f'<stop offset=".6" stop-color="{ACCENT}" stop-opacity="0"/></linearGradient></defs>',
            f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="{ELEV}" stroke="{BORDER}"/>',
            f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="url(#sheen)"/>']
    # orbiting light on the border
    delay = -i * 1.1
    for extra in (f'stroke-width="4" filter="url(#g)" opacity=".7"', 'stroke-width="1.5"'):
        body.append(f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="none" stroke="{ACCENT}" {extra} '
                    f'pathLength="100" stroke-dasharray="9 91" stroke-linecap="round">'
                    f'<animate attributeName="stroke-dashoffset" values="100;0" dur="6.5s" begin="{delay}s" repeatCount="indefinite"/></rect>')
    body.append(f'<text x="{W - 18}" y="92" text-anchor="end" font-size="84" font-weight="800" fill="{ACCENT}" opacity=".07">{i + 1:02d}</text>')
    body.append(f'<text x="20" y="32" font-size="11" fill="{DIM}">~/featured/<tspan fill="{ACCENT}">{p["slug"]}</tspan></text>')
    body.append(f'<circle class="led" cx="{W - 58}" cy="28" r="3.5" fill="{OK}"/>'
                f'<text x="{W - 20}" y="32" text-anchor="end" font-size="11" fill="{OK}">live</text>')
    body.append(f'<text x="20" y="68" font-size="24" font-weight="800" fill="{TEXT}">{escape(p["title"])}</text>')
    for j, line in enumerate(textwrap.wrap(p["desc"], 50)[:3]):
        body.append(f'<text x="20" y="{96 + j * 18}" font-size="12.5" fill="{DIM}">{escape(line)}</text>')
    x = 20
    for s in p["stack"]:
        w = len(s) * 11 * EM + 16
        body.append(f'<rect x="{x}" y="160" width="{w:.1f}" height="22" rx="6" fill="{ELEV2}" stroke="{BORDER}"/>'
                    f'<text x="{x + w / 2:.1f}" y="175" text-anchor="middle" font-size="11" fill="{TEXT}">{escape(s)}</text>')
        x += w + 6
    body.append(f'<text x="20" y="205" font-size="11" fill="{ACCENT}">↗ {escape(p["url"])}</text>')
    style = """
.led{animation:led 1.6s ease-in-out infinite}
@keyframes led{50%{opacity:.25}}
"""
    return svg(W, H, f'{p["title"]} — {p["desc"]}', "\n".join(body), style)


# ── classified client work ─────────────────────────────────────────────────

CLIENT = [
    ("Argus", "narrative & misinformation intelligence console", "react · fastapi · maplibre · whatsapp api"),
    ("Reelform", "AI content suite — text → image → video → reels", "react · node · ai apis"),
    ("Kinema", "AI video studio — drop a photo, get a motion clip", "react · ai video"),
    ("Sanctum", "devotional platform — pujas, live darshan, prasad", "react · tanstack start · typescript"),
    ("Blueprint", "AI website builder — idea → sitemap → wireframes", "react · supabase · openai"),
    ("Loan Mgmt System", "bank loan-approval backend — rules & workflows", "node · express · mongodb"),
]


def build_classified():
    W, H = 840, 318
    body = []
    head, tail = window(W, H, "~/client-work — access level: NDA", "cwin")
    body.append(head)
    body.append(f'<defs><linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{ACCENT}" stop-opacity="0"/>'
                f'<stop offset="1" stop-color="{ACCENT}" stop-opacity=".16"/></linearGradient></defs>')
    body.append(f'<text x="26" y="70" font-size="12" fill="{DIM}">6 client builds in production · no public links · '
                f'<tspan fill="{ACCENT}">declassifying…</tspan></text>')
    for i, (name, desc, stack) in enumerate(CLIENT):
        col, row = i % 2, i // 2
        x, y = 26 + col * 404, 108 + row * 72
        body.append(f'<text x="{x}" y="{y}" font-size="11" fill="{ACCENT2}">{i + 1:02d}</text>'
                    f'<text x="{x + 26}" y="{y}" font-size="16" font-weight="800" fill="{TEXT}">{escape(name)}</text>'
                    f'<text x="{x + 26}" y="{y + 20}" font-size="12" fill="{DIM}">{escape(desc)}</text>'
                    f'<text x="{x + 26}" y="{y + 38}" font-size="11" fill="{ACCENT}">{escape(stack)}</text>')
        body.append(f'<rect class="redact" x="{x + 22}" y="{y - 16}" width="370" height="60" rx="3" fill="{ELEV2}" '
                    f'style="animation-delay:{0.6 + i * 0.28:.2f}s"/>'
                    f'<text class="redact" x="{x + 30}" y="{y + 18}" font-size="12" fill="{DIM}" letter-spacing="2" '
                    f'style="animation-delay:{0.6 + i * 0.28:.2f}s">█████ REDACTED █████</text>')
    # stamp
    body.append(f'<g transform="translate({W - 128} 72) rotate(-8)"><g class="stamp">'
                f'<rect x="-84" y="-20" width="168" height="36" rx="4" fill="none" stroke="{ACCENT2}" stroke-width="2.5"/>'
                f'<text x="0" y="6" text-anchor="middle" font-size="17" font-weight="800" letter-spacing="4" fill="{ACCENT2}">CLASSIFIED</text></g></g>')
    body.append(f'<rect class="scan" x="0" y="0" width="{W}" height="46" fill="url(#scan)"/>')
    body.append(tail)
    style = """
.redact{transform-box:fill-box;transform-origin:right center;animation:redact .55s cubic-bezier(.7,0,.2,1) both}
@keyframes redact{from{transform:scaleX(1)}to{transform:scaleX(0)}}
.stamp{animation:stamp .45s cubic-bezier(.2,1.6,.4,1) 2.6s both}
@keyframes stamp{from{opacity:0;transform:scale(2.4)}to{opacity:.9;transform:scale(1)}}
.scan{animation:scan 4.5s linear infinite}
@keyframes scan{from{transform:translateY(-50px)}to{transform:translateY(330px)}}
"""
    return svg(W, H, "Client work under NDA: " + "; ".join(f"{n} — {d}" for n, d, _ in CLIENT), "\n".join(body), style)


# ── career timeline as git log --graph ─────────────────────────────────────

CAREER = [
    ("May 2026 — now", "Full Stack Developer", "Synctric", "client products end to end — intelligence console, devotional platform, AI tools", "HEAD -> main"),
    ("Jan 2025 — Nov 2025", "Full Stack Developer", "Radicle", "loan-approval platform for an international bank — rules engine, workflows", None),
    ("Oct 2024 — Dec 2024", "Backend Developer Intern", "Transition", "REST APIs, data models and a lot of code review", None),
    ("Apr 2023 — Sep 2023", "Full Stack Developer", "Bixel Technolab", "first dev job — built and shipped MERN apps end to end", "tag: v1.0.0"),
]
EDU = ("2019 — 2023", "B.Tech — Computer Science", "Prist University, Chennai", "fundamentals, algorithms, a lot of late-night lab work")


def build_timeline():
    W = 840
    step, top = 70, 112
    lane1, lane2 = 44, 74
    ys = [top + i * step for i in range(len(CAREER))]
    y_edu = ys[-1] + step
    y_root = y_edu + step - 8
    H = y_root + 34
    body = []
    head, tail = window(W, H, "~/career — git log --graph --career", "twin")
    body.append(head)
    body.append(f'<text x="26" y="68" font-size="13" fill="{DIM}"><tspan fill="{OK}" font-weight="700">➜ </tspan>'
                f'<tspan fill="{ACCENT}" font-weight="700">~ </tspan><tspan fill="{TEXT}">git log --graph --career</tspan></text>')

    main_d = f"M{lane1} {ys[0]}V{y_root}"
    branch_d = (f"M{lane1} {ys[-1]}C{lane1} {ys[-1] + 30} {lane2} {ys[-1] + 26} {lane2} {ys[-1] + 50}"
                f"V{y_edu}C{lane2} {y_edu + 26} {lane1} {y_edu + 24} {lane1} {y_root - 6}")
    body.append(f'<path class="draw" d="{main_d}" stroke="{ACCENT}" stroke-width="2.5" fill="none" pathLength="1"/>')
    body.append(f'<path class="draw b" d="{branch_d}" stroke="{ACCENT2}" stroke-width="2.5" fill="none" pathLength="1"/>')

    hashes = [f"{random.getrandbits(28):07x}" for _ in range(len(CAREER) + 2)]

    def commit(k, cx, y, color, filled, date, role, where, desc, ref):
        d = 0.35 + k * 0.32
        ref_s = f'  <tspan fill="{OK}">({escape(ref)})</tspan>' if ref else ""
        tx = cx + 26
        return (f'<g class="pop" style="animation-delay:{d:.2f}s">'
                f'<circle cx="{cx}" cy="{y}" r="7" fill="{color if filled else BG}" stroke="{color}" stroke-width="2.5"/></g>'
                f'<g class="rise" style="animation-delay:{d + 0.08:.2f}s">'
                f'<text x="{tx}" y="{y - 12}" font-size="12" fill="{DIM}"><tspan fill="{ACCENT2}">{hashes[k]}</tspan>  {escape(date)}{ref_s}</text>'
                f'<text x="{tx}" y="{y + 7}" font-size="15" font-weight="800" fill="{TEXT}">{escape(role)} <tspan fill="{ACCENT}" font-weight="400">@ {escape(where)}</tspan></text>'
                f'<text x="{tx}" y="{y + 26}" font-size="12" fill="{DIM}">{escape(desc)}</text></g>')

    for k, (date, role, where, desc, ref) in enumerate(CAREER):
        body.append(commit(k, lane1, ys[k], ACCENT, k == 0, date, role, where, desc, ref))
    body.append(f'<circle class="ring" cx="{lane1}" cy="{ys[0]}" r="7" fill="none" stroke="{ACCENT}" stroke-width="2"/>')
    date, role, where, desc = EDU
    body.append(commit(len(CAREER), lane2, y_edu, ACCENT2, False, date, role, where, desc, "branch: education"))
    k = len(CAREER) + 1
    body.append(f'<g class="pop" style="animation-delay:{0.35 + k * 0.32:.2f}s"><circle cx="{lane1}" cy="{y_root}" r="5" fill="{DIM}"/></g>'
                f'<text class="rise" style="animation-delay:{0.43 + k * 0.32:.2f}s" x="{lane1 + 26}" y="{y_root + 4}" font-size="12" fill="{DIM}">'
                f'<tspan fill="{ACCENT2}">{hashes[k]}</tspan>  init: hello, world</text>')
    body.append(tail)
    style = """
.draw{stroke-dasharray:1;stroke-dashoffset:1;animation:draw 2.2s cubic-bezier(.6,0,.2,1) .2s forwards}
.draw.b{animation-delay:1.3s;animation-duration:1.2s}
@keyframes draw{to{stroke-dashoffset:0}}
.pop{transform-box:fill-box;transform-origin:center;animation:pop .5s cubic-bezier(.2,1.8,.4,1) both}
@keyframes pop{from{opacity:0;transform:scale(0)}to{opacity:1;transform:scale(1)}}
.rise{animation:rise .6s cubic-bezier(.16,1,.3,1) both}
@keyframes rise{from{opacity:0;transform:translateX(-14px)}to{opacity:1;transform:none}}
.ring{transform-box:fill-box;transform-origin:center;animation:ring 2s ease-out 1s infinite}
@keyframes ring{from{opacity:.9;transform:scale(1)}to{opacity:0;transform:scale(2.6)}}
"""
    title = "Career: " + "; ".join(f"{r} @ {w} ({d})" for d, r, w, _, _ in CAREER) + f"; {EDU[1]} @ {EDU[2]} ({EDU[0]})"
    return svg(W, H, title, "\n".join(body), style)


# ── link buttons + footer ──────────────────────────────────────────────────

LINKS = [("portfolio", "portfolio"), ("linkedin", "linkedin"), ("mail", "mail me"), ("hire", "hire me")]


def build_button(slug, label):
    w = len(label) * 13 * EM + 76
    H = 40
    hot = slug == "hire"
    fill, stroke, color = (ACCENT, ACCENT, BG) if hot else (ELEV, BORDER, TEXT)
    body = (f'<rect x="1" y="1" width="{w - 2:.1f}" height="{H - 2}" rx="10" fill="{fill}" stroke="{stroke}"/>'
            f'<text x="18" y="25" font-size="13" font-weight="700" fill="{BG if hot else ACCENT}">~/</text>'
            f'<text x="{18 + 2 * 13 * EM:.1f}" y="25" font-size="13" font-weight="700" fill="{color}">{escape(label)}</text>'
            f'<text x="{w - 18:.1f}" y="25" text-anchor="end" font-size="13" font-weight="700" fill="{BG if hot else ACCENT}">↗</text>')
    if hot:
        body = (f'<rect class="halo" x="1" y="1" width="{w - 2:.1f}" height="{H - 2}" rx="10" fill="none" stroke="{ACCENT}" stroke-width="2"/>' + body)
    style = """
.halo{transform-box:fill-box;transform-origin:center;animation:halo 2s ease-out infinite}
@keyframes halo{from{opacity:.8;transform:scale(1)}to{opacity:0;transform:scale(1.15,1.5)}}
"""
    return svg(round(w), H, label, body, style)


def build_footer():
    W, H = 840, 120
    body = []
    for k, (color, amp, dur, op, yb) in enumerate(((ACCENT, 10, 7, .9, 44), (ACCENT2, 7, 5, .6, 48), (ACCENT, 5, 9, .35, 52))):
        def wave(phase):
            pts = []
            for i in range(0, 2 * W + 1, 20):
                y = yb + amp * math.sin((i / 140) * 2 * math.pi + phase)
                pts.append(f"{i - W} {y:.1f}")
            return "M" + "L".join(pts)
        body.append(f'<path d="{wave(0)}" fill="none" stroke="{color}" stroke-width="1.6" opacity="{op}">'
                    f'<animateTransform attributeName="transform" type="translate" from="0 0" to="{-140 * (1 if k % 2 == 0 else -1)} 0" dur="{dur}s" repeatCount="indefinite"/></path>')
    body.append(f'<text x="{W / 2}" y="92" text-anchor="middle" font-size="12.5" fill="{DIM}">'
                f'<tspan fill="{OK}">➜</tspan> <tspan fill="{ACCENT}">~</tspan> exit  '
                f'<tspan fill="{BORDER}">│</tspan>  connection to aravind@github closed — thanks for scrolling</text>')
    body.append(f'<text x="{W / 2}" y="112" text-anchor="middle" font-size="10.5" fill="{DIM}" opacity=".7">designed &amp; built by aravind shajan</text>')
    return svg(W, H, "connection closed — thanks for scrolling", "\n".join(body))


def main():
    files = {
        "hero.svg": build_hero(),
        "terminal.svg": build_terminal(),
        "classified.svg": build_classified(),
        "timeline.svg": build_timeline(),
        "footer.svg": build_footer(),
    }
    for i, p in enumerate(PROJECTS):
        files[f"projects/{p['slug']}.svg"] = build_card(i, p, len(PROJECTS))
    for slug, label in LINKS:
        files[f"links/{slug}.svg"] = build_button(slug, label)
    for name, data in files.items():
        path = OUT / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(data, encoding="utf-8")
        print(f"{len(data) / 1024:6.1f} KB  {path.relative_to(OUT.parent)}")


if __name__ == "__main__":
    main()
