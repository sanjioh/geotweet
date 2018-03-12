"""
Formatters module.

The class observer.ConsoleObserver uses a formatter to render a
string representation of a tweet to the terminal, according to
some particular formatting strategy.
This module can be extended with other formatter classes; they only
need to implement a format() method that takes as argument an
observers.Tweet instance.
"""


class SimpleFormatter:
    """Create simple string representations of tweets."""

    _format_string = (
        'User: @{tweet.user_screen_name} ({tweet.user_name})\n'
        'Location: {tweet.longitude} longitude, {tweet.latitude} latitude\n'
        'Tweet: {tweet.text}\n\n'
    )

    def format(self, tweet):
        """Build a string representation of a tweet."""
        return self._format_string.format(tweet=tweet)
