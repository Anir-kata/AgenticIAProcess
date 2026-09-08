import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from observer import observe

tasks = [
    {"name": "A", "status": "late"},
    {"name": "B", "status": "ok"},
    {"name": "C", "status": "late"}
]

result = observe(tasks)
print("result:", result)
print("expected: {'late_tasks': ['A', 'C']}")