import pprint
try:
    from utils.ordered_list import OrderedList
    from _errorbucketnode import _ErrorBucketNode
except:
    from .utils.ordered_list import OrderedList
    from ._errorbucketnode import _ErrorBucketNode

global __REPR__

__REPR__ = """
Generic Errors:
{0}


Custom Errors:
{1}
"""


class ErrorBucket(Exception):
    def __init__(self):
        self.errors = {}
        self.error_count = 0
        self.custom_errors = []

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        pretty_print = pprint.PrettyPrinter(depth=4)
        generic_errors = pretty_print.pformat(self.errors)
        custom_errors = pretty_print.pformat(self.custom_errors)
        return __REPR__.format(self.errors, self.custom_errors)

    def addError(self, var_name, err_obj):
        self.error_count = self.error_count + 1
        err_type = err_obj.error_name
        if err_type not in self.errors:
            self.errors[err_type] = _ErrorBucketNode()
        if var_name is None:
            self.errors[err_type].errors.append(err_obj)
        else:
            if var_name not in self.errors[err_type]:
                self.errors[err_type][var_name] = _ErrorBucketNode()
            self.errors[err_type][var_name].errors.append(err_obj)

    def addCustomError(self, error):
        self.custom_errors.append(error)

    def mergeChildBucket(self, child, child_namespace):
        child_namespace = child_namespace
        self.__mergeBucket__(child, child_namespace)

    def mergeBucket(self, other):
        self.__mergeBucket__(other)

    def __mergeBucket__(self, other, other_ns=None):
        self.error_count = self.error_count + other.error_count
        for err_type in other.errors:
            if err_type not in self.errors:
                self.errors[err_type] = _ErrorBucketNode()

            if other_ns is not None:
                if other_ns not in self.errors[err_type]:
                    self.errors[err_type][other_ns] = _ErrorBucketNode()
                self.errors[err_type][other_ns].merge(other.errors[err_type])
            else:
                self.errors[err_type].merge(other.errors[err_type])
        self.custom_errors.extend(other.custom_errors)

    def isEmpty(self):
        return self.errors == {} and self.custom_errors == []

    def countErrors(self):
        return self.error_count

    def countCustomErrors(self):
        return len(self.custom_errors)
