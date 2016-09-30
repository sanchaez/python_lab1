'Database Module'
from types import *
from collections import namedtuple

#it is DEPRECATED and WILL BE REMOVED!
#TODO: remove this class
class TableDouble(object):
    """Authors table abstraction class.
Table is assured to contain no duplicates."""

    def __init__(self, init_data):
        """Init function
            example data stored: {'Douglas Adams': 1, 'Stephen King': 2}"""
        # ratio is a table divisor (1/ratio). Used to print values.
        self.ratio = 10
        # rows is a number of rows used for printing values
        # following works in most linux systems:
        # import subprocess
        # rows = int(subprocess.check_output(['stty', 'size']).split()[0])
        self.rows = 40
        self.data_name_id = dict()
        self.data_id_name = dict()
        self.add_list(init_data)

    def add(self, identifier, name):
        """Add value to table. Do nothing if it exists"""
        assert type(identifier) is IntType, "id is not an integer: %r" % identifier
        assert type(name) is StringType, "name is not a string: %r" % name
        if name not in self.data_name_id:
            self.data_name_id[name] = identifier
            self.data_id_name[identifier] = name

    def add_list(self, name_list):
        # to perform all the nessesary restrictions and prevent duplicates
        for identifier, name in zip(range(len(name_list)), name_list):
            self.add(identifier, name)

    def by_name(self, search_key):
        """Find id of a key in table."""
        assert type(search_key) is StringType, "name is not a string: %r" % search_key
        identifier = self.data_name_id[search_key]
        # to ensure consistence
        assert self.data_id_name[identifier] == search_key
        return identifier

    def by_id(self, search_key):
        """Find a key by value."""
        assert type(search_key) is IntType, "id is not an integer: %r" % search_key
        name = self.data_id_name[search_key]
        # to ensure consistence
        assert self.data_name_id[name] == search_key
        return name

    def filter(self):
        """Return TableDouble object with applied filter"""
        pass  # not implemented

    def remove(self, key):
        """Remove record by name"""
        val = self.data_name_id[key]
        assert self.data_id_name[val] == key
        del self.data_id_name[val], self.data_name_id[key]

    def remove_id(self, key):
        """Remove record by identifier"""
        val = self.data_id_name[key]
        assert self.data_name_id[val] == key
        del self.data_id_name[key], self.data_name_id[val]

    def print_this(self):
        print self

    def __str__(self):
        """String representation"""
        if self.data_id_name.items() == []:
            return ""
        else:
            # divide into 2 columns
            assert type(self.rows) is IntType, "rows is not an integer: %r" % self.rows
            rows_1 = (self.rows // self.ratio)
            rows_2 = self.rows - rows_1 - 3
            result_string = self.rows * '*' + '\n'
            for name, identifier in sorted(self.data_name_id.items()):
                assert self.data_id_name[identifier] == name
                id_len = len(str(identifier))
                if id_len < rows_1:
                    id_spaces = (rows_1 - id_len) // 2
                    name_spaces = (rows_2 - len(name)) // 2 + 1
                else:
                    id_spaces = 0
                    name_spaces = (self.rows - len(name) - (id_len) - 1) // 2

                # make a string for each record
                result_string += ("*" + id_spaces * " " + "%r" + id_spaces * " " + "*"
                                  + name_spaces * " " + name + (name_spaces - int(0.5 + len(name) % 2)) * " "
                                  + "*\n" + (self.rows * "*") + "\n") % identifier
            return result_string

class DatabaseTable(object):
    """A table container"""
    def __init__(self, default_columns_namedtuple_class):
        #uid table contains an unique key and its row
        self.container_class = default_columns_namedtuple_class
        self.uid_index = list()

    def __getitem__(self, item):
        return self.uid_index[item]

    def __setitem__(self, key, value):
        assert isinstance(key, self.container_class)
        self.uid_index[key] = value
    def __add__(self, other):
        assert isinstance(other, self.container_class)
        self.uid_index.append(other)
        #TODO: class addition
    #TODO: addition, substraction and join

# container test
if __name__ == '__main__':
    test_1 = TableDouble(['John doe', 'test1'])
    test_1.add(1000000000000000000, "lol")
    print test_1
