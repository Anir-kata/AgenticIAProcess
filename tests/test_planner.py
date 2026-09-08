import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from planner import plan
from observer import observe


def test_plan_returns_unique_late_task_actions():
    tasks = [
        {"name": "A", "status": "late"},
        {"name": "B", "status": "ok"},
        {"name": "C", "status": "late"},
        {"name": "K1", "status": "ok"},
        {"name": "P2", "status": "ok"},
        {"name": "Lockout", "status": "late"},
        {"name": "ND2", "status": "ok"},
        {"name": "C", "status": "late"}
    ]

    result = plan(observe(tasks))

    assert result == {
        "actions": ["Relancer A", "Relancer C", "Relancer Lockout"]
    }