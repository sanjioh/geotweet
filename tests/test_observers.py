import io
from unittest import mock

from geotweet.observers import ConsoleObserver, MapObserver


class StubFormatter:
    def __init__(self, *, with_raise=False):
        self._raise = with_raise

    def format(self, tweet):
        if self._raise:
            raise Exception
        t = tweet
        return (
            f'{t.longitude}|{t.latitude}|{t.user_name}|'
            f'{t.user_screen_name}|{t.text}'
        )


def test_consoleobserver_update(status):
    formatter = StubFormatter()
    fp = io.StringIO()
    obs = ConsoleObserver(formatter, fp=fp)
    ret = obs.update(status)
    assert fp.getvalue() == '100|45|user_name|user_screen_name|Hello World'
    assert ret is None


def test_consoleobserver_update_malformed(status):
    del status.coordinates  # Simulate missing information.
    formatter = StubFormatter()
    fp = io.StringIO()
    obs = ConsoleObserver(formatter, fp=fp)
    ret = obs.update(status)
    assert fp.getvalue() == ''
    assert ret is None


def test_consoleobserver_update_formatter_error(status):
    formatter = StubFormatter(with_raise=True)
    fp = io.StringIO()
    obs = ConsoleObserver(formatter, fp=fp)
    ret = obs.update(status)
    assert fp.getvalue() == ''
    assert ret is None


def test_mapobserver_update(status):
    figure, worldmap = mock.Mock(), mock.Mock()
    worldmap.return_value = [10, 15]
    obs = MapObserver(figure, worldmap)
    ret = obs.update(status)
    worldmap.plot.assert_called_once_with(10, 15, 'ro', markersize=5)
    figure.canvas.start_event_loop.assert_called_once_with(0.001)
    assert ret is None


def test_mapobserver_update_malformed(status):
    del status.coordinates  # Simulate missing information.
    figure, worldmap = mock.Mock(), mock.Mock()
    obs = MapObserver(figure, worldmap)
    ret = obs.update(status)
    assert ret is None


def test_mapobserver_update_plot_error(status):
    figure, worldmap = mock.Mock(), mock.Mock()
    worldmap.return_value = [10, 15]
    worldmap.plot.side_effect = Exception
    obs = MapObserver(figure, worldmap)
    ret = obs.update(status)
    assert ret is None


def test_mapobserver_update_event_loop_error(status):
    figure, worldmap = mock.Mock(), mock.Mock()
    worldmap.return_value = [10, 15]
    figure.canvas.start_event_loop.side_effect = Exception
    obs = MapObserver(figure, worldmap)
    ret = obs.update(status)
    assert ret is None
