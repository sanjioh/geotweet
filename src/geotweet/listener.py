"""
Listener module.

This module contains the GeoStreamListener class.
"""

import tweepy


class GeoStreamListener(tweepy.StreamListener):
    """
    Provide hooks to be invoked when certain events happen.

    As a subclass of tweepy.StreamListener, this class
    is the main bridge between our code and the tweepy streaming library.
    It's methods are hooks that the tweepy machinery will invoke
    when something relevant happens (new tweets, unhandled errors,
    timeouts, and so on).
    This implementation shuts the program down whenever something
    erroneous or unexpected occurs.
    """

    def __init__(self, runner, observers=None):
        """Initialize a GeoStreamListener object."""
        self._runner = runner
        self._observers = observers or []
        super().__init__()

    def on_status(self, status):
        """Notify all the observers of a new geolocalized tweet."""
        if status.coordinates is not None:
            for observer in self._observers:
                observer.update(status)

    def _exit(self, reason):
        print(f'Something went wrong: {reason} - exiting.')
        self._runner.stop()

    def on_exception(self, exception):
        """Handle exceptions."""
        self._exit(f'unhandled exception ({exception!a})')

    def on_error(self, status_code):
        """Handle unexpected HTTP status codes coming from Twitter APIs."""
        self._exit(f'status code {status_code}')

    def on_timeout(self):
        """Handle stream timeouts."""
        self._exit('timeout')

    def on_disconnect(self, notice):
        """Handle stream disconnections."""
        self._exit('disconnected ({notice})')

    def on_warning(self, notice):
        """Handle Twitter warning notices."""
        self._exit('warning received ({notice})')
