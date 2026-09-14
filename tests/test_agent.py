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


def test_task_agent_prioritizes_high_priority_tasks():
	agent = TaskAgent()
	result = agent.run([
		{"name": "Low", "status": "late", "priority": 1},
		{"name": "High", "status": "late", "priority": 9},
		{"name": "Normal", "status": "ok", "priority": 3}
	])

	assert result["plan"] == {"actions": ["Relancer High", "Relancer Low"]}


def test_task_agent_persists_memory_between_runs(tmp_path):
	memory_file = tmp_path / "agent_memory.json"
	first_agent = TaskAgent(memory_file=str(memory_file))
	first_agent.run([
		{"name": "Alpha", "status": "late"},
		{"name": "Beta", "status": "ok"}
	])

	second_agent = TaskAgent(memory_file=str(memory_file))
	result = second_agent.run([
		{"name": "Alpha", "status": "late"},
		{"name": "Gamma", "status": "late"}
	])

	assert "Alpha" in result["memory"]["completed"]
	assert "Gamma" in result["memory"]["pending"]


def test_task_agent_runs_autonomous_cycles_until_queue_is_empty():
	agent = TaskAgent()
	result = agent.run([
		{"name": "Review", "status": "late", "priority": 2},
		{"name": "Deploy", "status": "late", "priority": 9},
		{"name": "Cleanup", "status": "late", "priority": 5}
	])

	assert result["status"] == "done"
	assert result["summary"]["pending"] == []
	assert result["summary"]["completed"] == ["Deploy", "Cleanup", "Review"]
	assert result["cycles"] >= 1


def test_task_agent_accepts_common_task_status_aliases():
	agent = TaskAgent()
	result = agent.run([
		{"name": "Backlog", "status": "todo"},
		{"name": "Blocked", "status": "OVERDUE"},
		{"name": "Done Item", "status": "done"}
	])

	assert "Backlog" in result["observation"]["late_tasks"]
	assert "Blocked" in result["observation"]["late_tasks"]
	assert "Done Item" not in result["observation"]["late_tasks"]


def test_task_agent_runs_multiple_autonomous_cycles():
	agent = TaskAgent()
	result = agent.run([
		{"name": "A", "status": "late", "priority": 1},
		{"name": "B", "status": "late", "priority": 4},
		{"name": "C", "status": "late", "priority": 2},
		{"name": "D", "status": "late", "priority": 3}
	], max_cycles=2)

	assert result["cycles"] == 2
	assert result["status"] == "done"
	assert result["summary"]["pending"] == []
