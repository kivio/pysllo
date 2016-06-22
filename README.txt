|Documentation Status| |Coverage Status| |Build Status|

Pysllo
======

Make your python logging more structured and easy to aggregate using all
features of pysllo. Pysllo is set of useful python logging extenders
that make possible saving logs into StackLight with possibility of flow
tracking, data binding and raising all logs if error occurs.

For more information go to documentation on
`ReadTheDocs <http://pysllo.readthedocs.io/>`__.

Quick start
-----------

.. code:: bash

    pip install pysllo

Features
--------

-  StructuredLogger
-  PropagationLogger
-  TrackingLogger
-  JsonFormatter
-  ElasticSearchUDPHandler

Example
-------

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

.. |Documentation Status| image:: https://readthedocs.org/projects/pysllo/badge/?version=latest
   :target: http://pysllo.readthedocs.io/en/latest/?badge=latest
.. |Coverage Status| image:: https://coveralls.io/repos/github/kivio/pysllo/badge.svg?branch=master
   :target: https://coveralls.io/github/kivio/pysllo?branch=master
.. |Build Status| image:: https://travis-ci.org/kivio/pysllo.svg?branch=master
   :target: https://travis-ci.org/kivio/pysllo
