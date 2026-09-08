import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from evaluator import evaluate


def test_evaluate_completed_execution():
    assert evaluate({"executed": ["Relancer A"]}) == {"status": "done"}


def test_evaluate_empty_execution():
    assert evaluate({"executed": []}) == {"status": "failed"}