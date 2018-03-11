from geotweet.formatters import SimpleFormatter
from geotweet.observers import Tweet


def test_simpleformatter_format(status):
    formatter = SimpleFormatter()
    tweet = Tweet(
        *status.coordinates['coordinates'],
        status.user.name,
        status.user.screen_name,
        status.text,
    )
    formatted_tweet = formatter.format(tweet)
    expected = (
        f'User: @{tweet.user_screen_name} ({tweet.user_name})\n'
        f'Location: {tweet.longitude} longitude, {tweet.latitude} latitude\n'
        f'Tweet: {tweet.text}\n\n'
    )
    assert formatted_tweet == expected
