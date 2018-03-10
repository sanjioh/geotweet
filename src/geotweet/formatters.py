class SimpleFormatter:
    _format_string = (
        'User: @{tweet.user_screen_name} ({tweet.user_name})\n'
        'Location: {tweet.longitude} longitude, {tweet.latitude} latitude\n'
        'Tweet: {tweet.text}\n\n'
    )

    def format(self, tweet):
        return self._format_string.format(tweet=tweet)
