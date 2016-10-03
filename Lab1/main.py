'''Main file'''
from __future__ import print_function
from database import *
from console_interface import *


def printer(obj):
    return lambda: print(obj)

if __name__ == '__main__':
    authors = DatabaseTable('Author YearOfBirth')
    books = DatabaseTable('Book NumOfPages AuthorID')
    # TODO: populate
    # TODO: use pickle
    menu_instance = Menu(["View table Author", "View table Books", "Filter...", "Search..."],
                         [printer(authors), printer(books), printer(''), printer('')])
    print(menu_instance)
    print(menu_instance.data.keys())
    while True:
        var = raw_input("Choose an option:")
        print(repr(var))
        menu_instance.call_entry(var)

