from src.Piece import *
import os
import pygame as py
from src.PyObjects import FakePointer

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
        self.is_game_over = False

    #pygame display and logic functions

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
        if self.player_color == "w":
            for dead_piece in self.dead_pieces[::-1]:
                dead_piece.draw(win, self.white_position(dead_piece.coordinates))
        elif self.player_color == "b":
            for dead_piece in self.dead_pieces[::-1]:
                dead_piece.draw(win, self.white_position(dead_piece.coordinates))

    #important helper functions

    def white_position(self, coordinates):
        return coordinates[0] * 64, (9 - coordinates[1]) * 64

    def black_position(self, coordinates):
        return (9 - coordinates[0]) * 64, coordinates[1] * 64

    #victory functions

    def is_check_mate(self):
        #go through all pieces and select them
        white_loss =  True
        black_loss = True
        own_color = self.player_color
        self.player_color = "w"
        for piece_pos in self.white_pieces.keys():
            #this will return True at [0] if there are valid moves, ie is not check mate
            #because of how select piece works we need to fake the position of the mouse
            if own_color == "w":
                fake_mouse = FakePointer(self.white_position(piece_pos))
            elif own_color == "b":
                fake_mouse = FakePointer(self.black_position(piece_pos))
            else:
                raise Exception("piece is not white or black at Board.is_check_mate")
            try:
                if self.select_piece(fake_mouse)[0]:
                    self.player_color = own_color
                    white_loss = False
                    break
            except Exception as e:
                if e.__str__()[:9] == "Promotion":
                    pass
                else:
                    raise e
        self.player_color = "b"
        for piece_pos in self.black_pieces.keys():
            if own_color == "w":
                fake_mouse = FakePointer(self.white_position(piece_pos))
            elif own_color == "b":
                fake_mouse = FakePointer(self.black_position(piece_pos))
            else:
                raise Exception("piece is not white or black at Board.is_check_mate")
            try:
                if self.select_piece(fake_mouse)[0]:
                    self.player_color = own_color
                    black_loss = False
                    break
            except Exception as e:
                if e.__str__()[:9] == "Promotion":
                    pass
                else:
                    raise e
        if white_loss or black_loss:
            self.player_color = own_color
            self.is_game_over = True
            raise Exception("Game over")

    def creates_check(self, original, new, color_flag):
        #initialise with colors
        if color_flag == "w":
            allies = self.white_pieces.copy()
            enemies = self.black_pieces.copy()
        elif color_flag == "b":
            allies = self.black_pieces.copy()
            enemies = self.white_pieces.copy()
        else:
            raise Exception("piece is not white or black at Board.creates_check")
        #find the king piece
        king = None
        for elt in allies.values():
            if elt.type == "K":
                king = elt
        if king is None:
            raise Exception(f"Could not find {color_flag} king at Board.creates_check")

        #fake the move
        allies[new] = allies[original]
        allies.pop(original)
        allies[new].coordinates = new
        #fake the death of aa piece if any would be killed by the move
        if new in enemies.keys():
            enemies.pop(new)
        # check if it put the king in check
        for enemy in enemies.values():
            if king.coordinates in enemy.valid_moves(args=(enemies, allies)):
                #this reset stopped it from crashing but shouldn't be needed in theory
                allies[original] = allies[new]
                allies.pop(new)
                allies[original].coordinates = original
                return True
        allies[original] = allies[new]
        allies.pop(new)
        allies[original].coordinates = original
        return False

    #piece selection functions

    def select_piece(self, pointer):
        #code is pretty much duplicated but I'm not sure how to not do this
        #restrict selection of pieces only to the player's color
        valid_moves = []
        selected_piece = None
        if self.player_color == "w":
            for piece in self.white_pieces.values():
                if piece.is_over(pointer) and piece.is_in_play:
                    #checks if pawn has piece in front and passes it
                    if piece.type == "P":
                        selected_piece, valid_moves = self.select_pawn(piece, self.white_pieces.keys(), self.black_pieces.keys())
                    #King piece must know movement options of all enemies to know where it can move
                    elif piece.type == "K":
                        blocked_moves = [pos for pos in self.white_pieces.keys()]
                        valid_moves = piece.valid_moves(args=(blocked_moves,))
                        selected_piece = piece
                        self.can_castle("w")

                    else:
                        valid_moves =  piece.valid_moves(args=(self.white_pieces.keys(), self.black_pieces.keys()))
                        selected_piece = piece
                    break
        elif self.player_color == "b":
            for piece in self.black_pieces.values():
                if piece.is_over(pointer) and piece.is_in_play:
                    if piece.type == "P":
                        selected_piece, valid_moves = self.select_pawn(piece, self.black_pieces.keys(), self.white_pieces.keys())
                    elif piece.type == "K":
                        blocked_moves = [pos for pos in self.black_pieces.keys()]
                        valid_moves =  piece.valid_moves(args=(blocked_moves,))
                        selected_piece = piece
                        self.can_castle("b")
                    else:
                        valid_moves =  piece.valid_moves(args=(self.black_pieces.keys(), self.white_pieces.keys()))
                        selected_piece = piece
                    break
        else:
            raise Exception("Player was not white or black at Board.select_piece")
        filtered_moves = []
        for move in valid_moves:
            if not self.creates_check(selected_piece.coordinates, move, selected_piece.color):
               filtered_moves.append(move)
        if filtered_moves:
            return True, selected_piece, filtered_moves
        else:
            return False, selected_piece, filtered_moves

    def select_pawn(self, piece, allies, enemies):
        if piece.coordinates[1] == 8 and piece.color == "w":
            raise Exception(f"Promotion selected at {piece.coordinates}")
        elif piece.coordinates[1] == 1 and piece.color == "b":
            raise Exception(f"Promotion selected at {piece.coordinates}")
        return piece, piece.valid_moves(args=(allies, enemies))

    #piece movement functions

    def make_move(self, original, new, color_flag):
        #kills piece if it is the case
        self.kill_piece(new, color_flag)
        #moves piece
        self.move_piece(original, new, color_flag)
        #returns a tuple with the original and new position tuples as a tuple
        self.update_collision_box_pos()
        return original, new


    def kill_piece(self, pos, color):
        #color indicates the killer piece, not the killed
        if color == "b":
            if pos in self.white_pieces:
                if self.white_pieces[pos].type == "K":
                    self.is_game_over = True
                self.white_pieces[pos].is_in_play = False
                #changes piece to the dead zone
                self.white_pieces[pos].coordinates = (0, self.dead_white_counter/2 + 1)
                self.dead_white_counter += 1
                self.dead_pieces.append(self.white_pieces[pos])
                self.white_pieces.pop(pos)
            return True
        elif color == "w":
            if pos in self.black_pieces:
                if self.black_pieces[pos].type == "K":
                    self.is_game_over = True
                self.black_pieces[pos].is_in_play = False
                self.black_pieces[pos].coordinates = (9, self.dead_black_counter/2 + 1)
                self.dead_black_counter += 1
                self.dead_pieces.append(self.black_pieces[pos])
                self.black_pieces.pop(pos)
            return True
        return False

    def move_piece(self, original, new, flag):
        #if piece is in play changes its coordinates and dictionary entry
        self.check_en_passant(original, new, flag)
        if flag == "w" and new not in self.white_pieces.keys():
            self.white_pieces[original].coordinates = new
            self.white_pieces[new] = self.white_pieces[original]
            self.white_pieces.pop(original)
            if self.white_pieces[new].type == "K" or self.white_pieces[new].type == "R":
                self.white_pieces[new].has_moved = True
        elif flag == "b" and new not in self.black_pieces.keys():
            self.black_pieces[original].coordinates = new
            self.black_pieces[new] = self.black_pieces[original]
            self.black_pieces.pop(original)
            if self.black_pieces[new].type == "K" or self.black_pieces[new].type == "R":
                self.black_pieces[new].has_moved = True
        else:
            raise Exception("Invalid move at Board.make_move")

    #special rules functions (en passant, promotion, castling)

    def check_en_passant(self, original, new, flag):
        if flag == "w":
            piece = self.white_pieces[original]
            if piece.type == "P" and new == (piece.coordinates[0], piece.coordinates[1] + 2):
                if (piece.coordinates[0], piece.coordinates[1] + 1) in self.black_pieces:
                    self.kill_piece((piece.coordinates[0], piece.coordinates[1] + 1), "w")
        elif flag == "b":
            piece = self.black_pieces[original]
            if piece.type == "P" and new == (piece.coordinates[0], piece.coordinates[1] - 2):
                if (piece.coordinates[0], piece.coordinates[1] - 1) in self.white_pieces:
                    self.kill_piece((piece.coordinates[0], piece.coordinates[1] - 1), "b")

    def promote_pawn(self, pawn_location, promote_to, color):
        if color == "w":
            self.white_pieces[pawn_location] = self.create_promotion_piece(pawn_location, promote_to, "w")
            print(self.white_pieces[pawn_location])
        elif color == "b":
            self.black_pieces[pawn_location] = self.create_promotion_piece(pawn_location, promote_to, "b")
            print(self.black_pieces[pawn_location])

    def create_promotion_piece(self, pawn_location, promote_to, color):
        if promote_to == 1:
            return Rook(color, pawn_location)
        elif promote_to == 2:
            return Knight(color, pawn_location)
        elif promote_to == 3:
            return Bishop(color, pawn_location)
        elif promote_to == 4:
            return Queen(color, pawn_location)

    def can_castle(self, color_flag):
        #find pertinent pieces
        king = None
        rook_1 = None
        rook_2 = None
        rook_marker = 0
        if color_flag == "w":
            for piece in self.white_pieces.values():
                if piece.type == "K":
                    king = piece
                elif piece.type == "R":
                    if piece.coordinates[0] == 1:
                        rook_1 = piece
                    elif piece.coordinates[0] == 8:
                        rook_2 = piece
        elif color_flag == "b":
            for piece in self.black_pieces.values():
                if piece.type == "K":
                    king = piece
                elif piece.type == "R":
                    if piece.coordinates[0] == 1:
                        rook_1 = piece
                    elif piece.coordinates[0] == 8:
                        rook_2 = piece
        else:
            raise Exception("Player was not white or black at Board.castling")
        #first condition: neither king or rook have been moved
        if not king.has_moved:
            if rook_1.has_moved:
                rook_1 = None
            if rook_2.has_moved:
                rook_2 = None
            if not rook_1 and not rook_2:
                return False
        else:
            return False
        if rook_1:
            self.castle_left(king, rook_1, color_flag)
        #second condition: no pieces in between of any color
        #third condition: none of the squares are in check

    def castle_left(self, king, left_rook, color_flag):
        pass

    def castle_right(self, king, right_rook, color_flag):
        pass

