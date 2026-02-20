import random
import matplotlib.pyplot as plt
import os

# ==========================================
# 1. INITIALIZATION & EVALUATION
# ==========================================

def create_initial_tour(num_cities):
    """
    Creates a random initial route (a permutation of cities).
    Example for 5 cities: [2, 0, 4, 1, 3]
    """
    tour = list(range(num_cities))
    random.shuffle(tour)
    return tour

def calculate_route_distance(route, distance_matrix):
    """
    Calculates the total distance of a given route using the distance matrix.
    Includes the return trip from the last city back to the first.
    """
    total_distance = 0
    num_cities = len(route)
    
    for i in range(num_cities):
        current_city = route[i]
        next_city = route[(i + 1) % num_cities] # Wraps around to 0 at the end
        total_distance += distance_matrix[current_city][next_city]
        
    return total_distance


# ==========================================
# 2. SWAP NEIGHBORHOOD (For basic algorithms)
# ==========================================
# 

def generate_random_swap_neighbor(tour):
    """
    Picks two random positions and swaps the cities at those positions.
    (Used mainly for Simulated Annealing)
    """
    new_tour = tour.copy() 
    n = len(tour)
    
    # Choose two different random indices
    i, j = random.sample(range(n), 2)
    
    # Swap the cities
    new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
    
    return new_tour

def generate_all_swap_neighbors(tour):
    """
    Generates a list of ALL possible neighbors by swapping 2 by 2.
    (Used mainly for Hill-Climbing Best/First Improvement)
    """
    neighbors = []
    n = len(tour)
    
    for i in range(n):
        for j in range(i + 1, n):
            neighbor = tour.copy()
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbors.append(neighbor)
            
    return neighbors


# ==========================================
# 3. 2-OPT NEIGHBORHOOD (Optional but highly recommended)
# ==========================================
# 

def generate_2opt_neighbor(tour, i, j):
    """
    Reverses the order of the cities in the segment from index i to index j.
    Assumes i < j.
    """
    # Keep the start, reverse the middle part, keep the end
    new_tour = tour[:i] + tour[i:j+1][::-1] + tour[j+1:]
    return new_tour

def generate_random_2opt_neighbor(tour):
    """
    Generates a single random 2-opt neighbor.
    (Can be used as an upgrade for Simulated Annealing)
    """
    n = len(tour)
    # Pick two random indices and make sure i < j using sorted()
    i, j = sorted(random.sample(range(n), 2))
    
    return generate_2opt_neighbor(tour, i, j)

def generate_all_2opt_neighbors(tour):
    """
    Generates a list of ALL possible 2-opt neighbors.
    (Can be used as an upgrade for Hill-Climbing)
    """
    neighbors = []
    n = len(tour)
    for i in range(n - 1):
        for j in range(i + 1, n):
            neighbors.append(generate_2opt_neighbor(tour, i, j))
    return neighbors

def plot_tsp_route(tour, coordinates, title, save_path):
    """
    Génère un graphique du trajet TSP et le sauvegarde en image.
    """
    plt.figure(figsize=(10, 7))
    
    # Extraire les coordonnées dans l'ordre du tour
    ordered_coords = [coordinates[i] for i in tour]
    # Ajouter le retour à la ville de départ
    ordered_coords.append(coordinates[tour[0]])
    
    x, y = zip(*ordered_coords)
    
    # Tracer les chemins
    plt.plot(x, y, color='red', linewidth=1, alpha=0.7, zorder=1)
    
    # Tracer toutes les villes (bleu)
    all_x, all_y = zip(*coordinates)
    plt.scatter(all_x, all_y, color='blue', s=30, zorder=2)
    
    # Tracer la ville de départ (GROS CERCLE VERT)
    start_city = coordinates[tour[0]]
    plt.scatter(start_city[0], start_city[1], color='lime', s=150, 
                edgecolors='black', label='Start City', zorder=3)
    
    plt.title(title)
    plt.legend()
    
    # Sauvegarde automatique
    plt.savefig(save_path)
    plt.close() # Fermer pour libérer la mémoire