# utils.py
import random
import matplotlib.pyplot as plt
import os

# ==========================================
# 1. INITIALISATION & ÉVALUATION
# ==========================================

def create_initial_tour(num_cities):
    """
    Crée un tour aléatoire simple (ancienne méthode).
    """
    tour = list(range(num_cities))
    random.shuffle(tour)
    return tour

def create_strictly_fixed_initial_tour(num_cities):
    """
    Génère un tour commençant TOUJOURS par la ville d'index 0.
    Le reste des villes (1 à n-1) est mélangé aléatoirement.
    """
    villes_restantes = list(range(1, num_cities))
    random.shuffle(villes_restantes)
    # On force la ville 0 en première position
    return [0] + villes_restantes

def calculate_route_distance(route, distance_matrix):
    """
    Calcule la distance totale d'une route.
    Inclut le retour de la dernière ville vers la première.
    """
    total_distance = 0
    num_cities = len(route)
    
    for i in range(num_cities):
        current_city = route[i]
        next_city = route[(i + 1) % num_cities] 
        total_distance += distance_matrix[current_city][next_city]
        
    return total_distance

# ==========================================
# 2. VOISINAGE (SWAP)
# ==========================================

def generate_random_swap_neighbor(tour):
    """
    Choisit deux positions (hors index 0) et échange les villes.
    Utilisé pour le Recuit Simulé.
    """
    new_tour = tour.copy() 
    n = len(tour)
    # On choisit deux indices entre 1 et n-1 pour ne pas toucher au départ
    i, j = random.sample(range(1, n), 2)
    new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
    return new_tour

def generate_all_swap_neighbors(tour):
    """
    Génère TOUS les voisins possibles par échange (hors index 0).
    Utilisé pour le Hill-Climbing.
    """
    neighbors = []
    n = len(tour)
    for i in range(1, n):
        for j in range(i + 1, n):
            neighbor = tour.copy()
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbors.append(neighbor)
    return neighbors

# ==========================================
# 3. VISUALISATION
# ==========================================

def plot_tsp_route(tour, coordinates, title, save_path):
    """
    Génère un graphique du trajet TSP et le sauvegarde.
    Affiche la ville de départ en évidence.
    """
    plt.figure(figsize=(10, 7))
    
    # Extraire les coordonnées dans l'ordre du tour
    ordered_coords = [coordinates[i] for i in tour]
    # Retour à la ville de départ
    ordered_coords.append(coordinates[tour[0]])
    
    x, y = zip(*ordered_coords)
    
    # Tracer les chemins (Lignes)
    plt.plot(x, y, color='#e74c3c', linewidth=1, alpha=0.7, zorder=1)
    
    # Tracer toutes les villes (Points bleus)
    all_x, all_y = zip(*coordinates)
    plt.scatter(all_x, all_y, color='#3498db', s=30, zorder=2)
    
    # Tracer la ville de départ (GROS POINT VERT)
    # On prend la première ville du tour (qui doit être l'index 0)
    start_city = coordinates[tour[0]]
    plt.scatter(start_city[0], start_city[1], color='#2ecc71', s=150, 
                edgecolors='black', label='Départ (Fixé)', zorder=3)
    
    plt.title(title)
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.5)
    
    plt.savefig(save_path, dpi=300)
    plt.close()