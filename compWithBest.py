import numpy as np
import math
import pandas as pd
import random
from io import StringIO
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

def lit_sol(n):
    #add your own file derictory 
    with open('Best_Results/z.txt'.replace("z", str(n)), 'r') as file:
        data = pd.read_csv(StringIO(file.read()), delim_whitespace=True, header=None, names=['Point', 'x', 'y','z'])
    
    df = pd.DataFrame(data)
   
    return df

def genDataFrame(file_path):
    # Open the file and read lines
    with open(file_path, 'r') as file:
        lines = file.readlines()
    # Initialize empty lists to store index and values
    indices = []
    values = []
    # Iterate over the lines to extract index and values
    for i in range(0, len(lines), 3):
        index = int(lines[i].strip())
        value = float(lines[i + 1].strip())
    
        indices.append(index)
        values.append(value)
    return pd.DataFrame({'Index': indices, 'Value': values})

simAnnealingDf = genDataFrame("./final_simAnnealing.txt")

# print(simAnnealingDf['Value'].get(6-2))
# print(lit_sol(6).iloc[0,1])

# Plotting our solutions versus ideal solutions
# for i in range(6, len(simAnnealingDf)):
#     if ((lit_sol(i).iloc[0,1]-simAnnealingDf['Value'].get(i-2))/lit_sol(i).iloc[0,1] < 0):
#         print(i)
#         print(simAnnealingDf['Value'].get(i-2))
A2=[ max(0,((lit_sol(i).iloc[0,1]-simAnnealingDf['Value'].get(i-2))/lit_sol(i).iloc[0,1])) for i in range(6,len(simAnnealingDf))]

plt.scatter([i for i in range(7,7+len(A2))],A2,color='blue')
plt.xlabel("Number of Points")
plt.ylabel("Difference Between Minimum Distance")
plt.title("--")
plt.show()
    
# X = [i for i in range(1,1+len(test1))];
    
# plt.scatter(X,test1,color='blue')    
