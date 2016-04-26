# importando todas as bibliotecas necessárias
import asyncio # Para métodos que rodam assincronamente
import websockets # Cuida dos métodos de websocket
import time 
from base import Base
from aviao import Aviao
import threading
import sys
# import shlex

# Inicializa base no centro
base = Base(5000, 5000, 0) 
aviao = Aviao(0, 0, 0)
print("tipo: " + str(aviao.tipo))


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
                # Escreve a mensagem vinda do teclado
                mensagem = input("Digite sua mensagem: ") # Pode digitar qualquer mensagem diferente de vazio
                
                #Coloca o tempo na hora de enviar a mensagem e envia
                tempoEnvio = time.time()
                tempoTotal = 0;
                intervaloLimite = 2;

                mensagemTotal = mensagem
                result = "1";

                print("\nEnviando....")

                while result == "1" and tempoTotal < intervaloLimite:
                    yield from self.envia(mensagemTotal)
                
                    # Recebe o retorno e pega o tempo que demora para ele retornar
                    result = yield from self.recebe()

                    
                    tempoRecebimento = time.time()
                    tempoTotal = tempoRecebimento - tempoEnvio
                    
                    # Aqui ele pega os dados necessários para o tiro no canhão
                    # Será processado abaixo
                    arrayResult = result.split(";")
                    
                    # Aqui estão as coordenadas do avião
                    angulacao = arrayResult[0]
                    outrasInfo = arrayResult[1]
                    
                    
                    print(arrayResult)

                    # Coloquei -1002, pois 1 km da base pra ser considerado acerto e 2 metros de raio do avião 
                    # distancia = base.distanciaEuclidiana(arrayResultNum) - 1002
                    
                    # Se ele chgar a uma distancia de 3 km e for desistir
                    '''
                    if (distancia < 3000 and vaiDesistir == 1):
                        # volta para uma altitude de 1200 m e velocidade de 750km/h ou 208,333 m/s
                        yield from self.envia("a")
                        # lá no client trata se ele já foi enviado uma vez a atualizacao
                        
                    elif distancia <= 0:
                        print("-----------------BASE ATINGIDA----------------")
                        yield from self.envia("d") # Destruida = d = base destruida
                        
                        
                    # Se a distancia for menor que 10km pode atirar de acordo que o mario 
                    # ache que é o momento certo, coloque as validações aqui
                    if distancia < 10000:
                        # dentro da classe base tem 4 balas com funcoes que ajudam
                        print("menos que 10 km")
                        #print(str(balaAtual.x) + ";" + str(balaAtual.y) + ";" + str(balaAtual.z))
                    
                        
                    print("Distancia entre avião: " + str(distancia))
                    '''


                # Está fora do while
                if result == "1":
                    print("Falha no envio, tempo limite excedido.")
                else:
                    servidor.tempos.append(tempoTotal);
                    print("Enviado! (tempo total: {0})".format(tempoTotal))
                    total = 0
                    for tempo in servidor.tempos:
                        total += tempo

                    print("tempo medio: {0}".format(total / len(servidor.tempos)) + "\n")
                    
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
    
# Esta função atualiza o avião
def atualizaPosicaoAviao():
    t = threading.Timer(1.0, atualizaPosicaoAviao).start()
    aviao.x += aviao.vx
    aviao.y += aviao.vy
    print("BASE - " + str(base.x) + ";" + str(base.y) + ";" + str(base.z))
    print("AVIAO - " + str(aviao.x) + ";" + str(aviao.y) + ";" + str(aviao.z))
    verificaDistanciaBaseAviao()
    
# Verifica a distancia entre a base e o avião
def verificaDistanciaBaseAviao():
    distancia = aviao.distanciaEuclidiana(base.points) - base.raio #(1002)
    
    
    if distancia < 0:
        distancia *= (-1)
    
    # Verifica se acertou o alvo
    if distancia < 1000: # Base tem 1000 de raio
        print("Acertou o alvo")                    
        start_server.close()
        loop.stop()
        sys.exit()
        websockets.close()
    
    # Verifica se está no intervalo de desistencia
    if distancia >= 1000 and distancia <= 3000:
        if aviao.desiste == 1:
            aviao.z = 1200
            aviao.valocidade = 208.333 # 750 km/h | Inicializarei desse jeito pois precisamos atualizar os valores de x e y
        

    print(distancia)



# O que precisa fazer?
# - Calcular a distancia de 3000 m
# - Calcular a distancia de 1000 m
# - Calcular se colidiu mesmo
    
# Criando o servidor efetivamente
servidor = Servidor()
loop = asyncio.get_event_loop()

# Inicializa o servidor com web socket 
start_server = websockets.serve(servidor.conecta, '0.0.0.0', 8766) # Usa-se 0.0.0.0 para pegar o ip do computador local

atualizaPosicaoAviao()

# Usa um trycatch para deixar rodando infinitamente o servidor de websocket
try:
    print("Servidor iniciado!")
    print("Esperando conexão de cliente...")
    loop.run_until_complete(start_server)
    loop.run_forever()
#    t.start()
finally:
    start_server.close()
 