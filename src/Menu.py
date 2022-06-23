import sys
import pygame as py
import os
from src.ErrorHandler import ErrorHandler
import src.PyObjects as po
from src.Game import host, join

def start_menu():
    #necessary set up
    py.init()
    py.display.set_caption("P2PChess Start Menu")
    win = py.display.set_mode((600, 200))
    run = True

    #texture imports
    dirname = os.path.join( os.path.dirname( __file__ ), '..' )
    join_normal = py.image.load(os.path.join(dirname, "Textures/Join_Normal.png"))
    join_hover = py.image.load(os.path.join(dirname, "Textures/Join_Hover.png"))
    host_normal = py.image.load(os.path.join(dirname, "Textures/Host_Normal.png"))
    host_hover = py.image.load(os.path.join(dirname, "Textures/Host_Hover.png"))

    #instatiate objects
    ip_input = po.InputBox(50, 50, 500, 25, py.font.Font(None, 32))
    join_button = po.Button(join_normal, join_hover, 100, 100)
    host_button = po.Button(host_normal, host_hover, 300, 100)

    #pygame loop
    while run:

        #events
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()

            if join_button.is_over(py.mouse) and event.type == py.MOUSEBUTTONDOWN:
                join_button.actions[0] = join(ip_input.text.text)
                try:
                    join_button.exe_all()
                except Exception as e:
                    if e.__str__() == "Game over":
                        end_menu()
                    else:
                        ErrorHandler().addError(e.__str__())

            elif host_button.is_over(py.mouse) and event.type == py.MOUSEBUTTONDOWN:
                host_button.actions[0] = host()
                try:
                    host_button.exe_all()
                except Exception as e:
                    if e.__str__() == "Game over":
                        end_menu()
                    else:
                        ErrorHandler().addError(e.__str__())

            elif ip_input.is_over(py.mouse) and event.type == py.MOUSEBUTTONDOWN:
                ip_input.select()
            elif (not ip_input.is_over(py.mouse)) and event.type == py.MOUSEBUTTONDOWN:
                ip_input.unselect()

            if event.type == py.KEYDOWN and ip_input.active:
                if event.key == py.K_BACKSPACE:
                    ip_input.delete()
                else:
                    ip_input.write(event.unicode)

        #output to window
        win.fill((255, 255, 255))

        ip_input.draw(win)
        join_button.draw(win)
        host_button.draw(win)

        #texts
        win.blit(py.font.Font(None, 48).render("Join", True, (0,0,0)), (160,110))
        win.blit(py.font.Font(None, 48).render("Host", True, (0,0,0)), (360,110))
        win.blit(py.font.Font(None, 16).render("By Pedro Ginel Camacho with help of Alberto Perez Ortega", True, (0,0,0)), (140,185))

        py.display.update()

    print("program end")

def end_menu():
    py.init()
    py.display.set_caption("P2PChess End Menu")
    win = py.display.set_mode((640, 582))
    run = True

    #textures are placeholder now its just for an idea
    dirname = os.path.join(os.path.dirname(__file__), '..')
    join_normal = py.image.load(os.path.join(dirname, "Textures/Join_Normal.png"))
    join_hover = py.image.load(os.path.join(dirname, "Textures/Join_Hover.png"))
    back_to_menu = po.Button(join_normal, join_hover, 100, 100)

    while run:

        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()

            if back_to_menu.is_over(py.mouse) and event.type == py.MOUSEBUTTONDOWN:
                start_menu()

        win.fill((255, 255, 255))
        back_to_menu.draw(win)
        win.blit(py.font.Font(None, 16).render("By Pedro Ginel Camacho with help of Alberto Perez Ortega", True, (0,0,0)), (140,185))

#for the instructions
def guide_menu():
    pass