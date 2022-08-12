from src.Menu import start_menu
from src.ErrorHandler import ErrorHandler
'''
=================================================================|
                        TO DO LIST
STUFF TO CONSIDER:
   -Do en passant well
   -Refactor
   -Castling
   -Make clear in end menu that the game has ended(eg: put GAME OVER)

STUFF TO DO NOT TO THINK ABOUT:
    -display if it was win or loose
    -historial de movimientos
    -timer, and display for it
    -chat con threads
BUGS:
    -promotion happens when it reaches the last square and I think its buggy
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
