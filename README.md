# Briefing matinal (podcast privado)

Podcast diario generado a partir de un texto.

## Cómo funciona

1. Se escribe el texto del día en `guion.txt` (raíz).
2. `python scripts/tts.py` lo convierte en `docs/episodes/AAAA-MM-DD.mp3` con edge-tts (voz `es-ES-AlvaroNeural`, fecha de Madrid).
3. `python scripts/feed.py` regenera `docs/feed.xml`, conserva los últimos 14 episodios y borra los MP3 más antiguos.
4. GitHub Pages publica la carpeta `docs/`.

## Uso

```
pip install -r requirements.txt
python scripts/tts.py
python scripts/feed.py
```

Activa GitHub Pages en Settings → Pages (rama `main`, carpeta `/docs`).
Feed: `https://<usuario>.github.io/briefing-a7x9/feed.xml`
(añádelo en Apple Podcasts → Archivo → Seguir un programa por URL).
El feed lleva `itunes:block = Yes`, así que no se indexa en el directorio público.
