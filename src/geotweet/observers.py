import logging
import sys
from collections import namedtuple

logger = logging.getLogger(__name__)

Tweet = namedtuple(
    'Tweet',
    ['longitude', 'latitude', 'user_name', 'user_screen_name', 'text'],
)


class ConsoleObserver:
    def __init__(self, formatter, tweet_cls=None, fp=None):
        self._formatter = formatter
        self._tweet_cls = tweet_cls or Tweet
        self._fp = fp or sys.stdout

    def update(self, status):
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
    def __init__(self, figure, worldmap):
        self._figure = figure
        self._worldmap = worldmap

    def update(self, status):
        try:
            longitude, latitude = self._worldmap(
                *status.coordinates['coordinates'],
            )
            self._worldmap.plot(longitude, latitude, 'ro', markersize=5)
            self._figure.canvas.start_event_loop(0.001)
        except Exception as e:
            logger.exception('Unable to render Tweet data.', exc_info=True)
