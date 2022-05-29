import socket
from src.ErrorHandler import ErrorHandler

class Error(Exception):
    pass

def mode_request(srv_ip, srv_port):
    cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cli_sock.connect((srv_ip, srv_port))
        return cli_sock
    except Exception as e:
        print(e)
        ErrorHandler().addError(e)

def mode_recieve(srv_port):
    srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        srv_sock.settimeout(1)#low number for testing purposes
        srv_sock.bind(("", srv_port))
        srv_sock.listen(1)
        cli_sock, cli_addr = srv_sock.accept()
        return cli_sock
    except Exception as e:
        ErrorHandler().addError(str(e.__str__()+"h"))

def send_move(sock, move):
    try:
        sock.sendall(move)
        return True
    except Exception as e:
        print(e)
        ErrorHandler().addError(e)
    return False

def recv_move(sock):
    try:
        move = sock.recv(1024)
        return move
    except Exception as e:
        print(e)
        ErrorHandler().addError(e)

def end(sock):
    try:
        sock.close()
    except Exception as e:
        print(e)
        ErrorHandler().addError(e)