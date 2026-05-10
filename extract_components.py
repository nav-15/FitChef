#!/usr/bin/env python3
"""
Extracts 4 food components from roast-exploded.jpg with background removed.
Run AFTER saving the source image as images/roast-exploded.jpg
"""
import cv2
import numpy as np
from PIL import Image
import os, sys

SRC  = 'images/roast-exploded.jpg'
SIZE = 900  # output square size in pixels

def remove_bg(bgr, bright=220, sat=30):
    h, w = bgr.shape[:2]
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    hsv  = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)

    # Pixels that are bright AND low-saturation = white/grey background
    bg = ((gray > bright) & (hsv[:,:,1] < sat)).astype(np.uint8) * 255

    # Flood-fill from all 4 corners so only CONNECTED background is removed
    ff = bg.copy()
    for px, py in [(0,0),(w-1,0),(0,h-1),(w-1,h-1)]:
        if bg[py, px] > 0:
            cv2.floodFill(ff, None, (px, py), 128)
    alpha = np.where(ff == 128, 0, 255).astype(np.uint8)

    # Clean up stray pixels and soften edges
    k = np.ones((3,3), np.uint8)
    alpha = cv2.morphologyEx(alpha, cv2.MORPH_CLOSE, k)
    alpha = cv2.GaussianBlur(alpha, (3,3), 0)
    alpha = np.clip(alpha.astype(np.float32) * 1.2, 0, 255).astype(np.uint8)

    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    return np.dstack([rgb, alpha])          # RGBA

if not os.path.exists(SRC):
    sys.exit(f"ERROR: Save the exploded dish image as '{SRC}' first, then re-run.")

print(f"Loading {SRC} ...")
src = cv2.imread(SRC)
H, W = src.shape[:2]
print(f"Source: {W}x{H}px")

print("Removing background …")
rgba = remove_bg(src)

# ----- Crop zones (tuned for the 2048×2048 exploded-dish photo) -----
# Each component spans the FULL width so relative X positions are preserved.
# When all 4 PNGs are displayed at the same size at the same position they
# align naturally — no JS position math needed.
s = W / 2048          # scale factor if image isn't exactly 2048
zones = {
    'comp-veggie':  (int(0*s),    int(510*s)),   # green beans + orange veg
    'comp-chicken': (int(370*s),  int(890*s)),   # sliced chicken breast
    'comp-potato':  (int(650*s),  int(1290*s)),  # roast potato cubes
    'comp-plate':   (int(1060*s), H),            # plate + sauce (to bottom)
}

out = {}
for name, (y0, y1) in zones.items():
    strip = rgba[y0:y1, :].copy()          # full-width strip

    # Scale width to SIZE, height proportionally
    aspect  = strip.shape[1] / strip.shape[0]
    out_h   = max(1, round(SIZE / aspect))
    pil     = Image.fromarray(strip).resize((SIZE, out_h), Image.LANCZOS)

    path = f'images/{name}.png'
    pil.save(path, 'PNG', optimize=True)
    kb = os.path.getsize(path) / 1024
    out[name] = {'y0': y0, 'y1': y1, 'out_h': out_h}
    print(f"  ✓  {path}  →  {SIZE}×{out_h}  ({kb:.0f} KB)")

# Print CSS position hints (percentages of full 2048px height, for reference)
print("\nY positions in original image (% of height):")
for name, info in out.items():
    center_pct = ((info['y0']+info['y1'])/2) / H * 100
    print(f"  {name}: center at {center_pct:.1f}% of image")

print("\n✅  Done! Refresh the browser.")
