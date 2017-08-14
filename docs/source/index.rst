.. mockquitto documentation master file, created by
   sphinx-quickstart on Mon Aug 14 14:45:38 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to mockquitto's documentation!
======================================

**mockquitto** — MQTT broker and generator of MQTT messages with payload in JSON
or any other formats based on forked version of HBMQTT_ library.

Quick start
-----------

For starting message generator use command-line tool ``mockquitto-async-generator``.
It allows generating messages for different study cases. By default, starting
``mockquitto-async-generator`` without parameters leads to connecting to server
with port 1883 and generate messages by devices from case #1.

For specifying server's port use ``-p`` option. For example::

   mockquitto-async-generator -p 1884

For specifying desired study case for which messages will be generated use either
``-c`` or ``--case`` option. For example::

   mockquitto-async-generator -c 1

Generator supports diffetent timings between generating of messages. By default
period is 1 second. Changing of period looks like::

   mockquitto-async-generator --period 2

Mockquitto also supplies MQTT server. Server can be launched from console via
command ``mockquitto-broker``. Server tries to bind to 1883 port and if this port
is binded by another application, ``mocqkuitto-broker`` use first available port
after port 1883.

Options
-------

Currently, only ``mockquitto-async-generator`` supports command-line options.

   -p, --port           Port of MQTT server.
   --period             Period of generating messages.
   -c, --case           Case number which determines emulating devices.
   -v                   Give more output. Option is additive, and can be used up
                        to 3 times.
   -q                   Give less output. Option is additive, and can be used up
                        to 2 times.
   --log-file           Path to a verbose appending log.
   -V, --version        Output program version and exit.



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. toctree::
   :maxdepth: 2


.. _HBMQTT: https://github.com/beerfactory/hbmqtt
