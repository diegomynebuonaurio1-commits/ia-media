import json, sys, html, re
from playwright.sync_api import sync_playwright
HANDLE = "@ia.senzafuffa"
CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:#0a0e1a;color:#f5f6fa;font-family:Inter,'Noto Color Emoji',sans-serif;position:relative;overflow:hidden}
.b1,.b2{position:absolute;border-radius:50%;filter:blur(10px)}
.b1{width:820px;height:820px;background:radial-gradient(circle,rgba(34,211,166,.38),rgba(34,211,166,0) 62%);top:-260px;left:-280px}
.b2{width:900px;height:900px;background:radial-gradient(circle,rgba(124,92,255,.42),rgba(124,92,255,0) 62%);bottom:-330px;right:-300px}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);background-size:54px 54px}
.wrap{position:absolute;inset:96px 80px 170px 80px;display:flex;flex-direction:column;justify-content:center}
.hl{background:linear-gradient(transparent 58%,rgba(255,216,77,.85) 58%);color:#fff;padding:0 6px}
.grad{background:linear-gradient(90deg,#22d3a6,#8b7bff);-webkit-background-clip:text;color:transparent}
.foot{position:absolute;left:80px;right:80px;bottom:62px}
.bar{display:flex;gap:8px;margin-bottom:22px}.bar i{flex:1;height:7px;border-radius:9px;background:rgba(255,255,255,.16)}.bar i.on{background:#22d3a6}
.fr{display:flex;justify-content:space-between;align-items:center;font-size:29px;font-weight:700;color:#d6dae6}
.swipe{background:#fff;color:#0a0e1a;padding:12px 26px;border-radius:999px;font-weight:800}
/* cover */
.sticker{align-self:flex-start;transform:rotate(-4deg);background:#ffd84d;color:#1a1400;font-weight:900;font-size:40px;padding:14px 28px;border-radius:14px;box-shadow:0 10px 0 #b8941f;margin-bottom:48px}
.huge{font-family:'Inter Display',Inter;font-weight:900;font-size:220px;line-height:.9;letter-spacing:-8px;word-break:keep-all;overflow-wrap:normal;white-space:nowrap}
.cov2{font-family:'Inter Display',Inter;font-weight:800;font-size:76px;line-height:1.06;letter-spacing:-2px;margin-top:18px}
.covsub{font-size:42px;color:#c9cfdd;margin-top:40px;line-height:1.35;font-weight:500}
.chips{display:flex;gap:16px;margin-top:46px}.chip{background:rgba(255,255,255,.08);border:2px solid rgba(255,255,255,.16);border-radius:999px;padding:12px 24px;font-size:30px;font-weight:600}
/* slide prompt */
.top{display:flex;align-items:center;gap:26px;margin-bottom:30px}
.num{width:118px;height:118px;border-radius:30px;background:linear-gradient(135deg,#22d3a6,#7c5cff);display:flex;align-items:center;justify-content:center;font-family:'Inter Display';font-weight:900;font-size:66px;color:#fff;box-shadow:0 14px 40px rgba(124,92,255,.45)}
.emo{font-size:92px}
.title{font-family:'Inter Display',Inter;font-weight:800;font-size:64px;line-height:1.1;letter-spacing:-1.5px;margin-bottom:38px}
.chat{background:#151a2b;border:2px solid #2a3150;border-radius:30px;overflow:hidden;box-shadow:0 30px 60px rgba(0,0,0,.45)}
.chat .hd{display:flex;gap:10px;padding:18px 24px;border-bottom:2px solid #232a44;align-items:center}
.chat .hd i{width:16px;height:16px;border-radius:50%;background:#ff5f57}.chat .hd i:nth-child(2){background:#febc2e}.chat .hd i:nth-child(3){background:#28c840}
.chat .hd span{margin-left:14px;color:#8a92ad;font-size:24px;font-weight:600}
.msg{margin:28px 28px 18px auto;max-width:92%;background:#2b3459;border-radius:26px 26px 6px 26px;padding:28px 32px;font-size:33px;line-height:1.42;color:#eef0f8}
.msg b{color:#ffd84d;font-weight:700}
.typing{margin:0 28px 26px;color:#8a92ad;font-size:26px;font-weight:600}
.badges{display:flex;gap:16px;margin-top:30px;flex-wrap:wrap}
.bdg{border-radius:999px;padding:12px 24px;font-size:29px;font-weight:700}
.bdg.t{background:rgba(34,211,166,.16);color:#5ef0c8;border:2px solid rgba(34,211,166,.5)}
.bdg.p{background:rgba(124,92,255,.18);color:#b9adff;border:2px solid rgba(124,92,255,.55)}
/* end */
.endt{font-family:'Inter Display',Inter;font-weight:900;font-size:104px;line-height:1.02;letter-spacing:-3px}
.cm{display:flex;gap:22px;align-items:center;background:#151a2b;border:2px solid #2a3150;border-radius:28px;padding:30px 34px;margin:52px 0 40px}
.av{width:84px;height:84px;border-radius:50%;background:linear-gradient(135deg,#ffd84d,#ff7a59);flex:none}
.cm .u{font-size:28px;color:#8a92ad;font-weight:600}.cm .t{font-size:60px;font-weight:900;color:#fff;letter-spacing:1px}
.cm .h{margin-left:auto;font-size:52px}
.ends{font-size:42px;color:#c9cfdd;line-height:1.4;font-weight:500}
"""
def mark(t):
    t = html.escape(t)
    return re.sub(r"\*([^*]+)\*", r"<span class='hl'>\1</span>", t)
def fprompt(t):
    return re.sub(r"\[([^\]]+)\]", r"<b>[\1]</b>", html.escape(t))
def page(inner, n, tot):
    bar = "".join(f"<i class='{'on' if k<=n else ''}'></i>" for k in range(1, tot+1))
    right = "<span class='swipe'>Scorri →</span>" if n < tot else "<span>💾 Salva · 📩 Condividi</span>"
    return (f"<html><head><style>{CSS}</style></head><body><div class='grid'></div><div class='b1'></div><div class='b2'></div>"
            f"<div class='wrap'>{inner}</div><div class='foot'><div class='bar'>{bar}</div><div class='fr'><span>{HANDLE}</span>{right}</div></div></body></html>")
def build(spec, outdir):
    c = spec["cover"]; s = []
    s.append(f"<div class='sticker'>{c['sticker']}</div><div class='huge grad'>{c['huge']}</div><div class='cov2'>{mark(c['line'])}</div>"
             f"<div class='covsub'>{c['sub']}</div><div class='chips'>" + "".join(f"<span class='chip'>{x}</span>" for x in c['chips']) + "</div>")
    for i, p in enumerate(spec["items"], 1):
        s.append(f"<div class='top'><div class='num'>{i}</div><div class='emo'>{p['emoji']}</div></div><div class='title'>{mark(p['title'])}</div>"
                 f"<div class='chat'><div class='hd'><i></i><i></i><i></i><span>Copia questo prompt</span></div><div class='msg'>{fprompt(p['prompt'])}</div>"
                 f"<div class='typing'>✨ L'IA sta scrivendo…</div></div><div class='badges'><span class='bdg t'>⏱ {p['time']}</span><span class='bdg p'>{p['for']}</span></div>")
    e = spec["end"]
    s.append(f"<div class='endt'>{mark(e['title'])}</div><div class='cm'><div class='av'></div><div><div class='u'>tu · adesso</div><div class='t'>{e['kw']}</div></div><div class='h'>❤️</div></div>"
             f"<div class='ends'>{e['sub']}</div>")
    tot = len(s)
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={"width":1080,"height":1350})
        for i, inner in enumerate(s, 1):
            pg.set_content(page(inner, i, tot)); pg.wait_for_timeout(250)
            pg.evaluate("""()=>{for(const el of document.querySelectorAll('.huge,.title,.endt')){let s=parseFloat(getComputedStyle(el).fontSize);const W=el.parentElement.clientWidth;while(el.scrollWidth>W+1&&s>40){s-=4;el.style.fontSize=s+'px';}}}""")
            if pg.evaluate("(()=>{const w=document.querySelector('.wrap');return w.scrollHeight>w.clientHeight+2})()"):
                print("TROPPO LUNGO slide", i)
            pg.screenshot(path=f"{outdir}/slide_{i:02d}.png")
        b.close()
    print("ok", tot)
if __name__ == "__main__":
    build(json.load(open(sys.argv[1])), sys.argv[2])
