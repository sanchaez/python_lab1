'Database module'


class TableDouble:
    """Authors table abstraction class.
Table is assured to contain no duplicates."""

    def __init__(self, init_data, default_ratio=10):
        """Init function"""
        # example data stored: {'Douglas Adams': 1, 'Stephen King': 2}
        # table divisor (1/ratio). Used to print values.
        self.ratio = default_ratio
        self.data = dict()
        assert isinstance(init_data, object)
        for key in init_data:
            for i in range(1, len(init_data)):
                self.data[key] = 1

    def add(self, key):
        """Add value to table. Do nothing if it exists"""
        if key not in self.data:
            self.data[key] += 1

    def find(self, search_key):
        """Find value of a key in table."""
        return self.data[search_key]

    def find_id(self, search_value):
        """Find a key by value (slow and linear)."""
        for key, value in self.data.items():
            if value == search_value:
                return key
    def filter(self):
        """Add a filter & return TableDouble object"""
    def remove(self, key):
        """Remove record by name"""
        del self.data[key]

    def remove_id(self, value):
        """Remove record by identifier"""
        del self.data[self.find_id(value)]

    def __str__(self):
        """String representation"""
        rows = 40
        # following works in most linux systems:
        # import subprocess
        # rows = int(subprocess.check_output(['stty', 'size']).split()[0])
        # divide into 2 columns
        rows_1 = rows // self.ratio
        rows_2 = rows - rows_1
        result_string = rows * '*' + '\n'
        for name, identifier in self.data.items():
            name_spaces = (rows_2 - len(name)) // 2
            id_spaces = (rows_1 - len(str(identifier))) // 2
            # make a table string
            result_string += ("*" + id_spaces * " " + "%d" + id_spaces * " " + "*"
                             + (name_spaces - 1) * " " + name + name_spaces * " "
                             + "*\n" + (rows * "*") + "\n") % identifier
        return result_string
