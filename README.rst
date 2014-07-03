About aftership-python
======================

aftership-python is a Python SDK (module) for `AfterShip API <https://www.aftership.com/docs/api/3.0>`_.
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

APIv3 object
------------

APIv3 object is used to make API calls. Object cunstructor:

.. code-block:: python

    class aftership.APIv3(key, max_calls_per_sec=10, datetime_convert=True)

#. **key** is AfterShip API key
#. **max_calls_per_sec** represents maximum number of calls provided for each second (10 is a limit for single client, but you might want to set less if you have multiple parallel API objects)
#. **datetime_convert** provides timestamp strings conversion to datetime in API output

Make API calls
--------------

The module provides direct bindings to API calls: https://www.aftership.com/docs/api/3.0

Each call consists of three parts:

#. Positional arguments (goes after api.aftership.com/v3/, separated by slash "/")
#. Named arguments (listed in Request —> Parameters section)
#. HTTP Method (GET, POST, PUT or DELETE)

The following convention showed in pseudo-API call is used to construct a call:

.. code-block:: python

    <APIv3 object>.positional.arguments.<HTTP method>(*more_positional_arguments, **named_arguments)

The code above makes a call to /positional/arguments/... endpoint with named arguments passed in request body as JSON or HTTP query (depending on HTTP method).

API calls examples
------------------

The following code creates, modifies and deletes tracking:

.. code-block:: pycon

    >>> import aftership
    >>> api = aftership.APIv3(API_KEY)
    >>> slug = 'dpd-uk'
    >>> number = '15502370264989N'

    # create tracking
    >>> api.trackings.post(tracking=dict(slug=slug, tracking_number=number, title="Title"))
    {u'tracking': { ... }}

    # get tracking by slug and number, return 'title' and 'created_at' field
    >>> api.trackings.get(slug, number, fields=['title', 'created_at'])
    {u'tracking': { ... }}

    # change tracking title
    >>> api.trackings.put(slug, number, tracking=dict(title="Title (changed)"))
    {u'tracking': { ... }}

    # delete tracking
    >>> api.trackings.delete(slug, number)
    {u'tracking': { ... }}

Positional arguments
----------------------------

Positional arguments passed in the following forms:

#. APIv3 object attributes.
#. APIv3 object keys.
#. HTTP Method arguments.

APIv3 object attributes used to represent constant parts of the endpoint, while HTTP Method arguments are used for variable parts, e.g.:

.. code-block:: python

    api.couriers.detect.get('15502370264989N')

Positional arguments passed as keys are useful if they are stored in variables and followed by constant value, e.g.:

.. code-block:: python

    api.trackings['dpd-uk']['15502370264989N'].reactivate.post()

Named arguments
---------------

Named arguments passed as keyword arguments.
Comma-separated values strings could be passed as regular lists, timestamp strings could be passed as regular datetime objects, e.g.:

.. code-block:: python

    api.trackings.get(created_at_min=datetime(2014, 6, 1), fields=['title', 'order_id'])

HTTP Method arguments
---------------------

The following HTTP methods are supported:

#. get()
#. post()
#. put()
#. delete()

Each method return either JSON of 'data' field or throws an aftership.APIv3RequestException.
aftership-python relies on Requests library and ones should expect `Requests exceptions <http://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions>`_.

APIv3RequestException
---------------------

An exception is throwed on errors. The following methods are provided to get details of an error:

#. code()
#. type()
#. message()

Each functions returns appropriate value from 'meta' field. See `Errors documentation <https://www.aftership.com/docs/api/3.0/errors>`_ for more details.
Code example:

.. code-block:: python

    try:
        api = aftership.APIv3('FAKE_API_KEY')
        api.couriers.get()
    except aftership.APIv3RequestException as error:
        # FAKE_API_KEY will result in InvalidCredentials (401) error
        print 'Error:', error.code(), error.type(), error.message()