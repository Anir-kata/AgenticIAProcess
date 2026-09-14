# AgenticIAProcess

Version actuelle : 0.1.7

Projet d'agent IA autonome orienté gestion de tâches. Il observe les tâches en retard, reconnaît les statuts courants comme `late`, `todo`, `pending` et `overdue`, priorise les actions selon la priorité, mémorise les tâches déjà accomplies et produit un cycle de vie explicite d'agent.

## Fonctionnement

- Observer : détecte les tâches actives ou en retard (`late`, `todo`, `pending`, `overdue`)
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
