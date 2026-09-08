def evaluate(execution_result):
    """
    Évalue si les actions ont été correctement exécutées.
    Ici : si tout est exécuté, on considère que c'est OK.
    """

    executed = execution_result.get("executed", [])

    if len(executed) > 0:
        return {"status": "done"}
    else:
        return {"status": "failed"}