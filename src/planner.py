import json
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

def plan(observation):

    """
    Génère un plan d'action à partir de l'observation.
    Ici : relancer toutes les tâches en retard.
    """
    
    late_tasks = sorted(observation.get("late_tasks", set()))
    prompt = f"""
    Tu es un agent IA chargé de gérer des tâches en retard.
    Tâches en retard : {late_tasks}
    Réponds uniquement avec un objet JSON valide, par exemple :
    {{"actions": ["Relancer A", "Relancer C"]}}
    Remplace A et C par les noms réels des tâches. Il ne faut pas avoir de doublons.
    """

    response = client.chat.completions.create(
        model="llama3.2",
        messages=[
            {"role": "system", "content": "Tu es un planificateur IA."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    expected_actions = [f"Relancer {task_name}" for task_name in late_tasks]

    try:
        plan_json = json.loads(response.choices[0].message.content)
        generated_actions = plan_json.get("actions", [])
    except (json.JSONDecodeError, AttributeError):
        generated_actions = []

    generated_actions = set(generated_actions)
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