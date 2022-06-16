import threading
from queue import Queue
import src.Net as Net
from src.State import *
from src.Board import Board


#functions to call the game in and out

def host():
    print("hosting game")
    game_loop("w", Net.mode_recieve(3000))

def join(ip):
    print(f"joining at {ip}")
    game_loop("b", Net.mode_request(ip, 3000))

#helper function needed to do threading

def threading_recv_move(socket, queue):
    print("executing")
    #listens for move
    recv_move = Net.recv_move(socket)
    #when it receives a move it puts it in the queue to stop state function
    queue.put(True)
    #puts the moved in the queue
    queue.put(recv_move)

#function containing the actual game

def game_loop(color, socket):
    print("Game loop started")

    #pygame setup
    py.init()
    py.display.set_caption("P2PChess Game")
    win = py.display.set_mode((640,582))
    run = True

    #instantiate objects
    queue = Queue()
    board = Board(color)
    
    #set order
    if color == "w":
        turn_flag = True
        state = Choosing(win, board, queue)
    else:
        turn_flag = False
        state = Waiting(win, board, queue)

    #pygame loop
    while run:

        print(f"This player is: {color} pieces. Is it their turn: {turn_flag}")
        #recv action if awaiting turn
        if turn_flag:
            state.run()
            move = queue.get()
            Net.send_move(socket, move)
            #change state
            turn_flag = False
            state = Waiting(win, board, queue)
        else:
            listener = threading.Thread(target=threading_recv_move, args=(socket,queue), daemon=True)
            listener.start()
            state.run()
            recv_move = queue.get()
            queue.task_done()
            #pass a true into queue to tell thread to stop execution
            print(f"Move received{recv_move}")
            #call board make_move thing, idk if before or after thread close
            if color == "b":
                board.make_move(recv_move[0], recv_move[1], "w")
            else:
                board.make_move(recv_move[0], recv_move[1], "b")
            #change state
            turn_flag = True
            state = Choosing(win, board, queue)

    Net.ErrorHandler().launch_log()

