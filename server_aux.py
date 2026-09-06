
def parse_HTTP_message(http_message: bytes) -> dict:
    """bytes -> dict
    receives http message on bytes format and extracts HEAD (startline + headers) + BODY"""
    http_dict = {}
    http_plain = http_message.decode()

    head_body = http_plain.split("\r\n\r\n") #body and head separation on a linked list
    head_split = head_body[0].split("\r\n")  #startline + headers

    http_dict["startline"] = head_split[0]   #string
    http_dict["headers"] = head_split[1:]    #list(str)
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










