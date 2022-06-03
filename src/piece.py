def checkNumber(coordinates):
    if (coordinates[0] > 9) or (coordinates[1] > 9) or (coordinates[0] < 0) or (coordinates[1] < 0):
        return False
    else:
        return True

class Piece:
    def __init__(self, colour, coordinates):
        self.is_in_play = True
        self.colour = colour
        self.coordinates = coordinates
    
    def move(self, input_coordinates):
        pass

    def whereMove(self, initial_coordinates):
        pass

    def diagonal(coordinates):
        output = []
        copy = coordinates
        for num in range(0,9):
            coordinates[0] = coordinates[0] + 1
            coordinates[1] = coordinates[1] + 1
            if checkNumber(coordinates):
                output.append(coordinates)
            else:
                break
        for num in range(0,9):
            coordinates[0] = coordinates[0] - 1
            coordinates[1] = coordinates[1] - 1
            if checkNumber(coordinates):
                output.append(coordinates)
            else:
                break
        return output

    def straight(coordinates):
        pass

class Pawn(Piece):
    def __init__(self, colour, coordinates):
        super().__init__(colour, coordinates)
        self.type = "P"
    
    def whereMove(self, coordinates):
        positions = []
        coordinates[0] = coordinates[0] + 1
        if checkNumber(coordinates):
            positions.append(coordinates)
        return positions
            


class Queen(Piece):
    def __init__(self, colour, coordinates):
        super().__init__(colour, coordinates)
        self.type = "Q"
    
    def whereMove(self, coordinates):
        positions = []
        positions.append(Piece.diagonal(coordinates))
        return positions

class King(Piece):
    def __init__(self, colour, coordinates):
        super().__init__(colour, coordinates)
        self.type = "K"
    pass

class Bishop(Piece):
    def __init__(self, colour, coordinates):
        super().__init__(colour, coordinates)
        self.type = "B"
    pass

class Knight(Piece):
    def __init__(self, colour, coordinates):
        super().__init__(colour, coordinates)
        self.type = "H"
    pass

class Rook(Piece):
    def __init__(self, colour, coordinates):
        super().__init__(colour, coordinates)
        self.type = "R"
    pass

x = Pawn("b", [1,1])

print (x.whereMove(x.coordinates))


y = Queen("b", [2,1])

print (y.whereMove(y.coordinates))
print("")

z = Piece("b", [3,5])

print(z.diagonal(z.coordinates))




