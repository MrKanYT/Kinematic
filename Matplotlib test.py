import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
# creating a subplot
ax = plt.axes(projection="3d")


def animate(i):
    if True:
        data = open('stock.txt', 'r').read()
        lines = data.split('\n')
        xs = []
        ys = []
        zs = []

        for line in lines:
            x, y, z = line.split(',')  # Delimiter is comma
            xs.append(float(x))
            ys.append(float(y))
            zs.append(float(z))

        ax.clear()
        ax.plot3D(xs, ys, zs, marker="o")
        scale= 500
        ax.plot3D([0, scale, scale, 0, 0], [0, 0, scale, scale, 0], [0, 0, 0, 0, 0], linewidth=1)
        ax.plot3D([0, scale, scale, 0, 0], [0, 0, scale, scale, 0], [scale, scale, scale, scale, scale], linewidth=1)

        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Test')


ani = animation.FuncAnimation(fig, animate, interval=100)
plt.show()