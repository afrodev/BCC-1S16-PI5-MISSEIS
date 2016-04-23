from numpy import *
from random import randint
from Vector3D import Vector3D
from scipy.spatial import distance
import time
from bala import Bala


# Esta é a base/alvo do avião
class Base(Vector3D):
    # Inicializa base 
    def __init__(self, x, y, z):
        Vector3D.__init__(self, x, y, z)
        self._tipo = randint(1, 2) 
        self._balas = [Bala(x, y, z), Bala(x, y, z), Bala(x, y, z), Bala(x, y, z)]

    @property
    def raio(self):
        return 10000    
    
    @property
    def balas(self):
        return self._balas
    
    def balaAtual(self):
        return self._balas[0]
    
    def destroiBalaAtual(self):
        self._balas.pop(0)
    
    
#base = Base(50000, 50000, 0) 
#base2 = Base(100, 100, 22) 

#print(base.balas)
#
#base.destroiBalaAtual()
#
#print(base.balas[0])


# Daqui pra baixo não é executado pois não faz parte da instância    

#dst = distance.euclidean(base.points, base2.points)
#print(dst)



#result = str(base2.x) + ";" + str(base2.y) + ";" + str(base2.z)
## Calcula a distancia do avião da base
#arrayResult = result.split(";")
#posAviao = [float(arrayResult[0]), float(arrayResult[1]), float(arrayResult[2])]
#dst = distance.euclidean(base.points, posAviao)
#print(base.distanciaEuclidiana(posAviao))
