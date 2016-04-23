# Importa bibliotecas 
from numpy import *
from random import randint
from Vector3D import Vector3D
from scipy.spatial import distance
import time

# Classe para ser usada na bala
class Bala(Vector3D):
    # Inicializa com os valores necessários para atirar
    def __init__(self, x, y, z):
        Vector3D.__init__(self, x, y, z)
        self.massa = 1.565
        self.velocidade = 1175
        self.alcance = 4000
        
    # Retorna o raio da bala
    @property
    def raio(self):
        return 1    

# Daqui pra baixo não é executado pois não faz parte da instância    
bala = Bala(1, 1, 0) 
bala2 = Bala(100, 100, 22) 


dst = distance.euclidean(bala.points, bala2.points)
print(dst)
