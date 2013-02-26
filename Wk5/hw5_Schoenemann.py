###################
# Joe Schoenemann #
# Homework 5      #
# 2/13/2013       #
###################

import re
from Tkinter import *
from datetime import *

t1 = datetime.now()

f = open("Polyline1024.txt")
polyline = [] # Empty list
for line in f: # Loop will format and and change values from string to float
    fl = re.findall(r"[-+]?\d*\.\d+|\d+",line) # Regex
    fl =  fl[1:]
    float_pts = [float(x) for x in fl] # String to float
    if float_pts:
        polyline.append(float_pts)


maxx = None
maxy = None
minx = float
miny = float
for segment in polyline: # Iterates to find the max/min values in the polyline list
    xcoords = [segment[2*i] for i in range (len(segment)/2)] # Sets x to even values in list
    ycoords = [segment[2*i+1] for i in range (len(segment)/2)] # Sets y to odd values in list
    if max(xcoords) > maxx: # Reads through x values to find if they are greater than the current greatest x
        maxx = max(xcoords) # If it finds a new value greater than the current maxx, it replaces maxx with new value
    if max(ycoords) > maxy:
        maxy = max(ycoords)
    if min(xcoords) < minx:
        minx = min(xcoords)
    if min(ycoords) < miny:
        miny = min(ycoords)

maxu = 800 # Max x in screen coordinate system
maxv = 600 # Max y in screen coordinate system
ratioX = (maxu - 0)/(maxx-minx)
ratioY = (maxv - 0)/(maxy-miny)
ratio = min(ratioX, ratioY)

moved_lines = []
for segment in polyline:
    moved_segment = []
    for index,coord in enumerate(segment):
        if index % 2 == 0:
            moved_segment.append(ratio * (coord - minx))
        elif index % 2 == 1:
            moved_segment.append(maxv + ((-1 * ratio) * (coord - miny)))
       
    moved_lines.append(moved_segment)

root = Tk()
can = Canvas(root, width = maxu, height = maxv) 

for line in moved_lines:
    can.create_line(line, fill='blue')

can.pack()

t2 = datetime.now()
print t2 - t1


root.mainloop()

