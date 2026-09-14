# AgenticIAProcess

Version actuelle : 0.1.3

Projet d'agent IA orienté gestion de tâches. Il observe les tâches en retard, construit un plan de relance, exécute les actions et évalue le résultat via une classe réutilisable `TaskAgent`.

## Fonctionnement

- Observer : détecte les tâches avec le statut `late`
- Planifier : génère les actions de relance
- Exécuter : simule l'exécution des actions
- Évaluer : vérifie qu'au moins une action a bien été exécutée

## Exécution

```bash
python src/agent.py
```

## Tests

```bash
python -m pytest -q
```

Le planificateur utilise un retour de secours déterministe si le service Ollama n'est pas disponible, afin de garder le comportement stable et testable.