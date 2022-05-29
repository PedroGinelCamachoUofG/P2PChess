import sys

import pygame as py
import src.PyObjects as po

class ErrorHandler:

    __instance = None
    """
    Key: exception as raised by python
    Value: [3] containing
    [error_encountered_flag(T/F),is_error_fatal(T/F),string interpretation of error]
    """
    error_dict = {
        "timed outh" : [False, True, "No one connected when hosting"],
        "[WinError 10061] No se puede establecer una conexión ya que el equipo de destino denegó expresamente dicha conexión" : [False, True, "Tried to connect to self but wasn't hosting"],
    }

    @staticmethod
    def getInstance():
        if ErrorHandler.__instance == None:
            ErrorHandler()
        return ErrorHandler.__instance

    def __init__(self):
        if ErrorHandler.__instance != None:
            raise Exception("2 instances of ErrorHandler detected")
        else:
            ErrorHandler.__instance = self

    def addError(self, error):
        if error in self.error_dict:
            self.error_dict[error][0] =  True
        else:
            #Unknow errors are considered fatal
            self.error_dict[error] = [True, True, ""]
        if self.error_dict[error][1]:
            self.launchLog()

    def launchLog(self):
        py.display.set_caption("P2PChess Error Log")
        run = True
        win = py.display.set_mode((1000, 400))
        drawables = []
        position_counter = 0
        for error, explanation in self.error_dict.items():
            drawables.append(po.Text(0, position_counter*24,
                                     f"Error: {error} | Explanation: {explanation[2]}",
                                     py.font.Font(None, 24)))
            position_counter += 1

        while run:

            for event in py.event.get():
                #add event to move around text
                if event.type == py.QUIT:
                    py.quit()
                    sys.exit()

            win.fill((255, 255, 255))
            for elt in drawables:
                elt.draw(win)

            py.display.update()

        exit()