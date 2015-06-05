import requests
import datetime


class Struct:
    def __init__(self, data):
        for name, value in data.iteritems():
            setattr(self, name, self._wrap(value))

    def _wrap(self, value):
        if isinstance(value, (tuple, list, set, frozenset)):
            return type(value)([self._wrap(v) for v in value])
        else:
            return Struct(value) if isinstance(value, dict) else value


class Xmlstats:

    def __init__(self, access_token, user_agent):
        self.access_token = access_token
        self.user_agent = user_agent

    def build_url(self, sport, method, event_id, format="json"):
        host = "https://erikberg.com/"
        path = "/".join(filter(None, (sport, method, event_id)))
        url = host + path + "." + format
        return url

    def http_get(self, url, params):
        headers = {"Authorization": "Bearer " + self.access_token,
                   "User-Agent": "xmlstats-py/0.1" + self.user_agent}
        r = requests.get(url, headers=headers, params=params)
        if r.status_code == requests.codes.ok:
            return r.json()
        elif r.status_code == 429:
            xmlstats_reset = r.headers["xmlstats-api-reset"]
            now = int(datetime.now().strftime('%s'))
            delta = xmlstats_reset - now
            print(
                '''Requests limit reached.
                Waiting {} seconds to make new request'''.format(delta))
            return self.http_get(self, url)
        else:
            r.raise_for_status()

    def get_nba_boxscore(self, event_id):
        data = self.http_get(
            self.build_url(sport="nba", method="boxscore", event_id=event_id),
            params=None
            )
        boxscore = Struct(data)
        return boxscore
