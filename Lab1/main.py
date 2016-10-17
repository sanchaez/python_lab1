'''Main file'''

if __name__ == '__main__':
    from tablecontroller import *


    class MainMenu(Menu):
        # default parameters
        def __init__(self, relational_table_controller):
            assert isinstance(relational_table_controller, VisualRelationalTableController), \
                "MainMenu should use RelationalController!: {0}".format(relational_table_controller)
            self.__controller = relational_table_controller
            self.view_master = self.__controller.update_view_master
            _names_array = ["View table Author",
                            "View table Books",
                            "Add...",
                            "Edit...",
                            "Delete...",
                            "Search...",
                            "Get Authors with books of >100 pages",
                            "Save/Load"]
            _fn_array = [self.__controller.update_view_master,
                         self.__controller.update_view_slave,
                         self.nested_menu_loop(["Authors", "Books"],
                                               [self.__controller.add_row_master, self.__controller.add_row_slave],
                                               name='Choose table'),
                         self.nested_menu_loop(["Authors", "Books"],
                                               [self.__controller.edit_master, self.__controller.edit_slave],
                                               name='Choose table'),
                         self.nested_menu_loop(["Authors", "Books"],
                                               [self.__controller.delete_master, self.__controller.delete_slave],
                                               name='Choose table'),
                         self.nested_menu_loop(["Authors", "Books"],
                                               [self.__controller.search_master, self.__controller.search_slave],
                                               name='Choose table'),
                         self.__controller.print_task_result,
                         self.nested_menu_loop(["Save pickle", "Load pickle"],
                                               [self.__controller.dump, self.__controller.load])]
            super(MainMenu, self).__init__(_names_array, _fn_array,
                                           name="Simple database", return_name="Exit", return_index="x")


    authors = TableController(DatabaseTableModel(('Author', 'YearOfBirth')))
    books = TableController(DatabaseTableModel(('Book', 'NumOfPages', 'Author')))

    try:
        authors.load()
    except:
        # load by code
        authors_data_starting_point = \
            (("Douglas Adams", "1952"), ("Ray Bradbury", "1920"), ("Taras Shevchenko", "1814"))
        for row in authors_data_starting_point:
            authors.add_row(row)
        # save
        authors.dump()
    try:
        books.load()
    except:
        # load by code
        books_data_starting_point = \
            (("Kobzar (1st ed.)", "100", "Taras Shevchenko"),
             ("Hitchhiker's Guide to Galaxy", "120", "Douglas Adams"),
             ("Fahrenheit 451", "159", "Ray Bradbury"))
        for row in books_data_starting_point:
            books.add_row(row)
        # save
        books.dump()

    books.set_item(1, "Author", "Morty")
    relation = VisualRelationalTableController(authors, books, ("Author", "Author"))
    main_menu = MainMenu(relation)
    main_menu.loop()
