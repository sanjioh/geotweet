from unittest import mock

from geotweet.listener import GeoStreamListener


def test_geostreamlistener_on_status(status):
    runner = None
    observers = [mock.Mock() for _ in range(2)]
    gsl = GeoStreamListener(runner, observers)
    ret = gsl.on_status(status)
    assert ret is None
    for obs in observers:
        obs.update.assert_called_once_with(status)


def test_geostreamlistener_on_status_no_coordinates(status):
    status.coordinates = None
    runner = None
    observers = [mock.Mock() for _ in range(2)]
    gsl = GeoStreamListener(runner, observers)
    ret = gsl.on_status(status)
    assert ret is None
    for obs in observers:
        obs.update.assert_not_called()


def test_geostreamlistener_on_exception():
    runner = mock.Mock()
    gsl = GeoStreamListener(runner)
    ret = gsl.on_exception(Exception())
    assert ret is None
    runner.stop.assert_called_once()


def test_geostreamlistener_on_error():
    runner = mock.Mock()
    gsl = GeoStreamListener(runner)
    ret = gsl.on_error(503)
    assert ret is None
    runner.stop.assert_called_once()


def test_geostreamlistener_on_timeout():
    runner = mock.Mock()
    gsl = GeoStreamListener(runner)
    ret = gsl.on_timeout()
    assert ret is None
    runner.stop.assert_called_once()


def test_geostreamlistener_on_disconnect():
    runner = mock.Mock()
    gsl = GeoStreamListener(runner)
    ret = gsl.on_disconnect('notice')
    assert ret is None
    runner.stop.assert_called_once()


def test_geostreamlistener_on_warning():
    runner = mock.Mock()
    gsl = GeoStreamListener(runner)
    ret = gsl.on_warning('notice')
    assert ret is None
    runner.stop.assert_called_once()
