import unittest2 as unittest
import warnings
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

try:
    from unittest_extension import ErrorBucketTestCase
    from errorbucket import ErrorBucket
    from _errorbucketnode import _ErrorBucketNode as _EBN
    from validator import Validator, And
    from errors import FuncFail
    from utils import OrderedList
except:
    from .unittest_extension import ErrorBucketTestCase
    from ..errorbucket import ErrorBucket
    from .._errorbucketnode import _ErrorBucketNode as _EBN
    from ..validator import Validator, And
    from ..errors import FuncFail
    from ..utils import OrderedList


class TestAndSchema(ErrorBucketTestCase):
    def setUp(self):
        def always_true(data):
            return True

        def len_lt_7(data):
            return len(data) < 7

        def always_false(data):
            return False

        self.always_true = always_true
        self.always_false = always_false
        self.len_lt_7 = len_lt_7

    def test_and_truthy(self):

        lt7_validator = Validator(And(self.always_true, self.len_lt_7))
        self.assertErrorBucket(
            lt7_validator, 'solongmorethan7',
            errors=
            {'func_fail': _EBN([FuncFail(self.len_lt_7, 'solongmorethan7')])},
            debug=False)

    def test_and_falsy(self):
        lt7_falsy_validator = Validator(And(self.always_true,
                                            self.always_false, self.len_lt_7))
        self.assertErrorBucket(
            lt7_falsy_validator, 'solongmorethan7',
            errors={
                'func_fail': _EBN([FuncFail(self.len_lt_7, 'solongmorethan7'),
                                   FuncFail(self.always_false, 'solongmorethan7')])
            },
            debug=True)


if __name__ == '__main__':
    unittest.main()
