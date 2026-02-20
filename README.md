# 🚀 Projet d'Optimisation : Problème du Voyageur de Commerce (TSP)

Ce projet implémente et compare plusieurs métaheuristiques pour résoudre le Problème du Voyageur de Commerce (TSP). L'objectif est de trouver le cycle le plus court passant par un ensemble de villes, en revenant au point de départ.

## 📊 Protocole Expérimental
Pour garantir la rigueur scientifique (Section 4 de l'énoncé), chaque algorithme a été testé sur **30 runs indépendants**. Les statistiques ci-dessous résument la performance et la stabilité de chaque approche.

---

## 📍 Instance : Ulysses20 (20 villes)
Instance de petite taille basée sur l'Odyssée d'Ulysse.

### Statistiques
| Algorithme | Meilleur Coût | Coût Moyen | Écart-Type |
| :--- | :---: | :---: | :---: |
| **HC First Improvement** | 72 | 85.57 | 8.56 |
| **HC Best Improvement** | 72 | 79.83 | 6.36 |
| **Recuit Simulé** | 75 | 86.67 | 7.27 |

### Visualisation des Résultats
| HC First | HC Best | Recuit Simulé |
| :---: | :---: | :---: |
| ![HC First](Instance_20_Cities/HC_First.png) | ![HC Best](Instance_20_Cities/HC_Best.png) | ![Recuit](Instance_20_Cities/Recuit_Simule.png) |

**Graphique Comparatif :**
![Comparaison 20](Instance_20_Cities/comparaison_algos.png)

---

## 📍 Instance : Berlin40 (40 villes)
Instance de taille intermédiaire (tronquée de Berlin52).

### Statistiques
| Algorithme | Meilleur Coût | Coût Moyen | Écart-Type |
| :--- | :---: | :---: | :---: |
| **HC First Improvement** | 7368 | 8380.37 | 629.61 |
| **HC Best Improvement** | 7669 | 8571.10 | 485.94 |
| **Recuit Simulé** | 9520 | 10303.37 | 483.94 |

### Visualisation des Résultats
| HC First | HC Best | Recuit Simulé |
| :---: | :---: | :---: |
| ![HC First](Instance_40_Cities/HC_First.png) | ![HC Best](Instance_40_Cities/HC_Best.png) | ![Recuit](Instance_40_Cities/Recuit_Simule.png) |

**Graphique Comparatif :**
![Comparaison 40](Instance_40_Cities/comparaison_algos.png)

---

## 📍 Instance : Eil80 (80 villes)
Instance à grande échelle pour tester la robustesse des algorithmes.

### Statistiques
| Algorithme | Meilleur Coût | Coût Moyen | Écart-Type |
| :--- | :---: | :---: | :---: |
| **HC First Improvement** | 11508 | 12846.63 | 752.43 |
| **HC Best Improvement** | 11618 | 13267.53 | 887.72 |
| **Recuit Simulé** | 19584 | 21796.83 | 936.30 |

### Visualisation des Résultats
| HC First | HC Best | Recuit Simulé |
| :---: | :---: | :---: |
| ![HC First](Instance_80_Cities/HC_First.png) | ![HC Best](Instance_80_Cities/HC_Best.png) | ![Recuit](Instance_80_Cities/Recuit_Simule.png) |

**Graphique Comparatif :**
![Comparaison 80](Instance_80_Cities/comparaison_algos.png)

---

## 🛠️ Structure du Projet
- **`experiment.py`** : Lance le protocole de test sur les 3 instances et génère les dossiers d'images.
- **`algorithms.py`** : Contient les classes `HillClimbing` et `SimulatedAnnealing`.
- **`utils.py`** : Fonctions de calcul de distance, gestion des tours et génération des graphiques.
- **`data_loader.py`** : Charge les fichiers `.tsp`.
- **`data/`** : Contient les fichiers sources des villes.

## 🚀 Comment l'utiliser ?
1. Installer les dépendances : `pip install matplotlib numpy`
2. Exécuter le script principal :
   ```bash
   python experiment.py