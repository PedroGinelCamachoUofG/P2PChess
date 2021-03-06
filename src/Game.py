import sys
import threading
from queue import Queue
import src.Net as Net
from src.ErrorHandler import ErrorHandler
from src.State import *
from src.Board import Board


#functions to call the game in and out

def host():
    print("hosting game")
    game_loop("w", Net.mode_receive(3000))

def join(ip):
    print(f"joining at {ip}")
    game_loop("b", Net.mode_request(ip, 3000))

#function containing the actual game

def game_loop(color, socket):

    #pygame setup
    py.init()
    py.display.set_caption("P2PChess Game")
    win = py.display.set_mode((640,582))
    run = True

    #instantiate objects for game
    queue = Queue()
    board = Board(color)

    #instantiate communication for game closing

    #set order
    if color == "w":
        turn_flag = True
        state = Choosing(win, board, queue)
    else:
        turn_flag = False
        state = Waiting(win, board, queue)

    #pygame loop
    while run:
        py.event.pump()

        print(f"This player is: {color} pieces. Is it their turn: {turn_flag}")
        #recv action if awaiting turn
        if turn_flag:
            state.run()
            move = queue.get()
            Net.send_move(socket, move)
            #change state
            # if the is_game_over flag is True it indicates that the move ended the game
            if board.is_game_over:
                Net.end(socket)
                raise Exception("Game over")
            turn_flag = False
            state = Waiting(win, board, queue)
        else:
            listener = threading.Thread(target=Net.threading_recv_move, args=(socket,queue), daemon=True)
            listener.start()
            state.run()
            recv_move = queue.get()
            queue.task_done()
            #0 in the second move indicates we are dealing with a promotion
            if recv_move[1][0] == 0:
                if color == "b":
                    board.promote_pawn(recv_move[0], recv_move[1][1], "w")
                else:
                    board.promote_pawn(recv_move[0], recv_move[1][1], "b")
            # other wise we make the move on the board
            else:
                if color == "b":
                    board.make_move(recv_move[0], recv_move[1], "w")
                else:
                    board.make_move(recv_move[0], recv_move[1], "b")
            # if the is_game_over flag is True it indicates that the move ended the game
            if board.is_game_over:
                Net.end(socket)
                raise Exception("Game over")
            #change state
            turn_flag = True
            state = Choosing(win, board, queue)

    Net.ErrorHandler().launch_log()

