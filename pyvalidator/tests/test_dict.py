import unittest
from unittest_extension import ErrorBucketTestCase
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from errorbucket import ErrorBucket
from validator import Validator, Optional, CustomMissingkeyError
from errors import WrongType, FuncFail, SurplusKey, MissingKey
from utils import OrderedList


class TestDictSchema(ErrorBucketTestCase):
    def test_simple(self):

        simple_validator = Validator({'test': 'hello'})
        simple_validator.validate({'test': 'hello'})

        simple_validator2 = Validator({'test': 'hello', 'wow so': 'doge'})
        simple_validator2.validate({'test': 'hello', 'wow so': 'doge'})

    def test_surplus(self):
        simple_validator = Validator({'test': 'hello'})
        self.assertErrorBucket(
            simple_validator, {'test': 'hello',
                               'wow so': 'doge'},
            errors={'surplus_key': {'wow so': SurplusKey('wow so', 'doge')}})

    def test_missing(self):
        simple_validator = Validator({'test': 'hello'})
        self.assertErrorBucket(
            simple_validator, {},
            errors={'missing_key': {'test': MissingKey('test', 'hello')}})

    def test_missing_custom_error(self):
        validator = Validator(
            {'test': CustomMissingkeyError('MISSINGKEY!', 'hello')})
        self.assertErrorBucket(
            validator, {},
            errors={'missing_key': {'test': MissingKey('test', 'hello')}},
            custom_errors=['MISSINGKEY!'])

    def test_optional_simple(self):
        validator = Validator({Optional('hello'): 'world'})
        data = validator.validate({})


if __name__ == '__main__':
    unittest.main()
