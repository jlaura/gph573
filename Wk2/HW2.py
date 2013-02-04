
import random
import sys
from math import sqrt

class Point:
    '''
    A point factory class that generates random points in either GCS or PCS.
    
    Parameters
    ----------
    number_points        :int
                          An integer number of points
                          
    crs                  :string
                          Either gcs (geographic coordinates) or
                                 pcs (pixel space coordinates)
                                 
    Returns
    -------
    
    coordinates          :list
                          A list of tuples storing the coordinates.
    
    '''
    def __init__(self, number_points, crs='pcs'):
        if type(number_points) != int:
            print "This class requires an integer number of points."
            sys.exit(0)
        self.number_points = number_points
        self.coordinates = []
        if crs == 'gcs':
            self.generateGCS()
        elif crs == 'pcs':
            self.generatePCS()

    def generateGCS(self):
        '''
        This function generates a random floating point coordinate pair
        in geographic coordinates.
        '''
        for coord in range(self.number_points):
            x = random.uniform(-90,90)
            y = random.uniform(-180, 180)
            self.coordinates.append((x,y))
            
        print "All we can do is generate in GCS, so here are your points.\n"
        print self.coordinates
        sys.exit(0)
    
    def generatePCS(self):
        '''
        This function generates a random floating point coordiante pair
        in pixel coordinates.  Pixel space origin is 0,0 and total size constrained
        to 1000 x 1000.
        '''
        for coord in range(self.number_points):
            x = random.randint(0,1000)
            y = random.randint(0,1000)
            self.coordinates.append((x,y))

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

def pair_generator(items, n):
    '''
    A generator that yields all unique combinations of n elements from list
    items.
    
    Parameters:
    -----------
    items                 :list
                           A list of items from which all permutations are
                           returned.
                           
    n                     :int
                           The number of items to include in each permutation.
    '''
    if n == 0: yield []
    else:
        for i in xrange(len(items)):
            for group in pair_generator(items[:i]+items[i+1:], n-1):
                yield[items[i]]+group

def main(number_points):   
    '''
    The main function that controls program flow.
    '''
    random_points = Point(number_points)
    random_coords = random_points.coordinates
    
    distance_dict = {}
    for x in pair_generator(random_coords,2):
        distance = euclidean_distance(x[0], x[1])
        distance_dict[str(x)] = distance
    
    minimum_distance = float('inf')
    for key, value in distance_dict.iteritems():
        #Brute force, we only have 12 combinations
        if value < minimum_distance:
            minimum_distance = value
            closest_coords = key
    
    #Write the output to a text file
    output = open(output_file, mode='a')
    output.write('New Iteration\n')
    output.write('=============\n')
    output.write('    Coordinates\n')
    output.write('    -----------\n')    
    for coord in random_coords:
        output.write('    '+ str(coord)+'\n')
    output.write('\n    Distances\n')
    output.write('    ---------\n')    
    output_string = ('    The two points closest are %s.\n    They are separated by %f units.\n\n') %(closest_coords,minimum_distance)
    output.write(output_string)


if __name__ == '__main__':
    number_points = int(sys.argv[1])
    output_file = sys.argv[2]
    main(number_points)