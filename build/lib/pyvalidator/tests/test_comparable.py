import unittest
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from errorbucket import ErrorBucket
from validator import Validator, And
from errors import NotEqual
from utils import OrderedList


class TestComparableSchema(unittest.TestCase):
    def test_str(self):

        hello_validator = Validator('hello')
        self.assertTrue(hello_validator.validate('hello').isEmpty())
        error_bucket = hello_validator.validate('Not hello')
        self.assertEquals(error_bucket.errors,
                          {'not_equal': {'': NotEqual('hello', 'Not hello')}})

    def test_int(self):
        hello_validator = Validator('hello')
        self.assertTrue(hello_validator.validate('hello').isEmpty())
        error_bucket = hello_validator.validate('Not hello')
        self.assertEquals(error_bucket.errors,
                          {'not_equal': {'': NotEqual('hello', 'Not hello')}})

if __name__ == '__main__':
    unittest.main()
