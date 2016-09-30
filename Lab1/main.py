'''Main file'''
from collections import Counter
from database import *
from console_interface import *


def dummy():
    pass
if __name__ == '__main__':

    authors = TableDouble(["Douglas Adams", "Ray Bradbury"])
    books = TableDouble(["Hitchiker's guide to the Galaxy", "451 Fahrenheit"])
    menu_instance = Menu(["View table Author", "View table Books", "Filter...", "Search..."],
                         [authors.print_this, books.print_this, dummy, dummy])
    print menu_instance
    print menu_instance.data.keys()
    while True:
        var = raw_input("Choose an option:")
        print repr(var)
        menu_instance.call_entry(var)