import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def initialize_points(num_points):
    points = np.random.rand(num_points, 3)-0.5 # I added the -0.5 as then each point can come from any octant of the sphere
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
                force = delta / (distance ** 2)
                forces[i] += force

    return forces

def calculate_random_walk(num_points, r1 = 0.01):
    offset = np.random.rand(num_points, 3)
    for i in range(num_points):
        # x,y,z deltas
        offset[i] = np.array([np.random.uniform(-r1,r1), np.random.uniform(-r1,r1), np.random.uniform(-r1,r1)])
    return offset
        
def update_points(points, forces, rand_walk, r1 = 1, step_size=0.1):
    points += (rand_walk + np.random.uniform(1-r1, 1+r1) * step_size * forces)
    points /= np.linalg.norm(points, axis=1)[:, None]
    return points

def calculate_minimum_distance(points):
    min_distance = np.inf

    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            distance = np.linalg.norm(points[i] - points[j])
            min_distance = min(distance, min_distance)

    return min_distance

bestGen = {}
bestBas = {}
lowerRange = 2
upperRange = 30
for num_points in range(lowerRange,upperRange+1):
    bestGen[num_points] = -np.inf
    bestBas[num_points] = -np.inf
for iter in range(0, 30):
    print(f"Iteration {iter}")
    for num_points in range(lowerRange,upperRange+1):
    # num_points = 10
        genpoints = initialize_points(num_points)
        baspoints = initialize_points(num_points)
        r1 = 0.03 ## random walk param, offset each coordinate with U[-r1, r1]
        c2 = 0.1 ## step size (force parameter)
        r2 = 0.1 ## force randomness, multiply force by U[1-r2, 1+r2]
        for iteration in range(100):
            genforces = calculate_repulsive_force(genpoints)
            walk = calculate_random_walk(num_points, r1)
            genpoints = update_points(genpoints, genforces, walk, r2, c2)
        
            min_distance_gen = calculate_minimum_distance(genpoints)
            if (min_distance_gen > bestGen[num_points]):
                bestGen[num_points] = min_distance_gen

            basforces = calculate_repulsive_force(baspoints)
            baspoints = update_points(baspoints, basforces, np.zeros_like(baspoints), 0, 0.1)
        
            min_distance_bas = calculate_minimum_distance(baspoints)
            if (min_distance_bas > bestBas[num_points]):
                bestBas[num_points] = min_distance_bas


for num_points in range(lowerRange, upperRange+1):
    print(num_points)
    print(f"Basic: {bestBas[num_points]}")
    print(f"General: {bestGen[num_points]}")
    print(f"General - Basic: {bestGen[num_points] - bestBas[num_points]}")
    print()
