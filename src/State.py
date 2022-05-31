import threading
import pygame as py
import sys
import src.PyObjects as po

class State(threading.Thread):

    def __init__(self, win, board, queue, args=(), kwargs=None):
        threading.Thread.__init__(self, args=(), kwargs=None)
        self.win = win
        self.board = board
        self.queue = queue
        self.drawables = []
        #self.daemon = True
        self.receive_messages = args[0]

    def run(self):
        while True:

            self.interactions()

            self.win.fill((255, 255, 255))
            for elt in self.drawables:
                elt.draw(self.win)

            if not self.queue.get():
                break

    #abstract method
    def interactions(self):
        pass

    def draw(self):
        self.board.draw(self.win)
        for elt in self.drawables:
            elt.draw(self.win)
        py.display.update()


class Waiting(State):

    def __init__(self, win, board, queue):
        super().__init__(win, board, queue)
        self.arrow_start = (None,None)
        self.arrow_end = (None,None)

    def interactions(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
        if py.mouse.get_pressed()[0]:
            #if right click delete all arrows
            self.drawables = []
        #draw arrows with left click
        if py.mouse.get_pressed()[2]:
            self.arrow_start = py.mouse.get_pos()
        if (not py.mouse.get_pressed()[2]) and self.arrow_start != (None,None):
            self.arrow_start = py.mouse.get_pos()
            self.drawables.append(po.arrow(self.arrow_start, self.arrow_end))


class Choosing(State):

    def __init__(self, win, board, queue):
        super().__init__(win, board, queue)

    def interactions(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            if event.type == py.MOUSEBUTTONDOWN:
                print("Click during choosing")