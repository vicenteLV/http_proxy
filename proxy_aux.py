import socket
import json

#CTTES
BUFSIZE = 1024
SERVER_NAME = "HTTP_REDES"
HTTP_VERSION = "HTTP/1.1"

HTML403 = "./content/error403.html"


#dict for code answer pairs
cod_ans = {
    "200": "OK",
    "403": "Forbidden"
}

def file_to_txt(rt: str) -> str:
    """str -> str
    receives a route to file and gives back its content as a plain text"""
    with open(rt) as file:
        cont = file.read()

    return cont


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


def create_response(client_msg: bytes, user: str, proxy_to_server:socket.socket, forbidden: list,
                    http_version: str = HTTP_VERSION) -> bytes:
    """bytes str socket list str-> bytes
    takes msg in bytes and generates dict for information for a response with help from
    create_HTTP_message() from a given response in communication with server, 
    adds header for user
    uses forbidden list for blocking"""
    dictionary = parse_HTTP_message(client_msg)
    startline_list = dictionary["startline"].split(" ")
    q_method = startline_list[0]
    q_route = startline_list[1]
    q_version = startline_list[2]

    domain = dictionary["HEAD"]["Host"]
    code = ""   #for response

    url = q_route[7:]
    if url[-1] != "/":
        url += "/"


    for i in range(len(forbidden)):
        print(forbidden[i])
        if forbidden[i][-1] != "/":
            forbidden[i] += "/"

    if "/img/403.jpg" in url:
        try:
            with open("../img/403.jpg", "rb") as f:
                img_bytes = f.read()
            code = "200"
            img_response_dict = {}
            img_response_dict["startline"] = f"{q_version} {code} {cod_ans[code]}"

            img_response_dict["HEAD"] = {}
            img_response_dict["HEAD"]["Server"] = SERVER_NAME
            img_response_dict["HEAD"]["Date"] = obtain_date()
            img_response_dict["HEAD"]["Content-Type"] = "image/jpg"
            img_response_dict["HEAD"]["Content-Length"] = str(len(img_bytes))
            img_response_dict["HEAD"]["Connection"] = "keep-alive"

            img_response_dict["BODY"] = img_bytes

            img_response = create_HTTP_message(img_response_dict)

            return img_response

        except FileNotFoundError:
            return "Img not found"



    #error
    if url in forbidden:
        print("##### PAGINA BLOQUEADA #####")
        code = "403"
        body403 = file_to_txt(HTML403)
        len_body403 = len(body403.encode())

        #startline 
        error_response_dict = {}
        error_response_dict["startline"] = f"{q_version} {code} {cod_ans[code]}"

        #head
        error_response_dict["HEAD"] = {}
        error_response_dict["HEAD"]["Server"] = SERVER_NAME
        error_response_dict["HEAD"]["Date"] = obtain_date()
        error_response_dict["HEAD"]["Content-Type"] = "text/html; charset=utf-8"
        error_response_dict["HEAD"]["Content-Length"] = str(len_body403)
        error_response_dict["HEAD"]["Connection"] = "keep-alive"

        #body
        error_response_dict["BODY"] = body403

        error_response = create_HTTP_message(error_response_dict)

        return error_response

    else:
        code = "200"
        proxy_to_server.connect((domain, 80))
        proxy_to_server.send(client_msg)

        server_resp_bytes = proxy_to_server.recv(BUFSIZE)
        server_resp_dict = parse_HTTP_message(server_resp_bytes)

        #add header
        server_resp_dict["HEAD"]["X-ElQuePregunta"] = user
        proxy_response = create_HTTP_message(server_resp_dict) 

        return proxy_response


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

    










