import numpy as np
import math
import pandas as pd
import random
from io import StringIO
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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
        
def update_points_rw(points, forces, rand_walk, step_size=0.1, scale=1):
    points += (rand_walk + step_size * forces)
    points /= np.linalg.norm(points, axis=1)[:, None]
    points *= scale
    return points

def calculate_minimum_distance(points):
    min_distance = np.inf

    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            distance = np.linalg.norm(points[i] - points[j])
            min_distance = min(distance, min_distance)

    return min_distance
def lit_sol(n):
    #add your own file derictory 
    with open('Best_Results/z.txt'.replace("z", str(n)), 'r') as file:
        data = pd.read_csv(StringIO(file.read()), delim_whitespace=True, header=None, names=['Point', 'x', 'y','z'])
    
    df = pd.DataFrame(data)
   
    return df

def initial(n,m='uniform',w=1,random=False):
    if m =='uniform':
        points = initialize_points(n)
    if m=='spiral':
        points = generate_points(n,w,random)
    return points

def simulation(to_n_points,runs,params):
               # params[0],params[1],params[2],params[3],params[4],params[5],params[6]):
    
    r1DecConstant = (params[1]/params[0])**(1/runs)
    c2DecConstant = (params[3]/params[2])**(1/runs)
    powerDecConstant = (params[5]/powerf)**(1/runs)
    
    best = {}
    
    for num_points in range(7,to_n_points+1):
        
        best[num_points] = -np.infty
    
    for num_points in range(7,to_n_points+1):
        
        points = initial(num_points,'spiral')
        
        r1 = params[0]
        
        c2 = params[2]
        
        power = params[4]
        
        for iteration in range(runs):
            
            forces = calculate_repulsive_force(points, power)
            
            walk = calculate_random_walk(num_points, r1)
            
            points = update_points_rw(points, forces, walk, c2, params[6])
            
            min_distance = calculate_minimum_distance(points)
            
            if (min_distance > best[num_points]):
                
                best[num_points] = min_distance
                
            r1 *= r1DecConstant
            c2 *= c2DecConstant
            power *= powerDecConstant
            
    for num_points in range(7,to_n_points+1):
        best[num_points] /= params[6]
    
    return pd.DataFrame.from_dict(best, orient='index')

def cost(pd_best):
    
    score = 0
    
    for i in range(0,len(pd_best)):
        
        score = score+(lit_sol(i+7).iloc[0,1]-pd_best.iloc[i,0])/lit_sol(i+7).iloc[0,1]
    
    return score

## THIS IS THE ACTUAL OPTIMIZATION PART

score = np.infty
for i in range(1,100):
    #random_walk_interval = (0,5]
    
    points_dist = pd.DataFrame()

    r1f = random.random()*10**(-2)
    
    r1s = 1.75+random.random()
    
    c2s=random.random()*10**(-1)
    
    c2f = 0.5+random.random()
    
    powers = 1+random.random()
    
    powerf = 3+6*random.random()
    
    scale = 1+6*random.random()

    params = [r1s,r1f,c2s,c2f,powers,powerf,scale]
    df1 = simulation(15,200,params)
        
    score_1 =cost(df1)
    
    if (score_1 < score):
        
        points_dist = df1
        
        score = score_1     
                  
        parameter = [r1s,r1f,c2s,c2f,powers,powerf,scale]

print(parameter)

test1 = [cost(simulation(20, 20, parameter)) for i in range(1,20)]

params2=[2.3200243756120966, 0.002262275383698383, 0.034820734711107415, 0.8342310303085669, 1.615408136622423, 6.879385239377747, 1.4282888849214053]

test2 = [cost(simulation(20,20, params2)) for i in range(1,20)]

X=[i for i in range(7,7+len(test2))]
plt.scatter(X, test1,color='red')
plt.scatter(X, test2,color='blue')
plt.show()
