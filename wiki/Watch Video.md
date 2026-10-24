---
tipo: herramienta
etiquetas: [video, transcripcion]
creado: 2026-10-25
---

# Watch Video

Skill de [[Claude Code]] (coreyhaines31/makerskills) para "ver" vídeos: YouTube, Instagram, TikTok, Loom, archivos locales…

```
/watch-video <url>            # solo transcripción (rápido, gratis)
/watch-video <url> visual     # + fotogramas analizados por Claude
```

Usa yt-dlp (descarga), ffmpeg (fotogramas/audio) y faster-whisper (transcripción local). Para meter la transcripción en el [[Segundo Cerebro]], pide que la guarde en `raw/`.
