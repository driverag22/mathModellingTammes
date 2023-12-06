import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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
                force = delta / (distance ** 2)
                forces[i] += force

    return forces

def update_points(points, forces, step_size=0.1):
    points += step_size * forces
    points /= np.linalg.norm(points, axis=1)[:, None]
    return points

def calculate_minimum_distance(points):
    min_distance = np.inf

    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            distance = np.linalg.norm(points[i] - points[j])
            min_distance = min(distance, min_distance)
            # if (distance < min_distance): min_distance = distance

    return min_distance

best = {}
lowerRange = 2
upperRange = 100
maxIter = 2000
for num_points in range(lowerRange,upperRange+1):
    best[num_points] = -np.inf
for num_points in range(lowerRange,upperRange+1):
    print(num_points)
    points = initialize_points(num_points)
    
    for iteration in range(maxIter):
        forces = calculate_repulsive_force(points)
        points = update_points(points, forces)
    
        min_distance_ = calculate_minimum_distance(points)
        if (min_distance_ > best[num_points]):
            best[num_points] = min_distance_

f = open("results/output_basicSol.txt", "a")
for num_points in range(lowerRange, upperRange+1):
    f.write(str(num_points))
    f.write("\n")
    f.write(str(best[num_points]))
    f.write("\n")
    f.write("\n")
f.close()

# def plot_sphere(ax):
#     u, v = np.mgrid[0:2*np.pi:50j, 0:np.pi:50j]
#     x = np.cos(u)*np.sin(v)
#     y = np.sin(u)*np.sin(v)
#     z = np.cos(v)
#     # alpha controls opacity
#     ax.plot_surface(x, y, z, color="b", alpha=0.3)

# fig = plt.figure(figsize=(8, 8))
# ax = fig.add_subplot(111, projection='3d')

# # Plotting the sphere
# plot_sphere(ax)

# # Plotting the points on the sphere
# ax.scatter3D(bPoints[:, 0], bPoints[:, 1], bPoints[:, 2], c='red', marker='o')

# # Setting aspect ratio to be equal to ensure the sphere looks spherical
# ax.set_box_aspect([np.ptp(axis) for axis in [ax.get_xlim(), ax.get_ylim(), ax.get_zlim()]])
# ax.set_title('Points on the Sphere')
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')

# plt.show()
