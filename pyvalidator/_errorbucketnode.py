class _ErrorBucketNode(object):
    def __init__(self, _errors=None, _error_dict=None):
        self.errors = _errors or []
        self.error_dict = _error_dict or {}

    def __eq__(self, other):
        if type(self) is not type(other):
            return False
        try:
            self.errors.sort()
            other.errors.sort()
        except:
            self_errors_set = set(self.errors)
            self.errors = list(self_errors_set)
            other_errors_set = set(other.errors)
            other.errors = list(other_errors_set)
        return (self.errors == other.errors) and self.error_dict == other.error_dict

    def __getitem__(self, key):
        return self.error_dict[key]

    def __setitem__(self, key, value):
        self.error_dict[key] = value

    def __contains__(self, key):
        return key in self.error_dict

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        if self.errors == [] and self.error_dict == {}:
            return "<NoError>"
        elif self.errors != [] and self.error_dict == {}:
            return "{0}".format(self.errors)
        elif self.errors == [] and self.error_dict != {}:
            return str(self.error_dict)
        else:
            return "{0} + {1}".format(self.errors, self.error_dict)

    def merge(self, other, recursion_nth=0):
        assert type(self) is type(other),\
            "Wrong type: got {0} instead of {1}".format(type(other), type(self))
        self.errors.extend(other.errors)
        for other_key in other.error_dict:
            if other_key not in self.error_dict:
                self.error_dict[other_key] = _ErrorBucketNode()
            self.error_dict[other_key].merge(other.error_dict[other_key], recursion_nth+1)
            

    def is_empty(self):
        return self.errors == [] and self.error_dict == {}
