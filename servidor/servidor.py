import queue
import socket
import threading
import time
import pickle


def debito():
    while True:
        try:
            global SALDO_ATUAL
            # paga da fila os clientes com operacao de debito
            dados, endereco = FILA_DEBITO.get(block=False)
            with LOCK:
                valor = dados["valor_operacao"]
                conta_cliente = dados["conta_cliente"]
                if SALDO_ATUAL - valor > 0:
                    SALDO_ATUAL -= valor
                    dados_bytes = pickle.dumps(
                        {
                            "conta_cliente": conta_cliente,
                            "debitado": valor,
                            "saldo_atual": SALDO_ATUAL,
                        }
                    )
                    sock.sendto(dados_bytes, endereco)
                else:
                    msg = pickle.dumps(
                        {"conta_cliente": conta_cliente, "msg": "saldo insuficiente"}
                    )
                    sock.sendto(msg, endereco)

            print(f"Saldo atual: {SALDO_ATUAL}")

        except queue.Empty:
            time.sleep(30)


def credito():
    while True:
        try:
            global SALDO_ATUAL
            # paga da fila os clientes com operacao de credito
            dados, endereco = FILA_CREDITO.get(block=False)
            with LOCK:
                valor = dados["valor_operacao"]
                conta_cliente = dados["conta_cliente"]

                SALDO_ATUAL += valor
                dados_bytes = pickle.dumps(
                    {
                        "conta_cliente": conta_cliente,
                        "creditado": valor,
                        "saldo_atual": SALDO_ATUAL,
                    }
                )
                sock.sendto(dados_bytes, endereco)
            print(f"Saldo atual: {SALDO_ATUAL}")

        except queue.Empty:
            time.sleep(20)


def transaction_coordinator():
    while True:
        try:
            # paga da fila os clientes
            dados_bytes, endereco = FILA_CLIENTE.get(block=False)

            dados = pickle.loads(dados_bytes)

            # envia confirmacao de recebido
            msg = pickle.dumps(
                f"requisicao recebida do cliente {dados['conta_cliente']}"
            )
            sock.sendto(msg, endereco)

            # coloca na fila de debito
            if dados["tipo_operacao"] == "D":
                FILA_DEBITO.put((dados, endereco))

            # coloca na fila de credito
            elif dados["tipo_operacao"] == "C":
                FILA_CREDITO.put((dados, endereco))

            else:
                conta_cliente = dados["conta_cliente"]
                msg = pickle.dumps(
                    {"conta_cliente": conta_cliente, "msg": "operacao nao disponivel"}
                )
                sock.sendto(msg, endereco)

        except queue.Empty:
            time.sleep(10)


UDP_IP = ""
UDP_PORT = 5005
FILA_CLIENTE = queue.Queue()
FILA_CREDITO = queue.Queue()
FILA_DEBITO = queue.Queue()

# trava para lidar com area critica
LOCK = threading.Lock()

# saldo atual
SALDO_ATUAL = 1000

sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM,
)

sock.bind((UDP_IP, UDP_PORT))

thread_cliente = threading.Thread(target=transaction_coordinator, name="Thread 1")
thread_debito = threading.Thread(target=debito, name="Thread 1")
thread_credito = threading.Thread(target=credito, name="Thread 1")
thread_cliente.start()
thread_debito.start()
thread_credito.start()

while True:
    print("servidor iniciado")
    dados_bytes, endereco = sock.recvfrom(1024)

    # coloca na fila de clientes
    FILA_CLIENTE.put((dados_bytes, endereco))
