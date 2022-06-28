import socket
from src.ErrorHandler import ErrorHandler

def mode_request(srv_ip, srv_port):
    cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cli_sock.connect((srv_ip, srv_port))
        return cli_sock
    except Exception as e:
        print("Exception at mode_request")
        ErrorHandler().add_error(e.__str__())

def mode_receive(srv_port):
    srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        srv_sock.settimeout(5)#low number for testing purposes
        srv_sock.bind(("", srv_port))
        srv_sock.listen(1)
        cli_sock, cli_addr = srv_sock.accept()
        return cli_sock
    except Exception as e:
        print("Exception at mode_receive")
        ErrorHandler().add_error(str(e.__str__() + "h"))

def send_move(sock, move):
    try:
        move_fixed = (move[0][0], move[0][1], move[1][0], move[1][1])
        sock.sendall(bytes(move_fixed))
        return True
    except Exception as e:
        print("Exception at send_move")
        ErrorHandler().add_error(e.__str__())
    return False

def threading_recv_move(sock, queue):
    try:
        #the listening function will always execute in a thread
        #listens for move
        raw_move = tuple(sock.recv(1024))
        move = ((raw_move[0], raw_move[1]), (raw_move[2], raw_move[3]))
        #when it receives a move it puts it in the queue to stop state function
        queue.put(True)
        #puts the moved in the queue
        queue.put(move)
    except Exception as e:
        #if it errors, since it is in a thread I can't call error handler
        #this is because pygame is not thread friendly, so it crashes pygame
        #so we pass it in the queue and check for it in the main thread
        queue.put(e.__str__())

def end(sock):
    try:
        sock.close()
    except Exception as e:
        print("Exception at end")
        ErrorHandler().add_error(e.__str__())