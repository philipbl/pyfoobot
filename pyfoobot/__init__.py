from collections import namedtuple
import requests

FoobotDevice = namedtuple('FooBotDevice', ['userId', 'uuid', 'name', 'mac'])

class Foobot:
    def __init__(self, username, password):
        self.base_url = 'https://api.Foobot.io/v2'
        self.username = username
        self.password = password

        self.token = self.login()
        if self.token is None:
            raise Exception("User does not exist.")

        self.auth_header = {'Accept': 'application/json;charset=UTF-8',
                            'x-auth-token': self.token}

    @staticmethod
    def _get_uuid(uuid):
        if isinstance(uuid, FoobotDevice):
            return uuid.uuid
        else:
            return uuid

    def login(self):
        url = '{base}/user/{user}/login/'.format(base=self.base_url,
                                                 user=self.username)
        req = requests.get(url, auth=(self.username, self.password))
        return req.headers['X-AUTH-TOKEN'] if req.text == "true" else None

    def devices(self):
        url = '{base}/owner/{user}/device/'.format(base=self.base_url,
                                                   user=self.username)
        req = requests.get(url, headers=self.auth_header)
        return [FoobotDevice(**device) for device in req.json()]

    def latest(self, uuid):
        uuid = self._get_uuid(uuid)
        url = '{base}/device/{uuid}/datapoint/{period}/last/{sampling}/'
        url = url.format(base=self.base_url,
                         uuid=uuid,
                         period=0,
                         sampling=0)
        req = requests.get(url, headers=self.auth_header)
        return req.json()

    def data_period(self, uuid, period, sampling):
        uuid = self._get_uuid(uuid)
        url = '{base}/device/{uuid}/datapoint/{period}/last/{sampling}/'
        url = url.format(base=self.base_url,
                         uuid=uuid,
                         period=period,
                         sampling=sampling)

        req = requests.get(url, headers=self.auth_header)
        return req.json()

    def data_range(self, uuid, start, end, sampling):
        uuid = self._get_uuid(uuid)
        url = '{base}/device/{uuid}/datapoint/{start}/{end}/{sampling}/'
        url = url.format(base=self.base_url,
                         uuid=uuid,
                         start=start,
                         end=end,
                         sampling=sampling)

        req = requests.get(url, headers=self.auth_header)
        return req.json()
