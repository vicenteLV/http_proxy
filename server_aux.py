import socket
import json

#CTTES
BUFSIZE = 1024
SERVER_NAME = "HTTP_REDES"
HTTP_VERSION = "HTTP/1.1"


#dict for code answer pairs
cod_ans = {
    "200": "OK"
}


def parse_HTTP_message(http_message: bytes) -> dict:
    """bytes -> dict
    receives http message on bytes format and extracts HEAD (startline + headers) + BODY"""
    http_dict = {}
    http_plain = http_message.decode()

    head_body = http_plain.split("\r\n\r\n") #body and head separation on a linked list
    head_split = head_body[0].split("\r\n")  #startline + headers

    http_dict["startline"] = head_split[0]   #string

    http_dict["HEAD"] = {}                   #dict for headers
    head_len = len(head_split) - 1  
       
    for i in range(1, head_len):
        header_split = head_split[i].split(": ")
        http_dict["HEAD"][header_split[0]] = header_split[1]


    http_dict["BODY"] = head_body[1]         #string

    return http_dict


def create_HTTP_message(http_struct: dict) -> bytes:
    """dict -> bytes
    takes a dict with message info, builds the http message and returns it encoded"""
    http_msg = ""

    http_msg += f"{http_struct["startline"]}\r\n"

    for header, description in http_struct["HEAD"].items():
        http_msg += f"{header}: {description}\r\n"


    http_msg += "\r\n" #double \r\n after final header

    http_msg += http_struct["BODY"]

    return http_msg.encode()


def create_response(method: str, route: str, user: str, code: str = "200",
                    http_version: str = HTTP_VERSION) -> bytes:
    """str str str str str-> bytes
    takes method and route and it generates a response with help from
    create_HTTP_message() depending on the response code number, adds header for user"""
    resp_dict = {}    #dict for http message formating
    rt = "." + route

    if method == "GET":
        if rt == "./":
            with open(f"{rt}content/main.html") as file:
                cont = file.read()

            cont_bytes = cont.encode()
            len_bodyResponse = len(cont_bytes)

            #startline
            resp_dict["startline"] = f"{http_version} {code} {cod_ans[code]}"

            #head
            resp_dict["HEAD"] = {}
            resp_dict["HEAD"]["Server"] = SERVER_NAME
            resp_dict["HEAD"]["Date"] = obtain_date()
            resp_dict["HEAD"]["Content-Type"] = "text/html; charset=utf-8"
            resp_dict["HEAD"]["Content-Length"] = str(len_bodyResponse)
            resp_dict["HEAD"]["Connection"] = "keep-alive"

            #additional header

            resp_dict["HEAD"]["X-ElQuePregunta"] = user

            #body
            resp_dict["BODY"] = cont

            response = create_HTTP_message(resp_dict)

            return response


def obtain_date(url: str = "cc4303.bachmann.cl") -> str:
    """str -> str
    method for obtaining current date extracting it from an http response from a domain 
    default url: cc4303.bachmann.cl"""

    date_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    date_socket.connect((url, 80))

    msg = "GET / HTTP/1.1\r\nHost: cc4303.bachmann.cl\r\nUser-Agent: curl/8.5.0\r\nAccept: */*\r\n\r\n"
    date_socket.send(msg.encode())

    received = date_socket.recv(BUFSIZE)
    received_decoded = parse_HTTP_message(received)

    date_socket.close()

    return received_decoded["HEAD"]["Date"]


def open_json(route: str) -> dict:
    with open(route) as file:
        data_dict = json.load(file)

    return data_dict



if __name__ == "__main__":
    print(obtain_date())

    










