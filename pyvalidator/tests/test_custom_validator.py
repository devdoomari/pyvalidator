import unittest
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

try:
    from unittest_extension import ErrorBucketTestCase
    from errorbucket import ErrorBucket
    from _errorbucketnode import _ErrorBucketNode as _EBN
    from validator import Validator
    from errors import WrongType
    from utils import OrderedList
except:
    from .unittest_extension import ErrorBucketTestCase
    from ..errorbucket import ErrorBucket
    from .._errorbucketnode import _ErrorBucketNode as _EBN
    from ..validator import Validator
    from ..errors import WrongType
    from ..utils import OrderedList


class TestCustomValidatorSchema(ErrorBucketTestCase):
    def test_error_count_validator(self):
        class ErrorCounter(object):
            def __init__(self, *args, **kw):
                self._args = args

            def __repr__(self):
                return "ErrorCounter({0})".format(args)

            def validate(self, data):
                error_bucket = ErrorBucket()
                for child_schema in self._args:
                    child_validator = Validator(child_schema)
                    try:
                        temp_data = child_validator.validate(data)
                    except ErrorBucket as child_error_bucket:
                        error_bucket.mergeBucket(child_error_bucket)
                    except Exception as e:
                        raise e
                count = error_bucket.countErrors()
                if not error_bucket.isEmpty():
                    error_bucket.addCustomError({'error_count': count})
                    raise error_bucket
                return data

        schema = ErrorCounter(str, int, float)
        custom_validator = Validator(schema)
        self.assertErrorBucket(
            custom_validator, 'Some data',
            errors={
                'wrong_type':
                _EBN([WrongType(str, float), WrongType(str, int)])
            },
            custom_errors=[{'error_count': 2}],
            debug=True)

    def test_transparent_validator(self):
        pass


if __name__ == '__main__':
    unittest.main()
