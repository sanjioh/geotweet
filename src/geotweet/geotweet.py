"""Main program module."""
import argparse
import signal
import sys
import warnings

import matplotlib as mpl
import matplotlib.pyplot as plt
import tweepy
from mpl_toolkits.basemap import Basemap

from geotweet import formatters, listener, observers


class Runner:
    """
    Control the main program loop.

    This class works as a factory for all the other entities involved:
    it's a wrapper around low-level logic, needed to encapsulate the
    creation and the internal working of the stream reader and the map
    renderer.
    """

    def __init__(self):
        """Initialize a Runner object."""
        self._credentials = None
        self._coordinates = None
        self._figure = None
        self._worldmap = None
        self._callback_id = None
        self._stream = None

    def _parse_cli(self):
        default_long = 180
        default_lat = 90
        parser = argparse.ArgumentParser(
            description='Fetch geolocalized tweets and plot them on a map.',
        )
        parser.add_argument(
            'consumer_key',
            help='Twitter Application Consumer Key',
        )
        parser.add_argument(
            'consumer_secret',
            help='Twitter Application Consumer Secret',
        )
        parser.add_argument(
            'access_token',
            help='Twitter User Access Token',
        )
        parser.add_argument(
            'access_token_secret',
            help='Twitter User Access Token Secret',
        )
        parser.add_argument(
            '--min-long',
            type=float,
            default=-default_long,
            help=f'Minimum longitude (default: {-default_long})',
        )
        parser.add_argument(
            '--min-lat',
            type=float,
            default=-default_lat,
            help=f'Minimum latitude (default: {-default_lat})',
        )
        parser.add_argument(
            '--max-long',
            type=float,
            default=default_long,
            help=f'Maximum longitude (default: {default_long})',
        )
        parser.add_argument(
            '--max-lat',
            type=float,
            default=default_lat,
            help=f'Maximum latitude (default: {default_lat})',
        )
        args = parser.parse_args()
        if not (
            (-default_long <= args.min_long <= args.max_long <= default_long)
            and
            (-default_lat <= args.min_lat <= args.max_lat <= default_lat)
        ):
            raise parser.error(
                f'Please ensure that '
                f'{-default_long} <= MIN_LONG <= MAX_LONG <= {default_long} '
                f'and that '
                f'{-default_lat} <= MIN_LAT <= MAX_LAT <= {default_lat}',
            )
        self._credentials = (
            args.consumer_key, args.consumer_secret,
            args.access_token, args.access_token_secret,
        )
        self._coordinates = [
            args.min_long,
            args.min_lat,
            args.max_long,
            args.max_lat,
        ]

    def _setup_worldmap(self):
        plt.ion()
        mpl.rcParams['toolbar'] = 'None'
        figure = plt.figure(figsize=(12, 8))
        worldmap = Basemap(projection='robin', lat_0=0, lon_0=0)
        with warnings.catch_warnings():
            # Temporarily silence MatplotlibDeprecationWarning.
            warnings.simplefilter('ignore')
            worldmap.drawcoastlines()
            worldmap.drawcountries()
            worldmap.fillcontinents(color='gray')
            worldmap.drawmapboundary()
        self._figure = figure
        self._worldmap = worldmap
        plt.show()
        plt.pause(0.001)

    def _setup_stream(self):
        (consumer_key, consumer_secret,
         access_token, access_token_secret) = self._credentials
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        obs = [
            observers.ConsoleObserver(formatters.SimpleFormatter()),
            observers.MapObserver(self._figure, self._worldmap),
        ]
        stream_listener = listener.GeoStreamListener(self, obs)
        stream = tweepy.Stream(
            auth=api.auth,
            listener=stream_listener,
            timeout=10,
        )
        self._stream = stream

    def _setup_event_handlers(self):
        def handler(*args, **kwargs):
            self.stop()

        self._callback_id = self._figure.canvas.mpl_connect(
            'close_event',
            handler,
        )

        signal.signal(signal.SIGINT, handler)

    def stop(self):
        """Halt the main loop and gracefully shutdown the program."""
        self._figure.canvas.mpl_disconnect(self._callback_id)
        plt.close(self._figure)
        self._stream.disconnect()
        sys.exit('\nGoodbye!')

    def start(self):
        """Build all the required objects and start the main loop."""
        self._parse_cli()
        self._setup_worldmap()
        self._setup_stream()
        self._setup_event_handlers()
        self._stream.filter(locations=self._coordinates)


def main():
    """Program entry point."""
    Runner().start()


if __name__ == '__main__':
    main()
