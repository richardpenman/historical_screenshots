======================
Historical Screenshots
======================

Generate historical screenshots for a website by downloading webpages from the `Wayback machine <http://archive.org>`_ and rendering with webkit.
Usage: ::

    Usage: historical_screenshots.py [options] <website>

    Options:
      -h, --help            show this help message and exit
      -s, --show-browser    Show the generated screenshots in a web browser
      -d DAYS, --days=DAYS  Days between archived webpages to generate screenshots
                            (default 365)


Dependencies are `python 2.6/2.7 <http://www.python.org/getit/>`_, `pyqt <http://www.riverbankcomputing.com/software/pyqt/intro>`_ / `pyside <http://qt-project.org/wiki/PySide>`_, and `webscraping <http://code.google.com/p/webscraping>`_.

These can be installed in Debian based distributions with: ::

    $ sudo apt-get install python-qt4 (or python-pyside)
    $ sudo pip install webscraping


This `Blog article <>`_ steps through the implementation.
