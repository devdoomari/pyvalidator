from errorbucket import ErrorBucket
from errors import WrongType, FuncFail, NotEqual

COMPARABLE, CALLABLE, VALIDATOR, TYPE, DICT, ITERABLE = range(6)


class And(object):
    def __init__(self, *args, **kw):
        self._args = args

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__,
                           ', '.join(repr(a) for a in self._args))

    def validate(self, data):
        child_validators = []
        error_bucket = ErrorBucket()
        for child_schema in self._args:
            child_validator = Validator(child_schema)
            child_error_bucket = child_validator.validate(data)
            error_bucket.mergeBucket(child_error_bucket)
        return error_bucket


class Or(And):
    def validate(self, data):
        child_validators = []
        error_bucket = ErrorBucket()
        for child_schema in self._args:
            child_validator = Validator(child_schema)
            child_error_bucket = child_validator.validate(data)
            if child_error_bucket.isEmpty():
                return ErrorBucket()
            error_bucket.mergeBucket(child_error_bucket)
        return error_bucket


class CustomError(object):
    def __init__(self, validator, custom_error):
        self.validator = validator
        self.custom_error = custom_error

    def validate(self, data):
        error_bucket = self.validator.validate(data)
        if not error_bucket.isEmpty():
            error_bucket.addCustomError(self.custom_error)
        return error_bucket

# class CustomMissingkeyError(object):
#     def __init__(self, )


def schema_type(schema):
    """Return priority for a given object."""
    if type(schema) in (list, tuple, set, frozenset):
        return ITERABLE
    if type(schema) is dict:
        return DICT
    if issubclass(type(schema), type):
        return TYPE
    if hasattr(schema, 'validate'):
        return VALIDATOR
    if callable(schema):
        return CALLABLE
    else:
        return COMPARABLE


class Validator(object):
    def __init__(self, schema):
        self._schema = schema
        self._schema_type = schema_type(self._schema)

    def _validate_comparable(self, data):
        error_bucket = ErrorBucket()
        if self._schema != data:
            error = NotEqual(self._schema, data)
            error_bucket.addError('', error)
        return error_bucket

    def _validate_iterable(self, data):
        child_schema = self._schema[0]
        child_validator = Validator(child_schema)
        error_bucket = ErrorBucket()
        if schema_type(data) != ITERABLE:
            error = WrongType(type(self._schema), type(data))
            error_bucket.addError('', error)
            return error_bucket
        for (child_index, child_item) in enumerate(data):
            child_bucket = child_validator.validate(child_item)
            error_bucket.__mergeBucket__(child_bucket, child_index)
        return error_bucket

    def _validate_type(self, data):
        error_bucket = ErrorBucket()
        if not isinstance(data, self._schema):
            child_type = str(type(data))
            error = WrongType(type(data), self._schema)
            error_bucket.addError('', error)
        return error_bucket

    def _valiate_validator(self, data):
        error_bucket = ErrorBucket()
        child_error_bucket = self._schema.validate(data)
        error_bucket.mergeBucket(child_error_bucket)
        return error_bucket

    def _validate_callable(self, data):
        error_bucket = ErrorBucket()
        if not self._schema(data):
            error = FuncFail(self._schema, data)
            error_bucket.addError('', error)
        return error_bucket

    def validate(self, data):
        if self._schema_type == COMPARABLE:
            return self._validate_comparable(data)

        if self._schema_type == ITERABLE:
            return self._validate_iterable(data)

        if self._schema_type == TYPE:
            return self._validate_type(data)

        if self._schema_type == VALIDATOR:
            return self._valiate_validator(data)

        if self._schema_type == CALLABLE:
            return self._validate_callable(data)
