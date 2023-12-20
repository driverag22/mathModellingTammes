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
    
    scale = 1+6*random.random()
    
    df1 = simulation(7,200,r1s,r1f,c2s,c2f,powers,powerf,scale)
        
    score_1 =cost(df1)
    
    if (score_1 < score):
        
        points_dist = df1
        
        score = score_1     
                  
        parameter = {r1s,r1f,c2s,c2f,powers,powerf,scale}
                  