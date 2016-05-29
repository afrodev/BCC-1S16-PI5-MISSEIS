# importa o essencial
from websocket import create_connection
# from aviao import Aviao
import time
import threading
from bala import Bala 
import math

# O cliente vai ser apenas pra base
# Ele que vai fazer o calculo para acertar o alvo
ws = create_connection("ws://127.0.0.1:9768")


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

        # Separa os dados vindos do websocket x, y, z  
        arrayResult = mensagem.split(";")

        x = float(arrayResult[0])
        y = float(arrayResult[1])
        z = float(arrayResult[2])
        vx = float(arrayResult[3])
        vy = float(arrayResult[4])
        tempoEnvio = float(arrayResult[5])
        

        xFuturo = x + 125 * vx
        yFuturo = y + 125 * vy
        print("\nPosX = " + str(xFuturo) + " PosY = " + str(yFuturo))

        distX = 5000 - xFuturo
        distY = 5000 - yFuturo

        distFutura = math.sqrt(distX * distX + distY * distY)

        vTiro = 1175
        gravidade = 9.8

        angulo = 0
        angulo1 = math.atan(((vTiro ** 2) - math.sqrt((vTiro ** 4) - gravidade * (gravidade * (distFutura * distFutura) + 2 * z * (vTiro * vTiro)))) / (gravidade * distFutura))
        angulo2 = math.atan(((vTiro ** 2) + math.sqrt((vTiro ** 4) - gravidade * (gravidade * (distFutura * distFutura) + 2 * z * (vTiro * vTiro)))) / (gravidade * distFutura))

        if angulo1 < angulo2:
            angulo = angulo1
        else:
            angulo = angulo2

        print("angulo = " + str(angulo))

        anguloAzimute = math.atan(distY / distX)
        if x < 5000:
            anguloAzimute -= math.pi

        if anguloAzimute < 0:
            anguloAzimute += 2 * math.pi

        print("anguloAzimute = " + str(anguloAzimute))


        vPlano = vTiro * math.cos(angulo)

        vxTiro = vPlano * math.cos(anguloAzimute)
        vyTiro = vPlano * math.sin(anguloAzimute)

        vzTiro = vTiro * math.sin(angulo)


        tempoVooTiro = distFutura / vPlano

        vAviao = math.sqrt(vx * vx + vy * vy)
        vAviao *= (1/0.025)

        distAbatimentoX = xFuturo - x
        distAbatimentoY = yFuturo - y
        distAbatimento = math.sqrt(distAbatimentoX ** 2 + distAbatimentoY ** 2)

        tempoVooAviao = distAbatimento / vAviao

        delay = tempoVooAviao - tempoVooTiro

        print("Delay = " + str(delay))

        print("Tempo de voo do tiro = " + str(tempoVooTiro))

        tempoEnvio = time.time()

        strRetorna = str(anguloAzimute) + ";" + str(angulo) + ";" + str(delay) + ";" + str(tempoEnvio) + ";" + str(tempoVooTiro)

        ws.send(strRetorna) # aqui eu retorno a angulação da bala e os dados de onde ele atirou

    # Quando sai do while infinito ele fecha a conexão
    ws.close()
    
    # Roda o websocket para sempre 
    ws.run_forever()

# Para que o avião continue andando mesmo que não receba nenhuma resposta foi usado uma 
# thread, para que a posicao do aviao seja atualizada e receba a resposta ao mesmo tempo
t = threading.Thread(name='resposta', target=recebeResposta)
t.start()
