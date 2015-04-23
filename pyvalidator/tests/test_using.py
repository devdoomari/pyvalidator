import unittest
from unittest_extension import ErrorBucketTestCase
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from errorbucket import ErrorBucket
from validator import Validator, Using
from errors import WrongType, FuncFail, FuncException
from utils import OrderedList


class TestUsingSchema(ErrorBucketTestCase):
    def test_typecast(self):
        to_int_validator = Validator(Using(int, 77))
        to_int_validator.validate(77.4)

    def test_const_func(self):
        def return_hello(data):
            return "hello"

        hello_validator = Validator(Using(return_hello, "hello"))
        hello_validator.validate(77.4)

    def test_exception_func(self):
        class SomeException(Exception):
            def __eq__(self, other):
                return True

        def raiser(data):
            raise SomeException()

        exception_validator = Validator(Using(raiser, 'nope'))
        self.assertErrorBucket(
            exception_validator, 'nope',
            errors={
                'func_exception':
                {'': FuncException(raiser, "nope", SomeException())}
            })


if __name__ == '__main__':
    unittest.main()
