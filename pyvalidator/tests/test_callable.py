import unittest
from unittest_extension import ErrorBucketTestCase
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from errorbucket import ErrorBucket
from validator import Validator
from errors import WrongType, FuncFail


class TestCallableSchema(ErrorBucketTestCase):
    def test_always_true_callable(self):
        test_data = 'hello world'

        def return_true(input):
            return True

        always_true_validator = Validator(return_true)
        always_true_validator.validate(test_data)

    def test_always_false_callable(self):
        test_data = 'hello world!'

        def return_false(input):
            return False

        always_false_validator = Validator(return_false)
        self.assertErrorBucket(
            always_false_validator, test_data,
            errors={'func_fail': {'': FuncFail(return_false, test_data)}})

    def test_is_dict_callable(self):
        ok_data = {'wow': 'so gukky'}
        nope_data = ['wow', 'so listy']

        def is_dict(input):
            return type(input) == dict

        is_dict_validator = Validator(is_dict)
        is_dict_validator.validate(ok_data)

        self.assertErrorBucket(
            is_dict_validator, nope_data,
            errors={'func_fail': {'': FuncFail(is_dict, nope_data)}})


if __name__ == '__main__':
    unittest.main()
