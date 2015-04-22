import unittest
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from errorbucket import ErrorBucket
from validator import Validator
from errors import WrongType, FuncFail


class TestCallableSchema(unittest.TestCase):
    def test_always_true_callable(self):
        test_data = 'hello world'

        def return_true(input):
            return True

        always_true_validator = Validator(return_true)
        self.assertTrue(
            always_true_validator.validate(test_data).isEmpty()
        )

    def test_always_false_callable(self):
        test_data = 'hello world!'

        def return_false(input):
            return False

        always_false_validator = Validator(return_false)
        bucket = always_false_validator.validate(test_data)
        self.assertEquals(bucket.errors, {
            'func_fail': {
                '': FuncFail(return_false, test_data)
                }
            })

    def test_is_dict_callable(self):
        ok_data = {'wow': 'so gukky'}
        nope_data = ['wow', 'so listy']

        def is_dict(input):
            return type(input) == dict

        is_dict_validator = Validator(is_dict)
        self.assertTrue(
            is_dict_validator.validate(ok_data).isEmpty())

        bucket = is_dict_validator.validate(nope_data)
        self.assertEquals(bucket.errors, {
            'func_fail': {
                '': FuncFail(is_dict, nope_data)
                }
            })

if __name__ == '__main__':
    unittest.main()