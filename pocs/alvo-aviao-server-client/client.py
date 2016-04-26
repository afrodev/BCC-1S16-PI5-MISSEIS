# importa o essencial
from websocket import create_connection
# from aviao import Aviao
import time
import threading
from bala import Bala 

# O cliente vai ser apenas pra base
# Ele que vai fazer o calculo para acertar o alvo
ws = create_connection("ws://172.16.1.169:8766")
bala = Bala(0, 0, 0)

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
        mensagem = ws.recv() # Aqui é recebido x, y e o z do avião que será calculado mais pra frente

        # Caso a mensagem for igual a c, calcula o x, y, z do avião e retorna
        if mensagem == "c":
            print("Mensagem: {0}".format(mensagem) + "")
            
            # Separa os dados vindos do websocket x, y, z  
            arrayResult = mensagem.split(";")
                    
            # Aqui estão as coordenadas do avião
            #arrayResultNum = [arrayResult[0]), float(arrayResult[1]), float(arrayResult[2])]

            ws.send("info1;info2") # aqui eu retorno a angulação da bala e os dados de onde ele atirou
        else:
            ws.send("1")

    # Quando sai do while infinito ele fecha a conexão
    ws.close()
    
    # Roda o websocket para sempre 
    ws.run_forever()

# Para que o avião continue andando mesmo que não receba nenhuma resposta foi usado uma 
# thread, para que a posicao do aviao seja atualizada e receba a resposta ao mesmo tempo
t = threading.Thread(name='resposta', target=recebeResposta)
t.start()

#--------------------------------------------------------------------------------------
'''


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
    jaDesistiu = 0

    # Crio um laço infinito para enviar mensagens que envia mensagens para o servidor
    while True:
        # Aguarda o valor a ser recebido
        mensagem = ws.recv() 
        
        # caso a mensagem for "p" de pontos, ele retorna todos os pontos no formato x;y;z
        if mensagem == "p":
            print("Mensagem: {0}".format(mensagem) + "")

            posicaoAtual = str(aviao.x) + ";" + str(aviao.y) + ";" + str(aviao.z) +  ";" + str(aviao.desiste)
            
            ws.send(posicaoAtual) 
            print("Posicao Enviada:  " + posicaoAtual)
            print("Desiste:  " + str(aviao.desiste))

            print("Aguardando mensagem...\n\n")
        
        elif mensagem == "a":
            # volta para uma altitude de 1200 m e velocidade de 750km/h ou 208,333 m/s
            if jaDesistiu == 0:
                aviao.z = 1200
                aviao.velocidade = 208.333

                posicaoAtual = str(aviao.x) + ";" + str(aviao.y) + ";" + str(aviao.z) +  ";" + str(aviao.desiste)
                ws.send(posicaoAtual)
                jaDesistiu = 1
                
        elif mensagem == "d": # destruiu a base
            print("-------------BASE DESTRUIDA---------------")
            ws.close()

            
        else:
            ws.send("1")
    
    # Quando sai do while infinito ele fecha a conexão
    ws.close()
    
    # Roda o websocket para sempre 
    ws.run_forever()

# Função atualiza a posição do avião, nela será colocada a formula S = So + Vo + t
# Intervalo com sleep de 1 seg, se está tudo em metros, seria 1 m/s
def atualizaPosicaoAviao():
    while True:
        aviao.x += 1
        aviao.y += 2
        aviao.z += 3
        time.sleep(1)

        
        
# Para que o avião continue andando mesmo que não receba nenhuma resposta foi usado uma 
# thread, para que a posicao do aviao seja atualizada e receba a resposta ao mesmo tempo
t = threading.Thread(name='resposta', target=recebeResposta)
w = threading.Thread(name='atualizaPosicaoAviao', target=atualizaPosicaoAviao)

w.start()
t.start()


'''
