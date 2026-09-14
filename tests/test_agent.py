import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from agent import TaskAgent, run_agent


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


def test_task_agent_executes_generic_task_list():
	agent = TaskAgent()
	result = agent.run([
		{"name": "Task 1", "status": "late"},
		{"name": "Task 2", "status": "ok"},
		{"name": "Task 3", "status": "late"}
	])

	assert result["observation"] == {"late_tasks": {"Task 1", "Task 3"}}
	assert result["plan"] == {"actions": ["Relancer Task 1", "Relancer Task 3"]}
	assert result["execution"] == {"executed": ["Relancer Task 1", "Relancer Task 3"]}
	assert result["evaluation"] == {"status": "done"}


def test_task_agent_handles_no_late_tasks():
	agent = TaskAgent()
	result = agent.run([
		{"name": "Alpha", "status": "ok"},
		{"name": "Beta", "status": "done"}
	])

	assert result["observation"] == {"late_tasks": set()}
	assert result["plan"] == {"actions": []}
	assert result["execution"] == {"executed": []}
	assert result["evaluation"] == {"status": "failed"}


def test_task_agent_accepts_case_insensitive_status():
	agent = TaskAgent()
	result = agent.run([
		{"name": "Urgent", "status": "LATE"},
		{"name": "Normal", "status": "OK"}
	])

	assert result["observation"] == {"late_tasks": {"Urgent"}}
	assert result["plan"] == {"actions": ["Relancer Urgent"]}
