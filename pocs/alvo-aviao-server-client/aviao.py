from numpy import *
from stsci.sphere.polygon import SphericalPolygon
from random import randint

import time


class Aviao(SphericalPolygon):
    def __init__(self, x, y, z):
        SphericalPolygon.__init__(self, [2,2,2], inside=[x,y,z])
        self._tipo = randint(1, 2)

        
    @property
    def x(self):
        return self.inside[0]
    
    @property
    def y(self):
        return self.inside[1]
    
    @property
    def z(self):
        return self.inside[2]
    
    @property
    def tipo(self):
        return self._tipo

    
    

esfera = Aviao(1, 1, 1) 
print(esfera)
print(esfera.x)
print(esfera.y)
print(esfera.z)
print(esfera.points[0])
print(esfera.inside)
print(esfera.inside[0])
print(esfera.inside[1])
print(esfera.inside[2])
print(esfera.area)



    
''''
from Vector3D import Vector3D
from random import randint


import time

# Herda da classe Vector3D
class Aviao(Vector3D):
    
    def __init__(self, x, y, z):
        Vector3D.__init__(self, x, y, z)
        self._tipo = randint(1, 2)
        
    @property
    def tipo(self):
        return self._tipo
    
    def andaX(self):
        self.x = self.x + 1

    def andaY(self):
        self.y = self.y + 1

    def andaZ(self):
        self.z = self.z + 1


aviao = Aviao(0.0, 0.0, 0.0)

while True:
    time.sleep(1)
    
    aviao.andaX()
    aviao.andaY()
    aviao.andaZ()
    
    print(str(aviao.tipo))
    print(str(aviao.x) +" - "+ str(aviao.y) +" - "+ str(aviao.z))
    
    
    


## Para lembrar como se altera

# aviao.andaX()
# aviao.y = 2.0
# aviao.z = 3.0
# print(str(aviao.x) +" - "+ str(aviao.y) +" - "+ str(aviao.z))
# randint(1,2 ) sorteio
'''
