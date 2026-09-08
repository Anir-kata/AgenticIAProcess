def execute(plan):
    """
    Exécute les actions du plan.
    Ici : on simule l'exécution.
    """

    actions = plan.get("actions", [])

    executed = []
    for action in actions:
        executed.append(action)

    return {
        "executed": executed
    }