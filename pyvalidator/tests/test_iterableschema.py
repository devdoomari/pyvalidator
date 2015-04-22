import unittest
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from errorbucket import ErrorBucket
from validator import Validator
from errors import WrongType


class TestIterableSchema(unittest.TestCase):
    def test_str_single_literal(self):
        str_validator = Validator([str])
        test_data = ['hello']
        self.assertTrue(str_validator.validate(test_data).isEmpty())

    def test_str_multiple_literal_ok(self):
        str_validator = Validator([str])
        test_data = ['hello', 'oh no', 'wow so', 'doge']
        self.assertTrue(str_validator.validate(test_data).isEmpty())

    def test_str_list_one_int(self):
        str_validator = Validator([str])
        test_data = ['hello', 'oh no', 777, 'doge']
        error_bucket = str_validator.validate(test_data)
        error_expected = WrongType(int, str)
        self.assertEquals(error_bucket.errors,
                          {'wrong_type': {'2': error_expected}})

    def test_not_list(self):
        int_data = 1234
        str_validator = Validator([str])
        bucket = str_validator.validate(int_data)
        self.assertEquals(bucket.errors,
                          {'wrong_type': {'': WrongType(list, int)}})


if __name__ == '__main__':
    unittest.main()
