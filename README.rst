====================
aftership-sdk-python
====================

.. image:: https://github.com/aftership/aftership-sdk-python/actions/workflows/test.yml/badge.svg?branch=master
    :target: https://github.com/AfterShip/aftership-sdk-python/actions/workflows/test.yml?query=branch%3Amaster

.. image:: https://coveralls.io/repos/github/AfterShip/aftership-sdk-python/badge.svg?branch=master
    :target: https://coveralls.io/github/AfterShip/aftership-sdk-python?branch=master


aftership-sdk-python is Python SDK (module) for `AfterShip API <https://www.aftership.com/docs/api/4>`_.
Module provides clean way to access API endpoints.

IMPORTANT NOTE
--------------

Current version of aftership-sdk-python `>=0.3` not **compatible** with
previous version of sdk `<=0.2`.

Also, version since 1.0 is **not** support Python 2.X anymore. If you want
to use this SDK under Python 2.X, please use versions `<1.0`.


Supported Python Versions
=========================

- 3.5
- 3.6
- 3.7
- 3.8
- 3.9
- pypy3

Installation
------------

Via pip
=======

Use Virtual Environment
=======================
We recommend using a `virtualenv <https://docs.python.org/3/library/venv.html>`_ or `poem <https://python-poetry.org/>`_
to use this SDK.

.. code-block:: bash

    $ pip install aftership

Via source code
===============

Download the code archive, without unzip it, go to the
source root directory, then run:

.. code-block:: bash

    $ pip install aftership-sdk-python.zip

Usage
-----

You need a valid API key to use this SDK. If you don't have one, please visit https://www.aftership.com/apps/api.

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
