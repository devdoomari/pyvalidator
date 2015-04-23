import unittest
from unittest_extension import ErrorBucketTestCase
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from errorbucket import ErrorBucket
from validator import Validator
from errors import WrongType
from utils import OrderedList


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
                {'': OrderedList(WrongType(str, float), WrongType(str, int))}
            },
            custom_errors=[{'error_count': 2}])

    def test_transparent_validator(self):
        pass


if __name__ == '__main__':
    unittest.main()
