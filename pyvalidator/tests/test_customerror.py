import unittest
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

try:
    from unittest_extension import ErrorBucketTestCase
    from errorbucket import ErrorBucket
    from _errorbucketnode import _ErrorBucketNode as _EBN
    from validator import Validator, And, CustomError
    from errors import NotEqual
    from utils import OrderedList
except:
    from .unittest_extension import ErrorBucketTestCase
    from ..errorbucket import ErrorBucket
    from .._errorbucketnode import _ErrorBucketNode as _EBN
    from ..validator import Validator, And, CustomError
    from ..errors import NotEqual
    from ..utils import OrderedList


class TestCustomErrorSchema(ErrorBucketTestCase):
    def test_custom_error(self):
        class SomeCustomError:
            def __eq__(self, other):
                return True

        hello_validator = Validator(CustomError(SomeCustomError, 'hello'))
        self.assertErrorBucket(
            hello_validator, 'Not hello',
            errors={'not_equal': _EBN([NotEqual('hello', 'Not hello')])},
            custom_errors=[SomeCustomError])


if __name__ == '__main__':
    unittest.main()
