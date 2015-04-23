import unittest
from unittest_extension import ErrorBucketTestCase
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from errorbucket import ErrorBucket
from validator import Validator, Or
from errors import WrongType, FuncFail
from utils import OrderedList


class TestOrSchema(ErrorBucketTestCase):
    def test_or(self):
        def always_true(data):
            return True

        def len_lt_7(data):
            return len(data) < 7

        def always_false(data):
            return False

        lt7_truthy_validator = Validator(Or(always_true, len_lt_7))
        lt7_truthy_validator.validate('hello')
        lt7_truthy_validator.validate('solongmorethan7')
        lt7_falsy_validator = Validator(Or(always_false, len_lt_7))
        self.assertErrorBucket(
            lt7_falsy_validator, 'solongmorethan7',
            errors={
                'func_fail': {
                    '': OrderedList(FuncFail(len_lt_7, 'solongmorethan7'),
                                    FuncFail(always_false, 'solongmorethan7'))
                }
            })


if __name__ == '__main__':
    unittest.main()
