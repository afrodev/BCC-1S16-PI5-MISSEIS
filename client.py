# importa o essencial
from websocket import create_connection
import time

#Inicializa a conexão com o WebSocket
ws = create_connection("ws://0.0.0.0:8766")

# Cuida do retorno da conexão de abertura com o websocket
resultParc = ws.recv()

result = resultParc.split("|", 1)

identityNumber = int(result[1])

print("Iniciando - " + str(result[0]))
    
# Envia mensagem de conexao no servidor
ws.send("Radar {0} conectado".format(identityNumber))
print("Aguardando mensagem...")
# Crio um laço infinito para enviar mensagens que envia mensagens para o servidor
while True:
    mensagem = ws.recv()
    if mensagem:
        print("Mensagem: {0}".format(mensagem))
        print("Aguardando mensagem...")
        ws.send("0")                                            
    else:
        ws.send("1")
    
ws.close()

ws.run_forever()