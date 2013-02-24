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
xmin = float('inf')
ymin = float('inf')

for geometry in geometries:
    if geometry[0::2].max() > xmax:
        xmax = geometry[0::2].max()
    if geometry[0::2].min() < xmin:
        xmin = geometry[0::2].min()
    if geometry[1::2].max() > ymax:
        ymax = geometry[1::2].max()
    if geometry[1::2].min() < ymin:
        ymin = geometry[1::2].min()
#print xmax,xmin,ymax,ymin

umax = 800
vmax = 600
ratioX = (umax - 0)/(xmax-xmin)
ratioY = (vmax - 0)/(ymax-ymin)
ratio = min(ratioX, ratioY)
#print ratio
    
for line in geometries:
    line[0::2] = ratio * (line[0::2] - xmin)
    line[1::2] = vmax + ((-1 * ratio) * (line[1::2] - ymin))

#TK window    
root = Tk()
can = Canvas(root, width=umax, height=vmax)


colors = ['red','green','blue','yellow','orange','purple']
for line in geometries:
    line = line.tolist()
    color = choice(colors)
    can.create_line(line, fill=color)

can.pack()

root.mainloop()   

