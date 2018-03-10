"""Main program module."""
import argparse
import signal
import sys
import warnings

import matplotlib as mpl
import matplotlib.pyplot as plt
import tweepy
from mpl_toolkits.basemap import Basemap

import formatters
import listener
import observers


def _get_worldmap():
    mpl.rcParams['toolbar'] = 'None'
    plt.figure(figsize=(12, 8))
    worldmap = Basemap(projection='robin', lat_0=0, lon_0=0)
    with warnings.catch_warnings():
        # Temporarily silence MatplotlibDeprecationWarning.
        warnings.simplefilter('ignore')
        worldmap.drawcoastlines()
        worldmap.drawcountries()
        worldmap.fillcontinents(color='gray')
        worldmap.drawmapboundary()
    return worldmap


def _get_stream(credentials, worldmap):
    (consumer_key, consumer_secret,
     access_token, access_token_secret) = credentials
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    obs = [
        observers.ConsoleObserver(formatters.SimpleFormatter()),
        observers.MapObserver(worldmap),
    ]
    stream_listener = listener.GeoStreamListener(obs)
    stream = tweepy.Stream(
        auth=api.auth,
        listener=stream_listener,
        timeout=10,
    )
    return stream


def _cli():
    default_long = 180
    default_lat = 90
    parser = argparse.ArgumentParser(
        description='Stream geolocalized tweets and plot them on a map.',
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
        (-default_long <= args.min_long <= args.max_long <= default_long) and
        (-default_lat <= args.min_lat <= args.max_lat <= default_lat)
    ):
        raise parser.error(
            (
                f'Please ensure that '
                f'{-default_long} <= MIN_LONG <= MAX_LONG <= {default_long} '
                f'and that '
                f'{-default_lat} <= MIN_LAT <= MAX_LAT <= {default_lat}'
            ),
        )
    return args


def main():
    """Program entry point."""
    args = _cli()
    credentials = (
        args.consumer_key, args.consumer_secret,
        args.access_token, args.access_token_secret,
    )
    worldmap = _get_worldmap()
    stream = _get_stream(credentials, worldmap)
    stream.filter(
        locations=[
            args.min_long,
            args.min_lat,
            args.max_long,
            args.max_lat,
        ],
        async=True,
    )

    def signal_handler(signum, frame):
        stream.disconnect()
        sys.exit('Aborted by user')

    signal.signal(signal.SIGINT, signal_handler)

    plt.show()


if __name__ == '__main__':
    main()
