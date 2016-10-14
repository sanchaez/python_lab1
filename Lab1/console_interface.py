'Console Interface Module'
from types import *
from tablecontroller import VisualRelationalTableController


class MenuEntry:
    """Menu entry storage
    name    = name of entry
    fn      = function that returns a string or None"""

    def __init__(self, name="", fn=None):
        """Init method"""
        self.name = name
        self.fn = fn

    def __str__(self):
        """String representation"""
        assert type(self.name) is StringType, "Name property is not a string: %r" % self.name
        return self.name


class Menu(object):
    """Generic simple customisable menu which stores entries in dict"""
    # class defaults
    __at_exit_default = lambda self: None

    def __init__(self, init_names, init_data_fn, **kwargs):
        """Init method.
         init_names should contain a list of string names of options
         init_data_fn - functions to call on each menu entry
         kwargs:
            index= custom index
            name= menu header
            return_name= custom return
            return_index= custom return index"""
        # custom index
        if 'index' in kwargs:
            _index = kwargs['index']
        else:
            _index = map(str, range(len(init_names)))
        if 'name' in kwargs:
            self.name = kwargs['name']
        else:
            self.name = "Menu"
        # dict creation
        self.data = dict(zip(_index,
                             map(MenuEntry, init_names, init_data_fn)))
        # add exit option
        if 'return_name' in kwargs:
            return_name = kwargs['return_name']
        else:
            return_name = 'Return'
        if 'return_index' in kwargs:
            return_index = kwargs['return_index']
        else:
            return_index = 'r'
        self.data[return_index] = MenuEntry(return_name, self.__exit)
        self.__exited = False
        self.__at_exit = self.__at_exit_default

    def add_entry(self, name, fn, index):
        """Adding entry to menu"""
        self.data[index] = MenuEntry(name, fn)

    def __call_entry(self, key):
        """Calling entry fn by key"""
        if key in self.data.keys():
            return self.data[key].fn()
        else:
            return None

    def loop(self):
        while not self.__exited:
            var = raw_input("Choose an option:")
            self.__call_entry(var)

    @staticmethod
    def __nested_menu_loop(index, fn_iterable, **kwargs):
        m = Menu(index, fn_iterable, **kwargs)
        return lambda: m.loop()

    def bool_true_exit(menu, bool):
        bool = True
        menu.__exit()

    def __exit(self):
        self.__exited = True
        self.__at_exit()

    def __str__(self):
        """String representation"""
        return "- " + self.name + " -\n" \
               + "".join(map(lambda x: str(x[0]) + ": " + str(x[1]) + "\n",
                             sorted(self.data.items())))

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
                         "Edit..."
                         "Delete..."
                         "Search...",
                         "Get Authors with books of >100 pages",
                         "Save/Load"]
        _fn_array = [self.__controller.update_view_master, self.__controller.update_view_slave,
                      self.__nested_menu_loop(["Authors", "Books"],
                                              [self.__controller.add_row_master(), self.__controller.add_row_slave()],
                                              name='Choose table'),
                      self.__nested_menu_loop(["Authors", "Books"],
                                       [visual_search(authors), visual_search(books)],
                                       name='Choose table'),
                      self.__nested_menu_loop(["Save pickle", "Load pickle"],
                                       [printer(''), printer('')])]
        super(MainMenu, self).__init__(_names_array, _fn_array,
                                       name="Simple database", return_name="Exit", return_index="x")
