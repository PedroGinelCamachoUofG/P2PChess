import sys
import pygame
import pygame as py
import src.PyObjects as po

class ErrorHandler:

    __instance = None
    error_dict = {}

    @staticmethod
    def get_instance():
        if ErrorHandler.__instance is None:
            ErrorHandler()
        return ErrorHandler.__instance

    def __init__(self):
        if ErrorHandler.__instance is not None:
            raise Exception("2 instances of ErrorHandler detected")
        else:
            self.clean_log()
            ErrorHandler.__instance = self

    def add_error(self, error):
        if error[1:10] == "WinError ":
            error = error[10:15]
        if error in self.error_dict:
            self.error_dict[error][0] =  True
        else:
            #Unknow errors are considered fatal
            self.error_dict[error] = [True, True, "Unknown Error"]
        if self.error_dict[error][1]:
            self.launch_log()

    def clean_log(self):
        """
        Key: exception as raised by python
        Value: [3] containing
        [error_encountered_flag(T/F),is_error_fatal(T/F),string interpretation of error]
        """
        self.error_dict = {
            "timed outh":[False, True, "No one connected when hosting"],
            "10061":[False, True, "Tried to connect to self but wasn't hosting"],
            "[Errno 11001] getaddrinfo failed":[False, True, "Input given was not an actual IP address"],
            "10054":[False, True, "Opponent closed window while waiting"],
            "tuple index out of range":[False, True, "Opponent closed window while choosing"]
        }

    def launch_log(self):
        py.init()
        win = py.display.set_mode((600, 300))
        py.display.set_caption("P2PChess Error Log")

        run = True
        drawables = []
        position_counter = 0
        for error, explanation in self.error_dict.items():
            if explanation[0]:
                if explanation[1]:
                    text = f"FATAL | Explanation: {explanation[2]} | Error: {error}"
                else:
                    text = f"Explanation: {explanation[2]} | Error: {error}"
                drawables.append(po.Text(0, position_counter*24,
                                         text,
                                         py.font.Font(None, 24)))
                position_counter += 1

        while run:
            py.event.pump()

            for event in py.event.get():
                if event.type == py.QUIT:
                    self.clean_log()
                    py.quit()
                    sys.exit()

            key_input = pygame.key.get_pressed()
            if key_input[pygame.K_LEFT]:
                for elt in drawables:
                    elt.x += 1
            if key_input[pygame.K_UP]:
                for elt in drawables:
                    elt.y += 1
            if key_input[pygame.K_RIGHT]:
                for elt in drawables:
                    elt.x -= 1
            if key_input[pygame.K_DOWN]:
                for elt in drawables:
                    elt.y -= 1

            win.fill((255, 255, 255))
            for elt in drawables:
                elt.draw(win)

            py.display.update()

        exit()