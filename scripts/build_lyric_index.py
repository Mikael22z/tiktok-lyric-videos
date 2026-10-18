"""Gera o index.html (HyperFrames) de um lyric video vertical da série.

Layout: fundo preto, clipe 16:9 centralizado, título acima, letra dentro do clipe.
Entradas: letra cronometrada (align_lyrics.py) e pontos de grave (punches).

Uso:
  python3 build_lyric_index.py --lyrics work/lyrics_timed.json --punches work/punches.json \
      --title "Vivendo Avançado" --artist "Filipe Ret · BK' · MC TH" --duration 80 \
      --out projeto/index.html
"""
import argparse, html, json

ap = argparse.ArgumentParser()
ap.add_argument("--lyrics", required=True)
ap.add_argument("--punches", required=True)
ap.add_argument("--title", required=True)
ap.add_argument("--artist", required=True)
ap.add_argument("--duration", type=float, required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--font-file", default="assets/fonts/Syne-ExtraBold.woff2", help="caminho relativo ao projeto")
ap.add_argument("--font-family", default="Syne ExtraBold")
ap.add_argument("--font-scale", type=float, default=0.78, help="1.0 = tamanhos pensados para a Excalibur Nouveau")
a = ap.parse_args()
px = lambda v: f"{round(v * a.font_scale)}px"

lyrics = json.load(open(a.lyrics, encoding="utf-8"))
punches = json.load(open(a.punches))

# Canvas 1080x1920; clipe 1080x608 com centro em y=860 (dentro das safe zones do TikTok)
STAGE_TOP = 556

phrases_html = []
for i, p in enumerate(lyrics):
    words = "".join(
        f'<span class="w {w["kind"]}" id="p{i}w{j}">{html.escape(w["text"])}</span>'
        for j, w in enumerate(p["words"])
    )
    phrases_html.append(f'<div class="phrase" id="p{i}">{words}</div>')

page = f"""<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      @font-face {{
        font-family: "{a.font_family}";
        src: url("{a.font_file}") format("woff2");
      }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
      #root {{
        position: relative; width: 100%; height: 100%; overflow: hidden; background: #000;
        font-family: "{a.font_family}", sans-serif; color: #fff;
      }}
      #title {{
        position: absolute; left: 0; right: 0; top: 330px; display: flex; flex-direction: column;
        align-items: center; gap: 10px;
      }}
      #title-main {{ display: block; max-width: 900px; font-size: {px(92)}; line-height: 0.92; color: #e3121f; letter-spacing: 0.01em; text-align: center; }}
      #title-sub {{ display: block; font-size: {px(40)}; line-height: 1; text-align: center; color: #fff; opacity: 0.85; }}
      #stage {{ position: absolute; left: 0; top: {STAGE_TOP}px; width: 1080px; height: 608px; overflow: hidden; }}
      #frame {{ position: absolute; inset: 0; transform-origin: 50% 45%; }}
      #pic {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
      #shade {{
        position: absolute; inset: 0;
        background: linear-gradient(180deg, rgba(0,0,0,0) 35%, rgba(0,0,0,0.6) 100%);
      }}
      #flash {{ position: absolute; inset: 0; background: #fff; opacity: 0; }}
      .phrase {{
        position: absolute; left: 0; right: 0; bottom: 36px; padding: 0 140px;
        display: flex; flex-wrap: wrap; justify-content: center; align-items: baseline;
        column-gap: {px(20)}; row-gap: 0; opacity: 0;
      }}
      .w {{
        display: inline-block; font-size: {px(64)}; line-height: 1.05; color: #fff; opacity: 0;
        text-shadow: 0 3px 4px rgba(0,0,0,0.9), 0 0 22px rgba(0,0,0,0.75);
        transform-origin: 50% 70%;
      }}
      .w.red, .w.zoom {{ color: #e3121f; font-size: {px(84)}; }}
      .w.zoom {{ font-size: {px(100)}; }}
      .w.censor {{ color: #fff; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{a.duration:g}"
         data-width="1080" data-height="1920">
      <div id="title">
        <span id="title-main">{html.escape(a.title.upper())}</span>
        <span id="title-sub">{html.escape(a.artist)}</span>
      </div>
      <div id="stage">
        <div id="frame" data-layout-allow-overflow>
          <video id="pic" class="clip" src="assets/picture.mp4" muted playsinline
                 data-start="0" data-duration="{a.duration:g}" data-track-index="0"></video>
        </div>
        <div id="shade"></div>
        <div id="flash"></div>
        {"".join(phrases_html)}
      </div>
      <audio id="music" src="assets/music.m4a" data-start="0" data-duration="{a.duration:g}"
             data-track-index="1" data-volume="1"></audio>
    </div>
    <script>
      const LYRICS = {json.dumps(lyrics, ensure_ascii=False)};
      const PUNCHES = {json.dumps(punches)};
      const DUR = {a.duration:g};
      const tl = gsap.timeline({{ paused: true }});
      const IR = {{ immediateRender: false }};

      // Título: entra com zoom no primeiro segundo
      tl.fromTo("#title-main", {{ scale: 1.9, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.55, ease: "expo.out" }}, 0.05);
      tl.fromTo("#title-sub", {{ y: 14, opacity: 0 }}, {{ y: 0, opacity: 0.85, duration: 0.4, ease: "power2.out" }}, 0.45);

      // Grave: alterna enquadramento (aberto/fechado) + pulso de zoom + flash.
      // Durações são cortadas antes do evento seguinte para nunca sobrepor tweens.
      const ZOOMS = LYRICS.flatMap((p) => p.words.filter((w) => w.kind === "zoom").map((w) => w.t));
      const fit = (times, t, d) => {{ const n = times.find((x) => x > t + 1e-3); return n === undefined ? d : Math.min(d, n - t - 0.01); }};
      const FLASH = [...new Set([...PUNCHES, ...ZOOMS].map((t) => +t.toFixed(3)))].sort((a, b) => a - b);
      FLASH.forEach((t) => {{
        const strong = ZOOMS.includes(t);
        tl.fromTo("#flash", {{ opacity: strong ? 0.35 : 0.3 }}, {{ opacity: 0, duration: fit(FLASH, t, strong ? 0.2 : 0.16), ease: "power1.out", ...IR }}, t);
      }});
      tl.set("#frame", {{ scale: 1, x: 0 }}, 0);
      PUNCHES.forEach((t, i) => {{
        const base = i % 2 === 0 ? 1.16 : 1.0;
        tl.fromTo("#frame", {{ scale: base * 1.07 }}, {{ scale: base, duration: fit(PUNCHES, t, 0.32), ease: "power3.out", ...IR }}, t);
      }});
      ZOOMS.forEach((t) => {{
        tl.fromTo("#frame", {{ x: -10 }}, {{ x: 0, duration: fit(ZOOMS, t, 0.24), ease: "elastic.out(1.2, 0.3)", ...IR }}, t);
      }});

      // Letra: frase aparece e cada palavra entra quando é cantada
      LYRICS.forEach((p, i) => {{
        const next = LYRICS[i + 1];
        const show = Math.max(0, p.words[0].t - 0.1);
        let hide = next ? Math.min(next.words[0].t - 0.1, p.end + 1.4) : DUR - 0.05;
        hide = Math.max(hide, p.end + 0.15);
        if (next) hide = Math.min(hide, Math.max(0, next.words[0].t - 0.1));
        tl.fromTo("#p" + i, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.06, ...IR }}, show);
        tl.to("#p" + i, {{ opacity: 0, duration: 0.1, ...IR }}, Math.max(show + 0.1, hide - 0.1));
        p.words.forEach((w, j) => {{
          const el = "#p" + i + "w" + j;
          if (w.kind === "zoom") {{
            tl.fromTo(el, {{ opacity: 0, scale: 2.0 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "expo.out", ...IR }}, w.t);
          }} else if (w.kind === "red") {{
            tl.fromTo(el, {{ opacity: 0, scale: 1.5, y: 0 }}, {{ opacity: 1, scale: 1, duration: 0.2, ease: "back.out(2.2)", ...IR }}, w.t);
          }} else {{
            tl.fromTo(el, {{ opacity: 0, y: 18, scale: 0.9 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.14, ease: "power2.out", ...IR }}, w.t);
          }}
        }});
      }});

      // Saída: escurece o clipe no último quarto de segundo
      tl.to("#stage", {{ opacity: 0, duration: 0.25, ...IR }}, DUR - 0.3);
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(a.out, "w", encoding="utf-8").write(page)
print("ok", a.out, len(lyrics), "frases", len(punches), "pulsos")
