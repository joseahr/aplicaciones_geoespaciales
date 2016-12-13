#!/usr/bin/python
# -*- coding: utf8 -*-

from BBOX import BBOX
from math import sqrt

class Quadtree(object):
    def __init__(self, bbox, max_objetos = 10, max_niveles = 4, nivel = 0):
        if not isinstance(bbox, BBOX) and not isinstance(bbox, list): 
            raise Exception('bbox debe ser de la clase BBOX o un array')
        if isinstance(bbox, list):
            self.bbox = BBOX(bbox)
        else : 
            self.bbox = bbox

        self.MAX_OBJETOS = max_objetos if max_objetos > 0 else 10
        self.MAX_NIVELES = max_niveles if max_niveles > 0 else 4

        self.nivel       = nivel
        self.objetos     = []
        self.nodos       = []

    def split(self):

        nivel_sig = self.nivel + 1
        dx        = self.bbox.getDX() / 2
        dy        = self.bbox.getDY() / 2
        x         = self.bbox.xmin
        y         = self.bbox.ymin

        qtso = Quadtree( BBOX(x, x + dx, y, y + dy), self.MAX_OBJETOS, self.MAX_NIVELES, nivel_sig  )
        qtse = Quadtree( BBOX(x + dx, self.bbox.xmax, y, y + dy), self.MAX_OBJETOS, self.MAX_NIVELES, nivel_sig  )
        
        qtno = Quadtree( BBOX(x, x + dx, y + dy, self.bbox.ymax), self.MAX_OBJETOS, self.MAX_NIVELES, nivel_sig  )
        qtne = Quadtree( BBOX(x + dx, self.bbox.xmax, y + dy, self.bbox.ymax), self.MAX_OBJETOS, self.MAX_NIVELES, nivel_sig  )

        self.nodos.extend((qtne, qtse, qtso, qtno))
    def getIndice(self, bbox):
        indice = -1
        x_pm   = self.bbox.xmin + (self.bbox.getDX() / 2)
        y_pm   = self.bbox.ymin + (self.bbox.getDY() / 2)

        cuadrante_norte = bbox.ymin > y_pm and bbox.ymax > y_pm
        cuadrante_sur   = bbox.ymin < y_pm

        if bbox.xmin < x_pm and bbox.xmax < x_pm :
            if cuadrante_norte : indice = 3
            elif cuadrante_sur : indice = 2
        elif bbox.xmin > x_pm :
            if cuadrante_norte : indice = 0
            elif cuadrante_sur : indice = 1
        return indice

    def insertar(self, bbox):
        if len(self.nodos):
            indice = self.getIndice(bbox)

            if not indice == -1 :
                self.nodos[indice].insertar(bbox)
                return True
            
        self.objetos.append(bbox)

        if len(self.objetos) > self.MAX_OBJETOS and self.nivel < self.MAX_NIVELES :
            if not len(self.nodos):
                self.split()
            
            for idx, objeto in enumerate(self.objetos):
                indice = self.getIndice(objeto)

                if not indice == -1 :
                    self.nodos[indice].insertar(objeto)
                    del self.objetos[idx]
                    return True
        return False
                
    def getObjetosColision(self, bbox):
        indice = self.getIndice(bbox)
        objetosDevueltos = self.objetos
        if len(self.nodos):
            if not indice == -1 :
                objetosDevueltos = objetosDevueltos + self.nodos[indice].getObjetosColision(bbox)
            else :
                for idx, n in self.nodos :
                    objetosDevueltos = objetosDevueltos + self.nodos[idx].getObjetosColision(bbox)
        return objetosDevueltos

def PuntoMasCercano(pt, *lista):
    xp, yp = pt
    dmin = float('inf')
    psol = None
    for p in list(lista):
        x2, y2 = p
        d = sqrt( (x2 - xp)**2 + (y2 - yp)**2 )
        if (d < dmin):
            dmin = d
            psol = p
    return [psol, dmin]


def main():
    import timeit
    from BBOX import RandomCloud
    import time
    rc = RandomCloud(100000)
    tps = RandomCloud(10)
    tp = tps[0]

    bb = BBOX.fromCloud(rc)
    qtree = Quadtree(bb, max_niveles = 10, max_objetos = 500)
    t = time.time()
    for p in rc :
        x, y = p
        f = 5
        bb2 = BBOX(x - f, x + f, y - f, y + f)
        qtree.insertar(bb2)
    print('Tiempo que tarda en generar el quadtree', time.time() - t)

    f = 0.0000005
    xtp, ytp = tp
    bbtp = BBOX(xtp - f, xtp - f, ytp - f, ytp + f)

    t = time.time() 
    oc = qtree.getObjetosColision(bbtp)
    print('Tiempo que tarda en conseguir los elementos que intersectan : ', time.time() - t)
    puntos_prox = []
    for pt in oc :

        puntos_prox.append([ pt.xmin + (pt.getDX()/2), pt.ymin + (pt.getDY()/2) ])

    #print(puntos_prox)
    print(len(oc))
    print('Punto Ref : ', tp)

    print('Puntos Más cercano Qtree', PuntoMasCercano(tp, *puntos_prox) )
    print(timeit.Timer(lambda : PuntoMasCercano(tp, *puntos_prox) ).timeit(number = 1))
    print('Punto Más cerca Normal', PuntoMasCercano(tp, *rc))
    print(timeit.Timer(lambda : PuntoMasCercano(tp, *rc)).timeit(number = 1))
if __name__ == '__main__':
    main()