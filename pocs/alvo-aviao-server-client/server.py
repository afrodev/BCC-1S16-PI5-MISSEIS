# importando todas as bibliotecas necessárias
import asyncio # Para métodos que rodam assincronamente
import websockets # Cuida dos métodos de websocket
import time 
# import shlex

# Classe Servidor - Cuida das funções do servidor
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
                mensagem = input("Digite sua mensagem: ")
                
                #Coloca o tempo na hora de enviar a mensagem e envia
                tempoEnvio = time.time()
                tempoTotal = 0;
                intervaloLimite = 2;

                mensagemTotal = mensagem
                result = "1";

                print("\nEnviando....")

                while not result == "0" and tempoTotal < intervaloLimite:
                    yield from self.envia(mensagemTotal)
                
                    # Recebe o retorno e pega o tempo que demora para ele retornar
                    result = yield from self.recebe()

                    tempoRecebimento = time.time()
                    tempoTotal = tempoRecebimento - tempoEnvio
                    
                if result != "0":
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
    