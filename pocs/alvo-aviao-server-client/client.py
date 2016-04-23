# importa o essencial
from websocket import create_connection
from aviao import Aviao
import time
import threading


#Inicializa a conexão com o WebSocket
ws = create_connection("ws://192.168.0.16:8766")
aviao = Aviao(0, 0, 0)

# Cuida do retorno da conexão de abertura com o websocket
print("Iniciando...")
result = ws.recv()
print(result)
    
# Envia mensagem de conexao no servidor
print("Aguardando mensagem...")

# Função que recebe o dado que deseja ser enviado para o servidor
def recebeResposta():
    # Crio um laço infinito para enviar mensagens que envia mensagens para o servidor
    while True:
        # Aguarda o valor a ser recebido
        mensagem = ws.recv() 
        
        # caso a mensagem for "p" de pontos, ele retorna todos os pontos no formato x;y;z
        if mensagem == "p":
            print("Mensagem: {0}".format(mensagem) + "")

            posicaoAtual = str(aviao.x) + ";" + str(aviao.y) + ";" + str(aviao.z)
            ws.send(posicaoAtual) 
            print("Posicao Enviada:  " + posicaoAtual)

            print("Aguardando mensagem...\n\n")

        else:
            ws.send("1")
    
    # Quando sai do while infinito ele fecha a conexão
    ws.close()
    
    # Roda o websocket para sempre 
    ws.run_forever()

# Função atualiza a posição do avião, nela será colocada a formula S = So + Vo + t
def atualizaPosicaoAviao():
    while True:
        aviao.x += 1
        aviao.y += 2
        aviao.z += 3
        
# Para que o avião continue andando mesmo que não receba nenhuma resposta foi usado uma 
# thread, para que a posicao do aviao seja atualizada e receba a resposta ao mesmo tempo
t = threading.Thread(name='resposta', target=recebeResposta)
w = threading.Thread(name='atualizaPosicaoAviao', target=atualizaPosicaoAviao)

w.start()
t.start()