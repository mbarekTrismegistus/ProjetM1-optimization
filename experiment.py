import os
import time
import statistics
import random
import matplotlib.pyplot as plt
from utils import plot_tsp_route, create_strictly_fixed_initial_tour
from algorithms import HillClimbing, SimulatedAnnealing, TabuSearch
from data_loader import load_tsplib_data, calculate_distance_matrix_from_coords

def generer_graphique_comparatif(resultats, folder_path, instance_name):
    """
    Design Esign : Graphique avec barres d'erreur pour l'écart-type.
    """
    noms = [r['nom'] for r in resultats]
    meilleurs = [r['meilleur'] for r in resultats]
    moyennes = [r['moyenne'] for r in resultats]
    ecarts = [r['std'] for r in resultats]

    x = range(len(noms))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Barres pour le meilleur résultat et la moyenne avec barres d'erreur
    rects1 = ax.bar([p - width/2 for p in x], meilleurs, width, label='Meilleur Coût', color='#2ecc71')
    rects2 = ax.bar([p + width/2 for p in x], moyennes, width, label='Coût Moyen', color='#3498db', yerr=ecarts, capsize=5)

    ax.set_ylabel('Distance (Coût)')
    ax.set_title(f'Statistiques - {instance_name} (Départ Fixe)')
    ax.set_xticks(x)
    ax.set_xticklabels(noms)
    ax.legend()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    plt.tight_layout()
    plt.savefig(os.path.join(folder_path, "comparaison_algos.png"))
    plt.close()

def evaluer_algorithme(nom_algo, classe_algo, distance_matrix, coordinates, fixed_tours, kwargs_algo, folder_path):
    couts = []
    temps_exec = []
    meilleur_tour = None
    meilleur_cout = float('inf')
    
    print(f"  > Exécution de {nom_algo}...", end=" ", flush=True)
    
    for i in range(len(fixed_tours)):
        # Utilisation du tour pré-généré (Ville 0 fixée)
        tour_initial = list(fixed_tours[i])
        algo = classe_algo(distance_matrix, tour_initial, **kwargs_algo)
        
        debut = time.time()
        tour_final, cout_final = algo.run()
        fin = time.time()
        
        couts.append(cout_final)
        temps_exec.append(fin - debut)
        
        if cout_final < meilleur_cout:
            meilleur_cout = cout_final
            meilleur_tour = tour_final
    
    print("Terminé.")

    stats = {
        "nom": nom_algo,
        "meilleur": meilleur_cout,
        "moyenne": round(statistics.mean(couts), 2),
        "std": round(statistics.stdev(couts), 2),
        "t_moy": round(statistics.mean(temps_exec), 4)
    }
    
    image_path = os.path.join(folder_path, f"{nom_algo.replace(' ', '_')}.png")
    plot_tsp_route(meilleur_tour, coordinates, f"{nom_algo} - Best: {meilleur_cout}", image_path)
    
    return stats

def main():
    instances = [
        {"file": "ulysses20.tsp", "name": "Instance_20_Cities"},
        {"file": "berlin40.tsp", "name": "Instance_40_Cities"},
        {"file": "eil80.tsp", "name": "Instance_80_Cities"}
    ]
    
    NB_RUNS = 30 
    print("\n🚀 DÉMARRAGE DU PROTOCOLE : DÉPART FIXE & STATS")

    for inst in instances:
        file_path = os.path.join("data", inst["file"])
        if not os.path.exists(file_path): continue

        output_folder = inst["name"]
        os.makedirs(output_folder, exist_ok=True)
        
        coords = load_tsplib_data(file_path)
        dist_matrix = calculate_distance_matrix_from_coords(coords)
        
        # --- Tours de départ identiques pour tous les algos (Ville 0 fixe) ---
        tours_fixes = [create_strictly_fixed_initial_tour(len(coords)) for _ in range(NB_RUNS)]
        
        print(f"\n--- ANALYSE : {inst['name']} ({len(coords)} villes) ---")
        # Design du terminal aligné
        print(f"{'Algorithme':<18} | {'Meilleur':<10} | {'Moyenne':<10} | {'Ecart-Type':<10} | {'Temps (s)':<10}")
        print("-" * 75)
        
        configurations = [
            ("HC First", HillClimbing, {"mode": "first"}),
            ("HC Best", HillClimbing, {"mode": "best"}),
            ("Recuit Simule", SimulatedAnnealing, {"T0": 1000, "alpha": 0.99, "T_min": 0.1}),
            ("Tabu Search", TabuSearch, {"tabu_size": 20, "max_iter": 100})
        ]
        
        resultats_instance = []
        for nom, classe, params in configurations:
            stats = evaluer_algorithme(nom, classe, dist_matrix, coords, tours_fixes, params, output_folder)
            resultats_instance.append(stats)
            print(f"{nom:<18} | {stats['meilleur']:<10.0f} | {stats['moyenne']:<10.2f} | {stats['std']:<10.2f} | {stats['t_moy']:<10.4f}")

        # --- Élection du Meilleur Algo sur les Statistiques ---
        # On choisit celui qui a la moyenne la plus basse
        best_algo = min(resultats_instance, key=lambda x: x['moyenne'])
        
        print("-" * 75)
        print(f"🏆 MEILLEUR ALGO POUR {inst['name']} : {best_algo['nom']}")
        print(f"   Score moyen: {best_algo['moyenne']} (Stabilité ±{best_algo['std']})")
        print("-" * 75)

        generer_graphique_comparatif(resultats_instance, output_folder, inst["name"])

    print("\n" + "="*50)
    print("✅ TOUTES LES EXPÉRIENCES SONT TERMINÉES.")
    print("="*50)

if __name__ == "__main__":
    main()