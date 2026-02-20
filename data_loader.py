import math

def load_tsplib_data(filepath):
    """
    Reads a TSPLIB file and extracts the coordinates.
    """
    coordinates = []
    with open(filepath, 'r') as file:
        lines = file.readlines()
        
        reading_nodes = False
        for line in lines:
            line = line.strip()
            if line == "NODE_COORD_SECTION":
                reading_nodes = True
                continue
            if line == "EOF":
                break
                
            if reading_nodes:
                # TSPLIB format: Node_ID X_Coordinate Y_Coordinate
                parts = line.split()
                if len(parts) >= 3:
                    x = float(parts[1])
                    y = float(parts[2])
                    coordinates.append((x, y))
                    
    return coordinates

def calculate_distance_matrix(coordinates):
    """
        Creates a 2D matrix where matrix[i][j] is the Euclidean distance 
        between city i and city j, rounded to the nearest integer.
    """
    n = len(coordinates)
    # Initialize an n x n matrix with zeros
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            if i != j:
                x1, y1 = coordinates[i]
                x2, y2 = coordinates[j]
                # Calculate Euclidean distance
                distance = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
                # Rounding to the nearest integer as suggested by the assignment
                matrix[i][j] = round(distance)
                
    return matrix

# --- Example Usage ---
# Ensure you have downloaded 'berlin52.tsp' as an example of a tsp file into a 'data' folder

coords = load_tsplib_data("data/berlin52.tsp")
dist_matrix = calculate_distance_matrix(coords)
print(f"Loaded {len(coords)} cities. Distance between city 0 and 1: {dist_matrix[0][1]}")