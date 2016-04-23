# importando todas as bibliotecas necessárias
import asyncio # Para métodos que rodam assincronamente
import websockets # Cuida dos métodos de websocket
import time 
from base import Base
import threading
# import shlex

# Inicializa base no centro
base = Base(6000, 6000, 6000) 



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


# Aqui a bala é atualizada na tela, colocada em thread 
# para não depender da resposta 
@asyncio.coroutine
def atualizaPosicaoBala():
    balaAtual = base.balaAtual()
    while True:
        # aqui ele atira
        balaAtual.x += 1
        balaAtual.y += 1
        balaAtual.z += 1000
        time.sleep(1)
        print("POSICAO BALA - " + str(balaAtual.x) + ";" + str(balaAtual.y) + ";" + str(balaAtual.z))

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
                mensagem = input("Digite sua mensagem: ") #"p"
                
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
                    print("POSICAO: " + result)
                    
                    tempoRecebimento = time.time()
                    tempoTotal = tempoRecebimento - tempoEnvio
                    
                    # Calcula a distancia do avião da base
                    arrayResult = result.split(";")
                    
                    # Aqui estão as coordenadas do avião
                    arrayResultNum = [float(arrayResult[0]), float(arrayResult[1]), float(arrayResult[2])]
                    vaiDesistir = int(arrayResult[3])
                    
                    # Coloquei -1002, pois 1 km da base pra ser considerado acerto e 2 metros de raio do avião 
                    distancia = base.distanciaEuclidiana(arrayResultNum) - 1002
                    
                    # Se ele chgar a uma distancia de 3 km e for desistir
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
    




# Criando o servidor efetivamente
servidor = Servidor()
loop = asyncio.get_event_loop()

# Inicializa o servidor com web socket 
start_server = websockets.serve(servidor.conecta, '0.0.0.0', 8766) # Usa-se 0.0.0.0 para pegar o ip do computador local

# Usa um trycatch para deixar rodando infinitamente o servidor de websocket
try:
    print("Servidor iniciado!")
    print("Esperando conexão de cliente...")
    loop.run_until_complete(start_server)
    loop.run_forever()
finally:
    start_server.close()
    
'''
ESTA SERÁ O RADAR, JÁ QUE ELE IDENTIFICARÁ O AVIÃO QUE VAI ESTAR NO CÉU E PASSA ATRAVES DE MENSAGENS A POSICAO X, Y, Z para o CLIENTE = BASE 
TRATAR
'''