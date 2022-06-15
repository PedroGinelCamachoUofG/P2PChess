import pygame as py
import os

class Piece:
    def __init__(self, color, coordinates):
        self.is_in_play = True
        self.color = color
        self.type = ""
        self.coordinates = coordinates
        self.object = py.Rect(self.coordinates, (64, 64))
        self.image = None
    
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
        for num in range(0,15):
            x_coord += 1
            if self.in_board((x_coord, self.coordinates[1])):
                output.append((x_coord, self.coordinates[1]))
        y_coord = self.coordinates[1] - 8
        for num in range(0, 15):
            y_coord += 1
            if self.in_board((self.coordinates[0], y_coord)):
                output.append((self.coordinates[0], y_coord))
        return output

    def in_board(self, coordinates):
        if ((coordinates[0] > 8) or (coordinates[1] > 8) or (coordinates[0] < 1) or (coordinates[1] < 1)) or self.coordinates == coordinates:
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

    def __init__(self, color, coordinates):
        super().__init__(color, coordinates)
        self.type = "P"
        dirname = os.path.join(os.path.dirname(__file__), '..')
        if color == "w":
            self.image = py.image.load(os.path.join(dirname, "Textures/White_Pawn.png"))
        else:
            self.image = py.image.load(os.path.join(dirname, "Textures/Black_Pawn.png"))
        self.image.set_colorkey((255,255,255))
        self.image = self.image.convert_alpha()

    def __str__(self):
        return f"{self.color} Pawn at {self.coordinates}"

    """
    Pawn has several possibilities which also change with color:
    0-Nothing strange -> 1 step
    1-Starting -> 2 steps
    2-Can eat left -> sideways left
    3-Can eat right -> sideways right
    4-Can eat both
    5-Promotion -> change piece
    """
    def valid_moves(self, args=(0,)):
        if self.color == "w":
            if args[0] == 0:
                return (self.coordinates[0], self.coordinates[1]+1),
            elif args[0] == 1:
                return (self.coordinates[0], self.coordinates[1]+2),
            elif args[0] == 2:
                return (self.coordinates[0]-1, self.coordinates[1]+1),
            elif args[0] == 3:
                return (self.coordinates[0]+1, self.coordinates[1]+1),
            elif args[0] == 4:
                return (self.coordinates[0]-1, self.coordinates[1]+1), (self.coordinates[0]+1, self.coordinates[1]+1)
            else:
                print("promotion")
        else:
            if args[0] == 0:
                return (self.coordinates[0], self.coordinates[1] - 1),
            elif args[0] == 1:
                return (self.coordinates[0], self.coordinates[1] - 2),
            elif args[0] == 2:
                return (self.coordinates[0] - 1, self.coordinates[1] - 1),
            elif args[0] == 3:
                return (self.coordinates[0] + 1, self.coordinates[1] - 1),
            elif args[0] == 4:
                return (self.coordinates[0] - 1, self.coordinates[1] - 1), (self.coordinates[0] + 1, self.coordinates[1] - 1)
            else:
                print("promotion")

class Queen(Piece):
    def __init__(self, color, coordinates):
        super().__init__(color, coordinates)
        self.type = "Q"
        dirname = os.path.join(os.path.dirname(__file__), '..')
        if color == "w":
            self.image = py.image.load(os.path.join(dirname, "Textures/White_Queen.png"))
        else:
            self.image = py.image.load(os.path.join(dirname, "Textures/Black_Queen.png"))
        self.image.set_colorkey((255, 255, 255))
        self.image = self.image.convert_alpha()
    
    def valid_moves(self, args=()):
        return self.diagonals() + self.straights()

    def __str__(self):
        return f"{self.color} Queen at {self.coordinates}"

class King(Piece):
    def __init__(self, color, coordinates):
        super().__init__(color, coordinates)
        self.type = "K"
        dirname = os.path.join(os.path.dirname(__file__), '..')
        if color == "w":
            self.image = py.image.load(os.path.join(dirname, "Textures/White_King.png"))
        else:
            self.image = py.image.load(os.path.join(dirname, "Textures/Black_King.png"))
        self.image.set_colorkey((255, 255, 255))
        self.image = self.image.convert_alpha()

    def valid_moves(self, args=([],)):
        positions = [(self.coordinates[0]-1+i,self.coordinates[1]-1+j) for i in range(0,3) for j in range(0,3) if self.in_board((self.coordinates[0]-1+i,self.coordinates[1]-1+j))]

        if args[0]:
            return positions
        for elt in args[0]:
            if elt in positions:
                positions.remove(elt)
        return positions

    def __str__(self):
        return f"{self.color} King at {self.coordinates}"

class Bishop(Piece):
    def __init__(self, color, coordinates):
        super().__init__(color, coordinates)
        self.type = "B"
        dirname = os.path.join(os.path.dirname(__file__), '..')
        if color == "w":
            self.image = py.image.load(os.path.join(dirname, "Textures/White_Bishop.png"))
        else:
            self.image = py.image.load(os.path.join(dirname, "Textures/Black_Bishop.png"))
        self.image.set_colorkey((255, 255, 255))
        self.image = self.image.convert_alpha()

    def valid_moves(self, args=()):
        return self.diagonals()

    def __str__(self):
        return f"{self.color} Bishop at {self.coordinates}"

class Knight(Piece):
    def __init__(self, color, coordinates):
        super().__init__(color, coordinates)
        self.type = "H"
        dirname = os.path.join(os.path.dirname(__file__), '..')
        if color == "w":
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
            (self.coordinates[0]+2, self.coordinates[1]+1),
            (self.coordinates[0]-2, self.coordinates[1]-1),
            (self.coordinates[0]-1, self.coordinates[1]-2),
            (self.coordinates[0]+1, self.coordinates[1]-2),
            (self.coordinates[0]+2, self.coordinates[1]-1)
        ]
        return [pos for pos in positions if self.in_board(pos)]

    def __str__(self):
        return f"{self.color} Knight at {self.coordinates}"

class Rook(Piece):
    def __init__(self, color, coordinates):
        super().__init__(color, coordinates)
        self.type = "R"
        dirname = os.path.join(os.path.dirname(__file__), '..')
        if color == "w":
            self.image = py.image.load(os.path.join(dirname, "Textures/White_Rook.png"))
        else:
            self.image = py.image.load(os.path.join(dirname, "Textures/Black_Rook.png"))
        self.image.set_colorkey((255, 255, 255))
        self.image = self.image.convert_alpha()

    def valid_moves(self, args=()):
        return self.straights()

    def __str__(self):
        return f"{self.color} Rook at {self.coordinates}"