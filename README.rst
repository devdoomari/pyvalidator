PyValidator: An improved version of Schema (https://github.com/keleshev/schema)
===============================================================================

**schema** is a library for validating Python data structures, such as those
obtained from config-files, forms, external services or command-line
parsing, converted from JSON/YAML (or something else) to Python data-types.

**PyValidator** is an (almost) drop-in replacement of Python Schema,
written almost from scratch for the sake of better error handling.

**Note: Most of the README here is a small edits on the original Python schema's README**

Examples (From python schema)
----------------------------------------------------------------------------

Here is a quick example to get a feeling of **schema**, validating a list of
entries with personal information:

.. code:: python

    >>> from pyvalidator import Validator, And, Use, Optional

    >>> validator = Validator([{'name': And(str, len),
    ...                   'age':  And(Use(int), lambda n: 18 <= n <= 99),
    ...                   Optional('sex'): And(str, Use(str.lower),
    ...                                        lambda s: s in ('male', 'female'))}])

    >>> data = [{'name': 'Sue', 'age': '28', 'sex': 'FEMALE'},
    ...         {'name': 'Sam', 'age': '42'},
    ...         {'name': 'Sacha', 'age': '20', 'sex': 'Male'}]

    >>> validated = validator.validate(data)

    >>> assert validated == [{'name': 'Sue', 'age': 28, 'sex': 'female'},
    ...                      {'name': 'Sam', 'age': 42},
    ...                      {'name': 'Sacha', 'age' : 20, 'sex': 'male'}]


If data is valid, ``Validator(some schema).validate`` will return the validated data
(optionally converted with `Use` calls, see below).

** Note: Since PyValidator is a drop-in replacement of Python Schema,
        See https://github.com/keleshev/schema for more usage examples.**

PyValidator vs Python Schema
--------------------------------------------------------------------

Python Schema emits SchemaError that can contain at most 1 type of error,
and its output is not very helpful in programming to handle errors.

On the other hand, PyValidator emits an "ErrorBucket" that shows all the errors,
along with fully-traversible structures for programs to use.

Enough with that long-talk, and here's a demo of python schema:

.. code:: python

    >>> from schema import Schema, Optional
    >>> sc = Schema({
    ...     'wow':'so schema',
    ...     'such':'validation',
    ...     'string!!!': str,
    ...     Optional('so int'): int})
    >>> try:
    ...     sc.validate({'so int': 'NOT int'})
    ... except Exception as e:
    ...     error = e
    >>> error
    SchemaError("'NOT int' should be instance of <type 'int'>",)
    >>> dir(error)
    [ ... , 'args', 'autos', 'code', 'errors', 'message']
    >>> error.args
    [None]
    >>> e.autos
    ["'NOT int' should be instance of <type 'int'>"] #string...

PyValidator's output demo:

.. code:: python

    >>> from pyvalidator import Validator, Optional
    >>> sc = Validator({
    ...     'wow':'so schema',
    ...     'such':'validation',
    ...     'string!!!': str,
    ...     Optional('so int'): int})
    >>> try:
    ...     sc.validate({'so int': 'NOT int'})
    ... except Exception as e:
    ...     error = e
    >>> error
    Generic Errors:
    {'wrong_type': {'so int': [Wrong Type: got str instead of int]}, 'missing_key': {'such': [Missing Key: such => validation], 'wow': [Missing Ke
    y: wow => so schema], 'string!!!': [Missing Key: string!!! => <type 'str'>]}}

    Custom Errors:
    []

    >>> error.errors # note: all errors are preserved.
    {'wrong_type': {'so int': [Wrong Type: got str instead of int]}, 'missing_key': {'such': [Missing Key: such => validation], 'wow': [Missing Ke
    y: wow => so schema], 'string!!!': [Missing Key: string!!! => <type 'str'>]}}
    >>> error.error_count
    4
    >>> error.errors['missing_key']  #needs formatting...
    {'such': [Missing Key: such => validation], 'wow': [Missing Key: wow => so schema], 'string!!!': [Missing Key: string!!! => <type 'str'>]}
    >>> type(error.errors['missing_key']['such'])
    <class 'pyvalidator._errorbucketnode._ErrorBucketNode'>
    >>> # Note: There's room for improvement here...
    >>> error.errors['missing_key']['such'].errors[0]
    Missing Key: such => validation
    >>> dir(error.errors['missing_key']['such'].errors[0])
    [ ..., 'args', 'data', 'error_name', 'key', 'message']
    >>> error.errors['missing_key']['such'].errors[0].key
    'such'
    >>> error.errors['missing_key']['such'].errors[0].error_name
    'missing_key'
    >>> error.errors['missing_key']['such'].errors[0].data
    'validation'

Rationale for _ErrorBucketNode instead of dict / list
------------------------------------------------------------------------


** Any suggestion for _ErrorBucketNode is welcome :)
   (_ErrorBucketNode itself is somewhat ugly) **


Installation
-------------------------------------------------------------------------------

Use `pip <http://pip-installer.org>`_ or easy_install::

    pip install pyvalidator

- **pyvalidator** is tested with Python 2.6, 2.7, and 3.x
- **pyvalitator** follows `semantic versioning <http://semver.org>`_.
