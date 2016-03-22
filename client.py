# importa o essencial
from websocket import create_connection
import time

#Inicializa a conexão com o WebSocket
ws = create_connection("ws://0.0.0.0:8766")

# Cuida do retorno da conexão de abertura com o websocket
result = ws.recv()
print("Abertura - " + result)
    
# Envia mensagem de conexao no servidor
ws.send("Radar conectado")

def on_error(ws, error):
    print(error)

# Crio um laço infinito para enviar mensagens que envia mensagens para o servidor
while True:
    # Escreve a mensagem vinda do teclado
    mensagem = input("Digite sua mensagem: ")
    
    #Coloca o tempo na hora de enviar a mensagem e envia
    tempoEnvio = time.time()

    mensagemTotal = str(tempoEnvio) + "|" + mensagem
    
    result = "1";

    while not result == "0":
        ws.send(mensagemTotal)
    
        print("Enviando....")
    
        # Recebe o retorno e pega o tempo que demora para ele retornar
        result = ws.recv()
        
    print("Enviado!")
    
    
ws.close()


print("Saiu do for")
ws.run_forever()