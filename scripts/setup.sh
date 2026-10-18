#!/usr/bin/env bash
# Prepara um ambiente novo (ex.: nova sessão na nuvem) para produzir os vídeos.
# Uso: bash scripts/setup.sh
set -euo pipefail

TOOLS_DIR="${TOOLS_DIR:-$HOME}"
SKILLS_DIR="$HOME/.claude/skills"
mkdir -p "$SKILLS_DIR"

# HyperFrames (composição HTML -> vídeo) e video-use (corte/edição de vídeo)
[ -d "$TOOLS_DIR/hyperframes" ] || git clone --depth 1 https://github.com/heygen-com/hyperframes "$TOOLS_DIR/hyperframes"
[ -d "$TOOLS_DIR/video-use" ]   || git clone --depth 1 https://github.com/browser-use/video-use "$TOOLS_DIR/video-use"

# Dependências Python do video-use + yt-dlp + análise de beat (librosa)
( cd "$TOOLS_DIR/video-use" && uv sync )
python3 -m pip install -q yt-dlp librosa numpy soundfile

# Registra as skills para o Claude Code
ln -sfn "$TOOLS_DIR/video-use" "$SKILLS_DIR/video-use"
for s in "$TOOLS_DIR"/hyperframes/skills/*/; do
  [ -f "$s/SKILL.md" ] && ln -sfn "$s" "$SKILLS_DIR/$(basename "$s")"
done

# Chrome headless usado pelo HyperFrames para renderizar
npx --yes hyperframes browser ensure

echo "Ambiente pronto."
