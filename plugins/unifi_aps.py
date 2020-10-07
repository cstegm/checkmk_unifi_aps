#!/usr/bin/python3
import pprint
pp = pprint.PrettyPrinter()



import os
import json
import logging
import requests
import shutil
import time
import warnings
import configparser

cfgfile = '/etc/check_mk/unifi_aps.cfg'

if not os.path.exists(cfgfile):
  quit()
 

config = configparser.ConfigParser()
config.read(os.fspath(cfgfile))
hostname = config.get('unifi_controller','hostname')
username = config.get('unifi_controller','username')
password = config.get('unifi_controller','password')
ssl_verify = config.getboolean('unifi_controller','ssl_verify')

class APIError(Exception):
    pass


def retry_login(func, *args, **kwargs):
    """To reattempt login if requests exception(s) occur at time of call"""
    def wrapper(*args, **kwargs):
        try:
            try:
                return func(*args, **kwargs)
            except (requests.exceptions.RequestException,
                    APIError) as err:
                controller = args[0]
                controller._login()
                return func(*args, **kwargs)
        except Exception as err:
            raise APIError(err)
    return wrapper

class Controller(object):

    def __init__(self, host, username, password, port=8443,
                 version='v5', site_id='default', ssl_verify=True):

        if version == "unifiOS":
            self.host = host
            self.username = username
            self.password = password
            self.site_id = site_id
            self.ssl_verify = ssl_verify
            self.url = 'https://' + host + '/proxy/network/'

            if ssl_verify is False:
                warnings.simplefilter("ignore", category=requests.packages.
                                      urllib3.exceptions.
                                      InsecureRequestWarning)

            self.session = requests.Session()
            self.session.verify = ssl_verify

            self._login()

        if version[:1] == 'v':
            if float(version[1:]) < 4:
                raise APIError("%s controllers no longer supported" % version)

            self.host = host
            self.port = port
            self.version = version
            self.username = username
            self.password = password
            self.site_id = site_id
            self.url = 'https://' + host + ':' + str(port) + '/'
            self.ssl_verify = ssl_verify

            if ssl_verify is False:
                warnings.simplefilter("ignore", category=requests.packages.
                                      urllib3.exceptions.
                                      InsecureRequestWarning)

            self.session = requests.Session()
            self.session.verify = ssl_verify

            self._login()

    @staticmethod
    def _jsondec(data):
        obj = json.loads(data)
        if 'meta' in obj:
            if obj['meta']['rc'] != 'ok':
                raise APIError(obj['meta']['msg'])
        if 'data' in obj:
            return obj['data']
        else:
            return obj

    def _api_url(self):
        return self.url + 'api/s/' + self.site_id + '/'

    @retry_login
    def _read(self, url, params=None):
        # Try block to handle the unifi server being offline.
        r = self.session.get(url, params=params)
        return self._jsondec(r.text)

    def _api_read(self, url, params=None):
        return self._read(self._api_url() + url, params)

    @retry_login
    def _write(self, url, params=None):
        r = self.session.post(url, json=params)
        return self._jsondec(r.text)

    def _api_write(self, url, params=None):
        return self._write(self._api_url() + url, params)

    @retry_login
    def _update(self, url, params=None):
        r = self.session.put(url, json=params)
        return self._jsondec(r.text)

    def _api_update(self, url, params=None):
        return self._update(self._api_url() + url, params)

    def _login(self):

        params = {'username': self.username, 'password': self.password}
        login_url = self.url + 'api/login'

        r = self.session.post(login_url, json=params)
        if r.status_code != 200:
            raise APIError("Login failed - status code: %i" % r.status_code)

    def _logout(self):
        self._api_write('logout')

    def get_aps(self):
        """Return a list of all APs,
        with significant information about each.
        """
        # Set test to 0 instead of NULL
        params = {'_depth': 3, 'test': 0}
        return self._api_read('stat/device', params)




c = Controller( hostname, username, password, ssl_verify = ssl_verify)
aps = c.get_aps()
for ap in aps:
  name = ap["name"].replace(":","_")
  print("<<<<" + name + ">>>>")
  print( "<<<unifi_aps>>>")
  print(json.dumps(ap))
  print( "<<<>>>")


