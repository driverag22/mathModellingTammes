import numpy as np
import math
import pandas as pd
import random
from io import StringIO

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

def simulation(to_n_points,runs,r1s,r1f,c2s,c2f,powers,powerf,scale):
    
    r1DecConstant = (r1f/r1s)**(1/runs)
    c2DecConstant = (c2f/c2s)**(1/runs)
    powerDecConstant = (powerf/powerf)**(1/runs)
    
    best = {}
    
    for num_points in range(7,to_n_points+1):
        
        best[num_points] = -np.infty
    
    for num_points in range(7,to_n_points+1):
        
        points = initial(num_points,'spiral')
        
        r1 = r1s
        
        c2 = c2s
        
        power = powers
        
        for iteration in range(runs):
            
            forces = calculate_repulsive_force(points, power)
            
            walk = calculate_random_walk(num_points, r1)
            
            points = update_points_rw(points, forces, walk, c2,scale)
            
            min_distance = calculate_minimum_distance(points)
            
            if (min_distance > best[num_points]):
                
                best[num_points] = min_distance
                
            r1 *= r1DecConstant
            c2 *= c2DecConstant
            power *= powerDecConstant
            
    for num_points in range(7,to_n_points+1):
        best[num_points] /= scale
    
    return pd.DataFrame.from_dict(best, orient='index')

def cost(pd_best):
    
    score = 0
    
    for i in range(0,len(pd_best)):
        
        score = score+(lit_sol(i+7).iloc[0,1]-pd_best.iloc[i,0])/lit_sol(i+7).iloc[0,1]
    
    return score

## THIS IS THE ACTUAL OPTIMIZATION PART

score = np.infty
for i in range(1,2):
    #random_walk_interval = (0,5]
    
    points_dist = pd.DataFrame()

    r1f = random.random()*10**(-2)
    
    r1s = 1.75+random.random()
    
    c2s=random.random()*10**(-1)
    
    c2f = 0.5+random.random()
    
    powers = 1+random.random()
    
    powerf = 3+6*random.random()
    
    # scale = 1+6*random.random()
    scale = 3
    
    df1 = simulation(7,200,r1s,r1f,c2s,c2f,powers,powerf,scale)
        
    score_1 =cost(df1)
    
    if (score_1 < score):
        
        points_dist = df1
        
        score = score_1     
                  
        parameter = [r1s,r1f,c2s,c2f,powers,powerf,scale]

print(parameter)

test1 = [cost(simulation(20,200,
0.002030114685897073,
 0.028771262355712736,
 1.063302818182938,
 1.1052332081563456,
 1.4613255534190475,
 2.237871910720762,
 6.231147973546684)) for i in range(1,20)]

test2 = [cost(simulation(20,200, 2.115832008737706,
 0.006021444096223975,
 0.014393304034470934,
 1.4238744127061507,
 1.4491259350544592,
 5.436509842397031,
 1.4431696752229017)) for i in range(1,20)];

X=[i for i in range(7,7+len(test2))]
plt.scatter(X,test1,color='red')
plt.scatter(X,test2,color='blue')
plt.show()
