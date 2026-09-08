from observer import observe
from planner import plan
from executor import execute
from evaluator import evaluate

def run_agent(tasks):
    """
    Boucle agentique complète :
    Observer → Planifier → Exécuter → Évaluer
    """

    observation = observe(tasks)
    plan_result = plan(observation)
    execution_result = execute(plan_result)
    evaluation = evaluate(execution_result)

    return {
        "observation": observation,
        "plan": plan_result,
        "execution": execution_result,
        "evaluation": evaluation
    }

if __name__ == "__main__":
    tasks = [
        {"name": "A", "status": "late"},
        {"name": "B", "status": "ok"},
        {"name": "C", "status": "late"}
    ]

    result = run_agent(tasks)
    print(result)