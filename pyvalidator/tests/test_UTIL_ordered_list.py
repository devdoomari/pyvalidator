import unittest
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from errorbucket import ErrorBucket
from validator import Validator
from errors import WrongType
from utils import OrderedList


class TestUTILOrderedList(unittest.TestCase):
    def test_add(self):
        olist1 = OrderedList('aaa', 2, 3)
        olist1.add('45', 77)
        olist2 = OrderedList(77, 'aaa', 2, 3, '45')
        self.assertEquals(olist1, olist2)

    def test_append(self):
        olist1 = OrderedList('aaa', 2, 3)
        olist1.append('45', 77)
        olist2 = OrderedList(77, 'aaa', 2, 3, '45')
        self.assertEquals(olist1, olist2)

    def test_add_obj(self):
        olist1 = OrderedList('aaa', {
            'hello': 'world'
        })
        olist2 = OrderedList('aaa', {
            'hello': 'world'
        })
        self.assertEquals(olist1, olist2)

    def test_type(self):
        olist = OrderedList('aaa', 2, 3)
        type(olist)
        self.assertEquals(type(olist), OrderedList)

if __name__ == '__main__':
    unittest.main()