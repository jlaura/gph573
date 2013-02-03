from random import randint
from numpy import *
from string import Formatter

class Rectangle():
    def __init__(self, ul=(100,100), lr=(150,50)):
        self.ul = ul
        self.lr = lr
        self.ll = None
        self.ur = None
    def makeRectangle(self,):
        self.ll = (self.ul[0],self.lr[1])
        self.ur = (self.lr[0],self.ul[1])
        return [self.ul, self.ll, self.lr, self.ur]

class Point:
    '''
    A Cartesian coordinate constructor.
    '''
    def __init__(self,x=None,y=None):
        self.coord=()
        if x==None and y==None:
            self.generatePCS()
        else:
            self.coord=(x,y)
    
    def generatePCS(self):
        x = random.randint(0,200)
        y = random.randint(0,200)
        self.coord = (x,y)


def ray_algorithm(x,y,rectangle):
    '''This is naive because we know that we are working in discrete cartesian coordinates.
    If the point intersects a side of the rectangle an even number of times it is outside of the polygon, else it is within the polygon.

    From: http://geospatialpython.com/2011/01/point-in-polygon.html
    
    Using the determinant method it is not possible to constrain the lines to line segments.
    '''
    n = len(rectangle)
    inside = False
    
    p1x,p1y = rectangle[0]
    for i in range(n+1):
        p2x, p2y = rectangle[i%n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y) + p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y
        
    return inside

outputds = open('sample_output.txt', 'w')

points = []
for x in range(10):
    point = Point()
    point.generatePCS()
    points.append((point.coord[0],point.coord[1]))

pointcounter = 1
outputds.write("The list of points are: \n")
for point in points:
    line = "p{}: {} \n".format(pointcounter, point) #This is the 'new' way to do string formatting.  %i notation is lilely going to be depreciated.  This is also much cleaner as python handles all the casting in the backend.  We can add additional formatting within the curly braces to, for example, truncate a float to n signifigant digits.
    outputds.write(line)
    pointcounter += 1

rectangles = []
for rectangle in range(4):
    r = Rectangle((randint(0,200),randint(0,200)),(randint(0,200),randint(0,200)))
    rectangles.append(r.makeRectangle())

rectanglecounter = 1
outputds.write("\nThe list of rectangles are:\n")
for rectangle in rectangles:
    line = "r{}: {} \n".format(rectanglecounter, rectangle)
    outputds.write(line)
    rectanglecounter += 1
  
outputds.write("\nThe spatial relationship between the points and the rectangles are\n")
pointcounter = 1
for point in points:
    within_list = []
    rectanglecounter = 1 #Initialize a key counter
    for rectangle in rectangles:
        within = ray_algorithm(point[0],point[1],rectangle)
        if within:
            within_list.append("r"+str(rectanglecounter))
        rectanglecounter += 1 #Increment the key counter
    if len(within_list) > 0:
        line = "p{} is within {} \n".format(pointcounter, within_list)
        outputds.write(line)   
    pointcounter += 1
