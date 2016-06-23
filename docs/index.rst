.. Pysllo documentation master file, created by
   sphinx-quickstart on Tue May 31 19:45:48 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Pysllo's documentation!
**********************************

Pysllo is set of useful python logging extenders that give possibility to
bind additional data to logs, raising all logs if error occurs or flow tracks
with tools like Elastic Stack or other monitoring tools based on document databases.

The most important benefit of using pysllo is that it's is just extension to
normal python logging library. It not requiring from you to change whole logs
implementation in your application. You can easy change just part of logging
configuration and use this tool in that part of code. It's really simple to
start working with Pysllo.

###########
Quick start
###########

.. code:: bash

    pip install pysllo

Features
--------

-  :class:`pysllo.loggers.StructuredLogger`
    Logger class that make available binding data to logs
-  :class:`pysllo.loggers.PropagationLogger`
    Logger class that make possible to propagate log level between few code block
-  :class:`pysllo.loggers.TrackingLogger`
    Logger that add functionality to track logs on all levels and push it if error
    occurs ignoring normal level configuration
- :class:`pysllo.utils.factory.LoggersFactory`
    Is class that can create you Logger class with functionality from
    classes above you want
-  :class:`pysllo.formatters.JsonFormatter`
    It's formatter class that convert your log records into JSON objects
-  :class:`pysllo.handlers.ElasticSearchUDPHandler`
    It's handler class that send your logs into Elastic cluster

Usage example
-------------

.. code:: python

    from pysllo.handlers import ElasticSearchUDPHandler
    from pysllo.formatters import JsonFormatter
    from pysllo.utils import LoggersFactory

    # configuration
    host, port = 'localhost', 9000
    handler = ElasticSearchUDPHandler([(host, port)])
    formatter = JsonFormatter()
    handler.setFormatter(formatter)
    MixedLogger = LoggersFactory.make(
            tracking_logger=True,
            propagation_logger=True,
            structured_logger=True
        )
    logger = MixedLogger('test')
    logger.addHandler(handler)

    # examlpe usage
    msg = "TEST"
    logger.bind(ip='127.0.0.1')
    logger.debug(msg, user=request.user)

#######
Loggers
#######
.. autoclass:: pysllo.loggers.StructuredLogger
   :members: bind, unbind, get
   :show-inheritance:

.. autoclass:: pysllo.loggers.PropagationLogger
   :members: set_propagation, reset_level, level_propagation, force_level, __init__
   :show-inheritance:

.. autoclass:: pysllo.loggers.TrackingLogger
   :members: trace, enable_tracking, disable_tracking, exit_with_exc, __init__
   :show-inheritance:

.. autoclass:: pysllo.utils.factory.LoggersFactory
   :members:

########
Handlers
########
.. autoclass:: pysllo.handlers.ElasticSearchUDPHandler
   :members: set_backup_path, enable_backup, disable_backup, set_limit, emit, __init__
   :show-inheritance:

##########
Formatters
##########

.. autoclass:: pysllo.formatters.JsonFormatter
   :members: format, __init__
   :show-inheritance:

##################
Indices and tables
##################

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

