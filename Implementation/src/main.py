# Import the required libraries
from tkinter import *
from tkinter import ttk, messagebox, simpledialog
from tkinter import font
import numpy as np
from delaunayRandomIncremental import DelaunayRI
from delaunayDivideAndConquer import delaunayDC
import matplotlib.pyplot as plt
import matplotlib.tri
import matplotlib.collections
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



def removePoint():
    for item in pointList.curselection():
        pointList.delete(item)
        global points
        points = np.delete(points, item, 0)

def divConquer():
    global radius
    global stepByStep
    if stepByStep == False:
        # Create triangulation
        edges = delaunayDC(points)
        fig, ax = plt.subplots()
        ax.margins(0.1)
        ax.set_aspect('equal')
        plt.axis([-1, radius + 1, -1, radius + 1])
        for e in edges:
            ax.plot([e.org[0], e.dest[0]], [e.org[1], e.dest[1]], 'bo--')
        plt.title("Delaunay Triangulation with Divide And Conquer Algorithm")
        plt.show()
    else:
        global timePerStep
        fig, ax = plt.subplots()
        ax.margins(0.1)
        ax.set_aspect('equal')
        plt.axis([-1, radius + 1, -1, radius + 1])
        plt.title("Delaunay Triangulation with Divide And Conquer Algorithm")
        edges = delaunayDC(points)
        for e in edges:
            ax.plot([e.org[0], e.dest[0]], [e.org[1], e.dest[1]], 'bo--')
            plt.pause(timePerStep)

def randomIncremental():
    global radius
    global stepByStep
    if stepByStep == False:
        # Create triangulation
        dt = DelaunayRI()
        for p in points:
            # print(p)
            dt.addPoint(p)


        # Plot triangulation
        fig, ax = plt.subplots()
        ax.margins(0.1)
        ax.set_aspect('equal')
        plt.axis([-1, radius + 1, -1, radius + 1])

        cx, cy = zip(*points)
        dt_tris = dt.exportTriangles()
        ax.triplot(matplotlib.tri.Triangulation(cx, cy, dt_tris), 'bo--')
        plt.title("Delaunay Triangulation with Randomized Incremental Algorithm")
        plt.show()
    else:
        global timePerStep
        dt = DelaunayRI()
        pc = 0
        fig, ax = plt.subplots()
        ax.margins(0.1)
        ax.set_aspect('equal')
        plt.axis([-1, radius + 1, -1, radius + 1])
        plt.title("Delaunay Triangulation with Randomized Incremental Algorithm")
        for p in points:
            # print(p)
            dt.addPoint(p)
            pc = pc + 1
            if pc > 2:
                cx, cy = zip(*points)
                dt_tris = dt.exportTriangles()
                ax.triplot(matplotlib.tri.Triangulation(cx, cy, dt_tris), 'bo--')
                plt.pause(timePerStep)
                plt.cla()


root = Tk()
root.title("Delaunay Triangulator")
root.configure(bg="navyblue")
style = ttk.Style(root)
style.theme_use('clam')

root.geometry("1010x380")
root.minsize(1010, 380)
root.maxsize(1010, 380)


stepByStep = IntVar(root)


f = font.nametofont("TkHeadingFont")
ttk.Label(root, text="LIST OF POINTS", font="f").grid(column=0, row=0, columnspan=2)
pointList = Listbox(root, bg="yellow")
pointList.grid(column=0, row=1, rowspan=10, columnspan=2, padx=5, pady=5, sticky=N + S + E + W)

ttk.Label(root, text="Add custom point", font="f").grid(column=2, row=1, sticky=W)
ttk.Label(root, text="X coordinate: ").grid(column=2, row=2, sticky=W, padx=0, pady=2)
xEntry = ttk.Entry(root)
xEntry.grid(column=3, row=2, sticky=W, padx=0, pady=5)
ttk.Label(root, text="Y coordinate: ").grid(column=2, row=3, sticky=W, padx=0, pady=2)
yEntry = ttk.Entry(root)
yEntry.grid(column=3, row=3, sticky=W, padx=0, pady=5)
ttk.Label(root, text="Select a point from the list and remove it", font="f").grid(column=2, row=5, sticky=W)


def addPoint():
    global points
    x = xEntry.get()
    y = yEntry.get()
    pointList.insert(pointList.size(), "x: " + str(x) + " y: " + str(y))

    points = np.append(points, np.array([[float(x), float(y)]]), axis=0)


def generatePoints():
    global points
    num = numOfPointsEntry.get()
    rad = radiusEntry.get()

    global radius
    global numOfPoints

    radius = int(rad)
    numOfPoints = int(num)
    points = radius * np.random.random((numOfPoints, 2))
    pointList.delete(0, END)

    for p in points:
        pointList.insert(pointList.size(), ("x: " + str(p[0]) + " y: " + str(p[1])))


def changeStepByStep(answer):
    global stepByStep
    if answer:
        answer_time = simpledialog.askfloat("Question", "What is the time between each frame (s)?", minvalue=0.000000000000000000001, maxvalue=100.0)
        global timePerStep
        timePerStep = answer_time
        stepByStep = True
    else:
        stepByStep = False


ttk.Button(root, text="Add Point", command=addPoint).grid(column=2, row=4, sticky=W, padx=5, pady=3)
ttk.Button(root, text="Remove Selected Point", command=removePoint).grid(column=2, row=6, sticky=W, padx=2, pady=3)



def divConquer_0():
    answer = messagebox.askyesno("Question", "Do you want to go step by step?")
    changeStepByStep(answer)
    divConquer()


def randomIncremental_0():
    answer = messagebox.askyesno("Question", "Do you want to go step by step?")
    changeStepByStep(answer)
    randomIncremental()

ttk.Button(root, text="Triangulate Using Divide&Conquer", command=divConquer_0).grid(column=0, row=11, sticky=W, padx=5, pady=3)
ttk.Button(root, text="Triangulate Using Randomized Incremental", command=randomIncremental_0).grid(column=1, row=11, sticky=W, padx=5,
                                                                                     pady=3)
ttk.Button(root, text="Generate Random Points", command=generatePoints).grid(column=2, row=10, sticky=W, padx=5, pady=3)

ttk.Label(root, text="Enter the attributes of the random numbers to be generated", font="f").grid(column=2, row=7)
ttk.Label(root, text="Number of points: ").grid(column=2, row=8, sticky=W, padx=0, pady=2)
numOfPointsEntry = ttk.Entry(root)
numOfPointsEntry.grid(column=3, row=8, sticky=W, padx=0, pady=5)
ttk.Label(root, text="Point radius: ").grid(column=2, row=9, sticky=W, padx=0, pady=2)
radiusEntry = ttk.Entry(root)
radiusEntry.grid(column=3, row=9, sticky=W, padx=0, pady=5)

root.mainloop()