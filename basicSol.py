import numpy as np

def initialize_points(num_points):
    points = np.random.rand(num_points, 3)
    points /= np.linalg.norm(points, axis=1)[:, None]
    return points

def calculate_repulsive_force(points):
    num_points = len(points)
    forces = np.zeros_like(points)

    for i in range(num_points):
        for j in range(num_points):
            if i != j:
                delta = points[i] - points[j]
                distance = np.linalg.norm(delta)
                force = delta / (distance ** 3)
                forces[i] += force

    return forces

def update_points(points, forces, step_size=0.1):
    points += step_size * forces
    points /= np.linalg.norm(points, axis=1)[:, None]

def calculate_minimum_distance(points):
    min_distance = np.inf

    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            distance = np.linalg.norm(points[i] - points[j])
            if (distance < min_distance): min_distance = distance

    return min_distance

# Example usage:
num_points = 10
points = initialize_points(num_points)

for iteration in range(100):
    forces = calculate_repulsive_force(points)
    update_points(points, forces)

    min_distance = calculate_minimum_distance(points)
    print(f"Iteration {iteration + 1}: Minimum Distance = {min_distance}")
    for p in points:
        if (abs(np.linalg.norm(p) - 1) > 0.01):
            print("error")
            return 
        print(p)

