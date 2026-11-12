"""Remove a baked-in white/grey checkerboard (fake transparency) from a pose image and save a real transparent PNG.

Usage: python3 -I tools/cutout.py <in.jpg|png> <out.png>
Works because the character art has bold black outlines and no light grey/white areas.
"""
import sys
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

im = Image.open(sys.argv[1]).convert("RGB")
a = np.asarray(im).astype(int)
mn, mx = a.min(2), a.max(2)
low_sat = (mx - mn) <= 28
bg = low_sat & (mn >= 165)
# grow background over light-ish grey JPEG fringe next to it (stops at the black outline)
fringe = low_sat & (mn >= 105)
for _ in range(2):
    bg = bg | (ndimage.binary_dilation(bg) & fringe)
# remove tiny specks of leftover foreground
fg = ~bg
lab, n = ndimage.label(fg)
sizes = ndimage.sum(fg, lab, range(1, n + 1))
keep = np.isin(lab, 1 + np.flatnonzero(sizes >= 400))
alpha = Image.fromarray((keep * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(0.6))
out = im.convert("RGBA"); out.putalpha(alpha)
out = out.crop(out.getbbox())
out.save(sys.argv[2])
print(sys.argv[2], out.size)
