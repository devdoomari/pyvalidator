import unittest
from unittest_extension import ErrorBucketTestCase
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from errorbucket import ErrorBucket
from validator import Validator
from errors import WrongType


class TestIterableSchema(ErrorBucketTestCase):
    def test_str_single_literal(self):
        str_validator = Validator([str])
        test_data = ['hello']
        str_validator.validate(test_data)

    def test_str_multiple_literal_ok(self):
        str_validator = Validator([str])
        test_data = ['hello', 'oh no', 'wow so', 'doge']
        str_validator.validate(test_data)

    def test_str_list_one_int(self):
        str_validator = Validator([str])
        test_data = ['hello', 'oh no', 777, 'doge']
        self.assertErrorBucket(
            str_validator, test_data,
            errors={'wrong_type': {'2': WrongType(int, str)}})

    def test_not_list(self):
        int_data = 1234
        str_validator = Validator([str])
        self.assertErrorBucket(
            str_validator, int_data,
            errors={'wrong_type': {'': WrongType(list, int)}})


if __name__ == '__main__':
    unittest.main()
