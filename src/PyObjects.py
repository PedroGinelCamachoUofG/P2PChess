import pygame as py

#classes for interactibles
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
    def __init__(self, x, y, wid, hei, font):
        self.x = x
        self.y = y
        self.wid = wid
        self.hei = hei
        self.text = Text(self.x, self.y, "Type IP here", font)
        self.object = py.Rect((self.x, self.y), (self.wid, self.hei))


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

    def draw(self, win):
        py.draw.rect(win, py.Color(255, 255, 255), self.object)
        self.text.draw(win)
        #win.blit(self.currentImage, (self.x, self.y))

    def is_over(self, pointer):
        if self.object.collidepoint(pointer.get_pos()):
            return True
        return False

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
