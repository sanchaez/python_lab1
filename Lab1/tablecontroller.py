from database import DatabaseTableModel
from tableview import *
from types import *


class TableController(object):
    # class defaults

    __default_join_type = 'inner'
    __default_direction = 'full'

    def __init__(self, table, view):
        assert isinstance(table, DatabaseTableModel)
        assert issubclass(view, TableView)
        self.__table = table
        self.__view = view

    def get_item(self, index, name):
        return self.__table.get_item(index, name)

    def set_item(self, index, name):
        self.__view.add_to_table(self.__table)

    def find(self, values, columns):
        """Finds first matching row by :columns: and :values:"""
        assert type(values) is TupleType or ListType
        for column in columns:
            for value in self.__table:
                if getattr(value, column) in values:
                    return value

    def update_view(self):
        self.__view.update()

    def add_row_visual(self):
        self.__view.add_to_table(self.__table)

    def edit_row_visual(self):
        self.__view.edit_table(self.__table)

    def delete_row_visual(self):
        self.__view.delete_row(self.__table)

    def subtable(self, *args, **kwargs):
        """Creates a subtable controller object from controlled table.
        :args: tuple with names of columns
        :kwargs:
            rows: tuple with numbers of rows
            filter: filter predicate
            filter_columns: columns to affect filter"""
        if args is None:
            _columns = self.__table.fields()
        else:
            _columns = args
        if 'rows' in kwargs:
            _rows = kwargs['rows']
        else:
            _rows = range(len(self.__table))
        if 'filter' in kwargs:
            _filter = kwargs['filter']
        else:
            _filter = lambda x: True

        if 'filter_columns' in kwargs:
            _filter_columns = kwargs['filter_columns']
        else:
            _filter_columns = self.__table.fields()
        # collecting values
        gathered_table = DatabaseTableModel(_columns)
        for index in _rows:
            gathered_row = map(lambda x: getattr(self.__table[index], x), _columns)
            # apply filter
            filter_good = True
            for filter_field in _filter_columns:
                if not _filter(getattr(self.__table[index], filter_field)):
                    filter_good = False
                    break
            if filter_good:
                gathered_table += gathered_row
        return TableController(gathered_table)

    def join(self, other, *args, **kwargs):
        return self._generic_join(self.__table, other, *args, **kwargs)

    @staticmethod
    def _generic_join(table1, table2, *args, **kwargs):
        """JOIN method that accepts keywords.
        other - other table class
        args = a tuple of tuples:
            column_1, column_2 - columns to join from self and other
            relation-predicate - boolean function that accepts at least 2 values
        kwargs:
            type = type of join - 'inner' 'outer' 'cross'
            direction = direction of join 'left' 'right' 'full'. Useless with inner join.
            fields_1, fields_2 = names of fields to concat into result table
        """

        def get_fields(table, fields, index):
            return map(lambda field: getattr(table[index], field), fields)

        # get parameters
        if 'type' in kwargs:
            _type = kwargs['type']
        else:
            _type = table1._default_join_type
        # set
        if _type == 'inner':
            _direction = 'full'
        elif _type != 'inner':
            _direction = kwargs['direction']
        else:
            _direction = table1._default_direction
        if 'fields_1' in kwargs:
            _fields_1 = kwargs['fields_1']
        else:
            _fields_1 = table1.fields()
        if 'fields_2' in kwargs:
            _fields_2 = kwargs['fields_2']
        else:
            _fields_2 = table2.fields()
        # make temporary index
        temporary_index_left_center = dict()
        temporary_index_right_center = dict()
        temporary_index_left = list()
        temporary_index_right = list()
        temporary_index_copy = None
        for relation in args:
            # find matching records
            assert isinstance(table1, DatabaseTableModel) and isinstance(table2, DatabaseTableModel)
            for index_row_1, row_1 in enumerate(table1):
                for index_row_2, row_2 in enumerate(table2):
                    if relation[2](getattr(row_1, relation[0]),
                                   getattr(row_2, relation[1])):
                        if row_1 in temporary_index_left_center:
                            temporary_index_left_center[index_row_1].append(index_row_2)
                        else:
                            temporary_index_left_center[index_row_1] = [index_row_2]
                        if row_2 in temporary_index_right_center:
                            temporary_index_right_center[index_row_2].append(index_row_1)
                        else:
                            temporary_index_right_center[index_row_2] = [index_row_1]
            # ANDing relations (intersection)
            if temporary_index_copy:
                temporary_index_left_center = {x: temporary_index_copy[x]
                                               for x in temporary_index_left_center
                                               if x in temporary_index_copy}
            # copy
            temporary_index_copy = temporary_index_left_center.copy()

        # outer join index
        if _type == 'outer':
            if _direction == 'left':
                for row_1 in range(table1):
                    if row_1 not in temporary_index_left_center:
                        temporary_index_left.append(row_1)
            elif _direction == 'right':
                for row_2 in range(table2):
                    if row_2 not in temporary_index_right_center:
                        temporary_index_right.append(row_2)
            elif _direction == 'full':
                for row_1 in range(table1):
                    if row_1 not in temporary_index_left_center:
                        temporary_index_left.append(row_1)
                for row_2 in range(table2):
                    if row_2 not in temporary_index_right_center:
                        temporary_index_right.append(row_2)
        # deleting unused index
        del temporary_index_right_center
        # populating new table
        # fields maintain the given order because of namedtuple()
        gathered_table = DatabaseTableModel(_fields_1 + _fields_2)
        # add center index
        for index_row_1, indexes_rows_2 in temporary_index_left_center.items():
            row_1_data = get_fields(table1, _fields_1, index_row_1)
            row_2_data = map(lambda index_row_2:
                             get_fields(table2, _fields_2, index_row_2),
                             indexes_rows_2)

            # add the fields in-order
            gathered_table += row_1_data + row_2_data

        # add blank left index
        for index_row_1 in temporary_index_left:
            row_1_data = get_fields(table1, _fields_1, index_row_1)
            # fill with None
            row_2_data = [None] * len(_fields_2)
            # gather fields
            gathered_table += row_1_data + row_2_data

        # add blank right index
        for index_row_2 in temporary_index_right:
            row_2_data = get_fields(table2, _fields_2, index_row_2)
            # fill with None
            row_1_data = [None] * len(_fields_1)
            # gather fields
            gathered_table += row_1_data + row_2_data
        # return completed table
        return gathered_table


class RelationalTableController(object):
    def __init__(self, slave, master, master_view=None, slave_view=None):
        # check values
        if isinstance(slave, TableController):
            self.__controller_slave = slave
        elif isinstance(slave, DatabaseTableModel):
            self.__controller_slave = TableController(slave)
        else:
            raise ValueError("Values must be models or controllers: {0}".format(slave))
        if isinstance(master, TableController):
            self.__controller_master = master
        elif isinstance(master, DatabaseTableModel):
            self.__controller_master = TableController(master)
        else:
            raise ValueError("Values must be models or controllers: {0}".format(master))
        self.__view_master = master_view
        self.__view_slave = slave_view

    # getters
    def get_item_master(self, index, name):
        return self.__controller_master.get_item(index, name)

    def get_item_slave(self, index, name):
        return self.__controller_slave.get_item(index, name)

    # setters
    def set_item_master(self, index, name):
        self.__controller_master.set_item(index, name)

    def set_item_slave(self, index, name):
        self.__controller_slave.set_item(index, name)

    # visual
    def update_view_master(self):
        self.__view_master.update()

    def update_view_slave(self):
        self.__view_slave.update()
