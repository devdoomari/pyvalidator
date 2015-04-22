import unittest
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from errorbucket import ErrorBucket
from utils import OrderedList


class TestErrorBucket(unittest.TestCase):
    def setUp(self):
        class ErrorType1:
            def __init__(self, text):
                self.error_name = "error_type1"
                self.text = text

            def __eq__(self, other):
                return type(self) == type(other) and self.text == other.text

            def __cmp__(self, other):
                if self.text < other.text:
                    return -1
                if self.text > other.text:
                    return 1
                else:
                    return 0

        class ErrorType2:
            def __init__(self, text):
                self.error_name = "error_type2"
                self.text = text

            def __eq__(self, other):
                return type(self) == other and self.text == other.text

            def __cmp__(self, other):
                if self.text < other.text:
                    return -1
                if self.text > other.text:
                    return 1
                else:
                    return 0

        self.ErrorType1 = ErrorType1
        self.ErrorType2 = ErrorType2

    def tearDown(self):
        pass

    def test_add_error(self):
        bucket = ErrorBucket()
        bucket.addError('somevar', self.ErrorType1('some error occurred!'))
        self.assertEquals(bucket.errors, {
            'error_type1': {
                'somevar': self.ErrorType1('some error occurred!')
            }
        })

    def test_mergeChildBucket_errors(self):
        # http://i.imgur.com/7CQd4.gif
        bucket1 = ErrorBucket()
        bucket2 = ErrorBucket()
        bucket1.addError('somevar', self.ErrorType1('some error occurred!'))
        bucket2.mergeChildBucket(bucket1, "child1")
        self.assertEquals(bucket2.errors, {
            'error_type1': {
                'child1.somevar': self.ErrorType1('some error occurred!')
            }
        })

    def test_mergeBucket_errors(self):
        # http://i.imgur.com/7CQd4.gif
        bucket1 = ErrorBucket()
        bucket2 = ErrorBucket()
        bucket1.addError('somevar', self.ErrorType1('some error occurred!'))
        bucket2.mergeBucket(bucket1)
        self.assertEquals(bucket2.errors, {
            'error_type1': {
                'somevar': self.ErrorType1('some error occurred!')
            }
        })

    def test_mergeBucket_duplicate_errors(self):
        bucket1 = ErrorBucket()
        bucket2 = ErrorBucket()
        bucket1.addError('somevar', self.ErrorType1('some error occurred!'))
        bucket2.addError('somevar', self.ErrorType1('more error!'))
        bucket2.mergeBucket(bucket1)
        self.assertEquals(bucket2.errors, {
            'error_type1': {
                'somevar': OrderedList(self.ErrorType1('some error occurred!'),
                                       self.ErrorType1('more error!'))
            }
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
        bucket1.addError('somevar', self.ErrorType1('some error occurred!'))
        bucket1.addError('somevar2', self.ErrorType2('some error2 occurred!'))
        bucket2.addError('somevar', self.ErrorType1('some error occurred!'))
        bucket2.mergeChildBucket(bucket1, "child1")
        self.assertEquals(bucket2.countErrors(), 3)

    def test_countDuplicateError(self):
        bucket1 = ErrorBucket()
        bucket2 = ErrorBucket()
        bucket1.addError('somevar', self.ErrorType1('some error occurred!'))
        bucket1.addError('somevar', self.ErrorType1('some error2 occurred!'))
        bucket2.addError('somevar', self.ErrorType1('some error3 occurred!'))
        bucket2.mergeChildBucket(bucket1, "child1")
        self.assertEquals(bucket2.countErrors(), 3)


if __name__ == '__main__':
    unittest.main()
