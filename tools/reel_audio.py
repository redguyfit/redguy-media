"""Make an original soundtrack for a RedGuy reel: synthesized beat + sound effects synced to the animation.

Usage (from repo root):
  python3 -I tools/reel_audio.py <reel.html> <out.wav> [seconds=16]
Cues are read from the HTML: every .pose (--ps) gets a whoosh, every .pop (--w) a pop,
the #cnt counter (6.6–7.5 s) gets ticks. All audio is generated here, so no licensing issues.
"""
import re, sys, wave
import numpy as np

SR = 44100


def env(n, a=0.002, d=0.2):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-t / d)


def kick():
    n = int(SR * .35); t = np.arange(n) / SR
    f = 50 + 110 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, .001, .12)


def snare(rng):
    n = int(SR * .2); t = np.arange(n) / SR
    return (rng.standard_normal(n) * .6 + np.sin(2 * np.pi * 190 * t) * .4) * env(n, .001, .06)


def hat(rng):
    n = int(SR * .05)
    x = rng.standard_normal(n); x = np.diff(x, prepend=0)
    return x * env(n, .0005, .012) * .5


def bass(freq, dur):
    n = int(SR * dur); t = np.arange(n) / SR
    x = np.sign(np.sin(2 * np.pi * freq * t)) * .3 + np.sin(2 * np.pi * freq * t) * .7
    return x * env(n, .005, dur * .6)


def pad(freqs, dur):
    n = int(SR * dur); t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * f * t + np.sin(2 * np.pi * .3 * t)) for f in freqs) / len(freqs)
    return x * np.minimum(1, t / .3) * np.minimum(1, (dur - t) / .3)


def whoosh(rng):
    n = int(SR * .45); t = np.arange(n) / SR
    x = rng.standard_normal(n)
    k = np.exp(-((t - .18) / .12) ** 2)
    # crude band movement: blend of smoothed noise
    sm = np.convolve(x, np.ones(8) / 8, 'same')
    return (sm * k) * .9


def pop():
    n = int(SR * .09); t = np.arange(n) / SR
    f = 900 + 900 * np.exp(-t * 60)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, .001, .03)


def tick():
    n = int(SR * .03); t = np.arange(n) / SR
    return np.sin(2 * np.pi * 2200 * t) * env(n, .0005, .006)


def add(buf, x, at, g):
    i = int(at * SR)
    if i >= len(buf): return
    x = x[: len(buf) - i]; buf[i:i + len(x)] += x * g


def main():
    html = open(sys.argv[1], encoding='utf-8').read()
    out = sys.argv[2]
    secs = float(sys.argv[3]) if len(sys.argv) > 3 else 16
    rng = np.random.default_rng(7)
    music = np.zeros(int(SR * secs)); sfx = np.zeros_like(music)
    bpm = 120; beat = 60 / bpm
    # A minor: Am F C G, one bar (4 beats) each
    roots = [55.0, 43.65, 65.41, 49.0]
    chords = [[220, 261.6, 329.6], [174.6, 220, 261.6], [261.6, 329.6, 392], [196, 246.9, 293.7]]
    nb = int(secs / beat)
    for b in range(nb):
        t = b * beat; bar = (b // 4) % 4
        add(music, kick(), t, .9)
        if b % 2 == 1: add(music, snare(rng), t, .45)
        add(music, hat(rng), t + beat / 2, .35); add(music, hat(rng), t, .2)
        add(music, bass(roots[bar], beat * .9), t, .35)
        if b % 4 == 0: add(music, pad(chords[bar], beat * 4), t, .12)
    for m in re.finditer(r'class="pose"[^>]*--ps:([\d.]+)s', html):
        add(sfx, whoosh(rng), float(m.group(1)) - .1, .5)
    for m in re.finditer(r'class="[^"]*pop[^"]*"[^>]*--w:([\d.]+)s', html):
        add(sfx, pop(), float(m.group(1)) + .05, .5)
    if 'id="cnt"' in html:
        for i in range(10):
            add(sfx, tick(), 6.6 + i * .09, .35)
    mix = music * .55 + sfx
    fade = int(SR * 1.2); mix[-fade:] *= np.linspace(1, 0, fade)
    mix[:int(SR * .05)] *= np.linspace(0, 1, int(SR * .05))
    mix = mix / (np.abs(mix).max() + 1e-9) * .89
    pcm = (np.repeat(mix[:, None], 2, 1) * 32767).astype('<i2')
    with wave.open(out, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    print(out)


if __name__ == '__main__':
    main()
