.. Pysllo documentation master file, created by
   sphinx-quickstart on Tue May 31 19:45:48 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Pysllo's documentation!
**********************************

Pysllo is set of useful python logging extenders
that make possible saving logs into StackLight with possibility of flow
tracking, data binding and raising all logs if error occurs.

.. code:: python

    from pysllo.handlers import ElasticSearchUDPHandler
    from pysllo.formatters import JsonFormatter
    from pysllo.utils import LoggersFactory

    # configuration
    host, port, limit = 'localhost', 9000
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

Loggers
=======
.. autoclass:: pysllo.loggers.StructuredLogger
   :members: bind, unbind, get
   :show-inheritance:

.. autoclass:: pysllo.loggers.PropagationLogger
   :members: set_propagation, reset_level, level_propagation, force_level
   :show-inheritance:

.. autoclass:: pysllo.loggers.TrackingLogger
   :members: trace, enable_tracking, disable_tracking, exit_with_exc
   :show-inheritance:

.. autoclass:: pysllo.utils.factory.LoggersFactory
   :members:

Handlers
========
.. automodule:: pysllo.handlers
   :members:
   :show-inheritance:

Formatters
==========
.. automodule:: pysllo.formatters
   :members:
   :show-inheritance:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

