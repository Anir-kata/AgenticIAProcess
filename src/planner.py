import json
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)


def _fallback_actions(late_tasks):
    return [f"Relancer {task_name}" for task_name in late_tasks]


def plan(observation, tasks=None):
    """
    Génère un plan d'action à partir de l'observation.
    Si le service de planification est indisponible, on revient à une logique
    déterministe avec priorisation par priorité si elle est fournie.
    """

    late_tasks = list(observation.get("late_tasks", set()))
    if tasks is not None:
        priorities = {}
        for task in tasks:
            name = str(task.get("name", "")).strip()
            if name:
                priorities[name] = task.get("priority", 0)
        late_tasks = sorted(late_tasks, key=lambda name: (-int(priorities.get(name, 0) or 0), name))
    else:
        late_tasks = sorted(late_tasks)

    expected_actions = _fallback_actions(late_tasks)
    prompt = f"""
    Tu es un agent IA chargé de gérer des tâches en retard.
    Tâches en retard : {late_tasks}
    Réponds uniquement avec un objet JSON valide, par exemple :
    {{"actions": ["Relancer A", "Relancer C"]}}
    Remplace A et C par les noms réels des tâches. Il ne faut pas avoir de doublons.
    """

    generated_actions = []
    try:
        response = client.chat.completions.create(
            model="llama3.2",
            messages=[
                {"role": "system", "content": "Tu es un planificateur IA."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        plan_json = json.loads(response.choices[0].message.content)
        raw_actions = plan_json.get("actions", [])

        seen = set()
        for action in raw_actions:
            if isinstance(action, str) and action not in seen:
                seen.add(action)
                generated_actions.append(action)
    except Exception:
        generated_actions = []

    actions = [
        action for action in expected_actions
        if action in generated_actions
    ]
    actions.extend(
        action for action in expected_actions
        if action not in actions
    )

    return {
        "actions": actions
    }