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
    win = py.display.set_mode((512,644))
    run = True

    #texture imports
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

        #recv action if awaiting turn
        if turn_flag:
            state.start()
            #this is useless now but might be useful if chat implemented
            state.join()#need to get information of move from the state
            Net.send_move(socket, None)
            turn_flag = False
            state = Waiting(win, board, queue)
        else:
            state.start()
            recv_move = Net.recv_move(socket)
            state.join()
            #call board make_move thing, idk if before or after thread close
            if color == "b":
                board.make_move(recv_move[0], recv_move[1], "w")
            else:
                board.make_move(recv_move[0], recv_move[1], "b")
            turn_flag = True
            state = Choosing(win, board, queue)




    Net.ErrorHandler().launchLog()

