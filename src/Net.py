import socket
from src.ErrorHandler import ErrorHandler

def mode_request(srv_ip, srv_port):
    cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cli_sock.connect((srv_ip, srv_port))
        return cli_sock
    except Exception as e:
        ErrorHandler().add_error(e.__str__())

def mode_recieve(srv_port):
    srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        srv_sock.settimeout(5)#low number for testing purposes
        srv_sock.bind(("", srv_port))
        srv_sock.listen(1)
        cli_sock, cli_addr = srv_sock.accept()
        return cli_sock
    except Exception as e:
        ErrorHandler().add_error(str(e.__str__() + "h"))

def send_move(sock, move):
    try:
        move_fixed = (move[0][0], move[0][1], move[1][0], move[1][1])
        sock.sendall(bytes(move_fixed))
        return True
    except Exception as e:
        ErrorHandler().add_error(e.__str__())
    return False

def recv_move(sock):
    print("Listening for moves")
    try:
        raw_move = tuple(sock.recv(1024))
        move = ((raw_move[0],raw_move[1]), (raw_move[2], raw_move[3]))
        print(move)
        return move
    except Exception as e:
        ErrorHandler().add_error(e.__str__())

def end(sock):
    try:
        sock.close()
    except Exception as e:
        ErrorHandler().add_error(e.__str__())