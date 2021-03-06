import numpy as np
import tkinter as tk
import tkinter.ttk as ttk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#test

startX, startY, startZ = 0, 0, 0
shoulderX, shoulderY, shoulderZ = 10, 20, 30
wristX, wristY, wristZ = 20, 30, 40
handX, handY, handZ = 30, 40, 50

root = None
canvas = None
plot3d = None
point = None
anim = None

cm2inch = lambda x: x * .39

class Create3DPlot:
    def __init__(self):
        self.figure, self.ax_3d = self.create_plot()  # Возвращает объект фигуры, нарисованной matplotlib
        self.create_form(self.figure)  # Отображение рисунка над формой tkinter

    def create_plot(self):
        fig = plt.figure(figsize=(cm2inch(14), cm2inch(12)))
        ax_3d = fig.add_subplot(111, projection="3d")

        return fig, ax_3d

    def create_form(self, figure):
        # Отображение нарисованной графики в окне tkinter
        figure.canvas.mpl_disconnect(figure.canvas.manager.key_press_handler_id)
        canvas = FigureCanvasTkAgg(figure, root)
        canvas.draw()
        canvas.get_tk_widget().place(x=10, y=10)



class CreatePoint:
    def __init__(self):
        self.setPointFlag = False
        self.AxesSphereMovementFlag = False
        self.ShiftFlag = False
        self.CtrlFlag = False

        self.max = 200
        self.min = -200

        self.points = {'x': [], 'y': [], 'z': [], 'rad': [], 'a': [], 'b': [], 'c': []}
        self.params = {'x': 0, 'y': 0, 'z': 0, 'rad': 0, 'a': 0, 'b': 0, 'c': 0}

        self.cornerNum = 0

        root.bind("<KeyPress>", self.place_point)
        root.bind("<KeyRelease>", self.changing_flags)

    def dictionaryUpdate(self, flag, values=(0, 0, 0, 0, 0, 0, 0)):
        if flag:
            self.points['x'].append(values[0])
            self.points['y'].append(values[1])
            self.points['z'].append(values[2])
            self.points['rad'].append(values[3])
            self.points['a'].append(values[4])
            self.points['b'].append(values[5])
            self.points['c'].append(values[6])
        else:
            for key in self.points.keys():
                self.points[key].pop()

    def changing_flags(self, event):
        if event.keysym == 'r':
            self.AxesSphereMovementFlag = not self.AxesSphereMovementFlag

        elif event.keysym == 'Control_L':
            self.CtrlFlag = not self.CtrlFlag

            if not self.CtrlFlag and self.setPointFlag:
                for i in range(self.cornerNum):
                    self.dictionaryUpdate(False)
                self.cornerNum = 0

        elif event.keysym == 'space':
            self.setPointFlag = not self.setPointFlag

            if self.setPointFlag:
                self.dictionaryUpdate(True, values=(self.params['x'], self.params['y'], self.params['z'], 0, 0, 0, 0))

        if not self.AxesSphereMovementFlag or not self.setPointFlag:
            self.CtrlFlag = False
            self.cornerNum = 0

    def getSphericalCoordinates(self, a):
        try:
            posX = self.points['x'][-2 - self.cornerNum]
            posY = self.points['y'][-2 - self.cornerNum]
            posZ = self.points['z'][-2 - self.cornerNum]

        except IndexError:
            posX = 0
            posY = 0
            posZ = 0

        b = self.params['b']
        c = self.params['c']

        x_ = self.params['rad'] * np.sin(np.radians(a))
        y_ = self.params['rad'] * np.cos(np.radians(a)) * np.cos(np.radians(b))

        x = x_ * np.cos(np.radians(c)) - y_ * np.sin(np.radians(c)) + posX
        y = x_ * np.sin(np.radians(c)) + y_ * np.cos(np.radians(c)) + posY

        z = self.params['rad'] * np.cos(np.radians(a)) * np.sin(np.radians(b)) + posZ

        return x, y, z

    def spherical_movement(self, event):

        # клавиши управления
        if event.keysym == 'a':
            self.params['a'] += 5
        elif event.keysym == 'd':
            self.params['a'] -= 5

        elif event.keysym == 'w':
            self.params['rad'] += 5
        elif event.keysym == 's':
            self.params['rad'] -= 5

        elif event.keysym == 'q':
            self.params['b'] += 5
        elif event.keysym == 'e':
            self.params['b'] -= 5

        elif event.keysym == 'z':
            self.params['c'] += 5
        elif event.keysym == 'c':
            self.params['c'] -= 5

        self.params['x'], self.params['y'], self.params['z'] = \
            self.getSphericalCoordinates(self.params['a'])

        self.points['rad'][-1] = self.params['rad']
        self.points['a'][-1] = self.params['a']
        self.points['b'][-1] = self.params['b']
        self.points['c'][-1] = self.params['c']

    def axes_movement(self, event):
        # клавиши управления
        if event.keysym == 'a':
            self.params['x'] += 5
        elif event.keysym == 'd':
            self.params['x'] -= 5
        elif event.keysym == 'w':
            self.params['y'] += 5
        elif event.keysym == 's':
            self.params['y'] -= 5
        elif event.keysym == 'q':
            self.params['z'] += 5
        elif event.keysym == 'e':
            self.params['z'] -= 5

            self.points['rad'][-1] = 0
            self.points['a'][-1] = 0
            self.points['b'][-1] = 0
            self.points['c'][-1] = 0

    def placing_polygon(self, event):
        if self.CtrlFlag:
            if event.keysym == 'equal' or event.keysym == 'plus':
                self.cornerNum += 1
                if self.cornerNum > 10:
                    self.cornerNum = 10
                else:
                    self.dictionaryUpdate(True)

            elif event.keysym == 'minus':

                self.cornerNum -= 1
                if self.cornerNum < 0:
                    self.cornerNum = 0
                else:
                    self.dictionaryUpdate(False)

            for i in range(1, self.cornerNum+1):
                self.points['x'][-i-1], self.points['y'][-i-1], self.points['z'][-i-1] = \
                    self.getSphericalCoordinates(360 / self.cornerNum * i + self.params['a'])


    def place_point(self, event):
        # сделать линию параллельной оси координат
        print(event)
        if event.keysym == 'Shift_L':
            self.ShiftFlag = True
        else:
            self.ShiftFlag = False

        # удаление точек
        if event.keysym == 'Delete':
            print()  # не работет
        # отменить размещение
        elif event.keysym == 'Escape':
            self.dictionaryUpdate(False)

            for key in self.params:
                self.params[key] = self.points[key][-1]

            self.setPointFlag = 0
            return

        if self.setPointFlag:

            # выбор типа управления
            if self.AxesSphereMovementFlag:
                self.spherical_movement(event)
                self.placing_polygon(event)
            else:
                self.axes_movement(event)

            # диапазоны
            if self.params['x'] > self.max:
                self.params['x'] = self.max
            elif self.params['x'] < self.min:
                self.params['x'] = self.min

            elif self.params['y'] > self.max:
                self.params['y'] = self.max
            elif self.params['y'] < self.min:
                self.params['y'] = self.min

            elif self.params['z'] > self.max + 200:
                self.params['z'] = self.max + 200
            elif self.params['z'] < self.min + 200:
                self.params['z'] = self.min + 200

            # присваивание координат точке
            self.points['x'][-1] = self.params['x']
            self.points['y'][-1] = self.params['y']
            self.points['z'][-1] = self.params['z']

def Build(_root):
    global root
    global canvas
    global plot3d
    global point
    global anim
    root = _root
    canvas = tk.Canvas(root)  # Создать холст для отображения графики

    plot3d = Create3DPlot()
    point = CreatePoint()
    anim = animation.FuncAnimation(plot3d.figure, drawObjects, interval=100)

if __name__ == "__main__":
    root = tk.Tk()  # Создать основную форму
    root.title("Manipulator control")

    canvas = tk.Canvas(root)  # Создать холст для отображения графики

    plot3d = Create3DPlot()
    point = CreatePoint()
    #interface = CreateInterface()

    anim = animation.FuncAnimation(plot3d.figure, drawObjects, interval=100)

    root.mainloop()
