from errors import NotEqual, WrongType
from errors import SurplusKey, MissingKey
from errors import FuncFail, FuncException
from utils import OrderedList
from errorbucket import ErrorBucket

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
            try:
                temp_data = child_validator.validate(data)
            except ErrorBucket as e:
                error_bucket.mergeBucket(e)
        if not error_bucket.isEmpty():
            raise error_bucket
        return data


class Or(And):
    def validate(self, data):
        child_validators = []
        error_bucket = ErrorBucket()
        min_pass = False
        for child_schema in self._args:
            child_validator = Validator(child_schema)
            try:
                temp_data = child_validator.validate(data)
            except ErrorBucket as e:
                error_bucket.mergeBucket(e)
            else:
                min_pass = True
        if not min_pass:
            raise error_bucket
        return data


class Using(object):
    def __init__(self, func, schema):
        self.func = func
        self.schema = schema

    def validate(self, data):
        error_bucket = ErrorBucket()
        try:
            data = self.func(data)
        except Exception as e:
            error = FuncException(self.func, data, e)
            error_bucket.addError('', error)
            raise error_bucket
        validator = Validator(self.schema)
        try:
            data = validator.validate(data)
        except ErrorBucket as e:
            error_bucket.mergeBucket(e)
            raise error_bucket
        return data


class CustomError(object):
    def __init__(self, schema, custom_error):
        self.schema = schema
        self.custom_error = custom_error

    def validate(self, data):
        error_bucket = ErrorBucket()
        validator = Validator(self.schema)
        try:
            data = validator.validate(data)
        except ErrorBucket as e:
            error_bucket.mergeBucket(e)
            error_bucket.addCustomError(self.custom_error)
            raise error_bucket
        return data


class Optional(object):
    def __init__(self, key):
        self.key = key


class CustomMissingkeyError(object):
    def __init__(self, custom_error, schema):
        self.schema = schema
        self.custom_error = custom_error

    def validate(self, data):
        validator = Validator(self.schema)
        try:
            data = validator.validate(data)
        except ErrorBucket as e:
            raise e
        return data


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
            raise error_bucket
        return data

    def _validate_iterable(self, data):
        child_schema = self._schema[0]
        child_validator = Validator(child_schema)
        error_bucket = ErrorBucket()
        if schema_type(data) is not ITERABLE:
            error = WrongType(type(self._schema), type(data))
            error_bucket.addError('', error)
            raise error_bucket
        for (child_index, child_item) in enumerate(data):
            try:
                data[child_index] = child_validator.validate(child_item)
            except ErrorBucket as e:
                error_bucket.__mergeBucket__(e, child_index)
        if not error_bucket.isEmpty():
            raise error_bucket
        return data

    def _validate_dict(self, data_dict):
        error_bucket = ErrorBucket()
        if schema_type(data_dict) is not DICT:
            error = WrongType(type(data_dict), type(self._schema))
            error_bucket.addError('', error)
            raise error_bucket
        requires = {}
        missing_keys = []
        optionals = {}
        surplus_data = {}
        # 1. parse self._schema
        for schema_key in self._schema:
            schema_item = self._schema[schema_key]
            if type(schema_key) == Optional:
                optionals[schema_key.key] = schema_item
            else:
                missing_keys.append(schema_key)
                requires[schema_key] = schema_item
        # 2. validate data.
        for data_key in data_dict:
            data_item = data_dict[data_key]
            if data_key in missing_keys:
                missing_keys.remove(data_key)
                child_validator = Validator(requires[data_key])
                try:
                    data_dict[data_key] = child_validator.validate(data_item)
                except ErrorBucket as e:
                    error_bucket.__mergeBucket__(e, data_key)
            else:
                surplus_data[data_key] = data_item
                for (optional_data, optionals_key) in enumerate(optionals):
                    optional_key_tester = Validator(optionals_key)
                    try:
                        optional_key_temp = optional_key_tester.validate(data_key)
                    except ErrorBucket as e:
                        pass
                    else:
                        del surplus_data[data_key]
                        child_validator = Validator(optional_data)
                        try:
                            data_dict[data_key] = child_validator.validate(
                                data_item)
                        except ErrorBucket as e:
                            error_bucket.__mergeBucket__(e, data_key)
        # 3. raise errors on surplus
        for surplus_key in surplus_data:
            surplus_item = surplus_data[surplus_key]
            error = SurplusKey(surplus_key, surplus_item)
            error_bucket.addError('', error)
        # 4. raise errors on missing_keys
        for missing_key in missing_keys:
            missing_item = requires[missing_key]
            if type(missing_item) == CustomMissingkeyError:
                error_bucket.addCustomError(missing_item.custom_error)
                error = MissingKey(missing_key, missing_item.schema)
            else:
                error = error = MissingKey(missing_key, missing_item)
            error_bucket.addError('', error)
        if not error_bucket.isEmpty():
            raise error_bucket
        return data_dict

    def _validate_type(self, data):
        error_bucket = ErrorBucket()
        if not isinstance(data, self._schema):
            child_type = str(type(data))
            error = WrongType(type(data), self._schema)
            error_bucket.addError('', error)
        if not error_bucket.isEmpty():
            raise error_bucket
        return data

    def _valiate_validator(self, data):
        error_bucket = ErrorBucket()
        try:
            data = self._schema.validate(data)
        except ErrorBucket as e:
            error_bucket.mergeBucket(e)
        if not error_bucket.isEmpty():
            raise error_bucket
        return data

    def _validate_callable(self, data):
        error_bucket = ErrorBucket()
        result = False
        try:
            result = self._schema(data)
        except Exception as e:
            error = FuncException(self._schema, data, e)
            error_bucket.addError('', error)
        if not result:
            error = FuncFail(self._schema, data)
            error_bucket.addError('', error)
        if not error_bucket.isEmpty():
            raise error_bucket
        return data

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

        if self._schema_type == DICT:
            return self._validate_dict(data)
