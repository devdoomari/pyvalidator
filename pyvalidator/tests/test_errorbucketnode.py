import unittest2 as unittest
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
try:
    from errors.funcfail import FuncFail
    from errors.funcexception import FuncException
    from errors.wrongtype import WrongType
    from _errorbucketnode import _ErrorBucketNode as _EBN
except:
    from ..errors.funcfail import FuncFail
    from ..errors.funcexception import FuncException
    from ..errors.wrongtype import WrongType
    from .._errorbucketnode import _ErrorBucketNode as _EBN


class TestErrorBucket(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
        pass

    def test_equal_nested_dict(self):
        node1 = _EBN([WrongType(int, str), WrongType(bool, str)], {
            'wow_so_error': _EBN([WrongType(int, str), WrongType(int, float)])
        })
        node2 = _EBN([WrongType(bool, str), WrongType(int, str)], {
            'wow_so_error': _EBN([WrongType(int, float), WrongType(int, str)])
        })
        self.assertEquals(node1, node2)

    def test_merge_bucketnode(self):
        node1 = _EBN([WrongType(int, str), WrongType(bool, str)], {
            'wow_so_error': _EBN([WrongType(int, str), WrongType(int, float)])
        })

        node2 = _EBN([FuncFail(int, "not int")], {
            'much_error': _EBN([WrongType(int, float), WrongType(int, str)]),
            'wow_so_error': _EBN([FuncFail(int, "not int")])
        })
        node1.merge(node2)

        self.assertEquals(node1, _EBN([
            WrongType(int, str), WrongType(bool, str), FuncFail(int, "not int")
        ], {
            'wow_so_error': _EBN([WrongType(int, str), WrongType(int, float),
                                  FuncFail(int, "not int")]),
            'much_error': _EBN([WrongType(int, float), WrongType(int, str)])
        }))
        self.assertEquals(node2, _EBN([FuncFail(int, "not int")], {
            'much_error': _EBN([WrongType(int, float), WrongType(int, str)]),
            'wow_so_error': _EBN([FuncFail(int, "not int")])
        }))


if __name__ == '__main__':
    unittest.main()
