import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from planner import plan
from observer import observe

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

observation = observe(tasks)
result = plan(observation)

print("plan:", result)
print("expected: {'actions': ['Relancer A', 'Relancer C', 'Relancer Lockout']}")

print(result=={'actions': ['Relancer A', 'Relancer C', 'Relancer Lockout']})