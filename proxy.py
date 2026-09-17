import socket
import sys
from proxy_aux import *

#CTTES
BUFSIZE = 1024
END_OF_MSG = "\n"

conf_json_name = sys.argv[1]    #block.json
CONF_JSON = open_json(f"./json/{conf_json_name}.json")

FORBIDDEN_ADS = CONF_JSON["blocked"]

#dict for code answer pairs
cod_ans = {
    "200": "OK"
}

proxy_ip = "0.0.0.0" 

proxy_ad = (proxy_ip, 8000)

proxy_listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
proxy_listening_socket.bind(proxy_ad)

proxy_listening_socket.listen(3)
print("Esperando clientes ...")

while True:

    client_proxy_socket, client_ad = proxy_listening_socket.accept()

    client_msg = client_proxy_socket.recv(BUFSIZE)

    print(client_msg)

    #connection to server
    proxy_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    header_user = CONF_JSON["user"]
    response = create_response(client_msg, header_user, proxy_server_socket, FORBIDDEN_ADS)

    client_proxy_socket.send(response)

        

    client_proxy_socket.close()

    print(f"Conexión con {client_ad} ha sido cerrada")





