import pygame as py
import sys
import src.PyObjects as po
from src.Piece import *

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
            self.arrow_start = (None, None)
            self.arrow_end = (None, None)
        #draw arrows with left click
        if py.mouse.get_pressed()[2] and self.arrow_start == (None, None):
            self.arrow_start = py.mouse.get_pos()
        if (not py.mouse.get_pressed()[2]) and self.arrow_start != (None,None):
            self.arrow_end = py.mouse.get_pos()
            self.drawables.append(po.Arrow(self.arrow_start, self.arrow_end))
            self.arrow_start = (None, None)
            self.arrow_end = (None, None)


class Choosing(State):

    def __init__(self, win, board, queue):
        super().__init__(win, board, queue)
        self.selected_flag = False
        self.selected_piece = None
        self.promotion_flag = False

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
                            original, new = self.board.make_move(self.selected_piece.coordinates, (elt.board_x,elt.board_y), self.board.player_color)
                            self.queue.put(True)#put true to signal that thread ends
                            self.queue.put((original, new))#put move information
                    # if click was outside selection squares, reset selection
                    self.drawables = []
                    self.selected_flag = False
                    # selection flag and piece get reset with assignation above
                else:
                    #find if a piece was clicked
                    try:
                        self.selected_flag, self.selected_piece, valid_moves = self.board.select_piece(py.mouse)
                    except Exception as e:
                        if e.__str__()[:17] == "Promotion selected":
                            self.promotion_flag = True
                            if e.__str__()[17:] in self.board.white_pieces.keys():
                                self.selected_piece = self.board.white_pieces[e.__str__()[17:]]
                            elif e.__str__()[17:] in self.board.black_pieces.keys():
                                self.selected_piece = self.board.black_pieces[e.__str__()[17:]]
                            self.start_promotion_menu()
                        else:
                            raise Exception("Unknown error during selection")
                    #display selection squares for piece
                    if self.selected_flag and self.board.player_color == "w":
                        for elt in valid_moves:
                            self.drawables.append(po.Square(elt, self.board.white_position(elt)))
                    elif self.selected_flag and self.board.player_color == "b":
                        for elt in valid_moves:
                            self.drawables.append(po.Square(elt, self.board.black_position(elt)))
                #for pawn promotion, we have a different selection menu
                if self.promotion_flag:
                    for elt in self.drawables:
                        if elt.is_over(py.mouse):
                            if self.selected_piece.color == "w":
                                self.board.white_pieces[self.selected_piece.coordinates] = self.create_promotion_piece(elt)
                            elif self.selected_piece.color == "b":
                                self.board.black_pieces[self.selected_piece.coordinates] = self.create_promotion_piece(elt)
                    self.drawables = []
                    self.promotion_flag = False


    def start_promotion_menu(self):
        #for pawn promotion, we have a different selection menu
        rook_select = po.Square((0,0), (192,0))
        rook_select.set_image("R", self.board.player_color)
        self.drawables.append(rook_select)
        knight_select = po.Square((0,0), (256,0))
        knight_select.set_image("H", self.board.player_color)
        self.drawables.append(knight_select)
        bishop_select = po.Square((0,0), (320,0))
        bishop_select.set_image("B", self.board.player_color)
        self.drawables.append(bishop_select)
        queen_select = po.Square((0,0), (384,0))
        queen_select.set_image("Q", self.board.player_color)
        self.drawables.append(queen_select)

    def create_promotion_piece(self, elt):
        if elt.info[0] == "R":
            return Rook(self.board.player_color, self.selected_piece.coordinates)
        elif elt.info[0] == "H":
            return Knight(self.board.player_color, self.selected_piece.coordinates)
        elif elt.info[0] == "B":
            return Bishop(self.board.player_color, self.selected_piece.coordinates)
        elif elt.info[0] == "Q":
            return Queen(self.board.player_color, self.selected_piece.coordinates)