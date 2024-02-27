import socket
import pickle
import datetime
import random


UDP_IP = "192.168.185.193"
UDP_PORT = 5005

print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)

sock = socket.socket(
    socket.AF_INET,  # Internet
    socket.SOCK_DGRAM,
)  # UDP


for i in range(20):
    dados_bytes = pickle.dumps(
        {
            "data_operacao": datetime.datetime.now(),
            "conta_cliente": f"00{i}",
            "tipo_operacao": random.choice(["C", "D"]),
            "valor_operacao": random.randint(100, 500),
        }
    )
    sock.sendto(dados_bytes, (UDP_IP, UDP_PORT))


for i in range(20):
    data, endereco = sock.recvfrom(1024)
    print(f"recebido: {pickle.loads(data)}")
    data, endereco = sock.recvfrom(1024)
    print(f"resultado: {pickle.loads(data)}")
