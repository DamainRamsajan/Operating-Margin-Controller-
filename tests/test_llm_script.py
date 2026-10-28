import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("llm_pair_spike", Path(__file__).resolve().parents[1] / "scripts" / "llm_pair_spike.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
LABELS = ["card_arrival", "refund_not_showing_up"]


def test_normalize_accepts_formatting_variants():
    assert mod.normalize("Card arrival.", LABELS) == "card_arrival"
    assert mod.normalize("`refund_not_showing_up`", LABELS) == "refund_not_showing_up"


def test_normalize_marks_unknown_as_invalid():
    assert mod.normalize("I think it is about cards", LABELS) == "INVALID"
