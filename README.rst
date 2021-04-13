====================
aftership-sdk-python
====================

.. image:: https://travis-ci.com/AfterShip/aftership-sdk-python.svg?branch=master
    :target: https://travis-ci.com/AfterShip/aftership-sdk-python

.. image:: https://coveralls.io/repos/github/AfterShip/aftership-sdk-python/badge.svg?branch=master
    :target: https://coveralls.io/github/AfterShip/aftership-sdk-python?branch=master


aftership-sdk-python is Python SDK (module) for `AfterShip API <https://www.aftership.com/docs/api/4>`_.
Module provides clean way to access API endpoints.

Supported Python Versions
=========================

- 3.6
- 3.7
- 3.8
- 3.9
- pypy3

Installation
------------

Virtual Environment
=======================
We recommend using a `virtualenv <https://docs.python.org/3/library/venv.html>`_ or `poetry <https://python-poetry.org/>`_
to use this SDK.
    
Using Poetry
============

.. code-block:: bash

    $ poetry add aftership

Using pip
=========

.. code-block:: bash

    $ pip install aftership

Via source code (tarbar)
========================

Download the code archive without unzip it and run:

.. code-block:: bash

    $ pip install <Download Path>/aftership-sdk-python.zip

Usage
-----

You need a valid API key to use this SDK. If you don't have one, please visit https://www.aftership.com/apps/api .

Quick Start 
===========

The following code gets list of supported couriers

.. code-block:: python

    import aftership
    aftership.api_key = 'YOUR_API_KEY_FROM_AFTERSHIP'
    couriers = aftership.courier.list_couriers()

You can also set API key via setting :code:`AFTERSHIP_API_KEY` environment varaible.

.. code-block:: bash

    export AFTERSHIP_API_KEY=THIS_IS_MY_API_KEY

.. code-block:: python

    import aftership
    tracking = aftership.get_tracking(tracking_id='your_tracking_id')

The functions of the SDK will return `data` field value if the API endpoints
return response with HTTP status :code:`2XX`, otherwise will throw an
exception.


Exceptions
==========

Exceptions are mapped from https://docs.aftership.com/api/4/errors,
and this table is the exception attributes mapping.

+------------------+----------------------+
| API error        | AfterShipError       |
+==================+======================+
| http status code | :code:`http_status`  |
+------------------+----------------------+
| :code:`meta.code`| :code:`code`         |
+------------------+----------------------+
| :code:`meta.type`| :code:`message`      |
+------------------+----------------------+


Keyword arguments
=================

Most of SDK functions only accept keyword arguments.


Examples
========

Goto `examples <examples>`_ to see more examples.
