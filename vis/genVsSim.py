import pandas as pd
import matplotlib.pyplot as plt

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

simAnnealingDf = genDataFrame("../results/ouput_simAnnealing.txt")
genSolDf = genDataFrame("../results/output_genSol.txt")
length = len(genSolDf['Index'])
diff = pd.DataFrame({'Index': [i for i in range(2,length)], 'Value': [0 for i in range(2,length)]})
diff['Value'] = simAnnealingDf['Value'] - genSolDf['Value']

plt.plot(diff['Index'], diff['Value'], marker='o', linestyle='', color='r')
plt.axhline(y = 0, color = 'b', linestyle = '--')
plt.xlabel('Number of points')
plt.ylabel('Difference')
plt.title('Difference between simulated annealing and general solution (=sim-gen)')
plt.grid(True)
# m = diff['Value'].max() * 1.2
m = 0.03
plt.ylim(-m,m)
plt.show()
