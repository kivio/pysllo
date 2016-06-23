[![PyPI](https://img.shields.io/pypi/pyversions/pysllo.svg?maxAge=2592000)](https://pypi.python.org/pypi/pysllo/)
[![PyPI](https://img.shields.io/pypi/status/pysllo.svg?maxAge=2592000)](https://pypi.python.org/pypi/pysllo/)
[![Documentation Status](https://readthedocs.org/projects/pysllo/badge/?version=latest)](http://pysllo.readthedocs.io/en/latest/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/github/kivio/pysllo/badge.svg?branch=master)](https://coveralls.io/github/kivio/pysllo?branch=master)
[![Build Status](https://travis-ci.org/kivio/pysllo.svg?branch=master)](https://travis-ci.org/kivio/pysllo)

Pysllo
======

Pysllo is set of useful python logging extenders that give possibility to
bind additional data to logs, raising all logs if error occurs or flow tracks
with tools like Elastic Stack or other monitoring tools based on document databases.

The most important benefit of using pysllo is that it's is just extension to
normal python logging library. It not requiring from you to change whole logs
implementation in your application. You can easy change just part of logging
configuration and use this tool in that part of code. It's really simple to
start working with Pysllo.


For more information go to documentation on [ReadTheDocs](http://pysllo.readthedocs.io/).

Quick start
-----------

```bash
pip install pysllo
```

Features
--------

* StructuredLogger
* PropagationLogger
* TrackingLogger
* JsonFormatter
* ElasticSearchUDPHandler

Example
-------

```python
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
```
