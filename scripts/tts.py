"""Convierte guion.txt (raíz del repositorio) en un MP3 con edge-tts.

Salida: docs/episodes/AAAA-MM-DD.mp3 (fecha de hoy en hora de Madrid).
"""
import asyncio
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import edge_tts

VOZ = "es-ES-AlvaroNeural"
RAIZ = Path(__file__).resolve().parent.parent


async def main():
    # Leemos el guion
    texto = (RAIZ / "guion.txt").read_text(encoding="utf-8").strip()
    if not texto:
        raise SystemExit("guion.txt está vacío")

    # Fecha de hoy según la hora de Madrid (no la del servidor)
    hoy = datetime.now(ZoneInfo("Europe/Madrid")).strftime("%Y-%m-%d")

    salida = RAIZ / "docs" / "episodes" / f"{hoy}.mp3"
    salida.parent.mkdir(parents=True, exist_ok=True)

    # Generamos el audio y lo guardamos
    await edge_tts.Communicate(texto, VOZ).save(str(salida))
    print(f"Creado {salida} ({salida.stat().st_size} bytes)")


if __name__ == "__main__":
    asyncio.run(main())
