from numpy import *
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
        self._velocidade = 0 
        self._vx = 0 
        self._vy = 0        # Inicializa parametros
        self.inicializaPosicao()
        self.inicializaVelocidade() # Inicializa a velocidade de acordo com o tipo
        self._desiste = randint(1, 10)
        print("TIPO: " + str(self.tipo) + " - DESISTE: " + str(self.desiste))
        
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
        if (self.tipo == 1):
            self.velocidade = 66.6667 # m/s
            self.z = 200 # altitude
            
            distX = 5000 - self.x 
            distY = 5000 - self.y

            # print("distX: " + str(distX))
            # print("distY: " + str(distY))

            tangente = distY / distX
            teta = arctan(tangente)   

            if distX < 0:
                teta += math.pi

            # print("tangente: " + str(tangente))
            # print("teta: " + str(teta))        

            cosseno = cos(teta)
            seno = sin(teta)

            # print("cosseno: " + str(cosseno))
            # print("seno: " + str(seno))

            self.vx = self.velocidade * cosseno 
            self.vy = self.velocidade * seno 

            # print("vx: " + str(self.vx))
            # print("vy: " + str(self.vy))
        else:
            self.z = 500
            self.velocidade = 111.111

            distX = 5000 - self.x 
            distY = 5000 - self.y

            # print("distX: " + str(distX))
            # print("distY: " + str(distY))

            tangente = distY / distX
            teta = arctan(tangente)

            if distX < 0:
                teta += math.pi

            # print("tangente: " + str(tangente))
            # print("teta: " + str(teta))    

            alteracao = randrange(10, 75)
            # print("alteracao antes: " + str(alteracao))
            alteracao = math.radians(alteracao)

            pos = randint(0, 1)
            if pos == 0:
                alteracao = -alteracao

            teta += alteracao

            # print("alteracao: " + str(alteracao))
            # print("teta: " + str(teta))        

            cosseno = cos(teta)
            seno = sin(teta)

            # print("cosseno: " + str(cosseno))
            # print("seno: " + str(seno))

            self.vx = self.velocidade * cosseno 
            self.vy = self.velocidade * seno 

            # print("vx: " + str(self.vx))
            # print("vy: " + str(self.vy))

    def inicializaPosicao(self):
        self.x = randint(0, 10000)

        a = 1
        b = -10000
        c = (self.x * self.x) - 10000 * self.x + 25000000

        pos = randint(0, 1)
        raizes = roots([a, b ,c])
        
        self.y = raizes[pos]

        print("x: " + str(self.x))
        print("y: " + str(self.y))

    
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
