import unittest2 as unittest
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from errorbucket import ErrorBucket
from _errorbucketnode import _ErrorBucketNode as _EBN
from utils import OrderedList


class TestErrorBucket(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

        class ErrorType1:
            def __init__(self, text):
                self.error_name = "error_type1"
                self.text = text

            def __eq__(self, other):
                return type(self) == type(other) and self.text == other.text

            def __lt__(self, other):
                return self.text < other.text

            def __gt__(self, other):
                return self.text > other.text

            def __cmp__(self, other):
                if self.__eq__(other):
                    return 0
                elif self.__lt__(other):
                    return -1
                else:
                    return 1

            def __hash__(self):
                return hash(self.error_name) ^ hash(self.text)

            def __repr__(self):
                return "ErrorType1 with text: {0}".format(self.text)

        class ErrorType2:
            def __init__(self, text):
                self.error_name = "error_type2"
                self.text = text

            def __eq__(self, other):
                return type(self) == type(other) and self.text == other.text

            def __lt__(self, other):
                return self.text < other.text

            def __gt__(self, other):
                return self.text > other.text

            def __cmp__(self, other):
                if self.__eq__(other):
                    return 0
                elif self.__lt__(other):
                    return -1
                else:
                    return 1

            def __hash__(self):
                return hash(self.error_name) ^ hash(self.text)

        self.ErrorType1 = ErrorType1
        self.ErrorType2 = ErrorType2

    def tearDown(self):
        pass

    def test_add_error(self):
        bucket = ErrorBucket()
        bucket.addError('somevar', self.ErrorType1('some error occurred!'))
        self.assertEquals(bucket.errors, {
            'error_type1': _EBN(
                None,
                {'somevar': _EBN([self.ErrorType1('some error occurred!')])})
        })

    def test_mergeChildBucket_errors(self):
        # http://i.imgur.com/7CQd4.gif
        bucket1 = ErrorBucket()
        bucket2 = ErrorBucket()
        bucket1.addError('somevar', self.ErrorType1('some error occurred!'))
        bucket2.mergeChildBucket(bucket1, "child1")
        self.assertEquals(bucket2.errors, {
            'error_type1': _EBN(None, {
                'child1': _EBN(None, {
                    'somevar': _EBN([self.ErrorType1('some error occurred!')])
                })
            })
        })

    def test_mergeBucket_errors(self):
        # http://i.imgur.com/7CQd4.gif
        bucket1 = ErrorBucket()
        bucket2 = ErrorBucket()
        bucket1.addError('somevar', self.ErrorType1('some error occurred!'))
        bucket2.mergeBucket(bucket1)
        self.assertEquals(bucket2.errors, {
            'error_type1': _EBN(
                None,
                {'somevar': _EBN([self.ErrorType1('some error occurred!')])})
        })

    def test_mergeBucket_duplicate_errors(self):
        bucket1 = ErrorBucket()
        bucket2 = ErrorBucket()
        bucket1.addError('somevar', self.ErrorType1('some error occurred!'))
        bucket2.addError('somevar', self.ErrorType1('more error!'))
        bucket2.mergeBucket(bucket1)
        self.assertEquals(bucket2.errors, {
            'error_type1': _EBN(None, {
                'somevar': _EBN([self.ErrorType1('some error occurred!'),
                                 self.ErrorType1('more error!')])
            })
        })

    def test_mergeChildBucket_custom(self):
        bucket1 = ErrorBucket()
        bucket2 = ErrorBucket()
        bucket3 = ErrorBucket()
        bucket1.addCustomError('error1')
        bucket2.addCustomError('error2')
        bucket2.mergeChildBucket(bucket1, "child1")
        bucket3.mergeChildBucket(bucket2, "child2")
        self.assertItemsEqual(bucket3.custom_errors, ['error1', 'error2'])

    def test_countError(self):
        bucket1 = ErrorBucket()
        bucket2 = ErrorBucket()
        bucket1.addError('bucket1_var1', self.ErrorType1('some bucket1 error1'))
        bucket1.addError('bucket1_var2', self.ErrorType2('some bucket1 error2'))
        bucket1.addError('bucket1_var3', self.ErrorType2('some bucket1 error3'))
        bucket2.addError('somevar', self.ErrorType1('some error occurred!'))
        bucket2.mergeChildBucket(bucket1, "child1")
        self.assertEquals(bucket2.countErrors(), 4)

    def test_countDuplicateError(self):
        bucket1 = ErrorBucket()
        bucket2 = ErrorBucket()
        bucket1.addError('somevar', self.ErrorType1('some error occurred!'))
        bucket1.addError('somevar', self.ErrorType1('some error2 occurred!'))
        bucket2.addError('somevar', self.ErrorType1('some error3 occurred!'))
        bucket2.mergeChildBucket(bucket1, "child1")
        self.assertEquals(bucket2.countErrors(), 3)

    def test_mergeChildBucketRoot(self):
        bucket1 = ErrorBucket()
        bucket2 = ErrorBucket()
        bucket1.addError(None, self.ErrorType1('some error occurred!'))
        bucket2.addError('somevar', self.ErrorType1('more error!'))
        bucket2.mergeChildBucket(bucket1, 'bucket1')
        self.assertEquals(bucket2.errors, {
            'error_type1': _EBN(None, {
                'somevar': _EBN([self.ErrorType1('more error!')]),
                'bucket1': _EBN([self.ErrorType1('some error occurred!')])
            })
        })


if __name__ == '__main__':
    unittest.main()
