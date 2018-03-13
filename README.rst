Geotweet: fetch geolocalized tweets and plot them on a map
==========================================================

This software fetches geolocalized tweets from the Twitter Streaming APIs,
shows them on the terminal and draws their location on a world map. It's based on
``tweepy`` and ``matplotlib``.

.. image:: http://www.ladybiss.it/map.png

Prerequisites
-------------

- Python 3.6
- the ``geos`` library must be installed on the system

This software is tested on Mac OS 10.13.3 and Ubuntu 17.10.

Installation
------------

This guide assumes you have a working setup of Python 3.6.

- install ``geos`` library

  ::

    brew install geos              # Mac OS
    sudo apt install libgeos-c1v5  # Ubuntu 17.10

- create a Python virtual environment and activate it (assuming Bash as shell)

  ::

    python3.6 -m venv geotweet_venv
    source geotweet_venv/bin/activate


- clone this repository and ``cd`` into it

  ::

    git clone https://github.com/sanjioh/geotweet
    cd geotweet

- install requirements (this can take long, since the ``basemap`` library is ~130MB)

  ::

    pip install -r requirements.txt

- install Geotweet

  ::

    pip install .

Usage
-----

::

    usage: geotweet [-h] [--min-long MIN_LONG] [--min-lat MIN_LAT]
                    [--max-long MAX_LONG] [--max-lat MAX_LAT]
                    consumer_key consumer_secret access_token access_token_secret

    Fetch geolocalized tweets and plot them on a map.

    positional arguments:
    consumer_key         Twitter Application Consumer Key
    consumer_secret      Twitter Application Consumer Secret
    access_token         Twitter User Access Token
    access_token_secret  Twitter User Access Token Secret

    optional arguments:
    -h, --help           show this help message and exit
    --min-long MIN_LONG  Minimum longitude (default: -180)
    --min-lat MIN_LAT    Minimum latitude (default: -90)
    --max-long MAX_LONG  Maximum longitude (default: 180)
    --max-lat MAX_LAT    Maximum latitude (default: 90)

Example
-------

::

    $ geotweet <consumer_key> <consumer_secret> <access_token> <access_token_secret> \
      --min-lat -70 --max-lat 80 --min-long -150 --max-long 120

Tests
-----

Simply run ``tox`` from the repository root.

Notes
-----

- this project uses an ``src`` directory layout to prevent packaging errors and to enforce
  testing against a ``pip``-installed copy of the program (as opposed to the one in the
  current working directory) [1]_ [2]_

- this program is single-threaded synchronous, so expect the map to appear frozen when tweets aren't flowing

.. [1] https://hynek.me/articles/testing-packaging/
.. [2] https://blog.ionelmc.ro/2014/05/25/python-packaging/
