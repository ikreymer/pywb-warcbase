pywb-warcbase
=============

This is an experimental add-on to `pywb <https://github.com/ikreymer/pywb>`_ to allow it to interface with the `warcbase <https://github.com/lintools/warcbase>_` project for serving WARC files.


Usage
~~~~~

To use this project, you may try the following:

1. `git clone github.com/ikreymer/pywb-warcbase`

2.  (Optional but Recommended) Setup a virtualenv for testing, eg. `virtualenv ./venv; source ./venv/bin/activate`

3. `cd pywb-warcbase; python setup install`

4.  (Optional but Recommended) run `python setup test` to ensure basic install succeeded.

5. Edit `config.yaml` and change the `warcbase_servlet_url` setting from `http://my-warcbase-servlet-host:8080/` to the actual URL where the warcbase servlet is running.

6. Run `wayback`

7. You should be able to load *example.com* `http://localhost:8080/warcbase/*/http://example.com`. 
   
   (The `/warcbase` path can modified by changing the name under `collections` in `config.yaml` as well).


Please refer to `pywb <https://github.com/ikreymer/pywb>`_ page for additional info about pywb.


How It Works
~~~~~~~~~~~~

This module provides an index reader for connecting to the warcbase `WarcBrowserServlet <https://github.com/lintool/warcbase/blob/master/src/main/java/org/warcbase/browser/WarcBrowserServlet.java>`_ 
to read the index and convert it to native format (CDXObject).

pywb can already has support for loading WARC/ARC files and records from an http prefix, and WarcBrowserServlet also provides such an interface for WARC/ARC loading.

