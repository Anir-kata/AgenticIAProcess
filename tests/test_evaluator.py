import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from planner import plan
from observer import observe
from executor import execute
from evaluator import evaluate

tasks = [
    {"name": "A", "status": "late"},
    {"name": "B", "status": "ok"},
    {"name": "C", "status": "late"}
]

observation = observe(tasks)
plan_result = plan(observation)
execution_result = execute(plan_result)

print("evaluation:", evaluate(execution_result))