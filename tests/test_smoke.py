"""Smoke tests for the transcription package.

Guard rails against accidental breakage — imports resolve, callables exist,
quality/IO helpers behave sanely on obvious inputs. Whisper model loading and
actual transcription are NOT exercised (would require GPU/model download).
"""

from __future__ import annotations

import json
from pathlib import Path


def test_package_imports() -> None:
    import transcription

    assert transcription.__version__


def test_engine_exports_callables() -> None:
    from transcription.core import engine

    assert callable(engine.get_model)
    assert callable(engine.transcribe_file)
    assert callable(engine.clear_model_cache)


def test_clear_model_cache_is_idempotent() -> None:
    from transcription.core.engine import _model_cache, clear_model_cache

    clear_model_cache()
    assert _model_cache == {}
    clear_model_cache()
    assert _model_cache == {}


def test_io_json_roundtrip(tmp_path: Path) -> None:
    from transcription.utils.io import load_json, save_json

    payload = {"chat": "test", "count": 3, "items": ["a", "b", "c"]}
    target = tmp_path / "nested" / "data.json"

    assert save_json(payload, target) is True
    assert target.exists()
    assert load_json(target) == payload


def test_load_json_returns_default_when_missing(tmp_path: Path) -> None:
    from transcription.utils.io import load_json

    assert load_json(tmp_path / "does-not-exist.json", default=[]) == []
    assert load_json(tmp_path / "still-missing.json") is None


def test_load_json_returns_default_on_corrupt_file(tmp_path: Path) -> None:
    from transcription.utils.io import load_json

    bad = tmp_path / "corrupt.json"
    bad.write_text("this is not json {{{", encoding="utf-8")

    assert load_json(bad, default={"fallback": True}) == {"fallback": True}


def test_save_json_is_atomic(tmp_path: Path) -> None:
    from transcription.utils.io import save_json

    target = tmp_path / "atomic.json"
    save_json({"ok": True}, target)

    leftover = list(tmp_path.glob("*.tmp"))
    assert leftover == []

    with open(target, encoding="utf-8") as f:
        assert json.load(f) == {"ok": True}


def test_quality_flags_empty_text() -> None:
    from transcription.utils.quality import check_quality

    result = check_quality("")
    assert result.is_valid is False
    assert "empty_text" in result.problems


def test_quality_flags_none_text() -> None:
    from transcription.utils.quality import check_quality

    result = check_quality(None)
    assert result.is_valid is False
    assert "no_text" in result.problems


def test_quality_flags_asian_chars_in_spanish() -> None:
    from transcription.utils.quality import check_quality

    spanish_with_hallucination = (
        "hola como estas hoy me siento bien pero cansado por el trabajo "
        "de la semana pasada y necesito descansar un poco 你好世界你好世界你好世界"
    )
    result = check_quality(spanish_with_hallucination)
    assert "asian_chars" in result.problems


def test_quality_flags_word_repetition() -> None:
    from transcription.utils.quality import check_quality

    result = check_quality(
        "hola hola hola hola bien bien bien bien esto no tiene sentido palabra"
    )
    assert "word_repetition" in result.problems


def test_quality_passes_normal_spanish() -> None:
    from transcription.utils.quality import check_quality

    normal = (
        "Hoy estuve pensando en lo que hablamos ayer sobre el proyecto. "
        "Creo que la mejor manera de avanzar es empezar con la parte "
        "más simple y luego ir agregando funcionalidad poco a poco."
    )
    result = check_quality(normal)
    assert result.is_valid, f"unexpected problems: {result.problems}"


def test_is_quality_transcript_rejects_short() -> None:
    from transcription.utils.quality import is_quality_transcript

    assert is_quality_transcript("hola") is False
    assert is_quality_transcript(None) is False


def test_format_quality_report_covers_both_branches() -> None:
    from transcription.utils.quality import (
        QualityResult,
        check_quality,
        format_quality_report,
    )

    ok = QualityResult()
    assert "passed" in format_quality_report(ok).lower()

    bad = check_quality("")
    report = format_quality_report(bad)
    assert "empty_text" in report
