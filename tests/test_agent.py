import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from agent import run_agent


def test_run_agent_completes_workflow():
	tasks = [
		{"name": "A", "status": "late"},
		{"name": "B", "status": "ok"}
	]

	result = run_agent(tasks)

	assert result["observation"] == {"late_tasks": {"A"}}
	assert result["plan"] == {"actions": ["Relancer A"]}
	assert result["execution"] == {"executed": ["Relancer A"]}
	assert result["evaluation"] == {"status": "done"}
