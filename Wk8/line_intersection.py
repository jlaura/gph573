import Tkinter, tkFileDialog
import turtle
import os
import numpy as np
from osgeo import ogr

import time
import multiprocessing as mp  
    
## If two lines are parallel but not overlap return 0, overlap return 1
## intersect reture inersection point, otherwise return -1
def intersect(lineseg1, lineseg2):
    
    def _overlap(lineseg1, lineseg2):
        small = min(lineseg1[0][1], lineseg1[1][1])
        big = max(lineseg1[0][1], lineseg1[1][1])
        if small<lineseg2[0][1]<big or small<lineseg2[1][1]<big:
            return 1
        else:
            return -1     
    #Check the bounding boxes
    _overlap(lineseg1, lineseg2)
    
    def _perp(a):
        b = np.empty_like(a)
        b[0] = -a[1]
        b[1] = a[0]
        return b
    
    #For speed these should be numpy arrays to start with.
    a1 = np.asarray(lineseg1[0])
    a2 = np.asarray(lineseg1[1])
    b1 = np.asarray(lineseg2[0])
    b2 = np.asarray(lineseg2[1])

    #Compute 4 determinants for the x,y coord pairs.  Essentially this is checking to see which side of the line an end point falls.
    det1 = np.linalg.det(np.asarray([[(a1[0]-b1[0]),(a2[0]-b1[0])],[(a1[1]-b1[1]),(a2[1]-b1[1])]]))
    det2 = np.linalg.det(np.asarray([[(a1[0]-b2[0]),(a2[0]-b2[0])],[(a1[1]-b2[1]),(a2[1]-b2[1])]]))
    det3 = np.linalg.det(np.asarray([[(b1[0]-a1[0]),(b2[0]-a1[0])],[(b1[1]-a1[1]),(b2[1]-a1[1])]]))
    det4 = np.linalg.det(np.asarray([[(b1[0]-a2[0]),(b2[0]-a2[0])],[(b1[1]-a2[1]),(b2[1]-a2[1])]]))
    #This works if the lines are parallel or colinear, but does not report if they are, i.e. we only care if they intersect.
    if det1 < 0 and det2 > 0 or det2 < 0 and det1 > 0:
        if det3 < 0 and det4 > 0 or det4 < 0 and det3 > 0:
            #print "The lines intersect"
            #Compute the intersection here.
            da = a2-a1
            db = b2-b1
            dp = a1-b1
            dap = _perp(da)
            denom = np.dot(dap, db)
            num = np.dot(dap, dp)
            
            return (num / denom) * db + b1                    
        else:
            #print "The lines do no intersect"
            return -1
            
    else:
        #print "The lines do not intersect"
        return -1
 
def intersect_mp(lines, q):
    out_list = []
    
    def _overlap(lineseg1, lineseg2):
        small = min(lineseg1[0][1], lineseg1[1][1])
        big = max(lineseg1[0][1], lineseg1[1][1])
        if small<lineseg2[0][1]<big or small<lineseg2[1][1]<big:
            return 1
        else:
            return -1   
        
    def _perp(a):
        b = np.empty_like(a)
        b[0] = -a[1]
        b[1] = a[0]
        return b    
    
    for line in lines:
        for seg in line:
            for lineseg2 in sharedlines2:
                
                #Check the bounding boxes
                overlap = _overlap(seg, lineseg2)
                if overlap == -1:
                    continue
                #For speed these should be numpy arrays to start with.
                a1 = np.asarray(seg[0])
                a2 = np.asarray(seg[1])
                b1 = np.asarray(lineseg2[0])
                b2 = np.asarray(lineseg2[1])
            
                #Compute 4 determinants for the x,y coord pairs.  Essentially this is checking to see which side of the line an end point falls.
                det1 = np.linalg.det(np.asarray([[(a1[0]-b1[0]),(a2[0]-b1[0])],[(a1[1]-b1[1]),(a2[1]-b1[1])]]))
                det2 = np.linalg.det(np.asarray([[(a1[0]-b2[0]),(a2[0]-b2[0])],[(a1[1]-b2[1]),(a2[1]-b2[1])]]))
                det3 = np.linalg.det(np.asarray([[(b1[0]-a1[0]),(b2[0]-a1[0])],[(b1[1]-a1[1]),(b2[1]-a1[1])]]))
                det4 = np.linalg.det(np.asarray([[(b1[0]-a2[0]),(b2[0]-a2[0])],[(b1[1]-a2[1]),(b2[1]-a2[1])]]))
                #This works if the lines are parallel or colinear, but does not report if they are, i.e. we only care if they intersect.
                if det1 < 0 and det2 > 0 or det2 < 0 and det1 > 0:
                    if det3 < 0 and det4 > 0 or det4 < 0 and det3 > 0:
                        #print "The lines intersect"
                        #Compute the intersection here.
                        da = a2-a1
                        db = b2-b1
                        dp = a1-b1
                        dap = _perp(da)
                        denom = np.dot(dap, db)
                        num = np.dot(dap, dp)
                        out_list.append((num / denom) * db + b1)
                    else:
                        #print "The lines do no intersect"
                        pass
                        
                else:
                    #print "The lines do not intersect"
                    pass
                
    q.put(out_list)
## Set up global variables
startDraw = False
lineSegs =[]
points = []
## Main function
def main():
    #Store the open shapefile geometries in a list
    list_of_shapefiles = []
    list_of_intersections = []
    
    win = Tkinter.Tk()
    win.title('Line Intersection Viewer')
    canvas = Tkinter.Canvas(win, bg='black', height = 600, width = 600)
    canvas.pack(side=Tkinter.LEFT)
    t = turtle.RawTurtle(canvas)
    screen = t.getscreen()
    """
    ## screensetworldcoordinates(llx,lly,urx,ury)
    ## llx: x coordinate of lower left corner of canvas
    ## urx: x coordinate of upper right corner of canvas
    """
    screen.setworldcoordinates(0,600,600,0)

    frame = Tkinter.Frame(win) ## create a frame
    frame.pack(side=Tkinter.RIGHT, fill = Tkinter.BOTH)

    def checkIntersectionHandler(list_of_shapefiles, list_of_intersections):
        linesegs1 = list_of_shapefiles[0]
        linesegs2 = list_of_shapefiles[1]
        
        for line1 in linesegs1:
            for line2 in linesegs2:        
                result = intersect(line1, line2)
                if type(result) == int:
                    pass
                else:
                    t.penup()
                    t.setposition(result[0], result[1])
                    t.dot(5, "red")
                    t.pendown()
                    list_of_intersections.append(result)
                    #t.write('Intersection: '+ str(result[0])+','+str(result[1]))

    checkIntersection = Tkinter.Button(frame, width = 15,text= 'Check Intersection',fg="blue", command=lambda: checkIntersectionHandler(list_of_shapefiles, list_of_intersections))
    checkIntersection.pack()

    def checkFastIntersectionHandler(list_of_shapefiles, list_of_intersections, canvas):
        t1 = time.time()

        def _set_globals(_linesegs2):
            global sharedlines2
            sharedlines2 = _linesegs2

        linesegs1 = list_of_shapefiles[0]
        linesegs2 = list_of_shapefiles[1]
        cores = mp.cpu_count() * 2
        step = len(linesegs1) / cores
        _set_globals(linesegs2)
        result_queue = mp.Queue()
        intersects = [intersect_mp([linesegs1[lines:lines+step:1]],result_queue) for lines in range(0,len(linesegs1), step)]
        jobs = [mp.Process(intersect) for intersect in intersects]
        for job in jobs: job.start()
        for job in jobs: job.join()   
        pt_list = [result_queue.get() for intersect in intersects]
        for pts in pt_list:
            for point in pts:  
                list_of_intersections.append(point)
                canvas.create_oval(point[0]-2.5, point[1]-2.5, point[0] +2.5 ,point[1] + 2.5 , fill='red')
        
        t2 = time.time()
        tt = t2-t1
        win = Tkinter.Toplevel()
        labeltext = 'Total processing time was {0:.2f} seconds'.format(tt)
        Tkinter.Label(win,  text=labeltext).pack()
        Tkinter.Button(win, text='OK', command=win.destroy).pack()        
        
    fastcheck = Tkinter.Button(frame, width=15, text='Fast Check', fg='blue', command=lambda:checkFastIntersectionHandler(list_of_shapefiles, list_of_intersections, canvas))
    fastcheck.pack()
    
    def openShapefile(canvas, list_of_shapefiles):
        
        def _displayshapefile(shapefile,canvas, list_of_shapefiles):
            ds = ogr.Open(shapefile)
            layer = ds.GetLayer(0)
            xmin, xmax, ymin, ymax = layer.GetExtent()
            umax = 600
            vmax = 600
            ratioX = (umax - 0)/(xmax-xmin)
            ratioY = (vmax - 0)/(ymax-ymin)
            ratio = min(ratioX, ratioY)
            feature = layer.GetNextFeature()
            geom_type = feature.GetGeometryRef().GetGeometryType()
            if geom_type == 2: #This is a polyline
                    polyline = []
                    polyline_array = []
                    while feature:
                            geom = feature.GetGeometryRef()
                            vertices = geom.GetPointCount()
                            line_feature = []
                            line_feature_array = []
                            for vertex in range(vertices):
                                    x,y,z = geom.GetPoint(vertex)
                                    x = ((ratio * (x - xmin))) * .95 + 10
                                    y = (vmax + ((-1 * ratio) * (y - ymin))) * 0.95 + 10
                                    line_feature.append(x)
                                    line_feature.append(y)
                                    line_feature_array.append([x,y])
                            polyline.append(line_feature)
                            polyline_array.append(line_feature_array)
                            feature = layer.GetNextFeature()
            if len(list_of_shapefiles) == 0:
                color = 'blue'
            else:
                color = 'green'
            for line in polyline:
                canvas.create_line(line, fill=color)
            canvas.pack()
            list_of_shapefiles.append(polyline_array)
            
        shapefile = tkFileDialog.askopenfilename(filetypes=[("Shapefiles", ".shp")]) 
        polyline_array =  _displayshapefile(shapefile,canvas,list_of_shapefiles)
    
    openshapefile1 = Tkinter.Button(frame, width=15, text='Open Shapefile', fg='blue', command=lambda: openShapefile(canvas, list_of_shapefiles))
    openshapefile1.pack()

    def saveIntersections(intersections):
        output = tkFileDialog.asksaveasfilename()
        driver = ogr.GetDriverByName("ESRI Shapefile")
        ds = driver.CreateDataSource(output)
        layer = ds.CreateLayer("intersection point", None, ogr.wkbPoint)
        featureDefn = layer.GetLayerDefn()
        feature = ogr.Feature(featureDefn)        
        for intersection in intersections:
            point = ogr.Geometry(ogr.wkbPoint)
            point.SetPoint_2D(0,intersection[0], intersection[1])
            feature.SetGeometry(point)
            layer.CreateFeature(feature)
 
    saveintersections = Tkinter.Button(frame, width=15, text='Save intersections', fg='blue', command=lambda: saveIntersections(list_of_intersections))
    saveintersections.pack()
    
    def quitHandler():
        print 'GoodBye'
        os._exit(1)
    button = Tkinter.Button(frame,width = 15, text= 'Quit',fg="blue", command=quitHandler)
    button.pack()
    win.mainloop()

if __name__=='__main__':
    main()

