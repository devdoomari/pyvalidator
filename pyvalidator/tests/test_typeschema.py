import unittest
from unittest_extension import ErrorBucketTestCase
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from errorbucket import ErrorBucket
from validator import Validator
from errors import WrongType


class TestTypeSchema(ErrorBucketTestCase):
    def test_str(self):
        str_validator = Validator(str)
        test_data = 'hello'
        str_validator.validate(test_data)
        test_error_data = 1234
        self.assertErrorBucket(
            str_validator, test_error_data,
            errors={'wrong_type': {'': WrongType(int, str)}})


if __name__ == '__main__':
    unittest.main()
