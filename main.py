'''Main file'''
from database import TableDouble

def test_fn_1():
    """Docstring"""
    test_1 = TableDouble(['John doe', 'test1'])
    test_1.add(1000000000000000000, "lol")
    print test_1

test_fn_1()
