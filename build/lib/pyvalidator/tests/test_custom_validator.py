import unittest
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from errorbucket import ErrorBucket
from validator import Validator
from errors import WrongType
from utils import OrderedList


class TestCustomValidatorSchema(unittest.TestCase):
    def test_error_count_validator(self):
        class ErrorCounter(object):
            def __init__(self, *args, **kw):
                self._args = args

            def __repr__(self):
                return '%s(%s)' \
                    % (self.__class__.__name__,
                       ', '.join(repr(a) for a in self._args))

            def validate(self, data):
                error_bucket = ErrorBucket()
                for child_schema in self._args:
                    child_validator = Validator(child_schema)
                    child_error_bucket = child_validator.validate(data)
                    try:
                        error_bucket.mergeBucket(child_error_bucket)
                    except Exception as e:
                        raise e
                count = error_bucket.countErrors()
                error_bucket.addCustomError({'error_count': count})
                return error_bucket

        schema = ErrorCounter(str, int, float)
        custom_validator = Validator(schema)
        error_bucket = custom_validator.validate('Some data')
        self.assertEquals(error_bucket.countErrors(), 2)
        temp = {
            'wrong_type': {
                '': OrderedList(WrongType(str, float),
                                WrongType(str, int))
            }
        }
        self.assertEquals(error_bucket.errors, {
            'wrong_type': {
                '': OrderedList(WrongType(str, float),
                                WrongType(str, int))
            }
        })

    def test_transparent_validator(self):
        pass

if __name__ == '__main__':
    unittest.main()
