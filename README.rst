pyfoobot
========

A tool for getting data from your `FooBot device <http://foobot.io>`__

Installation
------------
::

    pip install pyfootbot

Example
-------
::

    fb = Foobot("username", "password")
    devices = fb.devices()

    last_hour_data = fb.data_period(devices[0], 3600, 0)
    latest_data = fb.latest(devices[0])



Requirements
------------

-  `requests <https://pypi.python.org/pypi/requests>`__
