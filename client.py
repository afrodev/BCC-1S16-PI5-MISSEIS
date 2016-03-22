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

def on_error(ws, error):
    print(error)

# Crio um laço infinito para enviar mensagens que envia mensagens para o servidor
while True:
    # Escreve a mensagem vinda do teclado
    mensagem = input("Digite sua mensagem: ")
    
    #Coloca o tempo na hora de enviar a mensagem e envia
    tempoEnvio = time.time()
    tempoTotal = 0;
    intervaloLimite = 2;

    mensagemTotal = str(identityNumber) + "|" + str(tempoEnvio) + "|" + mensagem

    result = "1";

    print("Enviando....")

    while not result == "0" and tempoTotal < intervaloLimite:
        ws.send(mensagemTotal)
    
        # Recebe o retorno e pega o tempo que demora para ele retornar
        result = ws.recv()
        tempoRecebimento = time.time()
        tempoTotal = tempoRecebimento - tempoEnvio
        
    if result != "0":
        print("Falha no envio, tempo limite excedido.")
    else:
        print("Enviado!")
    
ws.close()

print("Saiu do for")
ws.run_forever()