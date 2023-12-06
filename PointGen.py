import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# WARNING: These are not the best starting positions (obv) so these are outperformed by
# random starting points like half the time
def generate_points(n, w = 1, random=False): #Generates points on a kind of screwed up spiral not really
    # w is number of windings,
    # random determines whether angles are random. Should be off lol
    k = n-2
    points = [[0,0,1],[0,0,-1]] #Two points are deterministic
    anglelist = [w*l*2*np.pi/k for l in range(k)]
    if random:
        np.random.shuffle(anglelist)
    for i in range(k):
        points.append([np.sin(anglelist[i]),np.cos(anglelist[i]),1-2*i/k])
    points = np.array(points)
    points /= np.linalg.norm(points, axis=1)[:, None]
    return points

# Rest of the code is for plotting

def plot_sphere(ax):
    u, v = np.mgrid[0:2*np.pi:50j, 0:np.pi:50j]
    x = np.cos(u)*np.sin(v)
    y = np.sin(u)*np.sin(v)
    z = np.cos(v)
    # alpha controls opacity
    ax.plot_surface(x, y, z, color="b", alpha=0.3)

def initialize_points(num_points):
    points = np.random.rand(num_points, 3)-0.5
    points /= np.linalg.norm(points, axis=1)[:, None]
    return points

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

points = generate_points(16)
#points = initialize_points(16)

# Plotting the sphere
plot_sphere(ax)

# Plotting the points on the sphere
ax.scatter3D(points[:, 0], points[:, 1], points[:, 2], c='red', marker='o')

# Setting aspect ratio to be equal to ensure the sphere looks spherical
ax.set_box_aspect([np.ptp(axis) for axis in [ax.get_xlim(), ax.get_ylim(), ax.get_zlim()]])
ax.set_title('Points on the Sphere')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()
print(type(points[1,1]))