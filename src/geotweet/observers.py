"""
Observers module.

Observers are objects which listen to streams of events and act
accordingly. In our case, observers receive geolocalized
tweets and perform different actions depending on their role.
"""
import logging
import sys
from collections import namedtuple

logger = logging.getLogger(__name__)

Tweet = namedtuple(
    'Tweet',
    ['longitude', 'latitude', 'user_name', 'user_screen_name', 'text'],
)


class ConsoleObserver:
    """
    Render tweets on the terminal.

    ConsoleObserver uses a formatter object to format tweets as a strings and
    then shows them on standard output.
    """

    def __init__(self, formatter, tweet_cls=None, fp=None):
        """Initialize a ConsoleObserver object."""
        self._formatter = formatter
        self._tweet_cls = tweet_cls or Tweet
        self._fp = fp or sys.stdout

    def update(self, status):
        """
        Print new tweets on standard output.

        update() receives a tweet as argument and performs a light
        validation of its structure. It then uses the formatter object
        to get a string representation of the tweet, and writes it to stdout.
        """
        try:
            tweet = self._tweet_cls(
                *status.coordinates['coordinates'],
                status.user.name,
                status.user.screen_name,
                status.text,
            )
            formatted_tweet = self._formatter.format(tweet)
        except Exception as e:
            logger.exception('Unable to render Tweet data.', exc_info=True)
        else:
            print(formatted_tweet, file=self._fp, end='')


class MapObserver:
    """
    Render tweets on a map.

    MapObserver extracts coordinates from tweets and plot their position
    on a world map using Matplotlib and Basemap.
    """

    def __init__(self, figure, worldmap):
        """Initialize a MapObserver object."""
        self._figure = figure
        self._worldmap = worldmap

    def update(self, status):
        """
        Plot new tweets as markers on a map.

        update() receives a tweet as argument and extracts its coordinates.
        It then adds a marker to the map, representing the location.
        """
        try:
            longitude, latitude = self._worldmap(
                *status.coordinates['coordinates'],
            )
            self._worldmap.plot(longitude, latitude, 'ro', markersize=5)
            self._figure.canvas.start_event_loop(0.001)
        except Exception as e:
            logger.exception('Unable to render Tweet data.', exc_info=True)
