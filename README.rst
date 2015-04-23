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


If data is valid, ``Validator.validate`` will return the validated data
(optionally converted with `Use` calls, see below).

If data is invalid, ``Schema`` will raise ``SchemaError`` exception.


Installation
-------------------------------------------------------------------------------

Use `pip <http://pip-installer.org>`_ or easy_install::

    pip install pyvalidator

- **pyvalidator** is tested with Python 2.6, 2.7.
- **pyvalitator** follows `semantic versioning <http://semver.org>`_.

How ``Validator`` validates data
-------------------------------------------------------------------------------

Types
~~~~~

If ``Validator(...)`` encounters a type (such as ``int``, ``str``, ``object``,
etc.), it will check if the corresponding piece of data is an instance of that type,
otherwise it will raise ``ErrorBucket``.