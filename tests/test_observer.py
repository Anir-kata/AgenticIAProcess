import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from observer import observe


def test_observe_returns_unique_late_tasks():
    tasks = [
        {"name": "A", "status": "late"},
        {"name": "B", "status": "ok"},
        {"name": "C", "status": "late"},
        {"name": "C", "status": "late"}
    ]

    assert observe(tasks) == {"late_tasks": {"A", "C"}}