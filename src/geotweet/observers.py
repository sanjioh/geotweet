import sys
from collections import namedtuple

import matplotlib.pyplot as plt

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
        tweet = self._tweet_cls(
            *status.coordinates['coordinates'],
            status.user.name,
            status.user.screen_name,
            status.text,
        )
        print(self._formatter.format(tweet), file=self._fp, end='')


class MapObserver:
    def __init__(self, worldmap):
        self._worldmap = worldmap

    def update(self, status):
        longitude, latitude = self._worldmap(
            *status.coordinates['coordinates'],
        )
        self._worldmap.plot(longitude, latitude, 'ro', markersize=2)
        plt.draw()
