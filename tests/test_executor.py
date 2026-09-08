import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from executor import execute


def test_execute_returns_all_plan_actions():
    plan = {"actions": ["Relancer A", "Relancer C"]}

    assert execute(plan) == {
        "executed": ["Relancer A", "Relancer C"]
    }