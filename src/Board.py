from src.Piece import *
import os
import pygame as py

class Board:

    def __init__(self, player_color):
        dirname = os.path.join(os.path.dirname(__file__), '..')
        """Key: position tuple Value: piece object"""
        self.white_pieces = {(0,0):Rook("w",(0,0))}
        self.dead_white_counter = 0
        self.black_pieces = {(0,0):Rook("b",(0,0))}
        self.dead_black_counter = 0
        self.image = py.image.load(os.path.join(dirname, "Textures/board1.png"))
        self.player_color = player_color

    def draw(self, win):
        win.blit(self.image, (0, 64))
        if self.player_color == "w":
            for piece in self.white_pieces.values():
                piece.draw(win, self.white_position(piece.coordinates))
            for piece in self.black_pieces.values():
                piece.draw(win, self.black_position(piece.coordinates))
        else:
            for piece in self.white_pieces.values():
                piece.draw(win, self.black_position(piece.coordinates))
            for piece in self.black_pieces.values():
                piece.draw(win, self.white_position(piece.coordinates))

    def white_position(self, coordinates):
        return coordinates[0] * 64, (coordinates[1] + 1) * 64

    def black_position(self, coordinates):
        return coordinates[0] * 64, (9 * 64) - (coordinates[1] * 64)

    def select_piece(self, coordinates):
        #code is roughly identical for each color
        #restrict selection of pieces only to the player's color
        if self.player_color == "w":
            for piece in self.white_pieces.values():
                if piece.is_over(coordinates) and piece.is_in_play:
                    #checks if pawn has piece in front and passes it
                    if piece.type == "P":
                        if (piece.coordinates[0],piece.coordinates[1]+1) in self.black_pieces.keys():
                            return True, piece, piece.valid_moves(args=True)
                        else:
                            return True, piece, piece.valid_moves(args=False)
                    #King piece must know movement options of all enemies to know where it can move
                    elif piece.type == "K":
                        enemy_moves = []
                        for elt in self.black_pieces.values():
                            enemy_moves.append(elt.valid_moves())
                        return True, piece, piece.valid_moves(args=enemy_moves)
                    else:
                        return True, piece, piece.valid_moves()
        else:
            for piece in self.black_pieces.values():
                if piece.is_over(coordinates) and piece.is_in_play:
                    if piece.type == "P":
                        if (piece.coordinates[0],piece.coordinates[1]-1) in self.white_pieces.keys():
                            return True, piece, piece.valid_moves(args=True)
                        else:
                            return True, piece, piece.valid_moves(args=False)
                    elif piece.type == "K":
                        enemy_moves = []
                        for elt in self.white_pieces.values():
                            enemy_moves.append(elt.valid_moves())
                        return True, piece, piece.valid_moves(args=enemy_moves)
                    else:
                        return True, piece, piece.valid_moves()
        return False, None, None

    def make_move(self, original, new, flag):
        #kills piece if it is the case
        self.kill_piece(original, flag)
        #moves piece
        self.move_piece(original, new, flag)
        #returns a tuple with the original and new position tuples as a tuple
        return original, new


    def kill_piece(self, pos, color):
        #color indicates the killer piece, not the killed
        if color == "b":
            if pos in self.white_pieces:
                self.white_pieces[pos].is_in_play = False
                #changes piece to the dead zone
                self.white_pieces[pos].coordinates(self.dead_white_counter / 2, -1)
                self.dead_white_counter += 1
                return True
        else:
            if pos in self.black_pieces:
                self.black_pieces[pos].is_in_play = False
                self.black_pieces[pos].coordinates(self.dead_black_counter / 2, -1)
                self.dead_black_counter += 1
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
