import json
import queue
import socket
import threading
import time


def transaction_coordinator():
    while True:
        try:
            dados, endereco = FILA.get(block=False)
            dados_convertido = json.loads(dados.decode())
            for chave in list(dados_convertido.keys()):
                if chave != "tipo_operacao" and chave != "valor_operacao":
                    del dados_convertido[chave]
            dados_json = json.dumps(dados_convertido)
            sock.sendto(dados_json.encode(), SHARD_A_B)
            resposta, endereco_resultado = sock.recvfrom(1024)
            print(resposta[0])
            sock.sendto(b"OK", endereco_resultado)
            sock.sendto(b"OK", endereco)
        except queue.Empty:
            print("Fila vazia")
            time.sleep(5)


UDP_IP = "127.0.0.1"
UDP_PORT = 5005
FILA = queue.Queue()
SHARD_A_B = ("localhost", 5006)

sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM,
)
sock.bind((UDP_IP, UDP_PORT))

t = threading.Thread(target=transaction_coordinator, name="Thread 1")
t.start()
while True:
    FILA.put(sock.recvfrom(1024))
    print("Requisicao na fila")
