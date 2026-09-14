from observer import observe
from planner import plan
from executor import execute
from evaluator import evaluate


class TaskAgent:
    """Agent IA simple pour traiter une liste de tâches."""

    def run(self, tasks):
        """Boucle agentique complète : Observer → Planifier → Exécuter → Évaluer."""
        observation = observe(tasks)
        plan_result = plan(observation)
        execution_result = execute(plan_result)
        evaluation = evaluate(execution_result)

        return {
            "observation": observation,
            "plan": plan_result,
            "execution": execution_result,
            "evaluation": evaluation,
        }


def run_agent(tasks):
    agent = TaskAgent()
    return agent.run(tasks)


if __name__ == "__main__":
    tasks = [
        {"name": "A", "status": "late"},
        {"name": "B", "status": "ok"},
        {"name": "C", "status": "late"}
    ]

    result = run_agent(tasks)
    print(result)