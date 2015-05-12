import unittest
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

try:
    from unittest_extension import ErrorBucketTestCase
    from errorbucket import ErrorBucket
    from _errorbucketnode import _ErrorBucketNode as _EBN
    from validator import Validator
    from errors import WrongType
except:
    from .unittest_extension import ErrorBucketTestCase
    from ..errorbucket import ErrorBucket
    from .._errorbucketnode import _ErrorBucketNode as _EBN
    from ..validator import Validator
    from ..errors import WrongType


class TestTypeSchema(ErrorBucketTestCase):
    def test_str(self):
        str_validator = Validator(str)
        test_data = 'hello'
        str_validator.validate(test_data)
        test_error_data = 1234
        self.assertErrorBucket(
            str_validator, test_error_data,
            errors={'wrong_type': _EBN([WrongType(int, str)])})


if __name__ == '__main__':
    unittest.main()
