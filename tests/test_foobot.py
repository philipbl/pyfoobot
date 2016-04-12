import os
import arrow
import pytest
from unittest.mock import patch
from pyfoobot import Foobot


def check_data(data):
    assert 'datapoints' in data
    assert 'units' in data
    assert 'sensors' in data
    assert (len(data['datapoints'][0]) ==
            len(data['units']) ==
            len(data['sensors']))


@pytest.mark.usefixtures('betamax_session')
class Test:
    def setup_method(self, method):
        self.user = os.environ.get('FOOBOT_USER', '')
        self.password = os.environ.get('FOOBOT_PASSWORD', '')

    def test_bad_login(self, betamax_session):
        with patch('pyfoobot.requests.Session',
                   return_value=betamax_session):
            with pytest.raises(ValueError):
                Foobot("username", "password")

    def test_devices(self, betamax_session):
        with patch('pyfoobot.requests.Session',
                   return_value=betamax_session):
            fb = Foobot(self.user, self.password)
            devices = fb.devices()

            assert len(devices) == 1
            assert devices[0].userId == 1234
            assert devices[0].uuid == '123456789ABCDEF'
            assert devices[0].name == 'HappyBot'
            assert devices[0].mac == '1234'

    def test_latest(self, betamax_session):
        with patch('pyfoobot.requests.Session',
                   return_value=betamax_session):
            fb = Foobot(self.user, self.password)

            devices = fb.devices()
            assert len(devices) == 1

            device = devices[0]
            data = device.latest()

            # General data checks
            check_data(data)

            # Specific checks
            assert len(data['datapoints']) == 1
            assert data['start'] == data['end']

    def test_data_period(self, betamax_session):
        period = 3600
        sampling = 60

        with patch('pyfoobot.requests.Session',
                   return_value=betamax_session):
            fb = Foobot(self.user, self.password)

            devices = fb.devices()
            assert len(devices) == 1

            device = devices[0]
            data = device.data_period(period=period, sampling=sampling)

            # General data checks
            check_data(data)

            # Specific checks
            assert len(data['datapoints']) == 13
            assert data['end'] - data['start'] < period

    def test_data_range(self, betamax_session):
        start = '2016-04-12T11:00:00'
        end = '2016-04-12T12:00:00'
        sampling = 0

        with patch('pyfoobot.requests.Session',
                   return_value=betamax_session):
            fb = Foobot(self.user, self.password)

            devices = fb.devices()
            assert len(devices) == 1

            device = devices[0]
            data = device.data_range(start=start,
                                     end=end,
                                     sampling=sampling)

            # General data checks
            check_data(data)

            # Specific checks
            assert len(data['datapoints']) == 13
            assert data['start'] > arrow.get(start).timestamp
            assert data['end'] < arrow.get(end).timestamp
            assert data['start'] != data['end']
