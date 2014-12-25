pywb-warcbase
=============

This is an experimental add-on to `pywb <https://github.com/ikreymer/pywb>`_ to allow it to interface with the `warcbase <https://github.com/lintool/warcbase>`_ project for serving WARC files.


Usage
~~~~~

To use this project, you may try the following:

1. ``git clone github.com/ikreymer/pywb-warcbase``

2.  (Optional but Recommended) Setup a virtualenv for testing, eg. ``virtualenv ./venv; source ./venv/bin/activate``

3. ``cd pywb-warcbase; python setup.py install``

4.  (Optional but Recommended) run ``python setup test`` to ensure basic install succeeded.

5. Edit `config.yaml <config.yaml>`_ and change the ``warcbase_servlet_hostname`` setting from ``http://localhost:8090`` to the actual host:port where the warcbase servlet is running. (A trailing slash should not be included)

6. Run ``wayback``

7. Visit ``http://localhost:8080/`` to see a list of available Warcbase collections. A link will provided to a search page for each collection.
   
   Standard Wayback paths can be used to access content. For example, to view an index for ``http://example.com/`` in collection ``Test``, you can visit ``http://localhost:8080/Test/*/http://example.com/``
   

Please refer to `pywb <https://github.com/ikreymer/pywb>`_ and `warcbase <https://github.com/lintool/warcbase>`_ pages for additional info about these projects.


How It Works
~~~~~~~~~~~~

This module provides an index reader for connecting to the warcbase `WarcBrowserServlet <https://github.com/lintool/warcbase/blob/master/src/main/java/org/warcbase/browser/WarcBrowserServlet.java>`_ 
to read the index and convert it to native format (CDXObject).

pywb uses a wildcard collection to accept any collection and pass it to the WarcBaseServlet. A listing of available Warcbase collection is provided from WarcbaseServlet as well.

pywb can already has support for loading WARC/ARC files and records from an http prefix, and WarcBrowserServlet also provides such an interface for WARC/ARC loading.

