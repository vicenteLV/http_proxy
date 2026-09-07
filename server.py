import socket
import sys
from server_aux import *

#CTTES
BUFSIZE = 1024
END_OF_MSG = "\n"

conf_json_name = sys.argv[1]    #block.json
CONF_JSON = open_json(f"./json/{conf_json_name}.json")

#dict for code answer pairs
cod_ans = {
    "200": "OK"
}

server_address = "0.0.0.0" 

server_ad = (server_address, 8000)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_ad)

server_socket.listen(3)
print("Esperando clientes ...")

while True:

    client_socket, client_ad = server_socket.accept()

    client_msg = client_socket.recv(BUFSIZE)

    #print(f"Mensaje recibido:\n{client_msg}")

    #extract info from dict
    http_request = parse_HTTP_message(client_msg)
    startline_list = http_request["startline"].split(" ")
    q_method = startline_list[0]
    q_route = startline_list[1]
    q_version = startline_list[2]
    print(f"Method: {q_method}, route: {q_route}, version http: {q_version}")

    header_user = CONF_JSON["user"]
    response = create_response(q_method, q_route, header_user)

    client_socket.send(response.encode())

        

    client_socket.close()

    print(f"Conexión con {client_ad} ha sido cerrada")





