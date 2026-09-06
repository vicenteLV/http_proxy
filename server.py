import socket
from server_aux import *

BUFSIZE = 1024
END_OF_MSG = "\n"

server_address = "192.168.100.137"

server_ad = (server_address, 8000)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_ad)

server_socket.listen(3)
print("Esperando clientes ...")

while True:
    client_socket, client_ad = server_socket.accept()

    client_msg = client_socket.recv(BUFSIZE)

    print(f"Mensaje recibido:\n{client_msg.decode()}")

    msg_respuesta = "Mensaje recibido" + END_OF_MSG
    client_socket.send(msg_respuesta.encode())

    client_socket.close()

    print(f"Conexión con {client_ad} ha sido cerrada")





