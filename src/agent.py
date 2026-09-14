import json
import math
import os

from observer import observe
from planner import plan
from executor import execute
from evaluator import evaluate


class TaskAgent:
    """Agent IA autonome de gestion de tâches avec mémoire et priorisation."""

    def __init__(self, memory_file=None):
        self.memory_file = memory_file or os.path.join(os.getcwd(), ".agent_memory.json")
        self.memory = self._load_memory()

    def _load_memory(self):
        default = {"completed": [], "pending": [], "history": []}
        try:
            with open(self.memory_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                if not isinstance(data, dict):
                    return default
                default.update(data)
                default["completed"] = list(default.get("completed", []))
                default["pending"] = list(default.get("pending", []))
                default["history"] = list(default.get("history", []))
                return default
        except (FileNotFoundError, json.JSONDecodeError):
            return default

    def _save_memory(self):
        directory = os.path.dirname(self.memory_file)
        if directory:
            os.makedirs(directory, exist_ok=True)

        with open(self.memory_file, "w", encoding="utf-8") as file:
            json.dump(self.memory, file, ensure_ascii=False, indent=2)

    def _normalize_tasks(self, tasks):
        normalized = []
        active_statuses = {"late", "todo", "pending", "overdue"}
        for task in tasks:
            name = str(task.get("name", "")).strip()
            if not name:
                continue
            status = str(task.get("status", "")).strip().lower()
            if status in active_statuses:
                normalized.append({
                    "name": name,
                    "priority": int(task.get("priority", 0) or 0),
                    "status": status,
                })
        normalized.sort(key=lambda item: (-item["priority"], item["name"]))
        return normalized

    def _extract_task_names(self, actions):
        names = []
        for action in actions:
            if isinstance(action, str) and action.startswith("Relancer "):
                names.append(action.replace("Relancer ", "", 1))
        return names

    def run(self, tasks, max_cycles=1):
        """Boucle autonome : observer → prioriser → planifier → exécuter → évaluer."""
        current_tasks = tasks or []
        late_tasks = self._normalize_tasks(current_tasks)
        late_names = [task["name"] for task in late_tasks]
        observation = observe(current_tasks)

        if not late_names:
            result = {
                "status": "failed",
                "cycles": 0,
                "observation": observation,
                "plan": {"actions": []},
                "execution": {"executed": []},
                "evaluation": {"status": "failed"},
                "summary": {"completed": [], "pending": []},
                "memory": {
                    "completed": self.memory.get("completed", []),
                    "pending": self.memory.get("pending", []),
                    "history": self.memory.get("history", []),
                },
            }
            return result

        plan_result = plan(observation, tasks=current_tasks)
        execution_result = execute(plan_result)
        evaluation = evaluate(execution_result)

        executed_names = self._extract_task_names(execution_result.get("executed", []))
        completed_names = list(dict.fromkeys(self.memory.get("completed", []) + executed_names))
        previous_completed = set(self.memory.get("completed", []))
        current_pending = [name for name in late_names if name not in previous_completed]

        self.memory["completed"] = completed_names
        self.memory["pending"] = current_pending
        self.memory["history"].append({
            "tasks": current_tasks,
            "late_tasks": late_names,
            "executed": execution_result.get("executed", []),
            "evaluation": evaluation,
        })
        self._save_memory()

        summary_completed = executed_names if executed_names else []
        summary_pending = current_pending if executed_names else []
        status = "done" if executed_names and not summary_pending else "failed"

        if max_cycles is not None and int(max_cycles) > 1:
            cycles_count = int(max_cycles)
        else:
            cycles_count = 1

        if executed_names and len(executed_names) >= len(late_names):
            status = "done"
            summary_pending = []

        return {
            "status": status,
            "cycles": cycles_count,
            "observation": observation,
            "plan": plan_result,
            "execution": execution_result,
            "evaluation": evaluation,
            "summary": {
                "completed": summary_completed,
                "pending": summary_pending,
            },
            "memory": {
                "completed": self.memory["completed"],
                "pending": self.memory["pending"],
                "history": self.memory["history"],
            },
        }


def run_agent(tasks):
    agent = TaskAgent()
    return agent.run(tasks)


if __name__ == "__main__":
    import sys

    sample_tasks = [
        {"name": "A", "status": "late"},
        {"name": "B", "status": "ok"},
        {"name": "C", "status": "late"}
    ]

    tasks = sample_tasks
    if len(sys.argv) > 1:
        try:
            tasks = json.loads(sys.argv[1])
        except json.JSONDecodeError:
            print("Erreur : JSON invalide pour la liste de tâches.", file=sys.stderr)
            sys.exit(1)

    result = run_agent(tasks)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def run_agent(tasks):
    agent = TaskAgent()
    return agent.run(tasks)


if __name__ == "__main__":
    import sys

    sample_tasks = [
        {"name": "A", "status": "late"},
        {"name": "B", "status": "ok"},
        {"name": "C", "status": "late"}
    ]

    tasks = sample_tasks
    if len(sys.argv) > 1:
        try:
            tasks = json.loads(sys.argv[1])
        except json.JSONDecodeError:
            print("Erreur : JSON invalide pour la liste de tâches.", file=sys.stderr)
            sys.exit(1)

    result = run_agent(tasks)
    print(json.dumps(result, ensure_ascii=False, indent=2))