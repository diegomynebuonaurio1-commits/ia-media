"""Crea un reel verticale 1080x1920 (circa 25 s, con musica originale) da uno spec di carosello.
Uso: python3 tools/make_reel.py postNN/spec.json postNN/reel.mp4 [numero_prompt=4]"""
import json, os, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(__file__))
import make_carousel as mc
from playwright.sync_api import sync_playwright

V_CSS = """body{height:1920px}
.wrap{inset:300px 80px 430px 80px}
.foot{bottom:300px}
.huge{font-size:240px}.title{font-size:70px}.msg{font-size:36px}"""

def frames(spec, n_items, outdir):
    c = spec["cover"]; items = spec["items"][:n_items]; e = spec["end"]
    s = [f"<div class='sticker'>{c['sticker']}</div><div class='huge grad'>{c['huge']}</div><div class='cov2'>{mc.mark(c['line'])}</div>"
         f"<div class='covsub'>{c['sub']}</div>"]
    for i, p in enumerate(items, 1):
        s.append(f"<div class='top'><div class='num'>{i}</div><div class='emo'>{p['emoji']}</div></div><div class='title'>{mc.mark(p['title'])}</div>"
                 f"<div class='chat'><div class='hd'><i></i><i></i><i></i><span>Copia questo prompt</span></div><div class='msg'>{mc.fprompt(p['prompt'])}</div>"
                 f"<div class='typing'>✨ L'IA sta scrivendo…</div></div><div class='badges'><span class='bdg t'>⏱ {p['time']}</span><span class='bdg p'>{p['for']}</span></div>")
    s.append(f"<div class='endt'>{mc.mark(e['title'])}</div><div class='cm'><div class='av'></div><div><div class='u'>tu · adesso</div><div class='t'>{e['kw']}</div></div><div class='h'>❤️</div></div>"
             f"<div class='ends'>{e['sub'].replace('Scrivilo nei commenti 👆','Scrivilo nei commenti 👇')}</div>")
    paths = []
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
        for i, inner in enumerate(s, 1):
            html = mc.page(inner, i, len(s)).replace("</style>", V_CSS + "</style>").replace("<span class='swipe'>Scorri →</span>", "<span class='swipe'>Salva il reel 💾</span>")
            pg.set_content(html); pg.wait_for_timeout(250)
            pg.evaluate("""()=>{for(const el of document.querySelectorAll('.huge,.title,.endt')){let s=parseFloat(getComputedStyle(el).fontSize);const W=el.parentElement.clientWidth;while(el.scrollWidth>W+1&&s>40){s-=4;el.style.fontSize=s+'px';}}}""")
            if pg.evaluate("(()=>{const w=document.querySelector('.wrap');return w.scrollHeight>w.clientHeight+2})()"):
                print("TROPPO LUNGO frame", i)
            p = os.path.join(outdir, f"f{i:02d}.png"); pg.screenshot(path=p); paths.append(p)
        b.close()
    return paths

def video(paths, out, durs):
    fade = 0.4
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for p, d in zip(paths, durs):
        cmd += ["-loop", "1", "-t", f"{d}", "-i", p]
    fl, prev, t = [], "0:v", 0.0
    for i in range(1, len(paths)):
        t += durs[i - 1] - fade
        lab = f"v{i}"
        fl.append(f"[{prev}][{i}:v]xfade=transition=slideleft:duration={fade}:offset={t:.2f}[{lab}]")
        prev = lab
    fl.append(f"[{prev}]format=yuv420p,fps=30[out]")
    cmd += ["-filter_complex", ";".join(fl), "-map", "[out]", "-c:v", "libx264", "-profile:v", "high",
            "-crf", "20", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    spec = json.load(open(sys.argv[1])); out = sys.argv[2]
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    with tempfile.TemporaryDirectory() as d:
        ps = frames(spec, n, d)
        durs = [3.0] + [5.0] * (len(ps) - 2) + [4.0]
        muto = os.path.join(d, "muto.mp4")
        video(ps, muto, durs)
        # base musicale originale (nessun copyright), diversa per ogni reel
        import zlib, music
        wav = os.path.join(d, "musica.wav")
        music.save(music.build(sum(durs) - 0.4 * (len(durs) - 1), zlib.crc32(out.encode()) % 1000), wav)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", muto, "-i", wav, "-c:v", "copy",
                        "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", out], check=True)
        cover = os.path.splitext(out)[0] + "_cover.jpg"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", ps[0], "-q:v", "2", cover], check=True)
    print("ok", out)
