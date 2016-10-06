"""Database Module"""

from types import *
from tabulate import tabulate
from collections import namedtuple


class DatabaseTableModel(object):
    """A table container"""
    # class defaults

    __default_output_type = 'grid'
    # counter
    __instance_count = 0

    def __init__(self, default_columns):
        """Init function"""
        self.__instance_count += 1
        # id table contains an unique key and its row
        self._container_class = namedtuple('__fields' + str(self.__instance_count), default_columns)
        self.__indexed_table = list()

    def __getitem__(self, item):
        assert type(self.__indexed_table) is ListType, "Invalid table : {0}".format(self.__indexed_table)
        got_item = self.__indexed_table[item]
        assert isinstance(got_item, self._container_class), "Invalid table on record : {0}".format(got_item)
        return got_item

    def __setitem__(self, key, value):
        assert type(self.__indexed_table) is ListType, "Invalid table : {0}".format(self.__indexed_table)
        assert type(value) is ListType or TupleType
        self.__indexed_table[key] = self._container_class._make(value)

    def __add__(self, other):
        if type(other) in (ListType, TupleType):
            self.__indexed_table.append(self._container_class._make(other))
        else:
            # no variants left
            assert isinstance(other, self.__class__), "Type of operand is invalid: {0}".format(other)
            self.__indexed_table += other.__indexed_table
        return self

    def __repr__(self):
        """
        String representation of object
        :rtype: str
        """
        return tabulate(self.__indexed_table,
                        headers=self.fields(),
                        tablefmt=self.__default_output_type)

    def __len__(self):
        return len(self.__indexed_table)

    # copy construct
    def __copy__(self):
        new_obj = DatabaseTableModel(self.fields)
        for row in self.__indexed_table:
            new_obj += row
        return new_obj

    # getters
    def get_item(self, index, field):
        return getattr(self.__indexed_table[index], field)

    def get_column(self, column_name):
        return map(lambda index: getattr(self[index], column_name), len(self.__indexed_table))

    def get_row(self, index):
        return self[index]

    def fields(self):
        return self._container_class._fields

    # deletion
    def del_row(self, index):
        self[index] = None

    def __delitem__(self, key):
        self[key] = None

    # setters
    def set_item(self, index, name, value):
        self[index] = self[index]._replace(**{name: value})


# container test
if __name__ == '__main__':
    test_1 = DatabaseTableModel('a b')
    test_2 = DatabaseTableModel('c d')
    for x, y in zip(range(1, 5), range(4)):
        test_1 += (x, y)
        test_2 += (y, x)

    print test_1.subtable(filter=lambda x: x > 2, filter_columns='a')
