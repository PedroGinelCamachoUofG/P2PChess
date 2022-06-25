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
    win = py.display.set_mode((600, 300))

    #texture imports
    dirname = os.path.join( os.path.dirname( __file__ ), '..' )
    join_normal = py.image.load(os.path.join(dirname, "Textures/Join_Normal.png"))
    join_hover = py.image.load(os.path.join(dirname, "Textures/Join_Hover.png"))
    host_normal = py.image.load(os.path.join(dirname, "Textures/Host_Normal.png"))
    host_hover = py.image.load(os.path.join(dirname, "Textures/Host_Hover.png"))
    empty_normal = py.image.load(os.path.join(dirname, "Textures/Empty_Normal.png"))
    empty_hover = py.image.load(os.path.join(dirname, "Textures/Empty_Hover.png"))

    #instatiate objects
    ip_input = po.InputBox(50, 50, 500, 25, py.font.Font(None, 32))
    join_button = po.Button(join_normal, join_hover, 100, 100)
    host_button = po.Button(host_normal, host_hover, 320, 100)
    help_button = po.Button(empty_normal, empty_hover, 237, 200)

    #pygame loop
    while True:

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
                        end_menu(ip_input.text.text)
                    else:
                        ErrorHandler().addError(e.__str__())

            elif ip_input.is_over(py.mouse) and event.type == py.MOUSEBUTTONDOWN:
                ip_input.select()
            elif (not ip_input.is_over(py.mouse)) and event.type == py.MOUSEBUTTONDOWN:
                ip_input.unselect()

            if help_button.is_over(py.mouse) and event.type == py.MOUSEBUTTONDOWN:
                help_menu()

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
        help_button.draw(win)

        #texts
        win.blit(py.font.Font(None, 48).render("Join", True, (0,0,0)), (160,110))
        win.blit(py.font.Font(None, 48).render("Host", True, (0,0,0)), (380,110))
        win.blit(py.font.Font(None, 48).render("Help", True, (0, 0, 0)), (250, 210))
        win.blit(py.font.Font(None, 16).render("By Pedro Ginel Camacho with help of Alberto Perez Ortega", True, (0,0,0)), (140,280))

        py.display.update()

def end_menu(ip):
    py.init()
    py.display.set_caption("P2PChess End Menu")
    win = py.display.set_mode((640, 582))

    #textures are placeholder now its just for an idea
    dirname = os.path.join(os.path.dirname(__file__), '..')
    empty_normal = py.image.load(os.path.join(dirname, "Textures/Empty_Normal.png"))
    empty_hover = py.image.load(os.path.join(dirname, "Textures/Empty_Hover.png"))

    ip_name_input = po.InputBox(50, 50, 500, 25, py.font.Font(None, 32))
    back_to_menu = po.Button(empty_normal, empty_hover, 100, 100)
    save_ip = po.Button(empty_normal, empty_hover, 100, 200)

    while True:

        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()

            if back_to_menu.is_over(py.mouse) and event.type == py.MOUSEBUTTONDOWN:
                start_menu()

            elif save_ip.is_over(py.mouse) and event.type == py.MOUSEBUTTONDOWN:
                with open(os.path.relpath('..Saved_IPs.txt', dirname),"a") as f:
                    f.write(f"{ip_name_input} : {ip}")

            elif ip_name_input.is_over(py.mouse) and event.type == py.MOUSEBUTTONDOWN:
                ip_name_input.select()
            elif (not ip_name_input.is_over(py.mouse)) and event.type == py.MOUSEBUTTONDOWN:
                ip_name_input.unselect()

            if event.type == py.KEYDOWN and ip_name_input.active:
                if event.key == py.K_BACKSPACE:
                    ip_name_input.delete()
                else:
                    ip_name_input.write(event.unicode)

        win.fill((255, 255, 255))
        ip_name_input.draw(win)
        back_to_menu.draw(win)
        save_ip.draw(win)

        win.blit(py.font.Font(None, 48).render("Menu", True, (0, 0, 0)), (160, 110))
        win.blit(py.font.Font(None, 48).render("Save IP", True, (0, 0, 0)), (360, 110))
        win.blit(py.font.Font(None, 16).render("By Pedro Ginel Camacho with help of Alberto Perez Ortega", True, (0,0,0)), (140,185))

        py.display.update()

#for the instructions
def help_menu():
    py.init()
    py.display.set_caption("P2PChess Info")
    win = py.display.set_mode((400, 400))

    dirname = os.path.join(os.path.dirname(__file__), '..')
    empty_normal = py.image.load(os.path.join(dirname, "Textures/Empty_Normal.png"))
    empty_hover = py.image.load(os.path.join(dirname, "Textures/Empty_Hover.png"))
    info_img = py.image.load(os.path.join(dirname, "Textures/Info_Img.png"))
    info_img_pos = [0,0]
    back_to_menu = po.Button(empty_normal, empty_hover, 55, 100)

    while True:

        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()

            if back_to_menu.is_over(py.mouse) and event.type == py.MOUSEBUTTONDOWN:
                start_menu()

            key_input = py.key.get_pressed()
            if key_input[py.K_LEFT]:
                info_img_pos[0] += 10
                back_to_menu.x += 10
            if key_input[py.K_UP]:
                info_img_pos[1] += 10
                back_to_menu.y += 10
            if key_input[py.K_RIGHT]:
                info_img_pos[0] -= 10
                back_to_menu.x -= 10
            if key_input[py.K_DOWN]:
                info_img_pos[1] -= 10
                back_to_menu.y -= 10

        win.fill((255, 255, 255))
        win.blit(info_img, tuple(info_img_pos))
        back_to_menu.draw(win)
        win.blit(py.font.Font(None, 48).render("Menu", True, (0, 0, 0)), (info_img_pos[0] + 60,info_img_pos[1] + 110))

        py.display.update()