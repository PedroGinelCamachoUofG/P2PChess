from src.Menu import start_menu
from src.ErrorHandler import ErrorHandler
'''
=================================================================|
                        TO DO LIST
STUFF TO CONSIDER: 
   -Refactor
   -King movement not blocked correctly-> haz una función para calcular el jaque, usala para ganar, enrocamiento y mover al rey
   -Enrocamiento
   -finish info menu

STUFF TO DO NOT TO THINK ABOUT:
    -historial de movimientos
    -timer, and display for it
    -chat con threads
BUGS:
    -how does winning player know it is check mate?:
        make the is_check_mate function check both players
        by changing the player color and executing the function as it works currently on both like that
        the issue is doing thins without a bunch of ifs for the color change
'''

# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        print_hi('PyCharm')
        start_menu()
    except Exception as e:
        ErrorHandler().add_error(e.__str__())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
