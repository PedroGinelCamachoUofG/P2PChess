import pygame as py

class ErrorHandler:

    __instance = None
    """
    Key: exception as raised by python
    Value: [3] containing
    [error_encountered_flag(T/F),is_error_fatal(T/F),string interpretation of error]
    """
    error_dict = {}

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
            self.error_dict[error] = [True, True, "Unknown error"]
        if self.error_dict[error][1]:
            self.logger()

    def launchLog(self):
        py.quit()
        py.init()
        py.display.set_caption("P2PChess Error Log")
        win = py.display.set_mode((600, 200))
