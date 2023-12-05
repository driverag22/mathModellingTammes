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
    # points += (rand_walk + np.random.uniform(1-r1, 1+r1) * step_size * forces)
    points += (rand_walk + step_size * forces)
    points /= np.linalg.norm(points, axis=1)[:, None]
    return points

def calculate_minimum_distance(points):
    min_distance = np.inf

    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            distance = np.linalg.norm(points[i] - points[j])
            min_distance = min(distance, min_distance)

    return min_distance

best = {}
lowerRange = 2
upperRange = 30
maxIter = 1000
# T = 500
tDecConstant = (1/T)**(1/100)
for num_points in range(lowerRange,upperRange+1):
    best[num_points] = -np.inf
for num_points in range(lowerRange,upperRange+1):
    print(num_points)
    points = initialize_points(num_points)
    ## r1 goes from 0.5 to 0.01
    r1 = 0.5 ## random walk param, offset each coordinate with U[-r1, r1]

    ## c2 goes from 0.01 to 0.5
    c2 = 0.1 ## step size (force parameter)
    r2 = 0.1 ## force randomness, multiply force by U[1-r2, 1+r2]
    
    for iteration in range(maxIter):
        # r1 *= np.log(T)/3
        # c2 *= min(np.exp(1/T) - 1/10, 0.1)
        forces = calculate_repulsive_force(points)
        walk = calculate_random_walk(num_points, r1)
        points = update_points(points, forces, walk, r2, c2)
    
        min_distance_ = calculate_minimum_distance(points)
        if (min_distance_ > best[num_points]):
            best[num_points] = min_distance_
        T *= tDecConstant # decrease temp
        r1 = 0.08
        c2 = 0.1
    


f = open("results/ouput_simAnnealing.txt", "a")
for num_points in range(lowerRange, upperRange+1):
    f.write(str(num_points))
    f.write("\n")
    f.write(str(best[num_points]))
    f.write("\n")
    f.write("\n")
    # print(num_points)
    # print(best[num_points])
    # print()
f.close()
