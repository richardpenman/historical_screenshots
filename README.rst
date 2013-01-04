======================
Historical Screenshots
======================

Generate historical screenshots for a website by downloading webpages from the `Wayback machine <http://archive.org>`_ and rendering with webkit. ::

    Usage: historical_screenshots.py [options] <website>

    Options:
      -h, --help            show this help message and exit
      -s, --show-browser    Show the generated screenshots in a web browser
      -d DAYS, --days=DAYS  Days between archived webpages to generate screenshots
                            (default 365)


Dependencies are `python 2.5+ <http://www.python.org/getit/>`_, `pyqt <http://www.riverbankcomputing.com/software/pyqt/intro>`_, and `webscraping <http://code.google.com/p/webscraping>`_.

These can be installed in Debian based distributions with: ::

    $ sudo apt-get install python-qt4
    $ sudo pip install webscraping

This `blog article <http://webscraping.com/blog/Generate-website-screenshot-history/>`_ steps through the implementation.
