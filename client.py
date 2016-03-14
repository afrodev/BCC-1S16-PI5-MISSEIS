# importa o essencial
from websocket import create_connection
import time

#Inicializa a conexão com o WebSocket
ws = create_connection("ws://0.0.0.0:8766")

# Cuida do retorno da conexão de abertura com o websocket
result = ws.recv()
print("ABERTURA - " + result)

# Cria um id para ser controlado pelo servidor e cuida do retorno do websocket
ws.send("/nome CLIENTE1")
result = ws.recv()
print("ID - " + result)

# Crio um laço infinito para enviar mensagens que envia mensagens para o servidor
while True:
    # Escreve a mensagem vinda do teclado
    mensagem = input("Digite sua mensagem: ")
    
    #Coloca o tempo na hora de enviar a mensagem e envia
    tempoEnvio = time.time() 
    ws.send(mensagem)
    
    print("ENVIADO")
    print("RECEBENDO RETORNO")
    
    # Recebe o retorno e pega o tempo que demora para ele retornar
    result = ws.recv()
    tempoRecebimento = time.time()
    print("RECEBIDO - " + result)
    
    # Calcula o tempo total
    print("Envio: " + str(tempoEnvio))
    print("Recebimento: " + str(tempoRecebimento))
    print("Tempo total: " + str(tempoRecebimento - tempoEnvio))
    
ws.close()


print("Saiu do for")

'''
# Importa todos os pacotes essenciais
import websocket
import time
import threading 

# Quando envia a mensagem
def on_message(ws, message):
    print("ON MESSAGE")
    print(message)

# Quando da um erro
def on_error(ws, error):
    print(error)

# Quando fecha a conexão
def on_close(ws):
    print("### closed ###")

# Quando a conexão com websocket abre
def on_open(ws):
    def run(*args):
        ws.send("/nome JEFFS")

        for i in range(30000):
            ws.send(input("Digite a mensagem:  "))
            #time.sleep(1)
            
        
        time.sleep(1)
        
        ws.close()
        print("thread terminating...")

    threading.Thread(target=run())

# Inicializa a conexão com o servidor mandando a mensagem com meu nome
if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://192.168.0.15:8766",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open
    ws.on_message = on_message
    
    # Roda para sempre
    ws.run_forever()
'''
