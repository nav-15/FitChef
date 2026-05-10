#!/usr/bin/env python3
"""
Extracts food components from 'ROAST CHECKING .jpg' via color segmentation.
Each output PNG is the same canvas size — they stack naturally when overlaid at
the same position in the browser (no JS position math needed).

Components produced:
  comp-plate.png    — the plate disc (CSS-circle not needed)
  comp-sauce.png    — dark brown gravy / sauce base
  comp-potato.png   — sweet potato + carrots (orange)
  comp-chicken.png  — sliced chicken breast (beige/neutral)
  comp-greens.png   — green beans + cauliflower (greens / whites)
  comp-dish-full.png — full dish, background removed (used for reveal moment)

Run from fitchef-landing/:
  python3 extract_from_dish.py
"""
import cv2, numpy as np, os, sys
from PIL import Image

SRC      = "images/ROAST CHECKING .jpg"
OUT_SIZE = 1000   # longest dimension in output PNGs
WORK_W   = 1600   # internal working resolution (speed vs. quality)

# ── helpers ──────────────────────────────────────────────────────────────────

def remove_bg(bgr, bright=230, sat=18):
    """Flood-fill from all 4 corners to kill white/grey studio background."""
    h, w = bgr.shape[:2]
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    hsv  = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    bg   = ((gray > bright) & (hsv[:,:,1] < sat)).astype(np.uint8) * 255
    ff   = bg.copy()
    for px, py in [(0,0),(w-1,0),(0,h-1),(w-1,h-1)]:
        if bg[py,px] > 0:
            cv2.floodFill(ff, None, (px,py), 128)
    alpha = np.where(ff==128, 0, 255).astype(np.uint8)
    k = np.ones((9,9), np.uint8)
    alpha = cv2.morphologyEx(alpha, cv2.MORPH_CLOSE,  k)
    alpha = cv2.morphologyEx(alpha, cv2.MORPH_ERODE,  np.ones((3,3),np.uint8))
    alpha = cv2.GaussianBlur(alpha, (5,5), 0)
    return np.clip(alpha.astype(np.float32)*1.3, 0, 255).astype(np.uint8)

def color_mask(hsv, ranges, dilate_k=25):
    """Union of HSV range masks, morphologically cleaned."""
    mask = np.zeros(hsv.shape[:2], np.uint8)
    for lo, hi in ranges:
        mask = cv2.bitwise_or(mask, cv2.inRange(hsv, np.array(lo), np.array(hi)))
    k = np.ones((dilate_k, dilate_k), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE,  k)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((dilate_k//2+1,dilate_k//2+1),np.uint8))
    return mask

def build_rgba(rgb, food_mask, bg_alpha):
    """Combine food-color mask with bg-removed alpha, feather edges."""
    alpha = np.where((bg_alpha > 80) & (food_mask > 80), 255, 0).astype(np.uint8)
    alpha = cv2.morphologyEx(alpha, cv2.MORPH_CLOSE, np.ones((15,15),np.uint8))
    alpha = cv2.GaussianBlur(alpha, (7,7), 0)
    return np.dstack([rgb, alpha])

def save(rgba, name, nw, nh):
    pil  = Image.fromarray(rgba).resize((nw, nh), Image.LANCZOS)
    path = f"images/{name}.png"
    pil.save(path, "PNG", optimize=True)
    kb   = os.path.getsize(path)/1024
    print(f"  ✓  {path}  →  {nw}×{nh}  ({kb:.0f} KB)")

# ── load & downscale for processing ──────────────────────────────────────────

if not os.path.exists(SRC):
    sys.exit(f"ERROR: '{SRC}' not found — run from fitchef-landing/")

print(f"Loading {SRC} …")
src_full = cv2.imread(SRC)
H, W     = src_full.shape[:2]
print(f"Source: {W}×{H}px")

# Downscale for processing speed
scale_w = WORK_W / W
work    = cv2.resize(src_full, (WORK_W, int(H*scale_w)), interpolation=cv2.INTER_AREA)
rgb     = cv2.cvtColor(work, cv2.COLOR_BGR2RGB)
hsv     = cv2.cvtColor(work, cv2.COLOR_BGR2HSV)
wH, wW  = work.shape[:2]

# Output canvas size
scale_out = OUT_SIZE / max(W, H)
nw, nh   = int(W*scale_out), int(H*scale_out)

# ── background mask ───────────────────────────────────────────────────────────
print("Removing background …")
bg_alpha = remove_bg(work)

# ── full dish ─────────────────────────────────────────────────────────────────
full_rgba = np.dstack([rgb, bg_alpha])
save(full_rgba, "comp-dish-full", nw, nh)

# ── component definitions  (name, [(lo_hsv, hi_hsv), …], dilate_k) ──────────
# HSV ranges tuned for this specific roast-chicken-on-grey-plate image:
#   Hue 0-180, Saturation 0-255, Value 0-255
COMPONENTS = [
    # Dark brown gravy/sauce — low-V, moderate-S, warm hue
    ("comp-sauce",   [([5,  60, 30], [20, 200, 110])],         20),
    # Orange sweet potato + carrot pieces
    ("comp-potato",  [([7, 130, 100], [22, 255, 230])],        22),
    # Sliced chicken breast — pale beige/greyish, low saturation
    ("comp-chicken", [([5,  15,  90], [25,  70, 210]),
                      ([0,   0, 110], [ 5,  30, 200])],        24),
    # Green beans (bright green) + cauliflower florets (off-white / very low sat)
    ("comp-greens",  [([32,  50, 50], [85, 255, 200]),         # green beans
                      ([0,    5,170], [40,  45, 255])],        18),  # cauliflower
]

for cname, ranges, dk in COMPONENTS:
    print(f"Extracting {cname} …")
    fmask = color_mask(hsv, ranges, dk)
    rgba  = build_rgba(rgb, fmask, bg_alpha)
    save(rgba, cname, nw, nh)

print("\n✅  Done — refresh the browser to see the animation.")
