# Importa bibliotecas 
from numpy import *
from random import randint
from Vector3D import Vector3D
from scipy.spatial import distance
import time
import math

# Classe para ser usada na bala
class Bala(Vector3D):
    # Inicializa com os valores necessários para atirar
    def __init__(self, base, anguloAzimute, angulo):
        Vector3D.__init__(self, base.x, base.y, base.z)
        self.anguloAzimute = anguloAzimute
        self.angulo = angulo
        self.vx = 0
        self.vy = 0
        self.vz = 0
        self.vZInicial = 0
        self.tempoVoando = 0
        self.massa = 1.565
        self.velocidade = 1175
        self.alcance = 4000
        self.atirada = False
        
    # Retorna o raio da bala
    @property
    def raio(self):
        return 1

    def atualizaVelocidades(self):
        vPlano = self.velocidade / (1/0.03) * math.cos(self.angulo)

        self.vx = vPlano * math.cos(self.anguloAzimute)
        self.vy = vPlano * math.sin(self.anguloAzimute)

        self.vZInicial = self.velocidade * math.sin(self.angulo)

        self.tempoVoando = 0
        self.atirada = True

        # print("vx = " + str(self.vx) + " vy = " + str(self.vy) + " vz = " + str(self.vZInicial))

    def atualizaPosicao(self):
        if self.atirada:
            self.tempoVoando += 0.03
            gravidade = 9.8
            # self.vz = self.vZInicial - (9.8 * self.tempoVoando)

            self.x += self.vx
            self.y += self.vy
            self.z = self.vZInicial * self.tempoVoando - ((gravidade * (self.tempoVoando ** 2)) / 2)

            # print("vz = " + str(self.vZInicial))
            # print("tempo = " + str(self.tempoVoando))
            print("BALA - x = {:5.2f}; y = {:5.2f}; z = {:5.2f}".format(self.x, self.y, self.z))
            # print("BALA - x = " + str(self.x) + " y = " + str(self.y) + " z = " + str(self.z))
    




# Daqui pra baixo não é executado pois não faz parte da instância    
# bala = Bala(1, 1, 0) 
# bala2 = Bala(100, 100, 22) 


#dst = distance.euclidean(bala.points, bala2.points)
#print(dst)
