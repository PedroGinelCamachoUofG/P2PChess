import pygame as py
import os

class Piece:
    def __init__(self, colour, coordinates):
        self.is_in_play = True
        self.colour = colour
        self.type = ""
        self.coordinates = coordinates
        self.object = py.Rect(self.coordinates, (64, 64))
    
    def move(self, coords):
        if coords in self.valid_moves():
            self.coordinates = coords

    def valid_moves(self, args=()):
        pass

    def diagonals(self):
        output = []
        x_coord,y_coord = self.coordinates[0]-8, self.coordinates[1]-8
        for num in range(0,16):
            x_coord += 1
            y_coord += 1
            if self.in_board((x_coord,y_coord)) and (x_coord != self.coordinates[0] and y_coord != self.coordinates[1]):
                output.append((x_coord,y_coord))
        x_coord,y_coord = self.coordinates[0]-8, self.coordinates[1]+8
        for num in range(0,16):
            x_coord += 1
            y_coord -= 1
            if self.in_board((x_coord,y_coord)) and (x_coord != self.coordinates[0] and y_coord != self.coordinates[1]):
                output.append((x_coord,y_coord))
        return output

    def straights(self):
        output = []
        x_coord = self.coordinates[0]-8
        for num in range(0,16):
            x_coord += 1
            if self.in_board((x_coord, self.coordinates[1])):
                output.append((x_coord, self.coordinates[1]))
        y_coord = self.coordinates[1] - 8
        for num in range(0, 16):
            y_coord += 1
            if self.in_board((self.coordinates[0], y_coord)):
                output.append((self.coordinates[0], y_coord))
        return output

    def in_board(self, coordinates):
        if ((coordinates[0] > 9) or (coordinates[1] > 9) or (coordinates[0] < 0) or (coordinates[1] < 0)) or self.coordinates == coordinates:
            return False
        else:
            return True

    def is_over(self, pointer):
        if self.object.collidepoint(pointer.get_pos()):
            return True
        return False

    def draw(self, win, coordinates):
        win.blit(self.image, coordinates)


class Pawn(Piece):

    def __init__(self, colour, coordinates):
        super().__init__(colour, coordinates)
        self.type = "P"
        dirname = os.path.join(os.path.dirname(__file__), '..')
        if colour == "w":
            self.image = py.image.load(os.path.join(dirname, "Textures/White_Pawn.png"))
        else:
            self.image = py.image.load(os.path.join(dirname, "Textures/Black_Pawn.png"))
        self.image.set_colorkey((255,255,255))
        self.image = self.image.convert_alpha()

    def valid_moves(self, args=False):
        if args[0]:
            return ((self.coordinates-1+(i*2), self.coordinates[1]+1) for i in range(0,1) if 0 < self.coordinates-1+(i*2) < 9)
        else:
            return ((self.coordinates-1+i, self.coordinates[1]+1) for i in range(0,2) if 0 < self.coordinates-1+i < 9)



class Queen(Piece):
    def __init__(self, colour, coordinates, image):
        super().__init__(colour, coordinates, image)
        self.type = "Q"
        dirname = os.path.join(os.path.dirname(__file__), '..')
        if colour == "w":
            self.image = py.image.load(os.path.join(dirname, "Textures/White_Queen.png"))
        else:
            self.image = py.image.load(os.path.join(dirname, "Textures/Black_Queen.png"))
        self.image.set_colorkey((255, 255, 255))
        self.image = self.image.convert_alpha()
    
    def valid_moves(self, args=()):
        positions = []
        positions.append(self.diagonals())
        positions.append(self.straights())
        return positions

class King(Piece):
    def __init__(self, colour, coordinates):
        super().__init__(colour, coordinates)
        self.type = "K"
        dirname = os.path.join(os.path.dirname(__file__), '..')
        if colour == "w":
            self.image = py.image.load(os.path.join(dirname, "Textures/White_King.png"))
        else:
            self.image = py.image.load(os.path.join(dirname, "Textures/Black_King.png"))
        self.image.set_colorkey((255, 255, 255))
        self.image = self.image.convert_alpha()

    def valid_moves(self, args=[]):
        positions = [(self.coordinates[0]-1+i,self.coordinates[1]-1+j) for i in range(0,2) for j in range(0,2) if self.in_board((self.coordinates[0]-1+i,self.coordinates[1]-1+j))]
        for elt in args[0]:
            if elt in positions:
                positions.remove(elt)
        return positions

class Bishop(Piece):
    def __init__(self, colour, coordinates):
        super().__init__(colour, coordinates)
        self.type = "B"
        dirname = os.path.join(os.path.dirname(__file__), '..')
        if colour == "w":
            self.image = py.image.load(os.path.join(dirname, "Textures/White_Bishop.png"))
        else:
            self.image = py.image.load(os.path.join(dirname, "Textures/Black_Bishop.png"))
        self.image.set_colorkey((255, 255, 255))
        self.image = self.image.convert_alpha()

    def valid_moves(self, args=()):
        return self.diagonals()

class Knight(Piece):
    def __init__(self, colour, coordinates):
        super().__init__(colour, coordinates)
        self.type = "H"
        dirname = os.path.join(os.path.dirname(__file__), '..')
        if colour == "w":
            self.image = py.image.load(os.path.join(dirname, "Textures/White_Knight.png"))
        else:
            self.image = py.image.load(os.path.join(dirname, "Textures/Black_Knight.png"))
        self.image.set_colorkey((255, 255, 255))
        self.image = self.image.convert_alpha()

    def valid_moves(self, args=()):
        #doing it by hand
        positions = [
            (self.coordinates[0]-2, self.coordinates[1]+1),
            (self.coordinates[0]-1, self.coordinates[1]+2),
            (self.coordinates[0]+1, self.coordinates[1]+2),
            (self.coordinates[0]+2, self.coordinates[1])+1,
            (self.coordinates[0]-2, self.coordinates[1]-1),
            (self.coordinates[0]-1, self.coordinates[1]-2),
            (self.coordinates[0]+1, self.coordinates[1]-2),
            (self.coordinates[0]+2, self.coordinates[1]-1)
        ]
        return [positions for pos in positions if self.in_board(pos)]

class Rook(Piece):
    def __init__(self, colour, coordinates):
        super().__init__(colour, coordinates)
        self.type = "R"
        dirname = os.path.join(os.path.dirname(__file__), '..')
        if colour == "w":
            self.image = py.image.load(os.path.join(dirname, "Textures/White_Rook.png"))
        else:
            self.image = py.image.load(os.path.join(dirname, "Textures/Black_Rook.png"))
        self.image.set_colorkey((255, 255, 255))
        self.image = self.image.convert_alpha()

    def valid_moves(self, args=()):
        return self.straights()