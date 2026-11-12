"""Build a "workout" reel page (HTML) from a JSON spec, then render it with tools/reel.py.

Usage (from repo root):
  python3 -I tools/workout_reel.py <spec.json> <out.html>
  python3 -I tools/reel.py <out.html> <out.mp4> <seconds> 30

spec.json:
{
  "title": "The Push Workout",            # top title
  "subtitle": "Science-backed",           # small red tag
  "outro": ["Save it for", "push day."],  # end card, 2 lines (2nd in red)
  "exercises": [
    {"name": "Incline DB Press", "muscle": "Upper chest", "sets": "3 × 8–12",
     "why": "Incline shifts work to the upper chest", "source": "",   # source optional, short: "Maeo et al., 2023"
     "pose": "assets/poses/incline-press.png", "placeholder": false}
  ]
}
Timing: 1.4 s intro, 2.8 s per exercise, 2.4 s outro. The script prints the total seconds.
"""
import html, json, os, pathlib, sys

INTRO, STEP, OUTRO = 1.4, 2.8, 2.4


def main():
    spec = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    out = pathlib.Path(sys.argv[2]).resolve()
    root = pathlib.Path(__file__).resolve().parent.parent
    rel = lambda p: os.path.relpath(root / p, out.parent)
    ex = spec["exercises"]; n = len(ex)
    total = INTRO + STEP * n + OUTRO
    e = html.escape

    steps = "".join(
        f'<div class="st" id="st{i}"><span>{i + 1}</span></div>' + ('<div class="ln"></div>' if i < n - 1 else "")
        for i in range(n))

    scenes = []
    for i, x in enumerate(ex):
        s = INTRO + i * STEP
        src = f'<div class="src up" style="--w:{s + .9:.2f}s">{e(x["source"])}</div>' if x.get("source") else ""
        ph = (f'<div class="ph" style="top:{560}px">PLACEHOLDER POSE</div>' if x.get("placeholder") else "")
        scenes.append(f'''
<div class="scene" style="--s:{s:.2f}s;--d:{STEP:.2f}s">
  <div class="chip pop" style="--w:{s + .05:.2f}s">{e(x["muscle"]).upper()}</div>
  <img class="pose" src="{rel(x["pose"])}" style="--ps:{s + .05:.2f}s">
  {ph}
  <div class="txt">
    <div class="nm pop" style="--w:{s + .3:.2f}s">{e(x["name"])}</div>
    <div class="sets pop" style="--w:{s + .55:.2f}s">{e(x["sets"])}</div>
    <div class="why up" style="--w:{s + .8:.2f}s">{e(x["why"])}</div>
    {src}
  </div>
</div>''')

    o = INTRO + n * STEP
    a, b = spec.get("outro", ["Save it for", "later."])
    page = f'''<!doctype html>
<html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@600;800&display=swap" rel="stylesheet">
<style>
@font-face{{font-family:'Archivo Black';src:url('{rel("tools/archivo-black.woff2")}') format('woff2');}}
*{{box-sizing:border-box}}
body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:#F5F3EE;font-family:Inter,sans-serif;color:#111;position:relative}}
.red{{color:#EF2020}}
.title{{position:absolute;top:110px;left:0;right:0;text-align:center;font-family:'Archivo Black';font-size:78px;text-transform:uppercase;line-height:1}}
.tag{{position:absolute;top:205px;left:50%;transform:translateX(-50%);background:#EF2020;color:#fff;border-radius:999px;padding:8px 26px;font-size:28px;font-weight:800;letter-spacing:2px;white-space:nowrap}}
.steps{{position:absolute;top:290px;left:90px;right:90px;display:flex;align-items:center}}
.st{{width:78px;height:78px;border-radius:50%;border:6px solid #C9C5BC;background:#F5F3EE;display:flex;align-items:center;justify-content:center;font-family:'Archivo Black';font-size:34px;color:#B5B0A6;flex-shrink:0;transition:none}}
.st.cur{{border-color:#EF2020;color:#EF2020;transform:scale(1.15);box-shadow:0 0 0 8px rgba(239,32,32,.15)}}
.st.done{{border-color:#EF2020;background:#EF2020;color:#fff}}
.ln{{flex:1;height:6px;background:#C9C5BC}}
.ln.done{{background:#EF2020}}
.scene{{position:absolute;inset:0;opacity:0;animation:show var(--d) linear var(--s) both}}
@keyframes show{{0%{{opacity:0}}4%{{opacity:1}}96%{{opacity:1}}100%{{opacity:0}}}}
.chip{{position:absolute;top:420px;left:50%;margin-left:-200px;width:400px;text-align:center;background:#111;color:#fff;border-radius:999px;padding:12px 0;font-size:30px;font-weight:800;letter-spacing:2px}}
.pose{{position:absolute;top:500px;left:50%;height:760px;transform:translateX(-50%);animation:slidein .45s cubic-bezier(.2,1.3,.4,1) var(--ps) both}}
@keyframes slidein{{from{{transform:translateX(-50%) translateY(80px) scale(.9);opacity:0}}to{{transform:translateX(-50%);opacity:1}}}}
.ph{{position:absolute;left:50%;transform:translateX(-50%) rotate(-6deg);background:#FFE14D;border:4px dashed #111;padding:8px 20px;font-size:26px;font-weight:800;z-index:3}}
.txt{{position:absolute;top:1270px;left:90px;right:90px;text-align:center;display:flex;flex-direction:column;align-items:center;gap:8px}}
.nm{{font-family:'Archivo Black';font-size:68px;line-height:1.05}}
.sets{{font-family:'Archivo Black';font-size:56px;color:#EF2020}}
.why{{font-size:34px;font-weight:800;color:#333}}
.src{{font-size:24px;font-weight:600;color:#666}}
.pop{{animation:pop .35s cubic-bezier(.2,1.6,.4,1) var(--w) both}}
@keyframes pop{{from{{transform:scale(0);opacity:0}}to{{transform:none;opacity:1}}}}
.up{{animation:up .4s ease-out var(--w) both}}
@keyframes up{{from{{transform:translateY(40px);opacity:0}}to{{transform:none;opacity:1}}}}
.intro{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:20px;opacity:0;animation:show {INTRO:.2f}s linear 0s both}}
.intro .big{{font-family:'Archivo Black';font-size:110px;text-transform:uppercase;line-height:1;text-align:center}}
.outro{{position:absolute;inset:0;background:#111;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:40px;opacity:0;animation:show {OUTRO:.2f}s linear {o:.2f}s both;z-index:4}}
.outro .big{{font-family:'Archivo Black';font-size:104px;line-height:1.02;text-align:center}}
.outro img{{height:640px}}
.fol{{background:#EF2020;border-radius:999px;padding:20px 40px;font-size:40px;font-weight:800}}
.wm{{position:absolute;left:90px;top:1590px;display:flex;align-items:center;gap:16px;z-index:5}}
.wm img{{width:72px;height:72px}}
.wm div{{font-family:'Archivo Black';font-size:32px}}
.intro-hide{{opacity:1}}
</style></head><body>

<div id="head">
  <div class="title">{e(spec["title"])}</div>
  <div class="tag">{e(spec.get("subtitle", "SCIENCE-BACKED")).upper()}</div>
  <div class="steps">{steps}</div>
</div>

<div class="intro"><div class="big pop" style="--w:.1s">{n} exercises</div><div class="big pop red" style="--w:.45s">Save it.</div></div>

{"".join(scenes)}

<div class="outro">
  <img class="pop" style="--w:{o + .05:.2f}s" src="{rel("assets/poses/flex.png")}">
  <div class="big pop" style="--w:{o + .25:.2f}s">{e(a)}<br><span class="red">{e(b)}</span></div>
  <div class="fol pop" style="--w:{o + .5:.2f}s">Follow @redguy.fit</div>
</div>

<div class="wm"><img src="{rel("assets/avatar.png")}"><div><span class="red">RED</span><span id="guy">GUY</span></div></div>

<script>
const N={n}, INTRO={INTRO * 1000}, STEP={STEP * 1000};
window.setT=function(ms){{
  document.getAnimations().forEach(a=>{{a.pause();a.currentTime=ms;}});
  document.getElementById('guy').style.color = ms>={o*1000} ? '#fff' : '#111';
  const cur=Math.floor((ms-INTRO)/STEP);
  for(let i=0;i<N;i++){{
    const el=document.getElementById('st'+i);
    el.className='st'+(i<cur?' done':(i===cur&&ms>=INTRO?' cur':''));
    el.firstChild.textContent = i<cur ? '✓' : String(i+1);
    const ln=el.nextElementSibling; if(ln&&ln.classList.contains('ln')) ln.className='ln'+(i<cur?' done':'');
  }}
}};
</script>
</body></html>'''
    out.write_text(page, encoding="utf-8")
    print(f"{total:.1f}")


if __name__ == "__main__":
    main()
