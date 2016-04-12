"""
A Python wrapper for the Foobot air quality sensor API.
"""

import requests

BASE_URL = 'https://api.Foobot.io/v2'


class Foobot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()

        self.token = self.login()
        if self.token is None:
            raise ValueError("Provided username or password is not valid.")

        self.auth_header = {'Accept': 'application/json;charset=UTF-8',
                            'x-auth-token': self.token}

    def login(self):
        """Log into a foobot device."""
        url = '{base}/user/{user}/login/'.format(base=BASE_URL,
                                                 user=self.username)
        req = self.session.get(url, auth=(self.username, self.password))
        return req.headers['X-AUTH-TOKEN'] if req.text == "true" else None

    def devices(self):
        """Get list of foobot devices owned by logged in user."""
        url = '{base}/owner/{user}/device/'.format(base=BASE_URL,
                                                   user=self.username)
        req = self.session.get(url, headers=self.auth_header)
        return [FoobotDevice(self.token, **device) for device in req.json()]


class FoobotDevice:
    def __init__(self, token, userId, uuid, name, mac):
        self.token = token
        self.userId = userId
        self.uuid = uuid
        self.name = name
        self.mac = mac
        self.session = requests.Session()
        self.auth_header = {'Accept': 'application/json;charset=UTF-8',
                            'x-auth-token': self.token}

    def latest(self):
        """Get latest sample from foobot device."""
        url = '{base}/device/{uuid}/datapoint/{period}/last/{sampling}/'
        url = url.format(base=BASE_URL,
                         uuid=self.uuid,
                         period=0,
                         sampling=0)
        req = self.session.get(url, headers=self.auth_header)
        return req.json()

    def data_period(self, period, sampling):
        """Get a specified period of data samples."""
        url = '{base}/device/{uuid}/datapoint/{period}/last/{sampling}/'
        url = url.format(base=BASE_URL,
                         uuid=self.uuid,
                         period=period,
                         sampling=sampling)

        req = self.session.get(url, headers=self.auth_header)
        return req.json()

    def data_range(self, start, end, sampling):
        """Get a specified range of data samples."""
        url = '{base}/device/{uuid}/datapoint/{start}/{end}/{sampling}/'
        url = url.format(base=BASE_URL,
                         uuid=self.uuid,
                         start=start,
                         end=end,
                         sampling=sampling)

        req = self.session.get(url, headers=self.auth_header)
        return req.json()
