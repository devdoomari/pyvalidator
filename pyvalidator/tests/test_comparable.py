import unittest
from unittest_extension import ErrorBucketTestCase
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from errorbucket import ErrorBucket
from validator import Validator, And
from errors import NotEqual
from utils import OrderedList


class TestComparableSchema(ErrorBucketTestCase):
    def test_str(self):

        hello_validator = Validator('hello')
        hello_validator.validate('hello')
        self.assertErrorBucket(
            hello_validator, 'Not hello',
            errors={'not_equal': {'': NotEqual('hello', 'Not hello')}})

    def test_int(self):
        hello_validator = Validator('hello')
        hello_validator.validate('hello')
        self.assertErrorBucket(
            hello_validator, 'Not hello',
            errors={'not_equal': {'': NotEqual('hello', 'Not hello')}})


if __name__ == '__main__':
    unittest.main()
