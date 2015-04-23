import unittest
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from errorbucket import ErrorBucket
from utils import OrderedList


class ErrorBucketTestCase(unittest.TestCase):
    def assertErrorBucket(self, validator, data,
                          errors=None,
                          custom_errors=None,
                          debug=False):
        try:
            test_data = validator.validate(data)
        except ErrorBucket as error_bucket:
            if debug is True:
                import pdb
                pdb.set_trace()
            if errors is not None:
                self.assertEquals(error_bucket.errors, errors)
            if custom_errors is not None:
                other_custom_errors = OrderedList(error_bucket.custom_errors)
                custom_errors = OrderedList(custom_errors)
                self.assertEquals(other_custom_errors, custom_errors)
        else:
            raise "Error: Expected exception but did not get one"
