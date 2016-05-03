from numpy import *
import numpy 

from random import *
from Vector3D import Vector3D
import asyncio # Para métodos que rodam assincronamente
import time

# Herda da classe Vector3D
class Aviao(Vector3D):
    # Inicializa o avião junto com a classe super, que é a herança
    def __init__(self, x, y, z):
        Vector3D.__init__(self, x, y, z)
        self._tipo = randint(1, 2)  # Sorteia entre tipo 1 e 2
        # self._tipo = 2 # <================================================================================
        self._velocidade = 0 
        self._vx = 0 
        self._vy = 0        # Inicializa parametros
        self.inicializaPosicao()
        self.inicializaVelocidade() # Inicializa a velocidade de acordo com o tipo
        self._desiste = randint(1, 10)
        # self._desiste = 0 #<===============================================================================
        self._jaDesistiu = 0
        self._tempoVoando = 0
        self._tempoMudanca = numpy.random.normal(7.5, 1)
        # print("TIPO: " + str(self.tipo) + " - DESISTE: " + str(self.desiste))
        
    # Cria as propriedades para poder ser acessada de outras classes (getters e setters)
    @property
    def velocidade(self):
        return self._velocidade
    
    @velocidade.setter
    def velocidade(self, value):
        self._velocidade = value

    @property
    def vx(self):
        return self._vx
    
    @vx.setter
    def vx(self, value):
        self._vx = value

    @property
    def vy(self):
        return self._vy
    
    @vy.setter
    def vy(self, value):
        self._vy = value
    
    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, value):
        self._tipo = value

    @property
    def jaDesistiu(self):
        return self._jaDesistiu

    @jaDesistiu.setter
    def jaDesistiu(self, value):
        self._jaDesistiu = value
    
    @property
    def tempoVoando(self):
        return self._tempoVoando

    @tempoVoando.setter
    def tempoVoando(self, value):
        self._tempoVoando = value

    @property
    def tempoMudanca(self):
        return self._tempoMudanca

    # Se o avião chegar a 3 km ele desiste ou não
    @property
    def desiste(self):
        if (self._desiste == 1):
            return 1
        else:
            return 0
    
    @property
    def raio(self):
        return 2
    
    # Inicializa a velocidade e altitude a partir do tipo
    def inicializaVelocidade(self):
        if self.tipo == 1:
            self.velocidade = 66.6666666 / (1/0.03) # m/s
            self.z = 200 # altitude
            
            distX = 5000 - self.x 
            distY = 5000 - self.y

            tangente = distY / distX
            teta = arctan(tangente)   

            if distX < 0:
                teta += math.pi

            cosseno = cos(teta)
            seno = sin(teta)

            self.vx = self.velocidade * cosseno 
            self.vy = self.velocidade * seno 
        elif self.tipo == 2:
            self.z = 500
            self.velocidade = 111.111111111 / (1/0.03)

            distX = 5000 - self.x 
            distY = 5000 - self.y

            tangente = distY / distX
            teta = arctan(tangente)

            if distX < 0:
                teta += math.pi

            alteracao = randrange(10, 75)
            alteracao = math.radians(alteracao)

            pos = randint(0, 1)
            if pos == 0:
                alteracao = -alteracao

            teta += alteracao       

            cosseno = cos(teta)
            seno = sin(teta)

            self.vx = self.velocidade * cosseno 
            self.vy = self.velocidade * seno 
        elif self.tipo == 3:
            self.z = 1200
            self.velocidade = 208.333333333 / (1/0.03) # 750 km/h

            distX = 5000 - self.x 
            distY = 5000 - self.y

            tangente = distY / distX
            teta = arctan(tangente)   

            if distX < 0:
                teta += math.pi

            cosseno = cos(teta)
            seno = sin(teta)

            self.vx = self.velocidade * cosseno 
            self.vy = self.velocidade * seno 

    def inicializaPosicao(self):
        self.x = randint(0, 10000)

        a = 1
        b = -10000
        c = (self.x * self.x) - 10000 * self.x + 25000000

        pos = randint(0, 1)
        raizes = roots([a, b ,c])
        
        self.y = raizes[pos]

        # print("x: " + str(self.x))
        # print("y: " + str(self.y))

    def verificaDesistencia(self):
        if self.jaDesistiu == 0 and self.desiste == 1:
            # print("desistiu")
            self.tipo = 3
            self.jaDesistiu = 1
            self.inicializaVelocidade()

    def atualizaPosicao(self):
        self.x += self.vx
        self.y += self.vy
        self.tempoVoando += 0.03
        # print("voando " + str(self.tempoVoando))
        # print("mudanca " + str(self.tempoMudanca))
        if self.tipo == 2 and self.tempoVoando >= self.tempoMudanca:
            self.tipo = 1
            self.inicializaVelocidade()

    def reiniciaAviao(self):
        self.__init__(0, 0, 1000000)

    
# Daqui pra baixo não é executado pois não faz parte da instância    
   
        
    
# esfera = Aviao(1, 1, 1) 

#
#print(esfera.velocidade)
#esfera.velocidade = 123
#print(esfera.velocidade)

#print(esfera.x)
#print(esfera.y)
#print(esfera.z)

#esfera.x = 5
#esfera.y = 10
#esfera.z = 15

#print(esfera.x)
#print(esfera.y)
#print(esfera.z)

#print(esfera.points)
