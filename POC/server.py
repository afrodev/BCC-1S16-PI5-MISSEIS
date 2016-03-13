# importando todas as bibliotecas necessárias
import asyncio # Para métodos que rodam assincronamente
import websockets # Cuida dos métodos de websocket
import time 
import shlex

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
        print("Cliente {1} desconectado. Total: {0}".format(self.nconectados, cliente.nome))     

    # De modo assincrono, envia a mensagem para todos que estão na sala.
    @asyncio.coroutine
    def envia_a_todos(self, origem, mensagem):
        print("Enviando a todos")
        for cliente in self.conectados:            
            if origem != cliente and cliente.conectado:
                print("Enviando de <{0}> para <{1}>: {2}".format(origem.nome, cliente.nome, mensagem))
                yield from cliente.envia("{0} >> {1}".format(origem.nome, mensagem))

    # De modo assincrono, envia mensagem para um destinatário específico a mensagem.
    @asyncio.coroutine
    def envia_a_destinatario(self, origem, mensagem, destinatario):        
        for cliente in self.conectados:            
            if cliente.nome == destinatario and origem != cliente and cliente.conectado:
                print("Enviando de <{0}> para <{1}>: {2}".format(origem.nome, cliente.nome, mensagem))
                yield from cliente.envia("PRIVADO de {0} >> {1}".format(origem.nome, mensagem))
                return True
        return False

    # Verifica se não existe outro nome igual ao seu, esse é o id da conversa, não pode haver outro igual
    def verifica_nome(self, nome):
        for cliente in self.conectados:
            if cliente.nome and cliente.nome == nome:
                return False
        return True

# Classe Cliente, que cuidará efetivamente
class Cliente:  
    # Inicializa a classe do websocket  
    def __init__(self, servidor, websocket, path):
        self.cliente = websocket
        self.servidor = servidor
        self.nome = None

    # Função que retorna se o cliente está conectado com o websocket
    @property
    def conectado(self):
        return self.cliente.open

    # De forma assincrona, gerencia as conexões dos usuários no websocket
    @asyncio.coroutine
    def gerencia(self):
        try:
            # De forma sequencial, envia a todos os usuários a mensagem
            yield from self.envia("Bem vindo ao servidor de chat escrito em Python 3.4 com asyncio e WebSockets. Identifique-se com /nome SeuNome")
            while True: # Enquanto a mensagem não chegar o servidor fica esperando
                mensagem = yield from self.recebe()
                if mensagem:
                    print("{0} < {1}".format(self.nome, mensagem))
                    yield from self.processa_comandos(mensagem)                                            
                else:
                    break
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

    # Processa os comandos do servidor
    # No caso temos /nome para que a pessoa tenha o id dela definido.
    @asyncio.coroutine
    def processa_comandos(self, mensagem):   
        # Caso tenha uma / no começo executa um comando de configuração do cliente no servidor     
        if mensagem.strip().startswith("/"): 
            # shlex executa uma string como se fosse um comando bash (Terminal)
            comandos = shlex.split(mensagem.strip()[1:])
            if len(comandos) == 0:
                yield from self.envia("Comando inválido")
                return
            print(comandos)
            comando = comandos[0].lower()            
            if comando == "horas":
                yield from self.envia("Hora atual: " + time.strftime("%H:%M:%S"))
            elif comando == "data":
                yield from self.envia("Data atual: " + time.strftime("%d/%m/%y"))
            elif comando == "clientes":
                yield from self.envia("{0} clientes conectados".format(self.servidor.nconectados))
            elif comando == "nome":
                yield from self.altera_nome(comandos)
            elif comando == "apenas":
                yield from self.apenas_para(comandos)
            else:
                yield from self.envia("Comando desconhecido")
        else:
            if self.nome:
                yield from self.servidor.envia_a_todos(self, mensagem)
            else:
                yield from self.envia("Identifique-se para enviar mensagens. Use o comando /nome SeuNome")

    # De forma assincrona, muda o nome configurado no servidor (id)
    @asyncio.coroutine
    def altera_nome(self, comandos):                
        if len(comandos) > 1 and self.servidor.verifica_nome(comandos[1]):
            self.nome = comandos[1]
            yield from self.envia("Nome alterado com sucesso para {0}".format(self.nome))
        else:
            yield from self.envia("Nome em uso ou inválido. Escolha um outro.")

    # De forma assincrona, manda mensagem apenas uma cliente
    @asyncio.coroutine
    def apenas_para(self, comandos):
        if len(comandos) < 3:
            yield from self.envia("Comando incorreto. /apenas Destinatário mensagem")
            return
        destinatario = comandos[1]
        mensagem = " ".join(comandos[2:])
        enviado = yield from self.servidor.envia_a_destinatario(self, mensagem, destinatario)
        if not enviado:
            yield from self.envia("Destinatário {0} não encontrado. Mensagem não enviada.".format(destinatario))



# Criando o servidor efetivamente
servidor = Servidor()
loop = asyncio.get_event_loop()

# Inicializa o servidor com web socket 
start_server = websockets.serve(servidor.conecta, '0.0.0.0', 8765) # Usa-se 0.0.0.0 para pegar o ip do computador local

# Usa um trycatch para deixar rodando infinitamente o servidor de websocket
try:
    loop.run_until_complete(start_server)
    loop.run_forever()
finally:
    start_server.close()




