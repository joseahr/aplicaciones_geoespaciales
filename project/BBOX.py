#!/usr/bin/python
# -*- coding: utf8 -*-
import numpy as np
import datetime
from math import sqrt
class BBOX(object):

    def __init__(self, *values):
        #print('new BBOX() --> ', values)
        if not len(values) == 4   : raise Exception('La función recibe 4 argumentos')
        if values[1] < values[0]  : raise Exception('xmax debe ser mayor que xmin')
        if values[3] < values[2]  : raise Exception('ymax debe ser mayor que ymin')

        self.xmin, self.xmax, self.ymin, self.ymax = list(values)

    def toArray(self):
        return [ self.xmin, self.xmax, self.ymin, self.ymax ]
    
    def getDX(self):
        return self.xmax - self.xmin
        
    def getDY(self):
        return self.ymax - self.ymin

    def inside(self, *point):
        x, y = list(point)
        if x < self.xmin : return False
        if x > self.xmax : return False
        if y < self.ymin: return False
        if y > self.ymax : return False
        return True
    
    @staticmethod
    def fromCloud(array):
        ##start = datetime.datetime.now()
        '''
        array = np.array(array)
        xcol = array[:,0]
        ycol = array[:,1]

        xmin, xmax, ymin, ymax = [ min(xcol), max(xcol), min(ycol), max(ycol) ]
        '''
        xmin = ymin = float('inf')
        xmax = ymax = -float('inf')
        for point in array:
            x, y = point
            if x < xmin : xmin = x
            if y < ymin : ymin = y
            if x > xmax : xmax = x
            if y > ymax : ymax = y
        ##end = datetime.datetime.now()
        ##print('time :', end - start)
        return BBOX(xmin, xmax, ymin, ymax)


def RandomCloud(num_points = 1000, bbox = BBOX(0, 1000, 0, 1000) ):
    from random import uniform as uni
    array = list(map(float, bbox.toArray()))
    xs, ys = [ array[:2], array[2:] ] 
    return [ [uni(*xs), uni(*ys)] for i in range(num_points) ]
'''
def closestPoint(rc, bbox, point, divisiones = 9, vecinos = 1):
    def closestPoint_(rc, bbox,  point, divisiones = 9, vecinos = 1):
        x, y = point
        bbox_principal = bbox
        #print('bbox principal-->', bbox_principal.toArray())
        dx = bbox_principal.getDX() / divisiones
        dy = bbox_principal.getDY() / divisiones

        dr = max(dx, dy)
        
        ## Nuevo BBOX envolvente
        xmin, xmax, ymin, ymax = [ x - (dr * vecinos) - (dr/2), x + (dr * vecinos) + (dr/2), y - (dr * vecinos) - (dr/2), y + (dr * vecinos) + (dr/2) ]
        bbox_vecinos = BBOX(xmin, xmax, ymin, ymax)
        #print('bbox vecinos-->', bbox_vecinos.toArray())
        rc_vecinos = [ p for p in rc if bbox_vecinos.inside(*p) ]
        #print('leeen', len(rc_vecinos))
        if len(rc_vecinos) == 0 :
             return closestPoint_(rc, bbox, point, divisiones, vecinos + 4)
        if len(rc_vecinos) == 1 :
            return rc_vecinos[0]
        
        return closestPoint_(rc_vecinos, bbox_vecinos, point)

    return closestPoint_(rc, bbox, point)

def distancia(p1, p2) : 
    x1, y1 = p1
    x2, y2 = p2
    return sqrt( (x2 - x1)**2 + (y2 - y1)**2 )

def closestPointASaco(rc, point) :
    distanciaMasCorta = float('inf')
    puntoSol = None
    for p in rc :
        dist = distancia(point, p)
        if (dist < distanciaMasCorta):
            distanciaMasCorta = dist
            puntoSol = p
    return puntoSol
'''


def main():
    '''
    bbox = BBOX(0, 10, 0, 20)
    print(bbox.xmin, bbox.xmax, bbox.ymin, bbox.ymax)
    print(bbox.inside(-5, 5))
    '''
    rc = RandomCloud(1000000, BBOX(500,1000,0,1000))
    #print(rc)
    bbox2 = BBOX.fromCloud(rc)
    print(bbox2.toArray())

    tp = RandomCloud(10, bbox2)
    '''
    cp = closestPoint(rc, tp[0])
    print(tp[0], cp, distancia(tp[0], cp), 'Alg' )

    cp2 = closestPointASaco(rc, tp[0])

    print(tp[0], cp2, distancia(tp[0], cp2))
    
    import timeit

    t = timeit.Timer(lambda : closestPoint(rc, bbox2, tp[0]))
    print(t.timeit(number=10))
    t = timeit.Timer(lambda : closestPointASaco(rc, tp[0]))
    print(t.timeit(number=10))
    '''
if __name__ == '__main__':
    main()