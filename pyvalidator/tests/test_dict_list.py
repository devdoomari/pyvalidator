import unittest2 as unittest
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

try:
    from unittest_extension import ErrorBucketTestCase
    from errorbucket import ErrorBucket
    from _errorbucketnode import _ErrorBucketNode as _EBN
    from validator import Validator, Optional, CustomMissingkeyError
    from validator import And, Using
    from errors import WrongType, FuncFail, SurplusKey, MissingKey
    from utils import OrderedList
except:
    from .unittest_extension import ErrorBucketTestCase
    from ..errorbucket import ErrorBucket
    from .._errorbucketnode import _ErrorBucketNode as _EBN
    from ..validator import Validator, Optional, CustomMissingkeyError
    from ..validator import And, Using
    from ..errors import WrongType, FuncFail, SurplusKey, MissingKey
    from ..utils import OrderedList

class TestDictList(ErrorBucketTestCase):
    def test_dict_list1(self):
        validator = Validator([{
            'name': And(str, len),
            'age': And(Using(int), lambda n: 18 <= n <= 99),
            Optional('sex'): And(str, Using(str.lower), lambda s: s in
                                 ('male', 'female'))
        }])

        data = [{'name': 'Sue',
                 'age': '28',
                 'sex': 'FEMALE'}, {'name': 'Sam',
                                    'age': '42'},
                {'name': 'Sacha',
                 'age': '20',
                 'sex': 'Male'}]
        validated = validator.validate(data)
        assert validated == [{'name': 'Sue',
                              'age': 28,
                              'sex': 'female'}, {'name': 'Sam',
                                                 'age': 42},
                             {'name': 'Sacha',
                              'age': 20,
                              'sex': 'male'}]

    def test_dict_list2(self):
        is_gender = lambda s: s in ('male', 'female')
        validator = Validator([{
            'name': And(str, len),
            'age': And(Using(int), lambda n: 18 <= n <= 99),
            Optional('sex'): And(str, Using(str.lower), is_gender)
        }])

        data = [{'name': 'Sue',
                 'age': '28',
                 'sex': 'MIDDLE'}, {'name': 'Sam',
                                    'age': '42'},
                {'nameto': 'Sacha',
                 'age': '20',
                 'sex': 'Male'}]
        self.assertErrorBucket(validator, data, errors={
            'func_fail': _EBN(None,
                              {0:_EBN(None,
                                      {'sex': _EBN([FuncFail(is_gender, 'middle')])}
                                      )}
                              ),
            'surplus_key': _EBN(None,
                                {2:_EBN(None, 
                                        {'nameto': _EBN([SurplusKey('nameto', 'Sacha')])
                                        }
                                        )
                                }),
            'missing_key': _EBN(None,
                                {2:_EBN(None,
                                        {'name': _EBN([MissingKey('name', And(str, len))])}
                                        )
                                }
                              )
        }, debug=True)

    def test_dict_list3(self):
        is_gender = lambda s: s in ('male', 'female')
        validator = Validator([{
            'sex': And(str, Using(str.lower), is_gender)
        }])

        data = [{
                 'sex': 'woah not yet'}]
        self.assertErrorBucket(validator, data, errors={
            'func_fail': _EBN(None,
                              {0:_EBN(None, 
                                      {'sex': _EBN([FuncFail(is_gender, 'woah not yet')])}
                                      )}
                              )
        }, debug=True)

if __name__ == '__main__':
    unittest.main()
