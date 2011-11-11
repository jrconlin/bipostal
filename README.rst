Getting Started
---------------

1. Make your virtualenv.
2. Install the python packages::

    pip install -r dev-reqs.txt

3. Start the server::

    paster serve etc/bipostal-dev.ini


Run the Server
--------------
::

    paster serve etc/bipostal-dev.ini


The API
-------

::

    GET /alias/
    >>> 200 OK {"email": <email>, "aliases": [<alias>, <alias>, ...]}

    Requires browserid auth.

::

    POST /alias/
    >>> 200 OK {"email": <email>, "alias": <alias>}

    Requires browserid auth.

::

    GET /alias/<alias>
    >>> 200 OK {"email": <email>}

    No auth required.

::

    DELETE /alias/<alias>
    >>> 200 OK

    Requires browserid auth.
