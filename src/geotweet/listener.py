import os

import tweepy


class GeoStreamListener(tweepy.StreamListener):
    def __init__(self, observers=None):
        self._observers = observers or []
        super().__init__()

    def on_status(self, status):
        if status.coordinates is not None:
            for observer in self._observers:
                observer.update(status)

    @staticmethod
    def _exit(reason):
        print(f'Something went wrong: {reason} - exiting.')
        os._exit(1)

    def on_exception(self, exception):
        self._exit(f'unhandled exception ({exception!a})')

    def on_limit(self, track):
        # TODO: ???
        return

    def on_error(self, status_code):
        self._exit(f'status code {status_code}')

    def on_timeout(self):
        self._exit('timeout')

    def on_disconnect(self, notice):
        self._exit('disconnected ({notice})')

    def on_warning(self, notice):
        self._exit('warning received ({notice})')
