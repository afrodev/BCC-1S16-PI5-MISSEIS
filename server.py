# importando todas as bibliotecas necessárias
import asyncio # Para métodos que rodam assincronamente
import websockets # Cuida dos métodos de websocket
import time 
# import shlex

# Classe Servidor - Cuida das funções do servidor
class Servidor:
    # Inicializa a classe
    def __init__(self):
        # Inicializa o array que terá todos os conectados no websocket
        self.conectados = [] 

    # Retorna o numero de pessoas conectadas no websocket
    @property
    def nconectados(self):
        return len(self.conectados)

    # Colocando esse codigo antes, executamos a função em modo assincrono
    @asyncio.coroutine
    def conecta(self, websocket, path): 
        cliente = Cliente(self, websocket, path)
        if cliente not in self.conectados:
            self.conectados.append(cliente)
            print("Novo cliente conectado. Total: {0}".format(self.nconectados))            
        yield from cliente.gerencia() # Com o yield podemos garantir que será executado de forma sequencial, colocando em uma fila.

    # Função para desconectar o cliente que entrou no servidor.
    def desconecta(self, cliente):
        if cliente in self.conectados:
            self.conectados.remove(cliente)
        print("Radar desconectado. Total: {0}".format(self.nconectados))     

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
                mensagem = yield from self.recebe()
                if mensagem:
                    tempoEnvio = 0;
                    msgFinal = mensagem.split("|", 1);

                    if len(msgFinal) > 1:
                        tempoEnvio = msgFinal[0]
                        msgFinal = msgFinal[1]
                        
                        tempoRecebimento = time.time()
                        tempoTotal = tempoRecebimento - float(tempoEnvio)

                        print("Mensagem recebida (tempo total - {0}): {1}".format(str(tempoTotal), str(msgFinal)))
                    else:
                        print("Mensagem: {0}".format(str(msgFinal[0])))
                    print("Aguardando mensagem...")
                    yield from self.envia("0")                                            
                else:
                    yield from self.envia("1")
                    break
        except Exception:
            print("Erro")
            yield from self.envia("1")
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
        self.cliente.send("Volta da mensagem: " + mensagem)
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




