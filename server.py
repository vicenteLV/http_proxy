import socket
from server_aux import *

#CTTES
BUFSIZE = 1024
END_OF_MSG = "\n"

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
    response = ""

    client_socket, client_ad = server_socket.accept()

    client_msg = client_socket.recv(BUFSIZE)

    #print(f"Mensaje recibido:\n{client_msg}")

    #extract info from dict
    http_request = parse_HTTP_message(client_msg.decode())
    startline_list = http_request["startline"].split(" ")
    q_method = startline_list[0]
    q_route = startline_list[1]
    q_version = startline_list[2]
    print(f"Method: {q_method}, route: {q_route}, version http: {q_version}")

    if q_method == "GET" and q_route == "/":

        with open("./content/response.html") as file:
            cont = file.read()

        cont_bytes = cont.encode()
        len_bodyResponse = len(cont_bytes)

        #startline
        code = "200"
        code_msg = cod_ans[code]
        response_startline = q_version + code + code_msg + "\r\n"
        response += response_startline

        #head
        response += "Server: http_proxy_redes\r\n"   #Server
        response += "Date: " + obtain_date() + "\r\n"
        response += "Content-Type: text/html; charset=utf-8\r\n"
        response += "Content-Length: " + str(len_bodyResponse) + "\r\n"
        response += "Connection: keep-alive\r\n"

        reponse += "\r\n"

        #Body
        response += cont

        client_socket.send(response.encode())

        

    client_socket.close()

    print(f"Conexión con {client_ad} ha sido cerrada")





