import unittest
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from errorbucket import ErrorBucket
from validator import Validator, And
from errors import NotEqual
from utils import OrderedList


class TestComparableSchema(unittest.TestCase):
    def test_str(self):

        hello_validator = Validator('hello')
        self.assertTrue(
            hello_validator.validate('hello').isEmpty()
        )
        error_bucket = hello_validator.validate('Not hello')
        self.assertEquals(error_bucket.errors,
                          {'not_equal', {'': NotEqual('hello',
                                                      'Not hello')
                                         }
                           }
                          )
        # errorbucket = lt7_validator.validate('solongmorethan7')
        # self.assertEquals(errorbucket.errors,
        #                   {'func_fail':
        #                       {'': FuncFail(len_lt_7, 'solongmorethan7')}
        #                    })
        # lt7_falsy_validator = Validator(And(always_true,
        #                                     always_false,
        #                                     len_lt_7))
        # errorbucket = lt7_falsy_validator.validate('solongmorethan7')
        # self.assertEquals(errorbucket.errors,
        #                   {'func_fail':
        #                       {'': OrderedList(
        #                        FuncFail(len_lt_7, 'solongmorethan7'),
        #                        FuncFail(always_false, 'solongmorethan7'))
        #                        }
        #                    })
        #                    
      
if __name__ == '__main__':
    unittest.main()