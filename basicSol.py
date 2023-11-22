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

best = np.inf
bPoints = np.random.rand(num_points, 3)

for iteration in range(100):
    forces = calculate_repulsive_force(points)
    update_points(points, forces)

    min_distance = calculate_minimum_distance(points)
    print(f"Iteration {iteration + 1}: Minimum Distance = {min_distance}")
    if (min_distance < best):
        bPoints = points
        min_distance = best

    for p in points:
        if (abs(np.linalg.norm(p) - 1) > 0.01):
            print("error")
            break
        # print(p)

def plot_sphere(ax):
    u, v = np.mgrid[0:2*np.pi:50j, 0:np.pi:50j]
    x = np.cos(u)*np.sin(v)
    y = np.sin(u)*np.sin(v)
    z = np.cos(v)
    # alpha controls opacity
    ax.plot_surface(x, y, z, color="b", alpha=0.3)

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

# Plotting the sphere
plot_sphere(ax)

# Plotting the points on the sphere
ax.scatter3D(bPoints[:, 0], bPoints[:, 1], bPoints[:, 2], c='red', marker='o')

# Setting aspect ratio to be equal to ensure the sphere looks spherical
ax.set_box_aspect([np.ptp(axis) for axis in [ax.get_xlim(), ax.get_ylim(), ax.get_zlim()]])
ax.set_title('Points on the Sphere')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()
