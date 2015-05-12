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
            errors={'wrong_type': _EBN(None,
                {2: _EBN([WrongType(int, str)])}
                )
            })

    def test_not_list(self):
        int_data = 1234
        str_validator = Validator([str])
        self.assertErrorBucket(
            str_validator, int_data,
            errors={'wrong_type': _EBN([WrongType(list, int)])})


if __name__ == '__main__':
    unittest.main()
