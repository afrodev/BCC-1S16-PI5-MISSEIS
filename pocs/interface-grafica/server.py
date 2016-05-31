# importando todas as bibliotecas necessárias
import asyncio # Para métodos que rodam assincronamente
import websockets # Cuida dos métodos de websocket
import time 
from base import Base
from aviao import Aviao
from bala import Bala

import threading
import math
import os

from sendOSCmessage import *


# import shlex

# Inicializa base no centro
base = Base(5000, 5000, 0) 
aviao = Aviao(0, 0, 1000000)
bala = Bala(base, 0, 0)

print("tipo: " + str(aviao.tipo))
distancia = 1000000000
distanciaAB = 1000000000
jaEnviouParaClient = 0
balasAtiradas = 0
tempoVooTiro = 1000
counter = 0


# Classe Servidor - Cuida das funções do servidor - é a base
class Servidor:
    def __init__(self):
        self.tempos = []
    
    
    # Colocando esse codigo antes, executamos a função em modo assincrono
    @asyncio.coroutine
    def conecta(self, websocket, path): 
        cliente = Cliente(self, websocket, path)

        print("Radar conectado.\n")
        yield from cliente.gerencia() # Com o yield podemos garantir que será executado de forma sequencial, colocando em uma fila.

    # Função para desconectar o cliente que entrou no servidor.
    def desconecta(self, cliente):
        print("Radar desconectado.")     

# Classe Cliente - Cuida das funçoes de transferencia de mensagem
class Cliente:  
    # Inicializa a classe do websocket  
    def __init__(self, servidor, websocket, path):
        self.cliente = websocket
        self.servidor = servidor

    # De forma assincrona, gerencia as conexões dos usuários no websocket
    @asyncio.coroutine
    def gerencia(self):
        try:
            # De forma sequencial, envia a todos os usuários a mensagem
            yield from self.envia("Radar Conectado")

            while True: # Enquanto a mensagem não chegar o servidor fica esperando
                
                #Coloca o tempo na hora de enviar a mensagem e envia
                tempoEnvio = time.time()
                tempoTotal = 0;
                intervaloLimite = 2;

                mensagemTotal = ""#mensagem
                result = "1";

                while result == "1" and tempoTotal < intervaloLimite:
                    #print(distancia)
                    global distancia
                    global aviao
                    global balasAtiradas

                    if distancia <= 3000 and aviao.z < 1000 and balasAtiradas < 4:
                        global jaEnviouParaClient
                        global bala

                        if jaEnviouParaClient == 0:
                            global tempoVooTiro

                            tempoEnvio = time.time()

                            mensagemTotal = str(aviao.x) + ";" + str(aviao.y) + ";" + str(aviao.z) + ";" + str(aviao.vx) + ";" + str(aviao.vy) + ";" + str(tempoEnvio)

                            yield from self.envia(mensagemTotal)
                    
                            # Recebe o retorno e pega o tempo que demora para ele retornar
                            result = yield from self.recebe()

                            arrayResult = result.split(";")
                            anguloAzimute = float(arrayResult[0])
                            angulo = float(arrayResult[1])
                            delay = float(arrayResult[2])
                            # tempoEnvio = float(arrayResult[3])
                            tempoVooTiro = float(arrayResult[4])
                            tempoRecebimento = time.time()

                            tempoTotal = tempoRecebimento - tempoEnvio

                            delay -= tempoTotal
                            print("delay = " + str(delay))
                            tempoInicio = aviao.tempoVoando

                            criaBala(anguloAzimute, angulo, delay, tempoInicio)
                            
                            jaEnviouParaClient = 1

                    else:
                        result = 0
                    
                # Está fora do while
                if result == "1":
                    print("Falha no envio, tempo limite excedido.")
                else:
                    servidor.tempos.append(tempoTotal);
                    #print("Enviado! (tempo total: {0})".format(tempoTotal))
                    total = 0
                    for tempo in servidor.tempos:
                        total += tempo

                    #print("tempo medio: {0}".format(total / len(servidor.tempos)) + "\n")
                    
        except Exception:
            print("Erro")
            raise        
        finally:
            self.servidor.desconecta(self)

    

    # Envia mensagem pelo websocket
    @asyncio.coroutine
    def envia(self, mensagem):
        yield from self.cliente.send(mensagem)

    # Recebe mensagem via websocket
    @asyncio.coroutine
    def recebe(self):
        mensagem = yield from self.cliente.recv()
        return mensagem

def criaBala(anguloAzimute, angulo, delay, tempoInicio):
    global bala
    global balasAtiradas

    tempo = aviao.tempoVoando - tempoInicio

    if tempo < delay:
        t = threading.Timer(0.025, criaBala, args = [anguloAzimute, angulo, delay, tempoInicio]).start()                            
    else:
        balasAtiradas += 1
        bala = Bala(base, anguloAzimute, angulo)
        bala.atualizaVelocidades()
    
# Esta função atualiza o avião
def atualizaPosicaoAviao():
    global tempoVooTiro
    global counter

    counter += 1

    t = threading.Timer(0.025, atualizaPosicaoAviao).start()
    
    if counter % 5 == 0:
        print("\nAVIAO - x = {:5.2f}; y = {:5.2f}; z = {:5.2f}; tempo = {:5.2f}\nBALA {} - x = {:5.2f}; y = {:5.2f}; z = {:5.2f}; tempo = {:5.2f}".format(aviao.x, aviao.y, aviao.z, aviao.tempoVoando, balasAtiradas, bala.x, bala.y, bala.z, bala.tempoVoando))
        
        # MANDA MENSAGEM OSC PARA A INTERFACE
        # AVIAOX, AVIAOY, AVIAOZ, AVIAOTEMPOVOANDO, BALAX, BALAY, BALAZ, BALAZ, BALATEMPOVOANDO
        messageOSC = "{:5.2f};{:5.2f};{:5.2f};{:5.2f};{:5.2f};{:5.2f};{:5.2f};{:5.2f};{:5.2f};0".format(aviao.x, aviao.y, aviao.z, aviao.tempoVoando, balasAtiradas, bala.x, bala.y, bala.z, bala.tempoVoando)
        sendMessageOSC(messageOSC) 
        
        
    # print("TEMPO VOANDO - " + str(aviao.tempoVoando) + "s")
    verificaDistanciaAviaoBala()
    verificaDistanciaBaseAviao()
    aviao.atualizaPosicao()
    if bala.tempoVoando < tempoVooTiro:
        bala.atualizaPosicao()
    else:
        reiniciaBala()

def reiniciaBala():
    global jaEnviouParaClient
    global tempoVooTiro
    global bala
    global distanciaAB

    distanciaAB = 100000000
    tempoVooTiro = 1000
    bala = Bala(base, 0, 0)
    bala.cancelaBala()
    jaEnviouParaClient = 0

# Verifica a distancia entre a base e o avião
def verificaDistanciaBaseAviao():
    distX = base.x - aviao.x
    distY = base.y - aviao.y
    distZ = 0 - aviao.z

    global distancia
    global counter

    distancia = math.sqrt(distX * distX + distY * distY + distZ * distZ)

    if counter % 5 == 0:
        print("DISTANCIA AVIAO/BASE - {:5.2f}m".format(distancia))
    
    # Verifica se acertou o alvo
    if distancia < 1000: # Base tem 1000 de raio
        print("Acertou a base")                    
        reiniciaAviao()


    # Verifica se está no intervalo de desistencia
    if distancia <= 3000:
        aviao.verificaDesistencia()
        mensagemTotal = "x"


    if distancia > 5000 and aviao.tempoVoando > 1:
        print("Avião Saiu do Raio")
        reiniciaAviao()

def verificaDistanciaAviaoBala():
    global balasAtiradas
    global counter
    global distanciaAB

    if bala.atirada:
        distX = bala.x - aviao.x
        distY = bala.y - aviao.y
        distZ = bala.z - aviao.z

        distanciaAB = math.sqrt(distX * distX + distY * distY + distZ * distZ)
        
        if counter % 5 == 0:
            print("DISTANCIA BALA/AVIAO - {:5.2f}m".format(distanciaAB))
        
        # Verifica se acertou o alvo
        if distanciaAB <= 2: # Base tem 1000 de raio
            print("\nAcertou o aviao com {} balas\nPosicao (x:{:5.2f}; y:{:5.2f})\nDistancia entre aviao e bala = {:5.2f}".format(balasAtiradas, bala.x, bala.y, distanciaAB))                    
            
            messageOSC = "{:5.2f};{:5.2f};{:5.2f};{:5.2f};{:5.2f};{:5.2f};{:5.2f};{:5.2f};{:5.2f};1".format(aviao.x, aviao.y, aviao.z, aviao.tempoVoando, ++balasAtiradas, bala.x, bala.y, bala.z, bala.tempoVoando)
            sendMessageOSC(messageOSC) 
            
            reiniciaAviao()


def reiniciaAviao():
    print("'s' - Se quiser sair do programa")
    print("'a' - Se quiser criar um aviao")

    global bala
    global jaEnviouParaClient
    global distancia   
    global distanciaAB
    global aviao     
    global balasAtiradas
    global tempoVooTiro

    distancia = 1000000000
    distanciaAB = 1000000000
    balasAtiradas = 0
    tempoVooTiro = 1000
    jaEnviouParaClient = 0

    op = input("")

    if op == 's':
        print("Programa foi fechado")
        os._exit(1)

    elif op == 'a':
        print("Avião foi criado")

        aviao.reiniciaAviao()
        bala = Bala(base, 0, 0)
        bala.cancelaBala()

        
# Criando o servidor efetivamente
servidor = Servidor()
loop = asyncio.get_event_loop()

# Inicializa o servidor com web socket 
start_server = websockets.serve(servidor.conecta, '0.0.0.0', 9768) # Usa-se 0.0.0.0 para pegar o ip do computador local

# Usa um trycatch para deixar rodando infinitamente o servidor de websocket
try:
    reiniciaAviao()
    atualizaPosicaoAviao()
    print("Servidor iniciado!")
    print("Esperando conexão de cliente...")
    loop.run_until_complete(start_server)
    loop.run_forever()
except(KeyboardInterrupt, SystemExit):
        start_server.close()
        loop.stop()
        sys.exit(0)
        websockets.close()

finally:
    start_server.close()
 