import unittest
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from errorbucket import ErrorBucket
from validator import Validator, Optional, CustomMissingkeyError
from errors import WrongType, FuncFail, SurplusKey, MissingKey
from utils import OrderedList


class TestDictSchema(unittest.TestCase):
    def test_simple(self):

        simple_validator = Validator({'test': 'hello'})
        self.assertTrue(simple_validator.validate({'test': 'hello'}).isEmpty())

        simple_validator2 = Validator({'test': 'hello', 'wow so': 'doge'})
        self.assertTrue(simple_validator2.validate(
            {'test': 'hello',
             'wow so': 'doge'}).isEmpty())

    def test_surplus(self):
        simple_validator = Validator({'test': 'hello'})
        error_bucket = simple_validator.validate(
            {'test': 'hello',
             'wow so': 'doge'})
        self.assertEquals(error_bucket.errors,
                          {'surplus_key': {'': SurplusKey('wow so', 'doge')}})

    def test_missing(self):
        simple_validator = Validator({'test': 'hello'})
        error_bucket = simple_validator.validate({})
        self.assertEquals(error_bucket.errors,
                          {'missing_key': {'': MissingKey('test', 'hello')}})

    def test_missing_custom_error(self):
        validator = Validator(
            {'test': CustomMissingkeyError('MISSINGKEY!', 'hello')})
        error_bucket = validator.validate({})
        self.assertEquals(error_bucket.errors,
                          {'missing_key': {'': MissingKey('test', 'hello')}})
        self.assertEquals(error_bucket.custom_errors, ['MISSINGKEY!'])

    def test_optional_simple(self):
        validator = Validator({
            Optional('hello'): 'world'
            })
        error_bucket = validator.validate({})
        self.assertTrue(error_bucket.isEmpty())

    def test_arrayin_dict(self):
        schema = {
            'test': 'wow'
        }

    def test_mixed_dict(self):
        schema = {
            Optional('hello'): 'world',
            'wow so': 'doge',
            'some int': int,
            'nested_dict': {'nest': 'le'},
            'customerr': CustomMissingkeyError('MISSINGKEY', str)
        }
        validator = Validator(schema)
        error_bucket = validator.validate({
            'wow so': 'doge',
            'some int': 'not int',
            'nested_dict': [123, 456],
        })
        self.assertEquals(error_bucket.errors, {
            'wrong_type': {
                'some int': WrongType(str, int),
                'nested_dict': WrongType(list, dict)
            },
            'missing_key': {'': MissingKey('customerr', str)}
        })


if __name__ == '__main__':
    unittest.main()
