import pygame as py
import threading
from queue import Queue
import src.Net as Net
from src.State import *


#functions to call the game in and out

def host():
    print("hosting game")
    game_loop("w", Net.mode_recieve(3000))

def join(ip):
    print(f"joining at {ip}")
    game_loop("b", Net.mode_request(ip, 3000))

#function containing the actual game
'''
=================================================================|
       TO DO LIST FOR THE GAME LOOP
STUFF TO CONSIDER:
   -which way will the board be facing, the same for both players?
   -exclude enemy pieces from interactibles?
   -how tf does texture import work when working in a function
   -make menu into a function preferably
   -get albertico to give you something,
    think about the pygame necessities of the objects
    include everything in the board draw,
   -Podria usar threads o algo para tener al bucle de juego parado
    y mientras hacer otras cosas como mover el timer o un chat??????

STUFF TO DO NOT TO THINK ABOUT:
    -get the textures for stuff on internet
    (learn to search for this sort of things)
    -test the Net functions
    -make some designs to find some proper background color ffs
    -timer, and display for it


'''
def game_loop(color, socket):

    #pygame setup
    py.init()
    py.display.set_caption("P2PChess Game")
    win = py.display.set_mode((600,600))
    run = True

    #texture imports
    #instantiate objects

    queue = Queue()
    board = None
    #FALTA QUE ALBERTICO ME DE LOS OBJETOS
    drawables = []
    
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
            state.join()
            Net.send_move(socket, None)#send the move when this is implemented
            turn_flag = False
            state = Waiting(win, board, queue)
        else:
            state.start()
            recv_move = Net.recv_move(socket)
            state.join()
            #change board state accordingly eg
            board.makeMove(recv_move)
            turn_flag = True
            state = Choosing(win, board, queue)




    Net.ErrorHandler().launchLog()

