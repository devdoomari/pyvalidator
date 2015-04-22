import unittest
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from errorbucket import ErrorBucket
from validator import Validator, CustomMissingkeyError
from errors import WrongType, FuncFail, SurplusKey, MissingKey
from utils import OrderedList


class TestDictSchema(unittest.TestCase):
    # def test_simple(self):

    #     simple_validator = Validator({'test': 'hello'})
    #     self.assertTrue(simple_validator.validate({'test': 'hello'}).isEmpty())

    #     simple_validator2 = Validator({'test': 'hello', 'wow so': 'doge'})
    #     self.assertTrue(simple_validator2.validate(
    #         {'test': 'hello',
    #          'wow so': 'doge'}).isEmpty())

    # def test_surplus(self):
    #     simple_validator = Validator({'test': 'hello'})
    #     error_bucket = simple_validator.validate(
    #         {'test': 'hello',
    #          'wow so': 'doge'})
    #     self.assertEquals(error_bucket.errors,
    #                       {'surplus_key': {'': SurplusKey('wow so', 'doge')}})

    # def test_missing(self):
    #     simple_validator = Validator({'test': 'hello'})
    #     error_bucket = simple_validator.validate({})
    #     self.assertEquals(error_bucket.errors,
    #                       {'missing_key': {'': MissingKey('test', 'hello')}})

    def test_missing_custom_error(self):
        validator = Validator(
            {'test': CustomMissingkeyError('MISSINGKEY!', 'hello')})
        error_bucket = validator.validate({})
        self.assertEquals(error_bucket.errors,
                          {'missing_key': {'': MissingKey('test', 'hello')}})
        self.assertEquals(error_bucket.custom_errors, ['MISSINGKEY!'])


if __name__ == '__main__':
    unittest.main()
