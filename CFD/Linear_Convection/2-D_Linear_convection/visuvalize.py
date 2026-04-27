
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0,2,21)
y = np.linspace(0,2,21)


with open('resu.txt','r') as file:
   data = file.readlines()
    
matrix = []
for line in data:
     row = list(map(float, line.split()))
     matrix.append(row)
    
matrix = np.array(matrix)

ax = plt.axes(projection = '3d')
X,Y = np.meshgrid(x , y)
surf = ax.plot_surface(X,Y,matrix, cmap = 'plasma')
plt.show()



