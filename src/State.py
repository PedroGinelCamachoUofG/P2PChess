import threading
import pygame as py
import sys
import src.PyObjects as po

class State(threading.Thread):

    def __init__(self, win, board, queue, args=(), kwargs=None):
        threading.Thread.__init__(self, args=(), kwargs=None)
        self.win = win
        self.board = board
        self.queue = queue
        self.drawables = []
        #self.daemon = True
        self.receive_messages = args[0]#IndexError: tuple index out of range

    def run(self):#Do I know what is going on here?
        while True:

            self.interactions()

            self.win.fill((255, 255, 255))
            for elt in self.drawables:
                elt.draw(self.win)

            if not self.queue.get():
                break

    #abstract method
    def interactions(self):
        pass

    def draw(self):
        self.win.fill((255, 255, 255))
        self.board.draw(self.win)
        for elt in self.drawables:
            elt.draw(self.win)
        py.display.update()


class Waiting(State):

    def __init__(self, win, board, queue):
        super().__init__(win, board, queue)
        self.arrow_start = (None,None)
        self.arrow_end = (None,None)

    def interactions(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
        if py.mouse.get_pressed()[0]:
            #if right click delete all arrows
            self.drawables = []
        #draw arrows with left click
        if py.mouse.get_pressed()[2]:
            self.arrow_start = py.mouse.get_pos()
        if (not py.mouse.get_pressed()[2]) and self.arrow_start != (None,None):
            self.arrow_start = py.mouse.get_pos()
            self.drawables.append(po.arrow(self.arrow_start, self.arrow_end))


class Choosing(State):

    def __init__(self, win, board, queue):
        super().__init__(win, board, queue)
        self.selected_flag = False
        self.selected_piece = None

    def interactions(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            if event.type == py.MOUSEBUTTONDOWN:
                #if clicks on a selection square call board to move piece
                if self.selected_flag:
                    for elt in self.drawables:
                        if elt.is_over(py.mouse):
                            original, new = self.board.make_move(self.selected_piece.coordinates, (elt.x,elt.y), self.board.player_color)
                            #need to send out the move info and also stop execution
                else:
                    #find if a piece was clicked
                    self.selected_flag, self.selected_piece, moves = self.board.select_piece(py.mouse.get_pos())
                    #display selection squares for piece
                    if self.selected_flag:
                        for elt in moves:
                            if self.selected_piece.type == "w":
                                self.drawables.append(po.Square(self.board.white_position(elt)[0],self.board.white_position(elt)[1]))
                            else:
                                self.drawables.append(po.Square(self.board.black_position(elt)[0],self.board.black_position(elt)[1]))
                    #if click was outside selection squares, reset selection
                    else:
                        self.drawables = []
                        #selection flag and piece get reset with assignation above