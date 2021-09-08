import tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
import matplotlib.animation as animation
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import numpy as np

keys = {"w": False, "a": False, "s": False, "d": False, "q": False, "e": False}


root = tkinter.Tk()
root.wm_title("Remote control")

fig = plt.figure(figsize=(4, 5), dpi=100)
ax = plt.axes(projection="3d")

xs = []
ys = []
zs = []

def AddPoint():
    xs.append(250)
    ys.append(250)
    zs.append(250)
    print(xs)

def keydown(event):
    step = 5
    try:
        if event.char == "w":
            ys[-1] += step
        if event.char == "s":
            ys[-1] -= step
        if event.char == "a":
            xs[-1] -= step
        if event.char == "d":
            xs[-1] += step
        if event.char == "q":
            zs[-1] -= step
        if event.char == "e":
            zs[-1] += step
    except:
        pass

def animate(i):
    if True:
        global xs
        global ys
        global zs

        ax.clear()
        ax.plot3D(xs, ys, zs, marker="o")
        scale = 500
        ax.plot3D([0, scale, scale, 0, 0], [0, 0, scale, scale, 0], [0, 0, 0, 0, 0], linewidth=0)
        ax.plot3D([0, scale, scale, 0, 0], [0, 0, scale, scale, 0], [scale, scale, scale, scale, scale], linewidth=0)



button = tkinter.Button(master=root, text="Add Point", command=AddPoint)
button.pack(side=tkinter.BOTTOM)

root.bind('<KeyPress>', keydown)

fig.canvas.mpl_disconnect(fig.canvas.manager.key_press_handler_id)
canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
ani = animation.FuncAnimation(fig, animate, interval=100)
canvas.draw()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas)




tkinter.mainloop()
