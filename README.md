# TikTok Lyric Videos

Vídeos verticais para o TikTok no estilo **lyric video**: a música toca de fundo, a letra aparece em tipografia animada e cenas do videoclipe oficial são cortadas no ritmo do beat.

Produzido com:
- [HyperFrames](https://github.com/heygen-com/hyperframes) — composição em HTML/CSS/GSAP renderizada para MP4 (workflow `music-to-video`)
- [video-use](https://github.com/browser-use/video-use) — seleção, corte e tratamento das cenas do videoclipe

## Padrão dos vídeos

| Item | Valor |
| --- | --- |
| Formato | 1080×1920 (9:16), 30 fps |
| Duração | 1:00 a 1:20 |
| Plataforma | TikTok |

## Estrutura

```
style/        estilo padrão da série (fonte, cores, animação do texto)
references/   referências de estilo e anotações sobre elas
videos/<nome-da-musica>/   um projeto HyperFrames por vídeo
scripts/setup.sh           prepara um ambiente novo
```

Mídia bruta (áudio original, videoclipe baixado) não é versionada: é pesada e pode ser baixada de novo pelo link anotado em cada projeto.

## Ambiente

```bash
bash scripts/setup.sh
```
