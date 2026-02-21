# 🌍 OPTIMISATION DU VOYAGEUR DE COMMERCE (TSP) - METAHEURISTIQUES 

## 🎓 Cadre Académique
* **Établissement :** Université Hassan II de Casablanca – ENSET Mohammedia
* **Master :** SDIA (Systèmes de Données & Intelligence Artificielle) / GESI
* **Module :** Optimisation / Métaheuristiques
* **Encadrant :** Pr. Mohammed MESTARI
* **Année universitaire :** 2025–2026

## 👥 Auteurs
* **Mustapha Elmifdali**
* **Mbarek Etalebi**

---

## 📝 Résumé du Projet

Le TSP est un problème de décision de classe **NP-difficile**. Il consiste à trouver le plus court **cycle hamiltonien** dans un graphe complet pondéré $G = (V, E, w)$ de $N$ sommets (villes).

Formellement, étant donné un ensemble de villes $\mathcal{C} = \{c_0, c_1, \dots, c_{n-1}\}$ et une matrice de distances $D \in \mathbb{R}^{n \times n}$, l'objectif est de minimiser la longueur totale de la tournée :

$$
\text{Minimiser} \quad f(\pi) = \sum_{i=0}^{n-1} d\!\left(\pi_i,\, \pi_{(i+1) \bmod n}\right)
$$

sous la contrainte que $\pi$ est une permutation de $\{0, \dots, n-1\}$, où $d(u, v)$ est la **distance euclidienne** entre les villes $u$ et $v$ :

$$
d(u, v) = \sqrt{(x_u - x_v)^2 + (y_u - y_v)^2}
$$

### Algorithmes Implémentés
Nous avons exploré et comparé quatre approches algorithmiques pour naviguer dans cet espace de recherche discret :
1.  **Hill Climbing (First Improvement)** : Une recherche locale gloutonne qui accepte le premier voisin améliorant trouvé.
2.  **Hill Climbing (Best Improvement)** : Une exploration exhaustive du voisinage immédiat pour choisir la direction la plus prometteuse.
3.  **Recuit Simulé (Simulated Annealing)** : Une métaheuristique stochastique permettant d'accepter des solutions dégradantes selon une probabilité décroissante pour s'échapper des optima locaux.
4.  **Recherche Tabou (Tabu Search)** : Une méthode utilisant une mémoire à court terme (liste tabou) pour interdire les mouvements récents et forcer l'exploration de nouvelles zones.

---

## 📊 Protocole Expérimental
Conformément à la démarche scientifique, chaque algorithme est évalué sur **30 runs indépendants**. Les statistiques extraites permettent d'analyser la convergence, la qualité de la solution (Meilleur coût) et la robustesse (Écart-type). **Le point de départ est fixé à la ville 0 pour tous les tests.**

---

## 📍 Instance 1 : Instance_20_Cities (20 villes)
Instance de petite taille basée sur l'Odyssée d'Ulysse.

### Statistiques
| Algorithme | Meilleur Coût | Coût Moyen | Ecart-Type | Temps (s) |
| :--- | :---: | :---: | :---: | :---: |
| **HC First Improvement** | 5366 | 6402.17 | 554.84 | 0.0038 |
| **HC Best Improvement** | 5535 | 6199.87 | 407.33 | 0.0048 |
| **Recuit Simulé** | 5634 | 6313.27 | 353.95 | 0.0038 |
| **Tabu Search** | **5278** | **5717.43** | **226.73** | **0.0407** |

### Visualisation des Meilleurs Trajets
| HC First Improvement | HC Best Improvement |
| :---: | :---: |
| ![HC First](Instance_20_Cities/HC_First.png) | ![HC Best](Instance_20_Cities/HC_Best.png) |
| **Recuit Simulé** | **Tabu Search** |
| ![Recuit](Instance_20_Cities/Recuit_Simule.png) | ![Tabu](Instance_20_Cities/Tabu_Search.png) |

**Analyse des Performances :**
![Comparaison 20](Instance_20_Cities/comparaison_algos.png) 
---

| 🏆 **Meilleur algorithme :** Tabu Search — Score moyen : **5645.23** (Stabilité ±233.19)|
| :---: |
| ![Tabu](Instance_20_Cities/Tabu_Search.png)|



---

## 📍 Instance 2 : Instance_40_Cities (40 villes)
Instance intermédiaire basée sur Berlin.

### Statistiques
| Algorithme | Meilleur Coût | Coût Moyen | Ecart-Type | Temps (s) |
| :--- | :---: | :---: | :---: | :---: |
| **HC First Improvement** | 7572 | 8815.80 | 720.61 | 0.0787 |
| **HC Best Improvement** | 7563 | 8778.17 | 701.58 | 0.0822 |
| **Recuit Simulé** | 9214 | 10293.47 | 559.05 | 0.0054 |
| **Tabu Search** | **7256** | **8223.40** | **535.04** | **0.2798** |

### Visualisation des Meilleurs Trajets
| HC First Improvement | HC Best Improvement |
| :---: | :---: |
| ![HC First](Instance_40_Cities/HC_First.png) | ![HC Best](Instance_40_Cities/HC_Best.png) |
| **Recuit Simulé** | **Tabu Search** |
| ![Recuit](Instance_40_Cities/Recuit_Simule.png) | ![Tabu](Instance_40_Cities/Tabu_Search.png) |

**Analyse des Performances :**
![Comparaison 40](Instance_40_Cities/comparaison_algos.png) 
---

| 🏆 **Meilleur algorithme :** Tabu Search — Score moyen : **8190.43** (Stabilité ±478.71) |
| :---: |
| ![Tabu](Instance_40_Cities/Tabu_Search.png)|


---

## 📍 Instance 3 : Instance_80_Cities (80 villes)
Instance à large échelle testant les limites de convergence.

### Statistiques
| Algorithme | Meilleur Coût | Coût Moyen | Ecart-Type | Temps (s) |
| :--- | :---: | :---: | :---: | :---: |
| **HC First Improvement** | **11374** | **13299.27** | 990.91 | 1.3441 |
| **HC Best Improvement** | 11796 | 13615.60 | 1067.18 | 1.6899 |
| **Recuit Simulé** | 19723 | 21358.43 | 875.38 | 0.0085 |
| **Tabu Search** | 11594 | 13454.97 | 1081.16 | 2.1154 |

### Visualisation des Meilleurs Trajets
| HC First Improvement | HC Best Improvement |
| :---: | :---: |
| ![HC First](Instance_80_Cities/HC_First.png) | ![HC Best](Instance_80_Cities/HC_Best.png) |
| **Recuit Simulé** | **Tabu Search** |
| ![Recuit](Instance_80_Cities/Recuit_Simule.png) | ![Tabu](Instance_80_Cities/Tabu_Search.png) |

**Analyse des Performances :**
![Graphique Comparatif](Instance_80_Cities/comparaison_algos.png) 
---

| 🏆 **Meilleur algorithme :** HC First — Score moyen : **12847.03** (Stabilité ±765.19) |
| :---: |
| ![HC First](Instance_80_Cities/HC_First.png)|
---

## 🗺️ Analyse de la Meilleure Solution (Best Traject)
L'analyse visuelle des solutions montre une élimination des croisements de segments. La fixation du point de départ à la **Ville 0** (point de départ des tracés) est respectée sur toutes les instances. La Recherche Tabou s'avère la plus stable sur 20 et 40 villes, tandis que le Hill Climbing (First) est plus performant sur 80 villes.



---

## 🛠️ Structure du Projet
```
ProjetM1-optimization/
│
├── data/              # Dossier contenant les fichiers de données TSPLIB (`.tsp`).
├── algorithms.py      # Logique : HillClimbing, SimulatedAnnealing, TabuSearch
├── experiment.py      # Orchestrateur : lance les tests et génère les images
├── utils.py           # Fonctions utilitaires (calculs, voisinages, Matplotlib)
└── data_loader.py     # Module de lecture des fichiers .tsp
```

## 🚀 Utilisation

**1. Installer les dépendances :**
```bash
pip install matplotlib
```

**2. Lancer le protocole :**
```bash
python experiment.py
```