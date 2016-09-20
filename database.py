'Database module'
from collections import Counter

class TableDouble:
    '''Authors table abstraction class. \ 
Table is assured to contain no duplicates.'''
    def __init__ (self, init_data=[], default_ratio=3):
        'Init function'
        #example data stored: {'Douglas Adams': 1, 'Stephen King': 2}
        #table divisor (1/ratio). Used to print values.
        self.ratio = default_ratio
        #Couter wrapper of dict used to autoincrement values
        self.data = Counter()
        for key in init_data:
            self.data[key] += 1
            
    def add(self, key):
        'Add value to table. Do nothing if it exists'
        if name not in self.data:
            self.data[key] += 1
        
    def find(self, search_key):
        'Find value of a key in table.'
        return self.data[search_key]
    
    def findByID(self, search_value):
        'Find a key by value (slow and linear).'
        for key, value  in self.data.items():
            if value == search_value:
                return name
    
    def remove(self, key):
        'Remove record by name'
        del self.data[key]
        
    def removeByID(self, value):
        'Remove record by identifier'
        del self.data[self.findByID[value]]
        
    def __str__(self):
        'String representation'        
        #get terminal size for better output
        rows, columns = subprocess.check_output(['stty', 'size']).split()
        #divide into 2 columns
        rows_1 = rows // ratio
        rows_2 = rows - rows_1
        result_string = rows * '*' + '\n'
        for name, identifier in self.data.items():
          name_spaces = rows_2 - len(name)) // 2
          id_spaces = (rows_1 - len(str(identifier))) // 2
          result_string += '*' + id_spaces * ' ' + identifier + (id_spaces - 1) + '*'\
            + (name_spaces - 1) + name + (name_spaces - 1) + '*\n' + rows * '*' + '\n'
        return result_string

