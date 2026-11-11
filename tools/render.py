"""Render RedGuy slides (.dc.html) to Instagram JPEGs.

Usage (from the repo root):
  python3 -I tools/render.py <slides_dir> <out_dir>
    Renders every NN-*.dc.html in <slides_dir> (sorted) to <out_dir>/NN.jpg at 1080x1350.
  python3 -I tools/render.py --story <slide.jpg> <out.jpg> "<top line>" "<bottom line>"
    Makes a 1080x1920 story image from a rendered slide.

Images in slides are referenced as /_blob/<id> (canvas ids) or assets/... paths; both map to files in this repo.
"""
import pathlib, re, shutil, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BLOBS = {
    "4de31f82ad4eca707d8d7ee0c37b510e": "assets/avatar.png",
    "89e14405c6c7147161b4d4ba422b1dd6": "assets/poses/crossed.png",
    "2ec7f5c2c9a6b2c7124998cb836f0f71": "assets/poses/flex.png",
    "5681d5b9e64701e6b624b64ead63e91a": "assets/poses/dumbbell.png",
    "c9d06982b8ed44a8310a8449c83c5146": "assets/poses/eating.png",
    "cc14a087fad864362fa9667122e8c1ca": "assets/poses/point.png",
    "4b84591bcca3a6410a11bcedd31d4ea1": "assets/poses/thumbsdown.png",
    "a1f83f1ae1435183cec52951d7405d5e": "assets/poses/thumbsup.png",
}
FONT = ROOT / "tools/archivo-black.woff2"


def chrome_path():
    for c in ("google-chrome", "chromium", "chromium-browser"):
        p = shutil.which(c)
        if p:
            return p
    return None


def render_slides(src: pathlib.Path, out: pathlib.Path):
    from playwright.sync_api import sync_playwright
    out.mkdir(parents=True, exist_ok=True)
    head = (f"<!doctype html><html><head><meta charset='utf-8'><style>"
            f"@font-face{{font-family:'Archivo Black';src:url('file://{FONT}') format('woff2');}}"
            f"body{{margin:0}}</style></head><body>")
    files = sorted(src.glob("*.dc.html"))
    with sync_playwright() as p:
        exe = chrome_path()
        b = p.chromium.launch(executable_path=exe, args=["--allow-file-access-from-files"]) if exe \
            else p.chromium.launch(args=["--allow-file-access-from-files"])
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for i, f in enumerate(files, 1):
            s = f.read_text()
            body = re.search(r"<x-dc>(.*)</x-dc>", s, re.S).group(1)
            body = re.sub(r"<helmet>.*?</helmet>", "", body, flags=re.S)
            for k, v in BLOBS.items():
                body = body.replace(f"/_blob/{k}", f"file://{ROOT / v}")
            body = re.sub(r'src="(assets/[^"]+)"', lambda m: f'src="file://{ROOT / m.group(1)}"', body)
            tmp = out / f"_{i:02d}.html"
            tmp.write_text(head + body + "</body></html>")
            pg.goto(f"file://{tmp}")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(300)
            pg.screenshot(path=str(out / f"{i:02d}.jpg"), type="jpeg", quality=92,
                          clip={"x": 0, "y": 0, "width": 1080, "height": 1350})
            tmp.unlink()
            print(out / f"{i:02d}.jpg")
        b.close()


def story(slide: str, dst: str, top: str, bottom: str):
    # 1080x1920: off-white ground, slide scaled to 960 wide in the middle, a line above and below.
    from playwright.sync_api import sync_playwright
    import html as h
    slide_p = pathlib.Path(slide).resolve()
    page = (f"<!doctype html><html><head><meta charset='utf-8'><style>"
            f"@font-face{{font-family:'Archivo Black';src:url('file://{FONT}') format('woff2');}}"
            f"body{{margin:0}}</style></head><body>"
            f"<div style=\"width:1080px;height:1920px;background:#F5F3EE;display:flex;flex-direction:column;"
            f"align-items:center;justify-content:center;gap:56px;font-family:'Archivo Black',sans-serif\">"
            f"<div style='font-size:84px;color:#EF2020;text-transform:uppercase'>{h.escape(top)}</div>"
            f"<img src='file://{slide_p}' style='width:960px;border:8px solid #111111;border-radius:32px'>"
            f"<div style='font-size:50px;color:#111111'>{h.escape(bottom)}</div></div></body></html>")
    tmp = pathlib.Path(dst).with_suffix(".html")
    tmp.write_text(page)
    with sync_playwright() as p:
        exe = chrome_path()
        b = p.chromium.launch(executable_path=exe, args=["--allow-file-access-from-files"]) if exe \
            else p.chromium.launch(args=["--allow-file-access-from-files"])
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto(f"file://{tmp.resolve()}")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(300)
        pg.screenshot(path=dst, type="jpeg", quality=92, clip={"x": 0, "y": 0, "width": 1080, "height": 1920})
        b.close()
    tmp.unlink()
    print(dst)


if __name__ == "__main__":
    if sys.argv[1] == "--story":
        story(*sys.argv[2:6])
    else:
        render_slides(pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]))
