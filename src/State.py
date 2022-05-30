import threading
import pygame as py
import sys

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
        #puts board and all drawables on screen
        #...
        py.display.update()


class Waiting(State):

    def __init__(self, win, board, queue):
        super().__init__(win, board, queue)

    def interactions(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            if event.type == py.MOUSEBUTTONDOWN:
                print("Click during waiting")


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