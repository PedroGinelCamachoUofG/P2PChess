import pygame as py
import sys
import src.PyObjects as po

class State:

    def __init__(self, win, board, queue):
        self.win = win
        self.board = board
        self.queue = queue
        self.drawables = []

    def run(self):
        while True:

            self.interactions()

            self.draw()

            if not self.queue.empty():
                end_flag = self.queue.get()
                self.queue.task_done()
                # if a move is being passed too(choosing state) mark as done so join doesn't block
                if not self.queue.empty():
                    self.queue.task_done()
                if end_flag:
                    break  # end thread


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
            self.drawables.append(po.Arrow(self.arrow_start, self.arrow_end))


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
                            #move piece and get the change as a tuple
                            original, new = self.board.make_move(self.selected_piece.coordinates, (elt.x,elt.y), self.board.player_color)
                            self.queue.put(True)#put true to signal that thread ends
                            self.queue.put((original, new))#put move information
                else:
                    #find if a piece was clicked
                    self.selected_flag, self.selected_piece, valid_moves = self.board.select_piece(py.mouse)
                    #display selection squares for piece
                    if self.selected_flag:
                        for elt in valid_moves:
                            if self.selected_piece.type == "w":
                                self.drawables.append(po.Square(self.board.white_position(elt)[0],self.board.white_position(elt)[1]))
                            else:
                                self.drawables.append(po.Square(self.board.black_position(elt)[0],self.board.black_position(elt)[1]))
                    #if click was outside selection squares, reset selection
                    else:
                        self.drawables = []
                        #selection flag and piece get reset with assignation above