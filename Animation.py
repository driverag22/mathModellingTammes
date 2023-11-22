import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# The next import is specific for animation
from matplotlib.animation import FuncAnimation


def initialize_points(num_points):
    points = np.random.rand(num_points, 3)-0.5 # I added the -0.5 as then each point can come from any octant of the sphere
                                               # Previously they could only spawn in the first octant lol
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

def calculate_maximum_angle(points): # Calculate maximum angle, in radians.
    min_dot = np.inf

    for i in range(len(points)):                # This for loop computes the minimal dot product naively
        for j in range(i + 1, len(points)):     # A minimal dot product corresponds to a maximum angle
            dot = np.dot(points[i],points[j])   # by dot(a,b) = |a||b|cos(alpha), and |a| = |b| = 1
            if (dot < min_dot): min_dot = dot
    
    return np.arccos(min_dot)                   # arccos, in radians.

# Example usage:
num_points = 6
iterations = 100
frames = 50

points = initialize_points(num_points)
sequence = []

best = np.inf
bPoints = np.random.rand(num_points, 3)

for iteration in range(iterations):
    if iteration % (iterations//frames) == 0:   # Adds the position of the points at certain times
        sequence.append(points.copy())
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
        #print(p)

def plot_sphere(ax):
    phi, theta = np.mgrid[0.0:np.pi:1000j, 0.0:2.0*np.pi:1000j]
    x_sphere = np.sin(phi) * np.cos(theta)
    y_sphere = np.sin(phi) * np.sin(theta)
    z_sphere = np.cos(phi)

    ax.plot_surface(x_sphere, y_sphere, z_sphere, alpha=0.2, color='blue', rstride=100, cstride=100)

# Setting aspect ratio to be equal to ensure the sphere looks spherical
#ax.set_box_aspect([np.ptp(axis) for axis in [ax.get_xlim(), ax.get_ylim(), ax.get_zlim()]])
#ax.set_title('Points on the Sphere')
#ax.set_xlabel('X')
#ax.set_ylabel('Y')
#ax.set_zlabel('Z')

#plt.show()

def update(frame): # A function to update the frame in the animation
    ax.cla()       # Clears previous plot
    ax.set_box_aspect([np.ptp(axis) for axis in [ax.get_xlim(), ax.get_ylim(), ax.get_zlim()]])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'Points on the Sphere. Frame {frame}')

    # Plot the points for the current frame
    pts = sequence[frame]
    ax.scatter(pts[:, 0], pts[:, 1], pts[:, 2], s=30, c='blue', marker='o')
    plot_sphere(ax)

# Set up the 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Create the animation
animation = FuncAnimation(fig, update, frames=frames, interval=100)

# Display the animation
plt.show()