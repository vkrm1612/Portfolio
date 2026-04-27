import matplotlib.pyplot as plt


x_values = []
u_values = []


file = open('non_linear.txt' , 'r')


for line in file:
	u , x = line.split()
	u = float(u)
	x = float(x)
	u_values.append(u)
	x_values.append(x)


plt.plot(x_values,u_values)
plt.show()
