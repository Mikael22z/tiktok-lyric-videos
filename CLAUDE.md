# TikTok Lyric Videos — instruções para o agente

Série de lyric videos verticais para o canal de TikTok do usuário (**@K4SMITTK**). Converse em **português**.

## Antes de começar uma sessão nova

Rode `bash scripts/setup.sh`. Ele clona HyperFrames e video-use em `$HOME`, instala as dependências, registra as skills e instala o Chrome usado no render.

## Especificação fixa

- Canvas 1080×1920 (9:16), 30 fps.
- Duração 60–80 s. A maioria das músicas é mais longa: propor o trecho (começar num momento forte para prender nos primeiros segundos, terminar num ponto que feche bem) e esperar aprovação.
- **Safe zones do TikTok** (aproximadas, em px no canvas 1080×1920): não colocar letra nos 160 px do topo, nos 480 px de baixo (legenda do post, perfil) nem nos 140 px da direita (botões). Manter a letra na faixa central.

## Fluxo de produção (por vídeo)

Workflow principal: skill `music-to-video` do HyperFrames.

1. Entradas: áudio da música, videoclipe (arquivo ou link — baixar com `yt-dlp`), letra em texto, trecho escolhido.
2. Projeto em `videos/<slug-da-musica>/`. Anotar em `videos/<slug>/SOURCES.md` os links de origem (mídia bruta não vai para o git).
3. Análise de beat com `analyze-beatgrid.py` da skill (único analisador — não medir beat de outro jeito).
4. Sincronizar a letra (linha ou palavra) usando a letra fornecida pelo usuário como texto de referência.
5. Selecionar cenas do clipe olhando quadros amostrados (`video-use/helpers/timeline_view.py` ou ffmpeg) e encaixar nos beats/frases.
6. Tipografia seguindo `style/` (estilo padrão da série).
7. Apresentar o plano trecho a trecho e **só produzir após aprovação**. Render só após aprovação da prévia.
8. Não conseguimos ouvir o áudio: a conferência final de sincronia é do usuário — pedir feedback e ajustar.

## Estilo da série

`style/` guarda o padrão visual (fonte, paleta, animações de entrada/saída do texto) definido a partir das referências em `references/`. Reutilizar em todos os vídeos; mudar só quando o usuário pedir.

## Git

Commits pequenos e frequentes — o ambiente é temporário. Não versionar mídia bruta (ver `.gitignore`).
