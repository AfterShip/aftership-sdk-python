About aftership-python
======================

aftership-python is a python binding to `AfterShip API <https://www.aftership.com/docs/api/3.0>`_.
Module provides clean and elegant way to access API endpoints.

Installation
============

Via pip
-------

Run the following (**note from Fedor: doesn't work since package is not in PyPi yet**):

.. code-block:: bash

    $ pip install aftership

Via source code
---------------

Download the code archive, unzip it, create/activate `virtualenv <http://virtualenv.readthedocs.org/en/latest/virtualenv.html>`_, go to the source root directory, then run:

.. code-block:: bash

    $ python setup.py install

Usage
=====

Quick Start
-----------

The following code gets the list of supported couriers

.. code-block:: python

    import aftership
    api = aftership.APIv3('AFTERSHIP_API_KEY')
    couriers = api.couriers.get()

Get API object
--------------

Import aftership module and obtain APIv3 object. Valid API key must be provided.

.. code-block:: python

    import aftership
    api = aftership.APIv3('AFTERSHIP_API_KEY')

Make API calls
--------------

The module provides direct bindings to API calls: https://www.aftership.com/docs/api/3.0

Each call consists of three parts:

#. HTTP Method (GET, POST, PUT or DELETE)
#. Positional arguments (goes after api.aftership.com/v3/, separated by slash "/")
#. Named agruments (listed in Request —> Parameters section)

The following convention showed in pseudo-API call is used to construct a call:

.. code-block:: python

    api.path['to'].api.get('foo', arg='bar')

Where 'path', 'to', 'api' and 'foo' are positional arguments, 'get' points to HTTP method, 'bar' is a named argument.
The code above makes /GET call to /path/to/api/foo?arg=bar.

API calls examples
------------------
