#!/usr/bin/env python3
"""World News — 18 November 2026: one-image summary.

make.fun bounty: news-image-20261118
"Sum up 18 November's world news in one image"

Deterministic, offline image generator. No network, no randomness,
no timestamps. Writes a 1024x1024 PNG to /output/entry.png when
/output exists (or can be created), otherwise to ./out/entry.png
(and always also writes ./out/entry.png locally for inspection).

program/v1 harness: when MAKEFUN_ENV_URL is set, this program binds
a free port (never 8080), POSTs {"port": port} to
$MAKEFUN_ENV_URL/register, answers GET /healthz with 200, and
long-polls GET $MAKEFUN_ENV_URL/done until done.
"""

import json
import os
import socket
import textwrap
import threading
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# --- Colours (fixed) -------------------------------------------------------
NAVY = (11, 28, 61)
NAVY_LIGHT = (23, 48, 94)
RED = (198, 32, 38)
WHITE = (255, 255, 255)
INK = (17, 24, 39)
GREY = (90, 100, 116)
LIGHT_GREY = (238, 240, 244)
RULE = (203, 213, 225)
GOLD = (255, 193, 7)

# --- Stories: researched 2026-11-18 from the briefings listed in README ---
# (tag, headline, one-line summary, source)
STORIES = [
    (
        "GULF CONFLICT",
        "US strikes Iran; Iran hits bases in Bahrain, Kuwait",
        "US jets hit a Revolutionary Guard missile site on Qeshm Island after "
        "Iranian drones targeted US forces in the Gulf.",
        "Reuters",
    ),
    (
        "SUMMIT",
        "Xi, Putin and Trump set for rare three-way talks",
        "Xi and Putin met in Shenzhen and denounced protectionism and sanctions "
        "at APEC, a day before Trump arrives.",
        "AFP / AP",
    ),
    (
        "UKRAINE WAR",
        "Ukraine hits Kerch Bridge to Crimea for second day",
        "Drones and missiles struck the bridge to occupied Crimea; part of its "
        "road span fell into the strait, Kyiv said.",
        "Zark News / One Turn",
    ),
    (
        "US POLITICS",
        "Peltola wins Alaska; Democrats take 56-44 majority",
        "Democrat Mary Peltola beat Republican Dan Sullivan in the final Senate "
        "race called, the party's ninth flip.",
        "Associated Press",
    ),
    (
        "HEALTH",
        "Congo Ebola outbreak passes 11,000 cases",
        "Cases more than doubled in three months across 67 health zones in eight "
        "provinces; over 5,400 have died, the UN said.",
        "United Nations",
    ),
    (
        "SPACE",
        "Voyager 1 reaches one light-day from Earth",
        "NASA's probe crossed about 16 billion miles - a distance no "
        "human-made object had ever reached before.",
        "NASA JPL",
    ),
]

TAG_COLOURS = {
    "GULF CONFLICT": (178, 34, 34),
    "SUMMIT": (23, 48, 94),
    "UKRAINE WAR": (120, 53, 15),
    "US POLITICS": (30, 64, 175),
    "HEALTH": (5, 122, 85),
    "SPACE": (88, 28, 135),
}


def _font(bold, size):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    for base in (
        "/usr/share/fonts/truetype/dejavu/",
        "/usr/share/fonts/",
    ):
        path = os.path.join(base, name)
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size=size)


def _wrap(draw, text, font, max_width):
    """Greedy word wrap to a pixel width; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def build_image():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    # ---- Header -----------------------------------------------------------
    d.rectangle([0, 0, W, 140], fill=NAVY)
    d.rectangle([0, 140, W, 146], fill=RED)
    title_font = _font(True, 58)
    d.text((48, 20), "WORLD NEWS", font=title_font, fill=WHITE)
    d.text((48, 94), "WEDNESDAY  •  18 NOVEMBER 2026", font=_font(True, 26), fill=GOLD)
    # date badge, top right
    d.rounded_rectangle([880, 20, 976, 120], radius=10, fill=WHITE)
    d.text((928, 30), "18", font=_font(True, 40), fill=NAVY, anchor="ma")
    d.text((928, 78), "NOV", font=_font(True, 26), fill=RED, anchor="ma")

    # ---- Story blocks ------------------------------------------------------
    y = 162
    block_h = 128
    gap = 5
    head_font = _font(True, 26)
    body_font = _font(False, 20)
    tag_font = _font(True, 19)
    num_font = _font(True, 30)
    for i, (tag, headline, summary, source) in enumerate(STORIES):
        top = y + i * (block_h + gap)
        # card background on alternating rows
        if i % 2 == 0:
            d.rectangle([32, top, W - 32, top + block_h], fill=LIGHT_GREY)
        # number badge
        colour = TAG_COLOURS[tag]
        d.ellipse([48, top + 16, 96, top + 64], fill=colour)
        d.text((72, top + 40), str(i + 1), font=num_font, fill=WHITE, anchor="mm")
        # tag
        d.text((116, top + 10), tag + "  —  " + source, font=tag_font, fill=colour)
        # headline (wrap to 2 lines max)
        head_lines = _wrap(d, headline, head_font, W - 116 - 48)
        hy = top + 36
        for line in head_lines[:2]:
            d.text((116, hy), line, font=head_font, fill=INK)
            hy += 30
        # summary (1-2 lines)
        sum_lines = _wrap(d, summary, body_font, W - 116 - 48)
        sy = hy + 2
        for line in sum_lines[:2]:
            d.text((116, sy), line, font=body_font, fill=GREY)
            sy += 24
        # divider
        if i < len(STORIES) - 1:
            d.line([32, top + block_h + 2, W - 32, top + block_h + 2], fill=RULE, width=1)

    # ---- Footer ------------------------------------------------------------
    fy = y + len(STORIES) * (block_h + gap) + 2
    d.rectangle([0, fy, W, H], fill=NAVY)
    d.text(
        (48, fy + 12),
        "Sources: Reuters  •  AFP  •  Associated Press  •  NASA JPL  •  United Nations",
        font=_font(False, 20),
        fill=WHITE,
    )
    d.text(
        (48, fy + 40),
        "Summarised from reporting published on 18 November 2026.  •  make.fun bounty news-image-20261118",
        font=_font(False, 18),
        fill=(180, 190, 205),
    )
    return img


def output_paths():
    """Primary path per spec; ./out/entry.png is always written too."""
    primary = None
    try:
        os.makedirs("/output", exist_ok=True)
        primary = "/output/entry.png"
    except OSError:
        primary = None
    local = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "entry.png")
    paths = []
    if primary:
        paths.append(primary)
    paths.append(local)
    return paths


def write_image():
    img = build_image()
    assert img.size == (1024, 1024), img.size
    paths = output_paths()
    for path in paths:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        img.save(path, format="PNG")
    return paths


# --- program/v1 harness -----------------------------------------------------

class _Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/healthz":
            body = b"ok"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, *args):
        pass


def _free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def _http_json(method, url, payload=None, timeout=10):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8", "replace")
    try:
        return json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        return {"_raw": raw}


def run_harness():
    """Register with the harness, serve /healthz, wait for /done."""
    base = os.environ["MAKEFUN_ENV_URL"].rstrip("/")
    port = _free_port()
    assert port != 8080, "must never bind 8080"
    server = ThreadingHTTPServer(("127.0.0.1", port), _Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        # Register (retry briefly; the harness endpoint may lag).
        last_err = None
        for _ in range(30):
            try:
                _http_json("POST", base + "/register", {"port": port}, timeout=5)
                last_err = None
                break
            except Exception as exc:  # noqa: BLE001 - retry then continue
                last_err = exc
                time.sleep(2)
        if last_err is not None:
            print("register failed (continuing):", last_err)
        # Long-poll /done until done, with a timeout.
        deadline = time.time() + 1800
        while time.time() < deadline:
            try:
                result = _http_json("GET", base + "/done", timeout=30)
                if isinstance(result, dict) and result.get("done") is True:
                    break
            except Exception:  # noqa: BLE001 - transient; keep polling
                pass
            time.sleep(2)
    finally:
        server.shutdown()
        server.server_close()


def main():
    paths = write_image()
    for path in paths:
        print("wrote", path)
    if os.environ.get("MAKEFUN_ENV_URL"):
        run_harness()


if __name__ == "__main__":
    main()
