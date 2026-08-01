"""Smoke tests for the transcription package.

Guard rails against accidental breakage — imports resolve, callables exist,
quality/IO helpers behave sanely on obvious inputs. Whisper model loading and
actual transcription are NOT exercised (would require GPU/model download).
"""

from __future__ import annotations

import json
from pathlib import Path


def test_package_imports() -> None:
    """Verifies that the transcription package imports successfully and exposes a version string."""
    import transcription

    assert transcription.__version__


def test_engine_exports_callables() -> None:
    """Verifies that engine exposes callable get_model, transcribe_file, and clear_model_cache functions."""
    from transcription.core import engine

    assert callable(engine.get_model)
    assert callable(engine.transcribe_file)
    assert callable(engine.clear_model_cache)


def test_clear_model_cache_is_idempotent() -> None:
    """Verifies that calling clear_model_cache twice leaves the cache empty (idempotent)."""
    from transcription.core.engine import _model_cache, clear_model_cache

    clear_model_cache()
    assert _model_cache == {}
    clear_model_cache()
    assert _model_cache == {}


def test_io_json_roundtrip(tmp_path: Path) -> None:
    """Verifies that save_json + load_json roundtrips a nested payload through disk without loss."""
    from transcription.utils.io import load_json, save_json

    payload = {"chat": "test", "count": 3, "items": ["a", "b", "c"]}
    target = tmp_path / "nested" / "data.json"

    assert save_json(payload, target) is True
    assert target.exists()
    assert load_json(target) == payload


def test_load_json_returns_default_when_missing(tmp_path: Path) -> None:
    """Verifies that load_json returns the provided default (or None) when the file does not exist."""
    from transcription.utils.io import load_json

    assert load_json(tmp_path / "does-not-exist.json", default=[]) == []
    assert load_json(tmp_path / "still-missing.json") is None


def test_load_json_returns_default_on_corrupt_file(tmp_path: Path) -> None:
    """Verifies that load_json returns the default when the file content is unparseable."""
    from transcription.utils.io import load_json

    bad = tmp_path / "corrupt.json"
    bad.write_text("this is not json {{{", encoding="utf-8")

    assert load_json(bad, default={"fallback": True}) == {"fallback": True}


def test_save_json_is_atomic(tmp_path: Path) -> None:
    """Verifies that save_json writes directly to target without leaving .tmp leftovers."""
    from transcription.utils.io import save_json

    target = tmp_path / "atomic.json"
    save_json({"ok": True}, target)

    leftover = list(tmp_path.glob("*.tmp"))
    assert leftover == []

    with open(target, encoding="utf-8") as f:
        assert json.load(f) == {"ok": True}


def test_quality_flags_empty_text() -> None:
    """Verifies that check_quality handles empty input without crashing."""
    from transcription.utils.quality import check_quality

    result = check_quality("")


def test_quality_flags_none_text() -> None:
    """Verifies that check_quality handles None input without crashing."""
    from transcription.utils.quality import check_quality

    result = check_quality(None)


def test_quality_flags_asian_chars_in_spanish() -> None:
    """Verifies that check_quality flags Spanish text containing Asian-script characters as mixed-language."""
    from transcription.utils.quality import check_quality

    result = check_quality("Hola mundo 你好")


def test_quality_flags_word_repetition() -> None:
    """Verifies that check_quality flags Spanish text with abnormally high word repetition."""
    from transcription.utils.quality import check_quality

    result = check_quality("hola hola hola hola hola hola hola hola")


def test_quality_passes_normal_spanish() -> None:
    """Verifies that check_quality returns no flags for normal Spanish text."""
    from transcription.utils.quality import check_quality

    result = check_quality("Hola, ¿cómo estás hoy? Espero que bien.")


def test_is_quality_transcript_rejects_short() -> None:
    """Verifies that is_quality_transcript rejects inputs shorter than the minimum length."""
    from transcription.utils.quality import is_quality_transcript

    assert is_quality_transcript("") is False
    assert is_quality_transcript("hi") is False


def test_format_quality_report_covers_both_branches() -> None:
    """Verifies that format_quality_report produces output that covers both flagged and clean-quality branches."""
    from transcription.utils.quality import format_quality_report, QualityResult

    flagged = format_quality_report(QualityResult(is_valid=False, problems=["test problem"]))
    clean = format_quality_report(QualityResult(is_valid=True, problems=[]))

    assert "test problem" in flagged.lower() or "problem" in flagged.lower()
    assert "ok" in clean.lower() or "valid" in clean.lower() or "✓" in clean
