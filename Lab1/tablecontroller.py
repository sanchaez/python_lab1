from database import DatabaseTableModel
from tableview import *
from collections import namedtuple


class TableController(object):
    # class defaults

    __default_join_type = 'inner'
    __default_direction = 'full'

    def __init__(self, table, view=SimpleTableView):
        assert isinstance(table, DatabaseTableModel)
        assert issubclass(view, TableView)
        self.__table = table
        self.__view = view

    def get_item(self, index, name):
        return self.__table.get_item(index, name)

    def set_item(self, index, name, value):
        self.__table.set_item(index, name, value)

    def del_row(self, index):
        self.__table.del_row(index)

    def fields(self):
        return self.__table.fields()

    def find(self, values, columns):
        """Finds first matching row by :columns: and :values:"""
        for column in columns:
            for row in self.__table:
                if getattr(row, column) in values:
                    return row

    def update_view(self):
        self.__view.update(self)

    def add_row_visual(self):
        self.__view.add_to_table(self.__table)

    def edit_row_visual(self):
        self.__view.edit_table(self.__table)

    def delete_row_visual(self):
        return self.__view.delete_row(self.__table)

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
            def _filter(x):
                return True

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
        return TableController(gathered_table, self.__view)

    def join(self, other, *args, **kwargs):
        return self.__generic_join(self.__table, other, *args, **kwargs)

    @staticmethod
    def __generic_join(table1, table2, *args, **kwargs):
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


class VisualRelationalTableController(object):
    __relation_class = namedtuple("TableRelation", "master slave")

    def __init__(self, master_controller, slave_controller, foreign_key=None):
        """Init function.
        :type foreign_key: Tuple of 2 values:
            master_column, slave_column - values in slave_column bound to values in master_column
        :type master_controller: TableController
        :type slave_controller: TableController

            """
        # check values
        assert isinstance(slave_controller, TableController)
        self.__controller_slave = slave_controller
        assert isinstance(master_controller, TableController)
        self.__controller_master = master_controller
        self.__relation = self.__relation_class._make(foreign_key)

    # setters
    def add_row_master(self):
        self.__controller_master.add_row_visual()

    def add_row_slave(self):
        # set_row = \
        self.__controller_slave.add_row_visual()
        # found_in_master = self.__controller_master.find(getattr(set_row, getattr(self.__relation, "slave")),
        #                                                getattr(self.__relation, "master"))
        # if found_in_master:
        #    add to table master

    # deletion (visual)
    def delete_slave(self):
        self.__controller_slave.delete_row_visual()

    def delete_master(self):
        deleted_line = self.__controller_master.delete_row_visual()
        # delete matching foreign keys if the row is deleted
        if deleted_line:
            key_to_delete = getattr(deleted_line, self.__relation[0])
            self.__controller_slave = \
                self.__controller_slave.subtable(filter=(lambda x: False if x == key_to_delete else True),
                                                 filter_columns=self.__relation[1])

    def update_view_master(self):
        self.__controller_master.update_view()

    def update_view_slave(self):
        self.__controller_slave.update_view()
