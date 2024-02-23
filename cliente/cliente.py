import socket
import json

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)

sock = socket.socket(
    socket.AF_INET,  # Internet
    socket.SOCK_DGRAM,
)  # UDP

data_operacao = input("data: ")
conta_cliente = input("conta: ")
tipo_operacao = input("tipo de operacao: ")
valor_operacao = int(input("valor: "))

dados_json = json.dumps(
    {
        "data_operacao": data_operacao,
        "conta_cliente": conta_cliente,
        "tipo_operacao": tipo_operacao,
        "valor_operacao": valor_operacao,
    }
)

sock.sendto(dados_json.encode(), (UDP_IP, UDP_PORT))
data, endereco = sock.recvfrom(1024)
print(f"Recebido: {data}")
