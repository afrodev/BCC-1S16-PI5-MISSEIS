from numpy import *
from random import randint
from Vector3D import Vector3D
import time


class Aviao(Vector3D):
    def __init__(self, x, y, z):
        Vector3D.__init__(self, x, y, z)
        self._tipo = randint(1, 2)  
        self._velocidade = 0
        self.inicializaVelocidade()
            
    @property
    def velocidade(self):
        return self._velocidade
    
    @velocidade.setter
    def velocidade(self, value):
        self._velocidade = value
    
    @property
    def tipo(self):
        return self._tipo
    
    @property
    def tipo(self):
        return self._tipo
    
    @property
    def raio(self):
        return 2
    
    def inicializaVelocidade(self):
        if (self.tipo == 1):
            self.velocidade = 66.6667 # km/h
            self.z = 200 # altitude
        else:
            self.z = 500
            self.velocidade = 111.111
    
    
    
esfera = Aviao(1, 1, 1) 

print(esfera.velocidade)
esfera.velocidade = 123
print(esfera.velocidade)

#print(esfera.x)
#print(esfera.y)
#print(esfera.z)

#esfera.x = 5
#esfera.y = 10
#esfera.z = 15

#print(esfera.x)
#print(esfera.y)
#print(esfera.z)

print(esfera.points)
