import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

def generate_points(n, w = 1, random=False): #Generates points on a kind of screwed up spiral not really
    # w is number of windings,
    # random determines whether angles are random. Should be off lol
    k = n-2
    points = [[0,0,1.0],[0,0,-1.0]] #Two points are deterministic
    anglelist = [w*l*2*np.pi/k for l in range(k)]
    if random:
        np.random.shuffle(anglelist)
    for i in range(k):
        points.append([np.sin(anglelist[i]),np.cos(anglelist[i]),1-2*i/k])
    points = np.array(points)
    points /= np.linalg.norm(points, axis=1)[:, None]
    points *= 3
    return points

def calculate_repulsive_force(points, power):
    num_points = len(points)
    forces = np.zeros_like(points)

    for i in range(num_points):
        for j in range(num_points):
            if i != j:
                delta = points[i] - points[j]
                distance = np.linalg.norm(delta)
                force = delta / (distance ** power)
                forces[i] += force

    return forces

def calculate_random_walk(num_points, r1 = 0.01):
    offset = np.random.rand(num_points, 3)
    for i in range(num_points):
        # x,y,z deltas
        # offset[i] = np.array([np.random.uniform(-r1,r1), np.random.uniform(-r1,r1), np.random.uniform(-r1,r1)])
        offset[i] = np.random.normal(0,r1,3)
    return offset
        
def update_points(points, forces, rand_walk, step_size=0.1):
    points += (rand_walk + step_size * forces)
    points /= np.linalg.norm(points, axis=1)[:, None]
    points *= 3
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
upperRange = 50
maxIter = 500
# frames = 500
# sequence = []
# r1init = 1
# r1final = 0.001
c2init = 0.05
c2final = 5
powerInitial = 1/2
powerFinal =  5
c2DecConstant = (c2final/c2init)**(1/maxIter)
powerDecConstant = (powerFinal/powerInitial)**(1/maxIter)
r1initVals = [5,3,2,1]
r1finalVals = [0.1, 0.01, 0.001, 0.0001]
for i in range(3,10):
    for r1init in r1initVals:
        for r1final in r1finalVals:
            r1DecConstant = (r1final/r1init)**(1/maxIter)
            for num_points in range(lowerRange,upperRange+1):
                best[num_points, r1init, r1final] = -np.inf
                points = generate_points(num_points, math.ceil(num_points/10), False)
                r1 = r1init ## random walk param, offset each coordinate with U[-r1, r1]
                c2 = c2init ## step size (force parameter)
                power = powerInitial
    
                for iteration in range(maxIter):
                    # if iteration % (maxIter//frames) == 0:   # Adds the position of the points at certain times
                    #     sequence.append(points.copy())
                    forces = calculate_repulsive_force(points, power)
                    walk = calculate_random_walk(num_points, r1)
                    points = update_points(points, forces, walk, c2)
    
                    min_distance_ = calculate_minimum_distance(points)
                    if (min_distance_ > best[num_points, r1init, r1final]):
                        best[num_points, r1init, r1final] = min_distance_
                    r1 *= r1DecConstant
                    c2 *= c2DecConstant
                    power *= powerDecConstant
                best[num_points, r1init, r1final] /= 3
                if (r1init == r1initVals[0] and r1final == r1finalVals[0]):
                    print(num_points)
            print("almost done")
    f = open(f'res/paramTuning_simAnnealing{i}.txt', "a")
    for r1init in [5, 3, 2, 1]:
        for r1final in [0.1, 0.01, 0.001, 0.0001]:
            for num_points in range(lowerRange, upperRange+1):
                f.write(":" + str(num_points) + " " + str(r1init) + " " + str(r1final))
                f.write("\n")
                f.write(str(best[num_points, r1init, r1final]))
                f.write("\n")
                f.write("\n")
    f.close()
