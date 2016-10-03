from types import *
from tabulate import tabulate
"""Database Module"""
from collections import namedtuple


# it is DEPRECATED and WILL BE REMOVED!
# TODO: remove this class
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

    # class defaults
    _default_join_type = 'inner'
    _default_direction = 'full'
    _default_output_type = 'grid'
    # counter
    _instance_count = 0
    def __init__(self, default_columns):
        """Init function"""
        self._instance_count += 1
        # id table contains an unique key and its row
        self._container_class = namedtuple('__fields' + str(self._instance_count), default_columns)
        self._indexed_table = list()

    def __getitem__(self, item):
        assert type(self._indexed_table) is ListType, "Invalid table : {0}".format(self._indexed_table)
        got_item = self._indexed_table[item]
        assert isinstance(got_item, self._container_class), "Invalid table on record : {0}".format(got_item)
        return got_item

    def __setitem__(self, key, value):
        assert type(self._indexed_table) is ListType, "Invalid table : {0}".format(self._indexed_table)
        assert type(value) is ListType or TupleType
        self._indexed_table[key] = self._container_class._make(value)


    def __add__(self, other):
        if type(other) in (ListType, TupleType):
            self._indexed_table.append(self._container_class._make(other))
        else:
            # no variants left
            assert isinstance(other, self.__class__), "Type of operand is invalid: {0}".format(other)
            self._indexed_table += other._indexed_table
        return self

    def __repr__(self):
        """
        String representation of object
        :rtype: str
        """
        return tabulate(self._indexed_table,
                        headers=self._container_class._fields,
                        tablefmt=self._default_output_type)
    
    def subtable(self, **kwargs):
        """Creates a subtable object from this table.
        :kwargs:
            columns: tuple with names of columns
            rows: tuple with numbers of rows
            filter: filter predicate
            filter_columns: columns to affect filter"""
        if 'columns' in kwargs:
            _columns = kwargs['columns']
        else:
            _columns = self._container_class._fields
        if 'rows' in kwargs:
            _rows = kwargs['rows']
        else:
            _rows = range(len(self._indexed_table))
        if 'filter' in kwargs:
            _filter = kwargs['filter']
        else:
            _filter = lambda x: True
        if 'filter_columns' in kwargs:
            _filter_columns = kwargs['filter_columns']
        else:
            _filter_columns = self._container_class._fields
        # collecting values
        gathered_table = DatabaseTable(_columns)
        for index in _rows:
            gathered_row = []
            for field in _columns:
                gathered_row.append(getattr(self._indexed_table[index], field))
            # apply filter
            filter_good = True
            for filter_field in _filter_columns:
                if not _filter(getattr(self._indexed_table[index], filter_field)):
                    filter_good = False
                    break
            if filter_good:
                gathered_table += gathered_row
        return gathered_table

    @staticmethod
    def _generic_join(self, other, *args, **kwargs):
        """JOIN method that accepts keywords.
        other - other table class
        *args = a tuple of tuples:
            column_1, column_2 - columns to join from self and other
            relation-predicate - boolean function that accepts at least 2 values
        kwargs:
            type = type of join - 'inner' 'outer' 'cross'
            direction = direction of join 'left' 'right' 'full'. Useless with inner join.
            fields_1, fields_2 = names of fields to concat into result table
        """
        # get parameters
        if 'type' in kwargs:
            _type = kwargs['type']
        else:
            _type = self._default_join_type
        #set
        if _type == 'inner':
            _direction = 'full'
        elif _type != 'inner':
            _direction = kwargs['direction']
        else:
            _direction = self._default_direction
        if 'fields_1' in kwargs:
            _fields_1 = kwargs['fields_1']
        else:
            _fields_1 = self._container_class._fields
        if 'fields_2' in kwargs:
            _fields_2 = kwargs['fields_2']
        else:
            _fields_2 = other._container_class._fields
        # make temporary index
        temporary_index_left_center = dict()
        temporary_index_right_center = dict()
        temporary_index_left = list()
        temporary_index_right = list()
        temporary_index_copy = None
        for relation in args:
            # find matching records
            assert type(self._indexed_table) is ListType and type(other._indexed_table) is ListType
            for row_1 in range(len(self._indexed_table)):
                for row_2 in range(len(other._indexed_table)):
                    if relation[2](getattr(self._indexed_table[row_1], relation[0]),
                                   getattr(other._indexed_table[row_2], relation[1])):
                        if row_1 in temporary_index_left_center:
                            temporary_index_left_center[row_1].append(row_2)
                        else:
                            temporary_index_left_center[row_1] = [row_2]
                        if row_2 in temporary_index_right_center:
                            temporary_index_right_center[row_2].append(row_1)
                        else:
                            temporary_index_right_center[row_2] = [row_1]
            #ANDing relations (intersection)
            if temporary_index_copy:
                temporary_index_left_center = {x:temporary_index_copy[x]
                                                for x in temporary_index_left_center
                                                if x in temporary_index_copy}
            #copy
            temporary_index_copy = temporary_index_left_center.copy()

        # outer join index
        if _type == 'outer':
            if _direction == 'left':
                for row_1 in range(len(self._indexed_table)):
                    if row_1 not in temporary_index_left_center:
                        temporary_index_left.append(row_1)
            elif _direction == 'right':
                for row_2 in range(len(other._indexed_table)):
                    if row_2 not in temporary_index_right_center:
                        temporary_index_right.append(row_2)
            elif _direction == 'full':
                for row_1 in range(len(self._indexed_table)):
                    if row_1 not in temporary_index_left_center:
                        temporary_index_left.append(row_1)
                for row_2 in range(len(other._indexed_table)):
                    if row_2 not in temporary_index_right_center:
                        temporary_index_right.append(row_2)

        del temporary_index_right_center
        # populating new table
        # fields maintain the given order because of namedtuple()
        gathered_table = DatabaseTable(_fields_1 + _fields_2)
        # add center index
        for index_row_1, indexes_rows_2 in temporary_index_left_center.items():
            row_1_data = []
            for field in _fields_1:
                row_1_data.append(getattr(self._indexed_table[index_row_1], field))

            for index_row_2 in indexes_rows_2:
                row_2_data = []
                for field in _fields_2:
                    row_2_data.append(getattr(other._indexed_table[index_row_2], field))
                # add the fields in-order
                gathered_table += row_1_data + row_2_data

        # add blank left index
        for index_row_1 in temporary_index_left:
            row_1_data = []
            for field in _fields_1:
                row_1_data.append(getattr(self._indexed_table[index_row_1], field))
            # fill with None
            row_2_data = []
            for field in _fields_2:
                row_2_data.append(None)
            # gather fields
            gathered_table += row_1_data + row_2_data

        # add blank right index
        for index_row_2 in temporary_index_right:
            row_2_data = []
            for field in _fields_2:
                row_2_data.append(getattr(other._indexed_table[index_row_2], field))
            # fill with None
            row_1_data = []
            for field in _fields_1:
                row_1_data.append(None)
            # gather fields
            gathered_table += row_1_data + row_2_data
        return gathered_table

# container test
if __name__ == '__main__':
    test_1 = DatabaseTable('a b')
    test_2 = DatabaseTable('c d')
    for x, y in zip(range(1,5), range(4)):
        test_1 += (x, y)
        test_2 += (y, x)
    print DatabaseTable._generic_join(test_1, test_2, ('a', 'c', lambda x, y: x == y))
    print DatabaseTable._generic_join(test_1, test_2, ('a', 'c', lambda x, y: x == y),
                                      type='outer', direction='full', fields_1 = tuple('a'), fields_2 = tuple('c'))
    print test_1.subtable(filter=lambda x: x > 2, filter_columns='a')
