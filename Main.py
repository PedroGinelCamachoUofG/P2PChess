from src.Menu import menu
from src.ErrorHandler import ErrorHandler
'''
=================================================================|
                        TO DO LIST
STUFF TO CONSIDER:
   -Piece display is jankey
   -o un chat con las threads
   -move errorhandler to be over all of game and menu and not in net and stuff
   -Passing information back from threads and closing them when a move has been made.
   -Debug
   -Refactor
   -Enrocamiento
   -Pawn promotion

STUFF TO DO NOT TO THINK ABOUT:
    -test the Net functions
    -timer, and display for it

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
        menu()
    except Exception as e:
        ErrorHandler().addError(e.__str__())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
