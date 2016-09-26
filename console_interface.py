'Console Interface Module'
from types import *
import sys

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


class Menu:
    """Generic simple editable menu which stores entries in dict"""

    def __init__(self, init_data, init_data_fn, init_index = None, name="Menu"):
        """Init method.
         init_data should contain a list of string names of options"""
        # custom index
        _index = init_index
        if _index is None:
            _index = range(len(init_data))
        # dict creation
        self.data = dict(zip(_index,
                             map(lambda x, y: MenuEntry(x, y), init_data, init_data_fn)))
        # add exit option
        self.data["exit"] =  MenuEntry("Exit", sys.exit)
        self.name = name

    def call_entry(self, key):
        """Calling entry fn by key"""
        if key in self.data.keys():
            return self.data[key].fn()
        else:
            return None

    def __str__(self):
        """String representation"""
        return "- " + self.name + " -\n" \
               + "".join(map(lambda x: str(x[0]) + ": " + str(x[1]) + "\n",
                             sorted(self.data.items())))

if __name__ == '__main__':
    def dummy():
        print "YES!"
    test_2 = Menu(["Entry1", "Entry2"], [dummy, dummy], ["a", "b"], "Custom Menu")
    print test_2
    test_2.call_entry("a")
    test_2.call_entry("exit")
    # code below is unreachable
    test_2.call_entry("b")