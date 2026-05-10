#!/usr/bin/env python3
"""
Slices 'ROAST CHECKING .jpg' into 3 transparent food-zone layers using GrabCut
for clean background removal and content-aware zone boundaries.

Each output PNG is the same canvas (nw×nh) — they align naturally when
overlaid at the same CSS position.

  comp-zone-base.png    — sauce + sweet potato (bottom of dish, falls first)
  comp-zone-chicken.png — chicken slices + veggies (center, falls second)
  comp-zone-greens.png  — green beans + garnish (top of dish, falls third)
  comp-dish-full.png    — full dish transparent (used for assembled reveal)
"""
import cv2, numpy as np, os, sys
from PIL import Image

SRC      = "images/ROAST CHECKING .jpg"
OUT_SIZE = 900   # longest dimension of output canvas

if not os.path.exists(SRC):
    sys.exit(f"ERROR: '{SRC}' not found — run from fitchef-landing/")

print(f"Loading {SRC} …")
src  = cv2.imread(SRC)
H, W = src.shape[:2]
print(f"Source: {W}×{H}px")

# ── downsample for processing ─────────────────────────────────────────────────
WORK_W = 1800
scale  = WORK_W / W
wW, wH = int(W*scale), int(H*scale)
work   = cv2.resize(src, (wW, wH), interpolation=cv2.INTER_AREA)

# ── GrabCut background removal ────────────────────────────────────────────────
print("Running GrabCut background removal …")
mask      = np.zeros(work.shape[:2], np.uint8)
bgd_model = np.zeros((1, 65), np.float64)
fgd_model = np.zeros((1, 65), np.float64)

# Rectangle that tightly brackets the dish (leave ~8% border as definite BG)
rx = int(wW * 0.06)
ry = int(wH * 0.05)
rw = int(wW * 0.88)
rh = int(wH * 0.90)
cv2.grabCut(work, mask, (rx, ry, rw, rh), bgd_model, fgd_model, 6, cv2.GC_INIT_WITH_RECT)

# Definite + probable foreground = 255
fg_mask = np.where((mask == 2) | (mask == 0), 0, 255).astype(np.uint8)

# Morphological cleanup
k3 = np.ones((7, 7),  np.uint8)
k5 = np.ones((13, 13), np.uint8)
fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE,  k5)
fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_DILATE, k3)
fg_mask = cv2.GaussianBlur(fg_mask, (9, 9), 0)
fg_mask = np.clip(fg_mask.astype(np.float32) * 1.4, 0, 255).astype(np.uint8)

rgb_work = cv2.cvtColor(work, cv2.COLOR_BGR2RGB)

# ── find food extent in the GrabCut mask ─────────────────────────────────────
rows = np.where((fg_mask > 50).sum(axis=1) > wW * 0.02)[0]
if len(rows) == 0:
    sys.exit("ERROR: GrabCut found no foreground — check the image.")
y_top, y_bot = int(rows[0]),  int(rows[-1])
dish_h = y_bot - y_top
print(f"Food extent: rows {y_top}–{y_bot}  ({dish_h}px of {wH}px working canvas)")

# ── output scale ─────────────────────────────────────────────────────────────
scale_out = OUT_SIZE / max(W, H)
nw, nh    = int(W * scale_out), int(H * scale_out)

# ── helpers ───────────────────────────────────────────────────────────────────
def make_rgba(rgb_src, alpha_src, y_a, y_b):
    """Zero out alpha outside zone [y_a, y_b], feather the cut edges."""
    alpha_zone = np.zeros_like(alpha_src)
    alpha_zone[y_a:y_b] = alpha_src[y_a:y_b]
    # Feather the horizontal cut lines so they don't look chopped
    feather = 18
    for dy in range(feather):
        t = dy / feather
        if y_a + dy < wH:
            alpha_zone[y_a + dy] = (alpha_zone[y_a + dy] * t).astype(np.uint8)
        if y_b - dy - 1 >= 0:
            alpha_zone[y_b - dy - 1] = (alpha_zone[y_b - dy - 1] * t).astype(np.uint8)
    return np.dstack([rgb_src, alpha_zone])

def save(rgba_work, name):
    pil  = Image.fromarray(rgba_work, "RGBA").resize((nw, nh), Image.LANCZOS)
    path = f"images/{name}.png"
    pil.save(path, "PNG", optimize=True)
    kb   = os.path.getsize(path) / 1024
    print(f"  ✓  {path}  →  {nw}×{nh}  ({kb:.0f} KB)")

# ── full dish ─────────────────────────────────────────────────────────────────
full_rgba = np.dstack([rgb_work, fg_mask])
save(full_rgba, "comp-dish-full")

# ── zone cuts — thirds of the detected food area ──────────────────────────────
# The dish is shot from above: top of image = top garnish, bottom = sauce/base
# Falling order: base (bottom) → chicken (middle) → greens (top)
cut_a = y_top + int(dish_h * 0.33)   # top of chicken zone
cut_b = y_top + int(dish_h * 0.66)   # top of base zone

zones = [
    # name,                ya,    yb     (in working-canvas coords)
    ("comp-zone-base",    cut_b, y_bot),  # bottom of dish — sauce + sweet potato
    ("comp-zone-chicken", cut_a, cut_b),  # center — chicken slices + veggies
    ("comp-zone-greens",  y_top, cut_a),  # top — green beans + cauliflower
]
for name, ya, yb in zones:
    rgba = make_rgba(rgb_work, fg_mask, ya, yb)
    save(rgba, name)

print("\n✅  Done — refresh the browser.")
