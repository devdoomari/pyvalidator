import unittest
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from errorbucket import ErrorBucket
from validator import Validator, Or
from errors import WrongType, FuncFail
from utils import OrderedList


class TestOrSchema(unittest.TestCase):
    def test_or(self):
        def always_true(data):
            return True

        def len_lt_7(data):
            return len(data) < 7

        def always_false(data):
            return False

        lt7_truthy_validator = Validator(Or(always_true, len_lt_7))
        self.assertTrue(lt7_truthy_validator.validate('hello').isEmpty())
        errorbucket = lt7_truthy_validator.validate('solongmorethan7')
        self.assertTrue(errorbucket.isEmpty())
        lt7_falsy_validator = Validator(Or(always_false,
                                           len_lt_7))
        errorbucket = lt7_falsy_validator.validate('solongmorethan7')
        self.assertEquals(errorbucket.errors, {
            'func_fail': {
                '': OrderedList(FuncFail(len_lt_7, 'solongmorethan7'),
                                FuncFail(always_false, 'solongmorethan7'))
            }
        })


if __name__ == '__main__':
    unittest.main()
