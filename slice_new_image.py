#!/usr/bin/env python3
"""
Slices the pre-separated exploded dish image into 3 zone PNGs.
Each output is the same canvas size so they stack in the browser.

Input:  images/Roast_Chicken_seprated.PNG.jpg-removebg-preview.png
Output:
  images/comp-zone-base.png    — plate + potatoes + sauce (bottom)
  images/comp-zone-chicken.png — sliced chicken (middle)
  images/comp-zone-greens.png  — green beans + carrots (top)
"""
import numpy as np, os, sys
from PIL import Image

SRC = "images/Roast_Chicken_seprated.PNG.jpg-removebg-preview.png"
if not os.path.exists(SRC):
    sys.exit(f"ERROR: '{SRC}' not found — run from fitchef-landing/")

img = Image.open(SRC).convert("RGBA")
W, H = img.size
print(f"Loaded {W}×{H}  {SRC}")

arr = np.array(img)          # shape (H, W, 4)
alpha = arr[:, :, 3]         # alpha channel

# ── find rows with meaningful content ────────────────────────────────────────
row_fill = (alpha > 30).sum(axis=1)          # non-transparent pixels per row
threshold = W * 0.01                          # at least 1% of width must be solid

content_rows = np.where(row_fill > threshold)[0]
if len(content_rows) == 0:
    sys.exit("ERROR: no content found — is the image truly transparent?")

y_top = int(content_rows[0])
y_bot = int(content_rows[-1])
print(f"Content rows: {y_top}–{y_bot}")

# ── find gap rows (near-empty rows between the 3 floating food groups) ────────
gap_rows = np.where(row_fill[y_top:y_bot+1] < threshold)[0] + y_top
print(f"Gap rows found: {len(gap_rows)}")

# Group consecutive gap rows into gap bands
bands = []
if len(gap_rows) > 0:
    band_start = gap_rows[0]
    for i in range(1, len(gap_rows)):
        if gap_rows[i] - gap_rows[i-1] > 1:
            bands.append((band_start, gap_rows[i-1]))
            band_start = gap_rows[i]
    bands.append((band_start, gap_rows[-1]))

print(f"Gap bands: {bands}")

# We expect 2 gap bands (3 food groups). Pick the 2 biggest.
bands.sort(key=lambda b: b[1]-b[0], reverse=True)
cut_bands = sorted(bands[:2], key=lambda b: b[0])

if len(cut_bands) < 2:
    # Fallback: even thirds of the content area
    print("WARNING: could not detect 2 clear gaps — using even thirds")
    span = y_bot - y_top
    cut_bands = [
        (y_top + int(span * 0.32), y_top + int(span * 0.36)),
        (y_top + int(span * 0.64), y_top + int(span * 0.68)),
    ]

# Cut points = midpoints of each gap band
cut1 = (cut_bands[0][0] + cut_bands[0][1]) // 2   # greens / chicken boundary
cut2 = (cut_bands[1][0] + cut_bands[1][1]) // 2   # chicken / base boundary

print(f"Cut lines: {cut1} (greens|chicken)  {cut2} (chicken|base)")

# ── helpers ───────────────────────────────────────────────────────────────────
FEATHER = 20   # pixel rows to soft-feather at each cut

def feather_edge(a, y, direction):
    """Linearly fade alpha across FEATHER rows from cut line outward."""
    for dy in range(FEATHER):
        t = dy / FEATHER
        row = y + dy if direction == 'down' else y - dy
        if 0 <= row < H:
            a[row] = (a[row] * t).astype(np.uint8)

def save_zone(name, y_a, y_b):
    """Save a full-canvas PNG with alpha zeroed outside [y_a, y_b]."""
    out = arr.copy()
    out[:y_a, :, 3] = 0
    out[y_b:, :, 3] = 0
    # Feather the cut edges
    feather_edge(out[:, :, 3], y_a, 'down')
    feather_edge(out[:, :, 3], y_b, 'up')
    path = f"images/{name}.png"
    Image.fromarray(out, "RGBA").save(path, "PNG", optimize=True)
    kb = os.path.getsize(path) / 1024
    print(f"  ✓  {path}  {W}×{H}  ({kb:.0f} KB)")

# ── save 3 zones ──────────────────────────────────────────────────────────────
# Top of image = greens (falls last), bottom = base (falls first)
save_zone("comp-zone-greens",  y_top,  cut1)     # top layer
save_zone("comp-zone-chicken", cut1,   cut2)     # middle layer
save_zone("comp-zone-base",    cut2,   y_bot+1)  # bottom layer (plate + sauce)

print("\n✅  Done — 3 zone PNGs written to images/")
