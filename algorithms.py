# algorithms.py
import math
import random
# Import our tools from the utils file we just made
from utils import (
    create_initial_tour, 
    calculate_route_distance, 
    generate_all_swap_neighbors
)

class HillClimbing:
    def __init__(self, distance_matrix, initial_tour, mode="best"):
        """
        mode: "best" for Best Improvement, "first" for First Improvement
        """
        self.distance_matrix = distance_matrix
        self.current_tour = initial_tour
        self.current_cost = calculate_route_distance(initial_tour, distance_matrix)
        self.mode = mode

    def run(self):
        """
        Executes the Hill-Climbing algorithm until no better neighbor is found.
        """
        improvement = True
        
        # Keep looping as long as we keep finding better routes
        while improvement:
            improvement = False
            
            if self.mode == "best":
                # --- BEST IMPROVEMENT LOGIC ---
                # Generate ALL possible neighbors
                neighbors = generate_all_swap_neighbors(self.current_tour)
                
                best_neighbor = None
                best_neighbor_cost = self.current_cost
                
                # Check every single neighbor to find the absolute best
                for neighbor in neighbors:
                    cost = calculate_route_distance(neighbor, self.distance_matrix)
                    if cost < best_neighbor_cost:
                        best_neighbor_cost = cost
                        best_neighbor = neighbor
                
                # If we found a strictly better neighbor, move to it
                if best_neighbor is not None:
                    self.current_tour = best_neighbor
                    self.current_cost = best_neighbor_cost
                    improvement = True
                    
            elif self.mode == "first":
                # --- FIRST IMPROVEMENT LOGIC ---
                n = len(self.current_tour)
                # We generate neighbors on the fly and stop immediately if one is better
                for i in range(n):
                    for j in range(i + 1, n):
                        # Create a neighbor
                        neighbor = self.current_tour.copy()
                        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                        
                        # Calculate its cost
                        cost = calculate_route_distance(neighbor, self.distance_matrix)
                        
                        # The MOMENT we find a better one, adopt it and break the loops
                        if cost < self.current_cost:
                            self.current_tour = neighbor
                            self.current_cost = cost
                            improvement = True
                            break # Break inner loop
                    if improvement:
                        break # Break outer loop
                        
        return self.current_tour, self.current_cost


class MultiStartHillClimbing:
    def __init__(self, distance_matrix, num_cities, num_starts=30, mode="best"):
        """
        Runs Hill Climbing multiple times from different random starting points.
        """
        self.distance_matrix = distance_matrix
        self.num_cities = num_cities
        self.num_starts = num_starts
        self.mode = mode
        
        self.best_global_tour = None
        self.best_global_cost = float('inf')

    def run(self):
        """
        Executes the multi-start process.
        """
        for _ in range(self.num_starts):
            # 1. Generate a brand new random starting point
            initial_tour = create_initial_tour(self.num_cities)
            
            # 2. Create a HillClimbing instance with this new start
            hc = HillClimbing(self.distance_matrix, initial_tour, mode=self.mode)
            
            # 3. Run it to find the local optimum
            final_tour, final_cost = hc.run()
            
            # 4. Compare it to our all-time best. If it's better, save it!
            if final_cost < self.best_global_cost:
                self.best_global_cost = final_cost
                self.best_global_tour = final_tour
                
        return self.best_global_tour, self.best_global_cost
    


class SimulatedAnnealing:
    def __init__(self, distance_matrix, initial_tour, T0=1000, alpha=0.99, T_min=0.1):
        """
        T0: Initial high temperature
        alpha: Cooling rate (e.g., 0.99 means T decreases by 1% each step)
        T_min: The temperature at which the algorithm stops
        """
        self.distance_matrix = distance_matrix
        self.current_tour = initial_tour
        self.current_cost = calculate_route_distance(initial_tour, distance_matrix)
        
        self.T = T0
        self.alpha = alpha
        self.T_min = T_min
        
        # Keep track of the absolute best we've ever seen
        self.best_tour = self.current_tour
        self.best_cost = self.current_cost

    def run(self):
        from utils import generate_random_swap_neighbor # Import our tool
        
        # Keep running until the system "freezes"
        while self.T > self.T_min:
            # 1. Pick just ONE random neighbor
            neighbor = generate_random_swap_neighbor(self.current_tour)
            neighbor_cost = calculate_route_distance(neighbor, self.distance_matrix)
            
            # 2. Calculate the difference in cost
            delta = neighbor_cost - self.current_cost
            
            # 3. Decide whether to move to this neighbor
            if delta < 0:
                # It's a BETTER route! Always accept it.
                self.current_tour = neighbor
                self.current_cost = neighbor_cost
                
                # Is it the best we've ever seen overall?
                if self.current_cost < self.best_cost:
                    self.best_cost = self.current_cost
                    self.best_tour = self.current_tour
            else:
                # It's a WORSE route! Accept it ONLY with a certain probability
                # Probability = exp(-delta / T)
                probability = math.exp(-delta / self.T)
                
                if random.random() < probability:
                    # We got lucky and accepted the worse move!
                    self.current_tour = neighbor
                    self.current_cost = neighbor_cost
            
            # 4. Cool down the temperature
            self.T *= self.alpha
            
        return self.best_tour, self.best_cost
    
class TabuSearch:
    def __init__(self, distance_matrix, initial_tour, tabu_size=15, max_iter=200):
        self.distance_matrix = distance_matrix
        self.current_tour = initial_tour
        self.current_cost = calculate_route_distance(initial_tour, distance_matrix)
        self.tabu_size = tabu_size
        self.max_iter = max_iter
        
        self.best_tour = self.current_tour
        self.best_cost = self.current_cost

    def run(self):
        from collections import deque
        tabu_list = deque(maxlen=self.tabu_size)
        n = len(self.current_tour)

        for _ in range(self.max_iter):
            best_candidate = None
            best_candidate_cost = float('inf')
            best_move = None

            # On explore le voisinage par Swap
            for i in range(n):
                for j in range(i + 1, n):
                    move = tuple(sorted((i, j)))
                    
                    # Générer voisin
                    neighbor = self.current_tour.copy()
                    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                    cost = calculate_route_distance(neighbor, self.distance_matrix)

                    # Critère : non tabou OU amélioration globale (aspiration)
                    if move not in tabu_list or cost < self.best_cost:
                        if cost < best_candidate_cost:
                            best_candidate_cost = cost
                            best_candidate = neighbor
                            best_move = move

            if best_candidate:
                self.current_tour = best_candidate
                self.current_cost = best_candidate_cost
                tabu_list.append(best_move)
                
                if best_candidate_cost < self.best_cost:
                    self.best_cost = best_candidate_cost
                    self.best_tour = best_candidate

        return self.best_tour, self.best_cost