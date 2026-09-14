# AgenticIAProcess

Version actuelle : 0.1.4

Projet d'agent IA autonome orienté gestion de tâches. Il observe les tâches en retard, priorise les actions selon la priorité, mémorise les tâches déjà accomplies et garde un historique de l'exécution.

## Fonctionnement

- Observer : détecte les tâches avec le statut `late`
- Prioriser : trie les tâches en retard par priorité décroissante
- Planifier : génère un plan de relance
- Exécuter : simule l'exécution des actions
- Mémoriser : conserve l'historique et les tâches déjà traitées
- Évaluer : vérifie qu'au moins une action a bien été exécutée

## Exécution

```bash
python src/agent.py
```

## Tests

```bash
python -m pytest -q
```
