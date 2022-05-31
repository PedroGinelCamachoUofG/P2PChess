import pygame as py
import math

#classes for interactives
class Button():
    def __init__(self, staticImage, hoverImage, x, y):
        self.currentImage = staticImage
        self.staticImage = staticImage
        self.hoverImage = hoverImage
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

class InputBox():
    """
    Code for giving the input box textures has been commented out
    """
    def __init__(self, x, y, wid, hei, font):
        self.x = x
        self.y = y
        self.wid = wid
        self.hei = hei
        self.text = Text(self.x, self.y, "Type IP here", font)
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

class Text():

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

class arrow():

    def __init__(self, start, end):
        self.color = (255,0,0)
        self.point = end
        self.length = int(math.sqrt(((start[0]-end[0])**2)+((start[1]-end[1])**2)))
        self.direction = ((end[0]-start[0]),(end[1]-start[1]))
        #make direction unitary
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
        py.draw.polygon(win, self.color, [self.a, self.b, self.c, self.point, self.d, self.e, self.f])
