import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import pylab
from matplotlib.widgets import Button

fig = plt.figure()
# creating a subplot
ax = plt.axes(projection="3d")

xs = []
ys = []
zs = []

def onButtonAddClicked(event):
    print("test")
    xs.append(250)
    ys.append(250)
    zs.append(250)
    print(xs)



def animate(i):
    if True:
        global xs
        global ys
        global zs

        ax.clear()
        ax.plot3D(xs, ys, zs, marker="o")
        scale= 500
        ax.plot3D([0, scale, scale, 0, 0], [0, 0, scale, scale, 0], [0, 0, 0, 0, 0], linewidth=0)
        ax.plot3D([0, scale, scale, 0, 0], [0, 0, scale, scale, 0], [scale, scale, scale, scale, scale], linewidth=0)


axes_button_add = pylab.axes([0.7, 0.05, 0.25, 0.075])

button_add = Button(axes_button_add, 'Добавить')
button_add.on_clicked(onButtonAddClicked)

ani = animation.FuncAnimation(fig, animate, interval=100)
plt.show()