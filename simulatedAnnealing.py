import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

def generate_points(n, w = 1, scaleFactor = 3, random=False): #Generates points on a kind of screwed up spiral not really
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
    points *= scaleFactor
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
        
def update_points(points, forces, rand_walk, scaleFactor = 3, step_size=0.1):
    points += (rand_walk + step_size * forces)
    points /= np.linalg.norm(points, axis=1)[:, None]
    points *= scaleFactor
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
upperRange = 200
maxIter = 1000
# frames = 500
# sequence = []
r1init = 1.43
r1final = 0.0002
c2init = 0.0369
c2final = 1.091
powerInitial = 1.419
powerFinal =  3.355
scaleFactor = 1.244
# parameter = [1.4287813154425049, 0.00016871670937294693, 0.03694326343695675, 1.0908696537706244, 1.41877422689782, 3.3546512290875095, 1.2442189088958135]
r1DecConstant = (r1final/r1init)**(1/maxIter)
c2DecConstant = (c2final/c2init)**(1/maxIter)
powerDecConstant = (powerFinal/powerInitial)**(1/maxIter)
for num_points in range(lowerRange,upperRange+1):
    best[num_points] = -np.inf
for num_points in range(lowerRange,upperRange+1):
    print(num_points)
    points = generate_points(num_points, math.ceil(num_points/10), scaleFactor, False)
    r1 = r1init ## random walk param, offset each coordinate with U[-r1, r1]
    c2 = c2init ## step size (force parameter)
    power = powerInitial
    
    for iteration in range(maxIter):
        # if iteration % (maxIter//frames) == 0:   # Adds the position of the points at certain times
        #     sequence.append(points.copy())
        forces = calculate_repulsive_force(points, power)
        walk = calculate_random_walk(num_points, r1)
        points = update_points(points, forces, walk, scaleFactor, c2)
    
        min_distance_ = calculate_minimum_distance(points)
        if (min_distance_ > best[num_points]):
            best[num_points] = min_distance_
        r1 *= r1DecConstant
        c2 *= c2DecConstant
        power *= powerDecConstant
    best[num_points] /= scaleFactor
    print(best[num_points])
    #def plot_sphere(ax):
    #    u, v = np.mgrid[0:2*np.pi:50j, 0:np.pi:50j]
    #    x = 3*np.cos(u)*np.sin(v)
    #    y = 3*np.sin(u)*np.sin(v)
    #    z = 3*np.cos(v)
    #    # alpha controls opacity
    #    ax.plot_surface(x, y, z, color="b", alpha=0.3)
    
    ## Setting aspect ratio to be equal to ensure the sphere looks spherical
    ##ax.set_box_aspect([np.ptp(axis) for axis in [ax.get_xlim(), ax.get_ylim(), ax.get_zlim()]])
    ##ax.set_title('Points on the Sphere')
    ##ax.set_xlabel('X')
    ##ax.set_ylabel('Y')
    ##ax.set_zlabel('Z')
    
    ##plt.show()
    
    #def update(frame): # A function to update the frame in the animation
    #    ax.cla()       # Clears previous plot
    #    ax.set_box_aspect([np.ptp(axis) for axis in [ax.get_xlim(), ax.get_ylim(), ax.get_zlim()]])
    #    ax.set_xlabel('X')
    #    ax.set_ylabel('Y')
    #    ax.set_zlabel('Z')
    #    ax.set_title(f'Points on the Sphere. Frame {frame}')
    
    #    # Plot the points for the current frame
    #    pts = sequence[frame]
    #    ax.scatter(pts[:, 0], pts[:, 1], pts[:, 2], s=30, c='red', marker='o')
    #    plot_sphere(ax)
    
    ## Set up the 3D plot
    #fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')
    
    ## Create the animation
    #animation = FuncAnimation(fig, update, frames=frames, interval=100)
    
    ## Display the animation
    #plt.show()

f = open("final2_simAnnealing.txt", "a")
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
