import unittest
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

try:
    from unittest_extension import ErrorBucketTestCase
    from errorbucket import ErrorBucket
    from _errorbucketnode import _ErrorBucketNode as _EBN
    from validator import Validator, And
    from errors import NotEqual
    from utils import OrderedList
except:
    from .unittest_extension import ErrorBucketTestCase
    from ..errorbucket import ErrorBucket
    from .._errorbucketnode import _ErrorBucketNode as _EBN
    from ..validator import Validator, And
    from ..errors import NotEqual
    from ..utils import OrderedList


class TestComparableSchema(ErrorBucketTestCase):
    def test_str(self):

        hello_validator = Validator('hello')
        hello_validator.validate('hello')
        self.assertErrorBucket(
            hello_validator, 'Not hello',
            errors={'not_equal': _EBN([NotEqual('hello', 'Not hello')])},
            debug=True)

    def test_int(self):
        hello_validator = Validator('hello')
        hello_validator.validate('hello')
        self.assertErrorBucket(
            hello_validator, 'Not hello',
            errors={'not_equal': _EBN([NotEqual('hello', 'Not hello')])})


if __name__ == '__main__':
    unittest.main()
