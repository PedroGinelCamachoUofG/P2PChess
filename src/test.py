import unittest

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

    def diagonals(self, allies, enemies):
        output = []
        for value in range(0,3):
            if value == 0:
                array = (8,8,-1,-1)
            elif value == 1:
                array = (-8,8,1,-1)
            elif value == 2:
                array = (8,-8,-1,1)
            else:
                array = (-8,-8,1,1)
            x_coord,y_coord = self.coordinates[0]-8, self.coordinates[1]-8
            for num in range(0,16):
                x_coord += 1
                y_coord += 1
                if self.in_board((x_coord,y_coord)) and (x_coord != self.coordinates[0] and y_coord != self.coordinates[1]):
                    output.append((x_coord,y_coord))
                elif (x_coord,y_coord) in allies:
                    break
                elif (x_coord,y_coord) in enemies:
                    output.append((x_coord, y_coord))
                    break
        
        x_coord,y_coord = self.coordinates[0]-8, self.coordinates[1]+8
        for num in range(0,16):
            x_coord += 1
            y_coord -= 1
            if self.in_board((x_coord,y_coord)) and (x_coord != self.coordinates[0] and y_coord != self.coordinates[1]):
                output.append((x_coord,y_coord))
            elif (x_coord, y_coord) in allies:
                break
            elif (x_coord, y_coord) in enemies:
                output.append((x_coord, y_coord))
                break
        x_coord,y_coord = self.coordinates[0]+8, self.coordinates[1]+8
        for num in range(0,16):
            x_coord -= 1
            y_coord -= 1
            if self.in_board((x_coord,y_coord)) and (x_coord != self.coordinates[0] and y_coord != self.coordinates[1]):
                output.append((x_coord,y_coord))
            elif (x_coord, y_coord) in allies:
                break
            elif (x_coord, y_coord) in enemies:
                output.append((x_coord, y_coord))
                break
        x_coord,y_coord = self.coordinates[0]+8, self.coordinates[1]-8
        for num in range(0,16):
            x_coord -= 1
            y_coord += 1
            if self.in_board((x_coord,y_coord)) and (x_coord != self.coordinates[0] and y_coord != self.coordinates[1]):
                output.append((x_coord,y_coord))
            elif (x_coord, y_coord) in allies:
                break
            elif (x_coord, y_coord) in enemies:
                output.append((x_coord, y_coord))
                break
        return output

    def straights(self, allies, enemies):
        output = []
        x_coord = self.coordinates[0]-8
        for num in range(0,15):
            x_coord += 1
            if self.in_board((x_coord, self.coordinates[1])):
                output.append((x_coord, self.coordinates[1]))
            elif (x_coord,self.coordinates[1]) in allies:
                break
            elif (x_coord,self.coordinates[1]) in enemies:
                output.append((x_coord, self.coordinates[1]))
                break
        y_coord = self.coordinates[1] - 8
        for num in range(0, 15):
            y_coord += 1
            if self.in_board((self.coordinates[0], y_coord)):
                output.append((self.coordinates[0], y_coord))
            elif (x_coord,self.coordinates[1]) in allies:
                break
            elif (x_coord,self.coordinates[1]) in enemies:
                output.append((x_coord, self.coordinates[1]))
                break
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

class tests(unittest.TestCase){

}