import pygame as py

class Piece:
    def __init__(self, colour, coordinates, image):
        self.is_in_play = True
        self.colour = colour
        self.type = ""
        self.coordinates = coordinates
        self.image = image
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

    def valid_moves(self, args=False):
        if args[0]:
            return ((self.coordinates-1+(i*2), self.coordinates[1]+1) for i in range(0,1) if 0 < self.coordinates-1+(i*2) < 9)
        else:
            return ((self.coordinates-1+i, self.coordinates[1]+1) for i in range(0,2) if 0 < self.coordinates-1+i < 9)

    def __init__(self, colour, coordinates, image):
        super().__init__(colour, coordinates, image)
        self.type = "P"

class Queen(Piece):
    def __init__(self, colour, coordinates, image):
        super().__init__(colour, coordinates, image)
        self.type = "Q"
    
    def valid_moves(self, args=()):
        positions = []
        positions.append(self.diagonals())
        positions.append(self.straights())
        return positions

class King(Piece):
    def __init__(self, colour, coordinates, image):
        super().__init__(colour, coordinates, image)
        self.type = "K"

    def valid_moves(self, args=[]):
        positions = [(self.coordinates[0]-1+i,self.coordinates[1]-1+j) for i in range(0,2) for j in range(0,2) if self.in_board((self.coordinates[0]-1+i,self.coordinates[1]-1+j))]
        for elt in args[0]:
            if elt in positions:
                positions.remove(elt)
        return positions

class Bishop(Piece):
    def __init__(self, colour, coordinates, image):
        super().__init__(colour, coordinates, image)
        self.type = "B"

    def valid_moves(self, args=()):
        return self.diagonals()

class Knight(Piece):
    def __init__(self, colour, coordinates, image):
        super().__init__(colour, coordinates, image)
        self.type = "H"

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
    def __init__(self, colour, coordinates, image):
        super().__init__(colour, coordinates, image)
        self.type = "R"

    def valid_moves(self, args=()):
        return self.straights()