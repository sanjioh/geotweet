from unittest import mock

import pytest


@pytest.fixture
def status():
    status = mock.Mock()
    status.coordinates = {
        'coordinates': [100, 45],
    }
    status.user.name = 'user_name'
    status.user.screen_name = 'user_screen_name'
    status.text = 'Hello World'
    return status
