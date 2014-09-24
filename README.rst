About aftership-python
======================

aftership-python is Python SDK (module) for `AfterShip API <https://www.aftership.com/docs/api/4>`_.
Module provides clean and elegant way to access API endpoints.

Installation
============

Via pip
-------

Run the following:

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

The following code gets list of supported couriers

.. code-block:: python

    import aftership
    api = aftership.APIv4('AFTERSHIP_API_KEY')
    couriers = api.couriers.all.get()

Get API object
--------------

Import aftership module and obtain APIv4 object. Valid API key must be provided.

.. code-block:: python

    import aftership
    api = aftership.APIv4('AFTERSHIP_API_KEY')

APIv4 object
------------

APIv4 object is used to make API calls. Object constructor:

.. code-block:: python

    class aftership.APIv4(key, max_calls_per_sec=10, datetime_convert=True)

#. **key** is AfterShip API key
#. **max_calls_per_sec** represents maximum number of calls provided for each second (10 is a limit for single client, but you might want to set less if you have multiple parallel API objects)
#. **datetime_convert** provides timestamp strings conversion to datetime in API output

Make API calls
--------------

The module provides direct bindings to API calls: https://www.aftership.com/docs/api/4

Each call consists of three parts:

#. **Positional arguments** (goes after api.aftership.com/v4/, separated by slash "/")
#. **Named arguments** (listed in Request —> Parameters section)
#. **HTTP Method** (GET, POST, PUT or DELETE)

The following convention is used to construct a call:

.. code-block:: python

    <APIv4 object>.positional.arguments.<HTTP method>(*more_positional_arguments, **named_arguments)

The code above makes a call to /positional/arguments/... endpoint with named arguments passed in request body as JSON or HTTP query (depending on HTTP method).

API calls examples
------------------

The following code creates, modifies and deletes tracking:

.. code-block:: pycon

    >>> import aftership
    >>> api = aftership.APIv4(API_KEY)
    >>> slug = 'russian-post'
    >>> number = 'EA333123991RU'

    # create tracking
    # https://www.aftership.com/docs/api/4/trackings/post-trackings
    >>> api.trackings.post(tracking=dict(slug=slug, tracking_number=number, title="Title"))
    {u'tracking': { ... }}

    # get tracking by slug and number, return 'title' and 'created_at' field
    # https://www.aftership.com/docs/api/4/trackings/get-trackings-slug-tracking_number
    >>> api.trackings.get(slug, number, fields=['title', 'created_at'])
    {u'tracking': { ... }}

    # change tracking title
    # https://www.aftership.com/docs/api/4/trackings/put-trackings-slug-tracking_number
    >>> api.trackings.put(slug, number, tracking=dict(title="Title (changed)"))
    {u'tracking': { ... }}

    # delete tracking
    # https://www.aftership.com/docs/api/4/trackings/delete-trackings
    >>> api.trackings.delete(slug, number)
    {u'tracking': { ... }}

Positional arguments
--------------------

Positional arguments passed in the following forms:

#. APIv4 object attributes
#. APIv4 object keys
#. HTTP Method arguments

APIv4 object attributes used to represent constant parts of the endpoint, while HTTP Method arguments are used for variable parts, e.g.:

.. code-block:: python

    api.trackings.get('russian-post', 'EA333123991RU')

Positional arguments passed as keys are useful if they are stored in variables and followed by constant value, e.g.:

.. code-block:: python

    api.trackings['russian-post']['EA333123991RU'].retrack.post()

Named arguments
---------------

Named arguments passed as keyword arguments of HTTP Methods calls.
Comma-separated values strings could be passed as [lists], timestamp strings could be passed as regular datetime objects, e.g.:

.. code-block:: python

    api.trackings.get(created_at_min=datetime(2014, 9, 1), fields=['title', 'order_id'])

HTTP Method arguments
---------------------

The following HTTP methods are supported:

#. get()
#. post()
#. put()
#. delete()

Each method return either JSON of 'data' field or throws an aftership.APIv4RequestException.
aftership-python relies on Requests library and ones should expect `Requests exceptions <http://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions>`_.

APIv3RequestException
---------------------

An exception is throwed on errors. The following methods are provided to get error details:

#. code()
#. type()
#. message()

Each functions returns appropriate value from 'meta' field. Check `errors documentation <https://www.aftership.com/docs/api/4/errors>`_ for more details.
Code example:

.. code-block:: python

    try:
        api = aftership.APIv4('FAKE_API_KEY')
        api.couriers.get()
    except aftership.APIv4RequestException as error:
        # FAKE_API_KEY will result in Unauthorized (401) error
        print 'Error:', error.code(), error.type(), error.message()
