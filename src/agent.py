import json
import os

from observer import observe
from planner import plan
from executor import execute
from evaluator import evaluate


class TaskAgent:
    """Agent IA autonome avec mémoire persistante et priorisation."""

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

    def _extract_task_names(self, actions):
        names = []
        for action in actions:
            if isinstance(action, str) and action.startswith("Relancer "):
                names.append(action.replace("Relancer ", "", 1))
        return names

    def run(self, tasks):
        """Boucle agentique complète : Observer → Planifier → Exécuter → Évaluer."""
        observation = observe(tasks)
        late_tasks = sorted(observation.get("late_tasks", set()))

        previous_completed = set(self.memory.get("completed", []))
        previous_pending = set(self.memory.get("pending", []))

        plan_result = plan(observation, tasks=tasks)
        execution_result = execute(plan_result)
        evaluation = evaluate(execution_result)

        executed_names = self._extract_task_names(execution_result.get("executed", []))
        new_completed = sorted(set(previous_completed) | set(executed_names))
        new_pending = sorted((set(late_tasks) - set(previous_completed)) | (previous_pending - set(new_completed)))

        self.memory["completed"] = new_completed
        self.memory["pending"] = new_pending
        self.memory["history"].append({
            "tasks": tasks,
            "late_tasks": late_tasks,
            "executed": execution_result.get("executed", []),
            "evaluation": evaluation,
        })
        self._save_memory()

        return {
            "observation": observation,
            "plan": plan_result,
            "execution": execution_result,
            "evaluation": evaluation,
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
    import json
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