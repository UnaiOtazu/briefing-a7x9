"""Regenera docs/feed.xml (RSS de podcast para Apple Podcasts).

Conserva solo los últimos 14 episodios y borra los MP3 más antiguos.
"""
import re
import subprocess
from datetime import datetime
from email.utils import format_datetime
from pathlib import Path
from xml.sax.saxutils import escape
from zoneinfo import ZoneInfo

RAIZ = Path(__file__).resolve().parent.parent
EPISODIOS = RAIZ / "docs" / "episodes"
MAX_EPISODIOS = 14
TITULO = "Briefing matinal"
MADRID = ZoneInfo("Europe/Madrid")


def url_base():
    """Saca el usuario del remoto de git y construye la URL de GitHub Pages."""
    remoto = subprocess.run(
        ["git", "config", "--get", "remote.origin.url"],
        cwd=RAIZ, capture_output=True, text=True, check=True,
    ).stdout.strip()
    # Valido para https://github.com/usuario/repo(.git) y git@github.com:usuario/repo(.git)
    m = re.search(r"github\.com[:/]+([^/]+)/([^/]+?)(?:\.git)?/?$", remoto)
    if not m:
        raise SystemExit(f"No puedo sacar el usuario del remoto: {remoto}")
    return f"https://{m.group(1)}.github.io/{m.group(2)}/"


def main():
    base = url_base()

    # Los nombres AAAA-MM-DD.mp3 ordenan igual alfabéticamente que por fecha
    mp3s = sorted(EPISODIOS.glob("????-??-??.mp3"), reverse=True)
    for viejo in mp3s[MAX_EPISODIOS:]:
        viejo.unlink()
        print(f"Borrado {viejo.name}")
    mp3s = mp3s[:MAX_EPISODIOS]

    items = []
    for mp3 in mp3s:
        fecha = mp3.stem
        # Publicación: 07:00 hora de Madrid del día del episodio
        pub = datetime.strptime(fecha, "%Y-%m-%d").replace(hour=7, tzinfo=MADRID)
        url = f"{base}episodes/{mp3.name}"
        items.append(f"""    <item>
      <title>Briefing {fecha}</title>
      <description>Briefing del {fecha}</description>
      <pubDate>{format_datetime(pub)}</pubDate>
      <guid isPermaLink="false">briefing-{fecha}</guid>
      <enclosure url="{escape(url)}" length="{mp3.stat().st_size}" type="audio/mpeg"/>
      <itunes:explicit>false</itunes:explicit>
    </item>""")

    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>{TITULO}</title>
    <link>{escape(base)}</link>
    <description>Briefing diario privado</description>
    <language>es-es</language>
    <itunes:author>Briefing</itunes:author>
    <itunes:summary>Briefing diario privado</itunes:summary>
    <itunes:explicit>false</itunes:explicit>
    <itunes:block>Yes</itunes:block>
    <itunes:category text="News"/>
{chr(10).join(items)}
  </channel>
</rss>
"""
    (RAIZ / "docs" / "feed.xml").write_text(feed, encoding="utf-8")
    print(f"feed.xml regenerado con {len(items)} episodios")


if __name__ == "__main__":
    main()
