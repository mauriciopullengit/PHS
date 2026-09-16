"""
Edge TTS Backend para OpenJarvis — PT-BR fluido e gratuito.
Usa Microsoft Edge TTS (neural, sem API key, qualidade próxima ao cloud pago).

Registro: importar este arquivo antes de iniciar o jarvis
  → TTSRegistry.register("edge_tts") é chamado automaticamente.

Vozes PT-BR disponíveis:
  pt-BR-AntonioNeural      — masculino, claro, ótimo para Jarvis
  pt-BR-FranciscaNeural    — feminino, natural
  pt-BR-ThalitaNeural      — feminino, mais jovem e fluido
  pt-BR-MacerioMultilingualNeural — masculino multilíngue
"""

from __future__ import annotations

import asyncio
import threading
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List

# Importações OpenJarvis — lazy para não quebrar se o módulo ainda não foi instalado
_tts_module = None
_TTSRegistry = None
_TTSResult = None
_TTSBackend = None


def _load_openjarvis():
    global _tts_module, _TTSRegistry, _TTSResult, _TTSBackend
    if _TTSBackend is not None:
        return
    from openjarvis.speech.tts import TTSBackend, TTSResult, TTSRegistry
    _TTSBackend = TTSBackend
    _TTSResult = TTSResult
    _TTSRegistry = TTSRegistry


def _run_async(coro):
    """Executa corrotina em thread isolada — evita conflito com loop do OpenJarvis."""
    result_holder = {}

    def _worker():
        loop = asyncio.new_event_loop()
        try:
            result_holder["value"] = loop.run_until_complete(coro)
        except Exception as e:
            result_holder["error"] = e
        finally:
            loop.close()

    t = threading.Thread(target=_worker, daemon=True)
    t.start()
    t.join(timeout=30)

    if "error" in result_holder:
        raise result_holder["error"]
    return result_holder.get("value", b"")


async def _synthesize_async(text: str, voice: str, rate: str) -> bytes:
    try:
        import edge_tts
    except ImportError:
        raise RuntimeError("edge-tts não instalado. Execute: pip install edge-tts")

    communicate = edge_tts.Communicate(text, voice, rate=rate)
    audio_chunks: list[bytes] = []
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_chunks.append(chunk["data"])
    return b"".join(audio_chunks)


def _speed_to_rate(speed: float) -> str:
    """Converte float OpenJarvis (1.0=normal) para string edge-tts ('+10%')."""
    pct = int((speed - 1.0) * 100)
    return f"+{pct}%" if pct >= 0 else f"{pct}%"


def _estimate_duration(audio_bytes: bytes) -> float:
    """Estimativa simples: MP3 ~128kbps."""
    return len(audio_bytes) / (128 * 1024 / 8)


def register_edge_tts_backend():
    """Registra o backend no TTSRegistry do OpenJarvis."""
    _load_openjarvis()

    @_TTSRegistry.register("edge_tts")
    class EdgeTTSBackend(_TTSBackend):
        backend_id = "edge_tts"

        VOICES_PT_BR = [
            "pt-BR-AntonioNeural",              # masculino — padrao Jarvis
            "pt-BR-FranciscaNeural",             # feminino
            "pt-BR-ThalitaMultilingualNeural",   # feminino, jovem, multilingual
        ]

        def __init__(self, **kwargs):
            self._default_voice = kwargs.get("voice_id", "pt-BR-FranciscaNeural")

        def synthesize(
            self,
            text: str,
            voice_id: str | None = None,
            speed: float = 1.0,
            output_format: str = "mp3",
        ) -> "_TTSResult":
            voice = voice_id or self._default_voice
            rate = _speed_to_rate(speed)
            audio = _run_async(_synthesize_async(text, voice, rate))
            return _TTSResult(
                audio=audio,
                format="mp3",
                duration_seconds=_estimate_duration(audio),
                voice_id=voice,
                sample_rate=24000,
                metadata={"backend": "edge_tts", "rate": rate},
            )

        def available_voices(self) -> List[str]:
            return self.VOICES_PT_BR

        def health(self) -> bool:
            try:
                import edge_tts  # noqa: F401
                return True
            except ImportError:
                return False

    return EdgeTTSBackend


# Auto-registro ao importar
try:
    EdgeTTSBackend = register_edge_tts_backend()
except Exception:
    pass  # OpenJarvis ainda não instalado — registro acontece no start.py
