import os

import pygame as py
import math

#classes for interactives
class Button:
    def __init__(self, static_image, hover_image, x, y):
        self.currentImage = static_image
        self.staticImage = static_image
        self.hoverImage = hover_image
        self.x = x
        self.y = y
        self.wid = self.currentImage.get_width()
        self.hei = self.currentImage.get_height()
        self.object = py.Rect(self.x, self.y, self.wid, self.hei)
        self.actions = [] #functions mus take no args currently

    def draw(self, win):
        win.blit(self.currentImage, (self.x, self.y))

    def is_over(self, pointer):
        if self.object.collidepoint(pointer.get_pos()):
            self.currentImage = self.hoverImage
            return True
        self.currentImage = self.staticImage
        return False

    def exe_all(self):
        for func in self.actions:
            func()

class InputBox:
    """
    Code for giving the input box textures has been commented out
    """
    def __init__(self, x, y, wid, hei, font):
        self.x = x
        self.y = y
        self.wid = wid
        self.hei = hei
        self.text = Text(self.x, self.y, "127.0.0.1", font)
        self.object = py.Rect((self.x, self.y), (self.wid, self.hei))
        self.active = False


        # self.currentImage = staticImage
        # self.staticImage = staticImage
        # self.hoverImage = hoverImage
        #self.wid = self.currentImage.get_width()
        #self.hei = self.currentImage.get_height()
        #self.active = False


    def write(self, char):
        if len(self.text.text) < 35:
            self.text.add_text(char)

    def delete(self):
        self.text.change_text(self.text.text[:-1])

    def is_over(self, pointer):
        if self.object.collidepoint(pointer.get_pos()):
            return True
        return False

    def select(self):
        self.active = True

    def unselect(self):
        self.active = False

    def draw(self, win):
        py.draw.rect(win, py.Color(255, 255, 255), self.object)
        self.text.draw(win)
        #win.blit(self.currentImage, (self.x, self.y))

class Text:

    def __init__(self, x, y, text, font):
        self.text = text
        self.x = x
        self.y = y
        self.font = font
        self.object = self.font.render(self.text, True, (0, 0, 0))

    def change_text(self, text):
        self.text = text

    def add_text(self,char):
        self.text += char

    def draw(self, win):
        self.object = self.font.render(self.text, True, (0,0,0))
        win.blit(self.object, (self.x, self.y))

class Arrow:

    def __init__(self, start, end):
        self.point = end
        self.length = int(math.sqrt(((start[0]-end[0])**2)+((start[1]-end[1])**2)))
        self.direction = [(end[0] - start[0]), (end[1] - start[1])]
        #make direction unitary
            #this to avoid division by 0 if the line is parallel
        if self.direction[0] == 0 or self.direction[1] == 0:
            self.direction[0] = 1
            self.direction[1] = 1
        self.direction = (self.direction[0]/math.sqrt((self.direction[0]**2)+(self.direction[1]**2)),
                          self.direction[1]/math.sqrt((self.direction[0]**2)+(self.direction[1]**2)))
        self.tangent = (-self.direction[1], self.direction[0])
        """points:    c\ 
        a-------------b  \point
        f-------------e  /
                      d/
        """
        self.a = (start[0]+(self.tangent[0]*5), start[1]+(self.tangent[1]*5))
        self.f = (start[0]-(self.tangent[0] * 5), start[1]-(self.tangent[1] * 5))
        self.b = (self.a[0]+(self.direction[0]*(self.length-10))), (self.a[1]+(self.direction[1]*(self.length-10)))
        self.e = (self.f[0]+(self.direction[0]*(self.length-10))), (self.f[1]+(self.direction[1]*(self.length-10)))
        self.c = (self.b[0]+self.tangent[0]*5, self.b[1]+self.tangent[1]*5)
        self.d = (self.e[0]-self.tangent[0]*5, self.e[1]-self.tangent[1]*5)

    def draw(self, win):
        py.draw.polygon(win, (255,0,0), [self.a, self.b, self.c, self.point, self.d, self.e, self.f])

class Square:

     def __init__(self, board_pos, real_pos):
         self.board_x = board_pos[0]
         self.board_y = board_pos[1]
         self.x = real_pos[0]
         self.y = real_pos[1]
         self.object = py.Rect((self.x, self.y), (64, 64))
         self.image = None
         self.info = []

     def is_over(self, pointer):
         if self.x < pointer.get_pos()[0] < self.x+64 and self.y < pointer.get_pos()[1] < self.y+64:
             return True
         return False

     def draw(self, win):
         py.draw.rect(win, (255,0,0), self.object, width=1)

    #this is for making the promotion selection squares
     def set_image(self, piece_type, piece_color):
         self.info.append(piece_type)
         self.info.append(piece_color)
         dirname = os.path.join(os.path.dirname(__file__), '..')
         if piece_color == "w":
             if piece_type == "R":
                 self.image = py.image.load(os.path.join(dirname, "Textures/White_Rook.png"))
             elif piece_type == "B":
                 self.image = py.image.load(os.path.join(dirname, "Textures/White_Bishop.png"))
             elif piece_type == "H":
                 self.image = py.image.load(os.path.join(dirname, "Textures/White_Knight.png"))
             elif piece_type == "Q":
                 self.image = py.image.load(os.path.join(dirname, "Textures/White_Queen.png"))
             else:
                 raise Exception("invalid piece selection")
         elif piece_color == "b":
             if piece_type == "R":
                 self.image = py.image.load(os.path.join(dirname, "Textures/Black_Rook.png"))
             elif piece_type == "B":
                 self.image = py.image.load(os.path.join(dirname, "Textures/Black_Bishop.png"))
             elif piece_type == "H":
                 self.image = py.image.load(os.path.join(dirname, "Textures/Black_Knight.png"))
             elif piece_type == "Q":
                 self.image = py.image.load(os.path.join(dirname, "Textures/Black_Queen.png"))
             else:
                 raise Exception("invalid piece selection")
         else:
             raise Exception("Invalid color at PyObjects.set_image")