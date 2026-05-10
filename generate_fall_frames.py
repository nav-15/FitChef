#!/usr/bin/env python3
"""
Generates 6 sequential falling-dish animation frames from the zone PNG layers.

Frame 1 — only the plate/base visible (chicken + greens above the viewport)
Frame 6 — all layers at their natural exploded positions (full dish revealed)

After running, the frames can be replaced with your own photos by saving them
as fall-frame-1.jpg … fall-frame-6.jpg inside the images/ folder.

Usage:  python generate_fall_frames.py   (run from fitchef-landing/)
"""
from PIL import Image
import os, sys

IMG_DIR  = "images"
N_FRAMES = 6

# (layer filename, max_upward_shift_as_fraction_of_canvas_height)
#   0.0 = layer stays in place   |   1.0 = layer starts fully off the top
LAYERS = [
    ("comp-zone-base.png",    0.00),   # plate + potatoes + sauce — stays in place
    ("comp-zone-chicken.png", 0.42),   # chicken breast  — falls from above
    ("comp-zone-greens.png",  0.68),   # garden greens   — falls furthest
]

# ── Load layers ───────────────────────────────────────────────────────────────
print("Loading zone layers…")
imgs, maxShifts = [], []
for fname, sh in LAYERS:
    p = os.path.join(IMG_DIR, fname)
    if not os.path.exists(p):
        sys.exit(f"\nERROR  —  '{p}' not found.\nRun this script from the fitchef-landing/ directory.\n")
    im = Image.open(p).convert("RGBA")
    imgs.append(im)
    maxShifts.append(sh)
    print(f"  {fname}: {im.size}")

W, H = imgs[0].size
print(f"Canvas: {W}×{H}\n")

# ── Generate frames ───────────────────────────────────────────────────────────
for i in range(N_FRAMES):
    # t = 0  →  most separated (frame 1, layers high up)
    # t = 1  →  natural position (frame 6, full exploded dish)
    t = i / (N_FRAMES - 1)

    # White RGBA background
    canvas = Image.new("RGBA", (W, H), (255, 255, 255, 255))

    for im, sh in zip(imgs, maxShifts):
        shift_up = int(sh * H * (1.0 - t))   # pixels to shift up from natural pos
        canvas.paste(im, (0, -shift_up), im)

    # Flatten to RGB (white bg)
    out = Image.new("RGB", (W, H), (255, 255, 255))
    out.paste(canvas, mask=canvas.split()[3])

    out_path = os.path.join(IMG_DIR, f"fall-frame-{i + 1}.jpg")
    out.save(out_path, "JPEG", quality=94, optimize=True)
    print(f"  Saved  {out_path}")

print(f"\n✓  {N_FRAMES} frames generated in {IMG_DIR}/")
print()
print("To use your own photos instead:")
print("  Save them as  images/fall-frame-1.jpg  through  images/fall-frame-6.jpg")
print("  Frame 1 = dish most separated / falling in   |   Frame 6 = fully assembled")
