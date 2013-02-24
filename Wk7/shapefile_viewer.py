from osgeo import ogr
import argparse
from Tkinter import *

parser = argparse.ArgumentParser(description='Shapefile visualizer')
parser.add_argument('input_data', action='store', help='The input shapefile to visualize.')
args = parser.parse_args()

#Open the input DS
ds = ogr.Open(args.input_data)
#These are single layer only, so we know we can get index 0
layer = ds.GetLayer(0)

#Get the extent of the layer and ratio
xmin, xmax, ymin, ymax = layer.GetExtent()
#print xmin, xmax, ymin, ymax


umax = 800
vmax = 600
ratioX = (umax - 0)/(xmax-xmin)
ratioY = (vmax - 0)/(ymax-ymin)
ratio = min(ratioX, ratioY)

#Iterate over the fetures
feature = layer.GetNextFeature()
#Get the geometry type - this way we can view any type of shapefile
geom_type = feature.GetGeometryRef().GetGeometryType()

if geom_type == 1: #This is a point
        points = []
        while feature:
                #Get the feature geometry object
                geom = feature.GetGeometryRef()
                #Make the transformation
                x = (ratio * (geom.GetX() - xmin)) * .95 + 10
                y = (vmax + ((-1 * ratio) * (geom.GetY() - ymin))) * .95 + 10
                #Append to the list
                points.append((x,y))
                #Increment to the next feature
                feature = layer.GetNextFeature() #Required to avoid an infinite loop
                
if geom_type == 2: #This is a polyline
        polyline = []
        while feature:
                geom = feature.GetGeometryRef()
                vertices = geom.GetPointCount()
                line_feature = []
                for vertex in range(vertices):
                        x,y,z = geom.GetPoint(vertex)
                        x = ((ratio * (x - xmin))) * .95 + 10
                        y = (vmax + ((-1 * ratio) * (y - ymin))) * 0.95 + 10
                        line_feature.append(x)
                        line_feature.append(y)
                polyline.append(line_feature)
                feature = layer.GetNextFeature()
                
if geom_type == 3: #This is a polygon
        polygon = []
        while feature:
                geom = feature.GetGeometryRef()
                ring = geom.GetGeometryRef(0) #We assume that these are not complex polygons
                out_ring = []
                vertices = ring.GetPointCount()
                for vertex in range(vertices):
                        x, y, z = ring.GetPoint(vertex)
                        x = ((ratio * (x - xmin))) * .95 + 10
                        y = (vmax + ((-1 * ratio) * (y - ymin))) * 0.95 + 10
                        out_ring.append(x)
                        out_ring.append(y)
                polygon.append(out_ring)
                feature = layer.GetNextFeature()

#TK window    
root = Tk()
can = Canvas(root, width=umax, height=vmax)

#Parse the geom_type to determine what geometry to draw
if geom_type == 1:
        for point in points:
                can.create_oval(point[0], point[1], point[0] + 5,point[1] + 5 , fill='black')
if geom_type == 2:
        for line in polyline:
                can.create_line(line, fill='blue')
if geom_type == 3:
        for poly in polygon:
                can.create_polygon(poly, fill='green', outline='black')

#Pack the canvas
can.pack()

#Initiate the loop to keep the window drawn
root.mainloop()