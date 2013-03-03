from osgeo import ogr
import sys
from random import randint

def rand_num():
    return randint(0,600)

def create_line():
    return ogr.Geometry(type=ogr.wkbLineString)


driver = ogr.GetDriverByName('ESRI Shapefile')
datasource1 = driver.CreateDataSource(sys.argv[1] + '_1.shp')
datasource2 = driver.CreateDataSource(sys.argv[1] + '_2.shp')

layer1 = datasource1.CreateLayer('layername1', geom_type=ogr.wkbLineString)
layer2 = datasource2.CreateLayer('layername2', geom_type=ogr.wkbLineString)

featureDefn1 = layer1.GetLayerDefn()
feature1 = ogr.Feature(featureDefn1)
featureDefn2 = layer2.GetLayerDefn()
feature2 = ogr.Feature(featureDefn2)

for num_lines in range(int(sys.argv[2])):
    line = create_line()
    line.AddPoint_2D(rand_num(), rand_num())
    line.AddPoint_2D(rand_num(), rand_num())
    feature1.SetGeometryDirectly(line)
    layer1.CreateFeature(feature1)
 
for num_lines in range(int(sys.argv[2])):
    line = create_line()
    line.AddPoint_2D(rand_num(), rand_num())
    line.AddPoint_2D(rand_num(), rand_num())
    feature2.SetGeometryDirectly(line)
    layer2.CreateFeature(feature2)  
    


    
