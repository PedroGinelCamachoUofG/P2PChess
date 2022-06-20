from src.Menu import menu
from src.ErrorHandler import ErrorHandler
'''
=================================================================|
                        TO DO LIST
STUFF TO CONSIDER: 
   -Refactor
   -King movement not blocked correctly-> haz una función para calcular el jaque, usala para ganar, enrocamiento y mover al rey
   -Enrocamiento
   -Pawn promotion

STUFF TO DO NOT TO THINK ABOUT:
    -historial de movimientos
    -timer, and display for it
    -and manual thing
    -chat con threads
    -game end nicely
    -play again
    -put the last IP address as default, historial de partidas
BUGS:
    
'''

# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #try:
    print_hi('PyCharm')
    menu()
    #except Exception as e:
    #    ErrorHandler().addError(e.__str__())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
