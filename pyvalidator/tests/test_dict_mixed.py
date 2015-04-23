import unittest
from unittest_extension import ErrorBucketTestCase
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from errorbucket import ErrorBucket
from validator import Validator, Optional, CustomMissingkeyError
from validator import And, Using
from errors import WrongType, FuncFail, SurplusKey, MissingKey
from utils import OrderedList


class TestDictMixedSchema(ErrorBucketTestCase):
    def test_mixed_dict(self):
        schema = {
            Optional('hello'): 'world',
            'wow so': 'doge',
            'some int': int,
            'nested_dict': {'nest': 'le'},
            'customerr': CustomMissingkeyError('MISSINGKEY T.T', str)
        }
        validator = Validator(schema)
        self.assertErrorBucket(
            validator, {
                'wow so': 'doge',
                'some int': 'not int',
                'nested_dict': [123, 456],
            },
            errors={
                'wrong_type': {
                    'some int': WrongType(str, int),
                    'nested_dict': WrongType(list, dict)
                },
                'missing_key': {'customerr': MissingKey('customerr', str)}
            },
            custom_errors=['MISSINGKEY T.T'])

    def test_mixed_schema_readme1(self):
        validator = Validator({
            'name': And(str, len),
            'age': And(Using(int), lambda n: 18 <= n <= 99),
            Optional('sex'): And(str, Using(str.lower), lambda s: s in
                                 ('male', 'female'))
        })
        validator.validate({'name': 'Sue', 'age': '28', 'sex': 'FEMALE'})
        validator.validate({'name': 'Sam', 'age': '42'})
        validator.validate({'name': 'Sacha', 'age': '20', 'sex': 'Male'})


if __name__ == '__main__':
    unittest.main()
