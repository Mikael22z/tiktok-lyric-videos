# Estilo padrão da série

Definido no primeiro vídeo (Vivendo Avançado). Ver `../references/README.md`.

- **Fonte:** **Syne ExtraBold** (`fonts/Syne-ExtraBold.woff2` / `.ttf`, instância fixa peso 800), SIL OFL (`fonts/Syne-OFL.txt`). Escolhida por ser a mais próxima da referência @cardoslirycs. No CSS: `font-family: "Syne ExtraBold"`. Cobre todos os acentos do português. (A Excalibur Nouveau, usada antes, continua em `fonts/`.)
- **Paleta:** fundo preto `#000`, texto branco `#fff`, destaque vermelho `#e3121f`.
- **Entrada/saída do texto:** frase dentro do clipe; cada palavra entra quando é cantada; palavras de peso em vermelho e maiores; palavras-chave com zoom (2× → 1×) + tremida + flash.
- **Layout:** canvas 1080×1920 preto, clipe 16:9 (1080×608) com topo em y=556, título da música (vermelho) + artistas acima do clipe, letra na parte de baixo do clipe.
- **Grave (808):** em cada batida forte, corte de enquadramento (alterna 1.0×/1.16×) + pulso de zoom + flash branco curto.
- **Censura:** palavras sensíveis para o TikTok aparecem só com a 1ª letra + `*`.
- **Tratamento das cenas do clipe:** cor original; cenas ilustrativas da letra entram cortadas no grave.
- **Geração:** `scripts/build_lyric_index.py` (fonte padrão Syne ExtraBold, `--font-scale 0.78`).
