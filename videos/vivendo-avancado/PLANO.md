# Plano — Vivendo Avançado

**Trecho:** 00:32.0 → 01:52.0 do clipe (80 s): verso completo + refrão completo, termina no último "ganhando".
**Formato:** 1080×1920, 30 fps. Layout: **B** — fundo preto, clipe 16:9 (1080×608) centralizado, título acima, letra dentro do clipe.

## Análise
- 117,5 BPM. 36 batidas fortes de grave (808) no trecho (`work/bass_hits.json`), intervalo mediano 2,4 s.
- Letra transcrita palavra a palavra (`work/words_whisper.json`) e corrigida pela letra oficial.
- 126 cenas do clipe mapeadas (`work/shots.tsv`, `work/sheet_*.jpg`).

## Regras gerais
- **Cortes:** todo corte cai numa batida de grave; em cada batida, pulso de zoom curto (~1,00→1,06→1,00) + flash leve.
- **Lip-sync:** quando o rapper aparece cantando, usar o trecho do clipe do mesmo instante (boca bate com a voz). Cenas de outras partes do clipe só como ilustração (sem boca visível).
- **Letra:** a frase aparece e cada palavra "pousa" no momento em que é cantada; palavras de peso em vermelho; algumas com zoom forte.

## Blocos (tempo do vídeo final)
| Tempo | Letra | Vermelho | Zoom | Imagem |
| --- | --- | --- | --- | --- |
| 0:00–0:01.6 | (abertura no beat) | VIVENDO AVANÇADO | título entra com zoom | prédio com as águias → corte na 1ª batida |
| 0:01.6–0:17 | "Filipe Ret é o aço… motos e carros" | AÇO, BICHO, NASCI, TTK, MOTOS, CARROS | AÇO | rapper de boné vermelho em sincronia; fumaça em "fumando vários"; galera |
| 0:17.9–0:32 | "Gosto de viver… pediu à Deus" | VIVER, MORRER, ARRISCAR, TRABALHO, SALÁRIO, DEUS | DEUS | braços abertos em "gosto de viver"; contra-plongée do palácio |
| 0:32.4–0:49 | "O rei voltou… escândalo" | REI, PÂNICO, DOIDÃO, VOANDO, OURO, ESTOURO, VÂNDALO, BONDE, R.E.T, ESCÂNDALO | PÂNICO, ESCÂNDALO | corrente/anel de ouro em "ouro"; bonde reunido em "meu bonde chegou" |
| 0:49–1:04 | "Do funk ao rap… brinda o momento" | FUNK, RAP, TRAP, RIO DE JANEIRO, FOGOS, TIROS, BRINDA | RIO DE JANEIRO | placa "Catete"/palácio em "Rio de Janeiro"; copos e garrafas em "copos pro ar"/"brinda" |
| 1:05.5–1:20 | Refrão "Vivendo avançado…" ×4 | VIVENDO AVANÇADO, SEM PERDER, PRA SEMPRE | VIVENDO AVANÇADO (cada vez) | cortes mais rápidos; fim com flash no último "ganhando" |

## Status
- [x] Plano e layout aprovados (B, fundo preto, letra dentro do clipe)
- [x] Censura: palavras sensíveis mostram só a 1ª letra + `*` (fumando, skunk, chapado, bonado, tiros)
- [ ] Aprovação da prévia

## Como reconstruir
```bash
cd videos/vivendo-avancado
python3 ../../scripts/align_lyrics.py                      # lyrics.txt + work/words_whisper.json -> work/lyrics_timed.json
python3 ../../scripts/build_picture.py edl.json projeto/assets/picture.mp4
ffmpeg -ss 32 -t 80 -i sources/full.wav -af "afade=t=in:st=0:d=0.03,afade=t=out:st=79.6:d=0.4" -c:a aac -b:a 256k projeto/assets/music.m4a
python3 ../../scripts/build_lyric_index.py --lyrics work/lyrics_timed.json --punches work/punches.json \
  --title "Vivendo Avançado" --artist "Filipe Ret part. BK' e MC TH" --duration 80 --out projeto/index.html
cd projeto && npx hyperframes check . && npx hyperframes render . -o renders/video.mp4 --fps 30
```
