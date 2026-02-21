# algorithms.py
import math
import random
from utils import (
    calculate_route_distance, 
    create_initial_tour
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
        improvement = True
        n = len(self.current_tour)
        
        while improvement:
            improvement = False
            best_neighbor = None
            best_neighbor_cost = self.current_cost
            
            # On commence à 1 pour ne jamais toucher à la ville de départ (index 0)
            for i in range(1, n):
                for j in range(i + 1, n):
                    neighbor = self.current_tour.copy()
                    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                    
                    cost = calculate_route_distance(neighbor, self.distance_matrix)
                    
                    if cost < best_neighbor_cost:
                        best_neighbor_cost = cost
                        best_neighbor = neighbor
                        
                        if self.mode == "first":
                            improvement = True
                            break # Sortie immédiate si premier meilleur trouvé
                
                if improvement and self.mode == "first":
                    break

            if best_neighbor:
                self.current_tour = best_neighbor
                self.current_cost = best_neighbor_cost
                improvement = True
                    
        return self.current_tour, self.current_cost

class SimulatedAnnealing:
    def __init__(self, distance_matrix, initial_tour, T0=1000, alpha=0.99, T_min=0.1):
        self.distance_matrix = distance_matrix
        self.current_tour = initial_tour
        self.current_cost = calculate_route_distance(initial_tour, distance_matrix)
        self.T = T0
        self.alpha = alpha
        self.T_min = T_min
        self.best_tour = self.current_tour
        self.best_cost = self.current_cost

    def run(self):
        n = len(self.current_tour)
        
        while self.T > self.T_min:
            # On choisit deux indices entre 1 et n-1 pour garder l'index 0 fixe
            i, j = random.sample(range(1, n), 2)
            
            neighbor = self.current_tour.copy()
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbor_cost = calculate_route_distance(neighbor, self.distance_matrix)
            
            delta = neighbor_cost - self.current_cost
            
            if delta < 0 or random.random() < math.exp(-delta / self.T):
                self.current_tour = neighbor
                self.current_cost = neighbor_cost
                
                if self.current_cost < self.best_cost:
                    self.best_cost = self.current_cost
                    self.best_tour = self.current_tour
            
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

            # On explore le voisinage en ignorant l'index 0
            for i in range(1, n):
                for j in range(i + 1, n):
                    move = tuple(sorted((i, j)))
                    
                    neighbor = self.current_tour.copy()
                    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                    cost = calculate_route_distance(neighbor, self.distance_matrix)

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