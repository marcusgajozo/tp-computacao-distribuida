import socket
import json

UDP_IP = "127.0.0.1"
UDP_PORT = 5006
DEBITO = 1000
CREDITO = 1000

sock = socket.socket(
    socket.AF_INET,  # Internet
    socket.SOCK_DGRAM,
)  # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    dados, endereco = sock.recvfrom(1024)
    if not dados:
        print("Nenhum dado recebido")
        continue

    try:
        dados_convertidos = json.loads(dados.decode())
        if dados_convertidos["tipo_operacao"] == "C":
            CREDITO += dados_convertidos["valor_operacao"]
        elif dados_convertidos["tipo_operacao"] == "D":
            DEBITO -= dados_convertidos["valor_operacao"]
        print("DEBITO:", DEBITO, "CREDITO:", CREDITO)

        # Envio de confirmação
        sock.sendto(b"OK", endereco)
        print("Confirmação enviada para", endereco)
    except json.decoder.JSONDecodeError as e:
        print("Erro ao decodificar JSON:", e)
        continue
