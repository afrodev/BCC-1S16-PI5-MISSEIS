#import logging
#logging.basicConfig(level=logging.DEBUG)
import asyncio
import websockets
import time
import shlex

class Servidor:
    def __init__(self):
        self.conectados = []
    
    @property
    def nconectados(self):
        return len(self.conectados)
    
    @asyncio.coroutine
    def conecta(self, websocket, path):
        cliente = Cliente(self, websocket, path)
        if cliente not in self.conectados:
            self.conectados.append(cliente)
            print("Novo cliente conectado. Total: {0}".format(self.nconectados))            
        yield from cliente.gerencia()

    def desconecta(self, cliente):
        if cliente in self.conectados:
            self.conectados.remove(cliente)
        print("Cliente {1} desconectado. Total: {0}".format(self.nconectados, cliente.nome))            

    @asyncio.coroutine
    def envia_a_todos(self, origem, mensagem):
        print("Enviando a todos")
        for cliente in self.conectados:            
            if origem != cliente and cliente.conectado:
                print("Enviando de <{0}> para <{1}>: {2}".format(origem.nome, cliente.nome, mensagem))
                yield from cliente.envia("{0} >> {1}".format(origem.nome, mensagem))

    @asyncio.coroutine
    def envia_a_destinatario(self, origem, mensagem, destinatario):        
        for cliente in self.conectados:            
            if cliente.nome == destinatario and origem != cliente and cliente.conectado:
                print("Enviando de <{0}> para <{1}>: {2}".format(origem.nome, cliente.nome, mensagem))
                yield from cliente.envia("PRIVADO de {0} >> {1}".format(origem.nome, mensagem))
                return True
        return False

    def verifica_nome(self, nome):
        for cliente in self.conectados:
            if cliente.nome and cliente.nome == nome:
                return False
        return True


class Cliente:    
    def __init__(self, servidor, websocket, path):
        self.cliente = websocket
        self.servidor = servidor
        self.nome = None        
    
    @property
    def conectado(self):
        return self.cliente.open

    @asyncio.coroutine
    def gerencia(self):
        try:
            yield from self.envia("Bem vindo ao servidor de chat escrito em Python 3.4 com asyncio e WebSockets. Identifique-se com /nome SeuNome")
            while True:
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

    @asyncio.coroutine
    def envia(self, mensagem):
        yield from self.cliente.send(mensagem)

    @asyncio.coroutine
    def recebe(self):
        mensagem = yield from self.cliente.recv()
        return mensagem

    @asyncio.coroutine
    def processa_comandos(self, mensagem):        
        if mensagem.strip().startswith("/"):
            comandos=shlex.split(mensagem.strip()[1:])
            if len(comandos)==0:
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

    @asyncio.coroutine
    def altera_nome(self, comandos):                
        if len(comandos)>1 and self.servidor.verifica_nome(comandos[1]):
            self.nome = comandos[1]
            yield from self.envia("Nome alterado com sucesso para {0}".format(self.nome))
        else:
            yield from self.envia("Nome em uso ou inválido. Escolha um outro.")

    @asyncio.coroutine
    def apenas_para(self, comandos):
        if len(comandos)<3:
            yield from self.envia("Comando incorreto. /apenas Destinatário mensagem")
            return
        destinatario = comandos[1]
        mensagem = " ".join(comandos[2:])
        enviado = yield from self.servidor.envia_a_destinatario(self, mensagem, destinatario)
        if not enviado:
            yield from self.envia("Destinatário {0} não encontrado. Mensagem não enviada.".format(destinatario))



servidor=Servidor()
loop=asyncio.get_event_loop()

start_server = websockets.serve(servidor.conecta, 'localhost', 8765)

try:
    loop.run_until_complete(start_server)
    loop.run_forever()
finally:
    start_server.close()