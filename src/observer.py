def observe(tasks):
    """
    Observe l'etat des taches et retourne les taches en retard.

    tasks : liste de dictionnaires
        Exemple :
        [
            {"name": "A", "status": "late"},
            {"name": "B", "status": "ok"},
            {"name": "C", "status": "late"}
        ]
    """
    late_tasks = set()
    for t in tasks:
        if t["status"] == "late":
            late_tasks.add(t["name"])

    return {
        "late_tasks": late_tasks
    }