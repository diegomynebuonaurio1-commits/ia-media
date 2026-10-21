"""Base musicale lo-fi originale generata al computer (nessun copyright).
Uso: python3 tools/music.py uscita.wav durata_secondi [seme]"""
import sys, wave
import numpy as np
SR = 44100

def note(f, dur, kind="pad"):
    t = np.arange(int(SR * dur)) / SR
    if kind == "pad":
        w = sum(np.sin(2*np.pi*f*k*t + k) / k**1.6 for k in range(1, 6))
        env = np.minimum(1, t / 0.35) * np.exp(-t * 0.35)
    elif kind == "keys":
        w = np.sin(2*np.pi*f*t) + 0.3*np.sin(2*np.pi*2*f*t) + 0.12*np.sin(2*np.pi*3*f*t)
        env = np.minimum(1, t / 0.01) * np.exp(-t * 3.2)
    else:  # bass
        w = np.sin(2*np.pi*f*t) + 0.25*np.sin(2*np.pi*2*f*t)
        env = np.minimum(1, t / 0.02) * np.exp(-t * 1.8)
    return w * env

def lowpass(x, a=0.08):
    y = np.zeros_like(x); acc = 0.0
    # filtro a un polo veloce con numpy (blocchi)
    for i in range(0, len(x), 4096):
        seg = x[i:i+4096]; out = np.empty_like(seg)
        for j, v in enumerate(seg):
            acc += a * (v - acc); out[j] = acc
        y[i:i+4096] = out
    return y

def build(dur, seed=1):
    rng = np.random.default_rng(seed)
    bpm = 84; beat = 60 / bpm; bar = 4 * beat
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    progs = [[(60,64,67,71),(57,60,64,67),(53,57,60,64),(55,59,62,65)],   # Cmaj7 Am7 Fmaj7 G7
             [(57,60,64,67),(53,57,60,64),(60,64,67,71),(55,59,62,67)]]
    prog = progs[seed % len(progs)]
    n = int(SR * (dur + 2)); mix = np.zeros(n)
    t0, k = 0.0, 0
    while t0 < dur + 1:
        ch = prog[k % 4]; i0 = int(t0 * SR)
        for m in ch:
            s = note(hz(m), bar + 0.5, "pad") * 0.06
            mix[i0:i0+len(s)] += s[:n-i0]
        b = note(hz(ch[0] - 24), bar * 0.9, "bass") * 0.10
        mix[i0:i0+len(b)] += b[:n-i0]
        for st in range(8):                       # arpeggio di piano
            if rng.random() < 0.7:
                m = ch[rng.integers(0, 4)] + 12 * rng.integers(0, 2)
                s = note(hz(m), 1.2, "keys") * 0.07
                j = i0 + int(st * beat / 2 * SR); mix[j:j+len(s)] += s[:max(0, n-j)]
        for bt in range(4):                       # cassa morbida e hi-hat
            j = i0 + int(bt * beat * SR)
            if bt in (0, 2):
                tt = np.arange(int(0.25*SR)) / SR
                kick = np.sin(2*np.pi*(55 + 70*np.exp(-tt*25))*tt) * np.exp(-tt*14) * 0.22
                mix[j:j+len(kick)] += kick[:max(0, n-j)]
            for off in (0, beat/2):
                jj = j + int(off*SR); hl = int(0.04*SR)
                hat = rng.standard_normal(hl) * np.exp(-np.arange(hl)/SR*90) * 0.025
                mix[jj:jj+hl] += hat[:max(0, n-jj)]
        t0 += bar; k += 1
    mix = lowpass(mix, 0.45)
    crackle = (rng.random(n) < 0.0004) * rng.standard_normal(n) * 0.05   # fruscio vinile
    mix = mix + crackle + rng.standard_normal(n) * 0.0015
    mix = mix[:int(SR*dur)]
    fade = int(SR*1.2); mix[:fade] *= np.linspace(0, 1, fade); mix[-fade:] *= np.linspace(1, 0, fade)
    mix = mix / (np.abs(mix).max() + 1e-9) * 0.8
    return mix

def save(x, path):
    st = (np.stack([x, np.roll(x, 120)], 1) * 32767).astype("<i2")   # stereo leggero
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())

if __name__ == "__main__":
    out, dur = sys.argv[1], float(sys.argv[2]); seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    save(build(dur, seed), out); print("ok", out)
