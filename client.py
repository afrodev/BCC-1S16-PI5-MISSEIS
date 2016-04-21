# importa o essencial
from websocket import create_connection
import time

#Inicializa a conexão com o WebSocket
ws = create_connection("ws://172.20.10.6:8766")


# Cuida do retorno da conexão de abertura com o websocket
print("Iniciando...")
result = ws.recv()
print(result)
    
# Envia mensagem de conexao no servidor
print("Aguardando mensagem...")
# Crio um laço infinito para enviar mensagens que envia mensagens para o servidor
while True:
    mensagem = ws.recv()
    if mensagem:
        print("\nMensagem: {0}".format(mensagem) + "\n")
        print("Aguardando mensagem...")
        ws.send("0")                                            
    else:
        ws.send("1")
    
ws.close()

ws.run_forever()
