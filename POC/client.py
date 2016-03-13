# Importa todos os pacotes essenciais
import websocket
import time
import threading 

# Quando envia a mensagem
def on_message(ws, message):
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
        for i in range(30000):
            time.sleep(1)
            ws.send("/nome JEFFS")
            result =  ws.recv()

            ws.send("foi foi")
            ws.send("foi foi")
            print("Received - "+ result)

        time.sleep(1)


        ws.close()
        print("thread terminating...")

    threading.Thread(target=run())

# Inicializa a conexão com o servidor mandando a mensagem com meu nome
if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://192.168.0.15:8765",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open
    # Roda para sempre
    ws.run_forever()
