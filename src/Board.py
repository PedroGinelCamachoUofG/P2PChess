from src.Piece import *
import os
import pygame as py

class Board:

    def __init__(self, player_color):
        dirname = os.path.join(os.path.dirname(__file__), '..')
        """Key: position tuple Value: piece object"""
        self.white_pieces = {(1,1):Rook("w",(1,1)), (2,1):Knight("w",(2,1)), (3,1):Bishop("w",(3,1)), (4,1):Queen("w",(4,1)), (5,1):King("w",(5,1)), (6,1):Bishop("w",(6,1)), (7,1):Knight("w",(7,1)), (8,1):Rook("w",(8,1)), (1,2):Pawn("w",(1,2)), (2,2):Pawn("w",(2,2)), (3,2):Pawn("w",(3,2)), (4,2):Pawn("w",(4,2)), (5,2):Pawn("w",(5,2)), (6,2):Pawn("w",(6,2)), (7,2):Pawn("w",(7,2)), (8,2):Pawn("w",(8,2))}
        self.dead_white_counter = 0
        self.black_pieces = {(1,8):Rook("b",(1,8)), (2,8):Knight("b",(2,8)), (3,8):Bishop("b",(3,8)), (4,8):Queen("b",(4,8)), (5,8):King("b",(5,8)), (6,8):Bishop("b",(6,8)), (7,8):Knight("b",(7,8)), (8,8):Rook("b",(8,8)), (1,7):Pawn("b",(1,7)), (2,7):Pawn("b",(2,7)), (3,7):Pawn("b",(3,7)), (4,7):Pawn("b",(4,7)), (5,7):Pawn("b",(5,7)), (6,7):Pawn("b",(6,7)), (7,7):Pawn("b",(7,7)), (8,7):Pawn("b",(8,7))}
        self.dead_black_counter = 0
        self.dead_pieces = []
        if player_color == "w":
            self.image = py.image.load(os.path.join(dirname, "Textures/board1.png"))
        else:
            self.image = py.transform.rotate(py.image.load(os.path.join(dirname, "Textures/board1.png")), 180)
        self.player_color = player_color
        self.update_collision_box_pos()

    def update_collision_box_pos(self):
        if self.player_color == "w":
            for piece in self.white_pieces.values():
                piece.object = py.Rect(self.white_position(piece.coordinates), (64, 64))
            for piece in self.black_pieces.values():
                piece.object = py.Rect(self.white_position(piece.coordinates), (64, 64))
        else:
            for piece in self.white_pieces.values():
                piece.object = py.Rect(self.black_position(piece.coordinates), (64, 64))
            for piece in self.black_pieces.values():
                piece.object = py.Rect(self.black_position(piece.coordinates), (64, 64))
        for dead_piece in self.dead_pieces[::-1]:
            dead_piece.object = py.Rect((-1,-1), (1,1))

    def draw(self, win):
        win.blit(self.image, (64, 58))
        if self.player_color == "w":
            for piece in self.white_pieces.values():
                piece.object = py.Rect(self.white_position(piece.coordinates), (64, 64))
                piece.draw(win, self.white_position(piece.coordinates))
            for piece in self.black_pieces.values():
                piece.draw(win, self.white_position(piece.coordinates))
        else:
            for piece in self.white_pieces.values():
                piece.draw(win, self.black_position(piece.coordinates))
            for piece in self.black_pieces.values():
                piece.draw(win, self.black_position(piece.coordinates))
        for dead_piece in self.dead_pieces[::-1]:
            dead_piece.draw(win, self.white_position(dead_piece.coordinates))

    def white_position(self, coordinates):
        return coordinates[0] * 64, (9 * 64) - (coordinates[1] * 64)

    def black_position(self, coordinates):
        return (9 * 64) - (coordinates[0] * 64), coordinates[1] * 64

    def select_pawn(self, piece):
        if piece.coordinates[1] == 2 or piece.coordinates[1] == 7:
            return True, piece, piece.valid_moves(args=(1,))
        if piece.color == "w":
            if (piece.coordinates[0] - 1, piece.coordinates[1] + 1) in self.black_pieces.keys() and (piece.coordinates[0] + 1, piece.coordinates[1] + 1) in self.black_pieces.keys():
                return True, piece, piece.valid_moves(args=(4,))
            elif (piece.coordinates[0] - 1, piece.coordinates[1] + 1) in self.black_pieces.keys():
                return True, piece, piece.valid_moves(args=(2,))
            elif (piece.coordinates[0] + 1, piece.coordinates[1] + 1) in self.black_pieces.keys():
                return True, piece, piece.valid_moves(args=(3,))
        else:
            if (piece.coordinates[0] - 1, piece.coordinates[1] - 1) in self.white_pieces.keys() and (piece.coordinates[0] + 1, piece.coordinates[1] - 1) in self.white_pieces.keys():
                return True, piece, piece.valid_moves(args=(4,))
            elif (piece.coordinates[0] - 1, piece.coordinates[1] - 1) in self.white_pieces.keys():
                return True, piece, piece.valid_moves(args=(2,))
            elif (piece.coordinates[0] + 1, piece.coordinates[1] - 1) in self.white_pieces.keys():
                return True, piece, piece.valid_moves(args=(3,))
        return True, piece, piece.valid_moves(args=(0,))

    def select_piece(self, coordinates):
        #code is pretty much duplicated but I'm not sure how to not do this
        #restrict selection of pieces only to the player's color
        if self.player_color == "w":
            for piece in self.white_pieces.values():
                if piece.is_over(coordinates) and piece.is_in_play:
                    print(piece)
                    #checks if pawn has piece in front and passes it
                    if piece.type == "P":
                        return self.select_pawn(piece)
                    #King piece must know movement options of all enemies to know where it can move
                    elif piece.type == "K":
                        enemy_moves = []
                        for elt in self.black_pieces.values():
                            enemy_moves.append(elt.valid_moves(args=(self.black_pieces.keys(), self.white_pieces.keys())))
                        return True, piece, piece.valid_moves(args=(enemy_moves,))
                    else:
                        return True, piece, piece.valid_moves(args=(self.white_pieces.keys(), self.black_pieces.keys()))
        else:
            for piece in self.black_pieces.values():
                if piece.is_over(coordinates) and piece.is_in_play:
                    print(piece)
                    if piece.type == "P":
                        return self.select_pawn(piece)
                    elif piece.type == "K":
                        enemy_moves = []
                        for elt in self.white_pieces.values():
                            enemy_moves.append(elt.valid_moves(args=(self.black_pieces.keys(), self.white_pieces.keys())))
                        return True, piece, piece.valid_moves(args=(enemy_moves,))
                    else:
                        return True, piece, piece.valid_moves(args=(self.black_pieces.keys(), self.white_pieces.keys()))
        return False, None, None

    def make_move(self, original, new, flag):
        #kills piece if it is the case
        self.kill_piece(original, flag)
        #moves piece
        self.move_piece(original, new, flag)
        #returns a tuple with the original and new position tuples as a tuple
        self.update_collision_box_pos()
        return original, new


    def kill_piece(self, pos, color):
        #color indicates the killer piece, not the killed
        if color == "b":
            if pos in self.white_pieces:
                self.white_pieces[pos].is_in_play = False
                #changes piece to the dead zone
                self.white_pieces[pos].coordinates = (0, self.dead_white_counter/2 + 1)
                self.dead_white_counter += 1
                self.dead_pieces.append(self.white_pieces[pos])
                self.white_pieces.pop(pos)
                return True
        else:
            if pos in self.black_pieces:
                self.black_pieces[pos].is_in_play = False
                self.black_pieces[pos].coordinates = (9, self.dead_black_counter/2 + 1)
                self.dead_black_counter += 1
                self.dead_pieces.append(self.black_pieces[pos])
                self.black_pieces.pop(pos)
            return True
        return False

    def move_piece(self, original, new, flag):
        #if piece is in play changes its coordinates and dictionary entry
        if flag == "w" and self.white_pieces[original].is_in_play:
            self.white_pieces[original].coordinates = new
            self.white_pieces[new] = self.white_pieces[original]
        elif self.black_pieces[original].is_in_play:
            self.black_pieces[original].coordinates = new
            self.black_pieces[new] = self.black_pieces[original]
        else:
            raise Exception("Invalid move")
