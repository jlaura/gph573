import sys
import re
from Tkinter import *
from random import choice
import numpy as np

inputds = sys.argv[1]

#Read the geometries using regex to extract the floating point coordinates
f = open(sys.argv[1])
geometries = []
for line in f:
    fl = re.findall(r"[-+]?\d*\.\d+|\d+",line)
    fl =  fl[1:]
    float_pts = [float(x) for x in fl]
    float_arr = np.asarray(float_pts)
    if float_pts:
        geometries.append(float_arr)

#Geotransform
xmax = None
ymax = None
for geometry in geometries:
    if geometry[0::2].max() > xmax:
        xmax = geometry[0::2].max()
    if geometry[1::2].max() > ymax:
        ymax = geometry[0::2].max()


umax = 800
vmax = 600
ratioX = umax / xmax
ratioY = vmax / ymax
ratio = min(ratioX, ratioY)

    
for line in geometries:
    #line[::2] *= ratio
    #line[1::2] *= -ratio
    line *= ratio
    
#TK window    
root = Tk()
can = Canvas(root, width=vmax, height=umax)


colors = ['red','green','blue','yellow','orange','purple']
for line in geometries:
    line = line.tolist()
    print line
    color = choice(colors)
    can.create_line(line, fill=color)
can.create_line(500,50,498,50,fill='red')

can.pack()

#root.mainloop()   

