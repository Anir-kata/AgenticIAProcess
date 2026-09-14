def _fallback_actions(late_tasks):
    return [f"Relancer {task_name}" for task_name in late_tasks]


def plan(observation, tasks=None):
    """
    Génère un plan de relance déterministe et priorisé.
    Le planificateur ne dépend pas d'un service externe pour rester fiable,
    testable et réellement exécutable dans un agent autonome.
    """

    late_tasks = list(observation.get("late_tasks", set()))
    if tasks is not None:
        priorities = {}
        for task in tasks:
            name = str(task.get("name", "")).strip()
            if name:
                priorities[name] = int(task.get("priority", 0) or 0)
        late_tasks = sorted(
            late_tasks,
            key=lambda name: (-int(priorities.get(name, 0) or 0), str(name))
        )
    else:
        late_tasks = sorted(late_tasks, key=lambda item: str(item))

    return {"actions": _fallback_actions(late_tasks)}