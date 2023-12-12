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

# genSolDf = genDataFrame('./results/output_genSol.txt')
simAnnealingDf = genDataFrame("../results/ouput_simAnnealing.txt")
basicSolDf = genDataFrame("../results/output_basicSol.txt")
length = len(basicSolDf['Index'])
diff = pd.DataFrame({'Index': [i for i in range(2,length)], 'Value': [0 for i in range(2,length)]})
diff['Value'] = simAnnealingDf['Value'] - basicSolDf['Value']

# Plot the values against indices
# plt.plot(simAnnealingDf['Index'], simAnnealingDf['Value'], marker='o', linestyle='', color='b')
# plt.plot(genSolDf['Index'], genSolDf['Value'], marker='o', linestyle='', color='r')
# plt.plot(basicSolDf['Index'], basicSolDf['Value'], marker='o', linestyle='', color='g')
plt.plot(diff['Index'], diff['Value'], marker='o', linestyle='', color='r')
plt.axhline(y = 0, color = 'b', linestyle = '--')
plt.xlabel('Number of points')
plt.ylabel('Value')
plt.title('Values vs. Number of points')
plt.grid(True)
m = diff['Value'].max() * 1.2
plt.ylim(-m,m)
plt.show()
