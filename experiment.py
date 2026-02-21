import os
import time
import statistics
import matplotlib.pyplot as plt
from utils import create_initial_tour, plot_tsp_route
from algorithms import HillClimbing, SimulatedAnnealing,TabuSearch
from data_loader import load_tsplib_data, calculate_distance_matrix_from_coords

def generer_graphique_comparatif(resultats, folder_path, instance_name):
    """
    Crée un graphique à barres comparant les performances des algorithmes.
    """
    noms = [r['nom'] for r in resultats]
    meilleurs = [r['meilleur'] for r in resultats]
    moyennes = [r['moyenne'] for r in resultats]
    ecarts = [r['std'] for r in resultats]

    x = range(len(noms))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Barre pour le meilleur résultat et la moyenne
    rects1 = ax.bar([p - width/2 for p in x], meilleurs, width, label='Meilleur Coût', color='#2ecc71')
    rects2 = ax.bar([p + width/2 for p in x], moyennes, width, label='Coût Moyen', color='#3498db', yerr=ecarts, capsize=5)

    ax.set_ylabel('Distance (Coût)')
    ax.set_title(f'Comparaison Statistiques - {instance_name}')
    ax.set_xticks(x)
    ax.set_xticklabels(noms)
    ax.legend()

    # Ajouter les valeurs au-dessus des barres
    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    plt.tight_layout()
    plt.savefig(os.path.join(folder_path, "comparaison_algos.png"))
    plt.close()

def evaluer_algorithme(nom_algo, classe_algo, distance_matrix, coordinates, kwargs_algo, folder_path, num_runs=30):
    couts = []
    temps_exec = []
    meilleur_tour = None
    meilleur_cout = float('inf')
    num_villes = len(coordinates)
    
    print(f"  > Exécution de {nom_algo}...", end=" ", flush=True)
    
    for i in range(num_runs):
        tour_initial = create_initial_tour(num_villes)
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

    moyenne_cout = statistics.mean(couts)
    ecart_type_cout = statistics.stdev(couts) if num_runs > 1 else 0
    temps_moyen = statistics.mean(temps_exec)
    
    # Image du trajet
    file_safe_name = nom_algo.replace(" ", "_")
    image_path = os.path.join(folder_path, f"{file_safe_name}.png")
    titre_graphique = f"{nom_algo} - {num_villes} Villes\nMeilleur Coût: {meilleur_cout}"
    plot_tsp_route(meilleur_tour, coordinates, titre_graphique, image_path)
    
    # Retourner les stats pour le graphique comparatif
    return {
        "nom": nom_algo,
        "meilleur": meilleur_cout,
        "moyenne": round(moyenne_cout, 2),
        "std": round(ecart_type_cout, 2),
        "t_moy": round(temps_moyen, 4)
    }

def main():
    instances = [
        {"file": "ulysses20.tsp", "name": "Instance_20_Cities"},
        {"file": "berlin40.tsp", "name": "Instance_40_Cities"},
        {"file": "eil80.tsp", "name": "Instance_80_Cities"}
    ]
    
    NB_RUNS = 30 
    
    print("🚀 DÉMARRAGE DU PROTOCOLE EXPÉRIMENTAL TSP")

    for inst in instances:
        file_path = os.path.join("data", inst["file"])
        if not os.path.exists(file_path):
            print(f"❌ Fichier {file_path} introuvable.")
            continue

        output_folder = inst["name"]
        os.makedirs(output_folder, exist_ok=True)
        
        coords = load_tsplib_data(file_path)
        dist_matrix = calculate_distance_matrix_from_coords(coords)
        
        print(f"\n--- ANALYSE : {inst['file']} ({len(coords)} villes) ---")
        
        configurations = [
            ("HC First", HillClimbing, {"mode": "first"}),
            ("HC Best", HillClimbing, {"mode": "best"}),
            ("Recuit Simule", SimulatedAnnealing, {"T0": 1000, "alpha": 0.99, "T_min": 0.1}),
    ("Tabu Search", TabuSearch, {"tabu_size": 20, "max_iter": 100})
        ]
        
        resultats_instance = []
        
        for nom, classe, params in configurations:
            stats = evaluer_algorithme(nom, classe, dist_matrix, coords, params, output_folder, NB_RUNS)
            resultats_instance.append(stats)
            
            print(f"      🔹 Meilleur: {stats['meilleur']} | Moyenne: {stats['moyenne']} | Ecart-Type: {stats['std']}")

        # GÉNÉRATION DU GRAPHIQUE COMPARATIF PAR INSTANCE
        generer_graphique_comparatif(resultats_instance, output_folder, inst["name"])
        print(f"      📊 Graphique comparatif généré dans {output_folder}/")

    print("\n" + "="*50)
    print("✅ TOUTES LES EXPÉRIENCES SONT TERMINÉES.")
    print("="*50)

if __name__ == "__main__":
    main()