import socket

BUFSIZE = 1024


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

    for i in range(len(http_struct["headers"])):
        http_msg += f"{http_struct["headers"][i]}\r\n"

    http_msg += "\r\n" #double \r\n after final header

    http_msg += http_struct["BODY"]

    return http_msg.encode()


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


if __name__ == "__main__":
    print(obtain_date())

    










