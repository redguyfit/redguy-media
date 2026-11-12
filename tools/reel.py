"""Render a RedGuy reel (HTML with CSS animations + window.setT(ms)) to a 1080x1920 MP4.

Usage (from repo root):
  python3 -I tools/reel.py <reel.html> <out.mp4> [seconds=16] [fps=30]
Frames are captured deterministically by pausing all animations at each timestamp.
"""
import pathlib, subprocess, sys, tempfile


def main():
    src = pathlib.Path(sys.argv[1]).resolve()
    out = pathlib.Path(sys.argv[2]).resolve()
    secs = float(sys.argv[3]) if len(sys.argv) > 3 else 16
    fps = int(sys.argv[4]) if len(sys.argv) > 4 else 30
    from playwright.sync_api import sync_playwright
    with tempfile.TemporaryDirectory() as tmp, sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto(src.as_uri(), wait_until="networkidle")
        pg.evaluate("document.fonts.ready")
        n = int(secs * fps)
        for i in range(n):
            pg.evaluate(f"window.setT({i * 1000 / fps})")
            pg.screenshot(path=f"{tmp}/f{i:05d}.png")
        b.close()
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", f"{tmp}/f%05d.png",
                        "-f", "lavfi", "-t", str(secs), "-i", "anullsrc=r=44100:cl=stereo",
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-crf", "20",
                        "-c:a", "aac", "-shortest", "-movflags", "+faststart", str(out)], check=True)
    print(out)


if __name__ == "__main__":
    main()
