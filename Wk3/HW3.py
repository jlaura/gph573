import random
import sys
from math import sqrt
import multiprocessing as mp

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

class Poly(Point):
    '''
    A polygon and polyline constructor.  Subclasses Point.
    '''
    def __init__(self):
        Point.__init__(self)
    
    def createPolyline(self,farg):
        geometry = []
        if type(farg) == list:
            geometry = farg
        elif type(farg) == int:
            for x in range(farg):
                Point.generatePCS(self)#Essentially, reinitialize the class to fire the random number generator.
                geometry.append(self.coord)
        else:
            print "This function requires either an integer number of vertices or a list of coordinates in the format (x,y)."
        return geometry

    def createPolygon(self,farg):
        geometry = []
        if type(farg) == list:
            geometry = farg
        elif type(farg) == int:
            for x in range(farg):
                Point.generatePCS(self)#Essentially, reinitialize the class to fire the random number generator.
                geometry.append(self.coord)
            if geometry[0] != geometry[-1]:
                geometry.append(geometry[0])
        else:
            print "This function requires either an integer number of vertices or a list of coordinates in the format (x,y)."
        return geometry    

def euclidean_distance(coordA, coordB):
    '''
    Calculate the euclidean distance between two points.
    
    Parameters
    ----------
    
    coordA, coordB       :tuple
                          Two tuples of coordinates to compute the distance 
                          between
                          
    Returns
    -------              
    distance             :float
                          The Euclidean distance between two points.
    '''
    distance = sqrt((coordA[0]-coordB[0])**2+(coordA[1]-coordB[1])**2)
    return distance

def compute_length(geometry):
    '''
    Calculate the sum of the distance between all vertices.
    
    Parameters
    ----------
    
    coordA, coordB       :tuple
                          Two tuples of coordinates to compute the distance 
                          between
                          
    Returns
    -------              
    distance             :float
                          The Euclidean distance between two points.
    '''    
    geometrydistance = 0
    if len(geometry) < 2:
        print "Length can only be computed for polylines and polygons."
    else:
        for index,coord in enumerate(geometry):
            if index < len(geometry)-1:#Ignore the final point, since lists do not wrap.
                geometrydistance += euclidean_distance(coord,geometry[index+1])
            else:
                break
    return geometrydistance

p = Point(1,1).coord
print p

polyline = Poly().createPolyline([(2, 2), (3, 3), (4, 5)])
print compute_length(polyline)

polygon = Poly().createPolygon([(1, 2), (3, 5),  (5, 6), (1, 2)])
print compute_length(polygon)