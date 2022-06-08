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

#function containing the actual game

def game_loop(color, socket):

    #pygame setup
    py.init()
    py.display.set_caption("P2PChess Game")
    win = py.display.set_mode((600,600))
    run = True

    #texture imports
    #instantiate objects

    queue = Queue()
    board = Board()
    
    #set order
    if color == "w":
        turn_flag = True
        state = Choosing(win, board, queue)
    else:
        turn_flag = False
        state = Waiting(win, board, queue)
        
    #pygame loop
    while run:

        #recv action if awaiting turn
        if turn_flag:
            state.start()
            #this is useless now but might be useful if chat implemented
            Net.send_move(socket, None)#send the move when this is implemented
            state.join()
            turn_flag = False
            state = Waiting(win, board, queue)
        else:
            state.start()
            recv_move = Net.recv_move(socket)
            state.join()
            #change board state accordingly eg
            board.make_move(recv_move)
            turn_flag = True
            state = Choosing(win, board, queue)




    Net.ErrorHandler().launchLog()

