from numpy import *
from random import randint
from Vector3D import Vector3D
from scipy.spatial import distance
import time


import time



class Base(Vector3D):
    def __init__(self, x, y, z):
        Vector3D.__init__(self, x, y, z)
        self._tipo = randint(1, 2)    
    
    @property
    def raio(self):
        return 10000    
    
base = Base(50000, 50000, 0) 
base2 = Base(100, 100, 22) 


dst = distance.euclidean(base.points, base2.points)
print(dst)

#
#
#print(base.array)
#print(dst)



