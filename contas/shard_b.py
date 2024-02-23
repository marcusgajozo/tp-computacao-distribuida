import socket

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
    data, endereco = sock.recvfrom(1024)  # buffer size is 1024 bytes
    print(CREDITO, DEBITO)
    # print(f"received message: {FILA.get()}")
