import unittest
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from errorbucket import ErrorBucket
from validator import Validator
from errors import WrongType


class TestTypeSchema(unittest.TestCase):
    def test_str(self):
        str_validator = Validator(str)
        test_data = 'hello'
        self.assertTrue(
            str_validator.validate(test_data).isEmpty()
        )
        test_error_data = 1234
        bucket = str_validator.validate(test_error_data)
        self.assertEquals(
            bucket.errors, {
                'wrong_type': {
                    '': WrongType(int, str)
                }
            })

if __name__ == '__main__':
    unittest.main()