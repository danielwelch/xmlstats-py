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

    def build_url(self, method, sport=None, date=None, id=None, format="json"):
        host = "https://erikberg.com/"
        path = "/".join(filter(None, (sport, method, date, id)))
        url = host + path + "." + format
        return url

    def http_get(self, url, params=None):
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

    def get_boxscore(self, sport, event_id):
        data = self.http_get(
            self.build_url(sport=sport, method="boxscore", id=event_id),
            params=None
            )
        boxscore = Struct(data)
        return boxscore

    def get_nba_team_stats(self, date, team_id=None):
        data = self.http_get(
            self.buildurl(sport="nba", method="team-stats", date=date),
            params={
                "team_id": team_id,
                }
            )
        team_stats = Struct(data)
        return team_stats

    def get_events(self, date, sport):
        data = self.http_get(
            self.build_url(method="events"),
            params={
                "date": date,
                "sport": sport,
                }
            )
        events = Struct(data)
        return events

    def get_roster(self, sport, team_id, status=None):
        '''arg stats="expanded" will return 40-man roster for MLB team,
        rather than 25-man roster
        '''
        data = self.http_get(
            self.build_url(sport=sport, method="roster", id=team_id),
            params={
                "status": status
                }
            )
        roster = Struct(data)
        return roster

    def get_nba_draft_results(self, season=None, team_id=None):
        data = self.http_get(
            self.build_url(sport="nba", method="draft"),
            params={
                "season": season,
                "team_id": team_id
                }
            )
        draft_results = Struct(data)
        return draft_results

    def get_nba_leaders(self, category, limit=None,
                        qualified=None, season_type=None):
        '''For list of category IDs, see xmlstats API docs:
        https://erikberg.com/api/methods/nba-leaders
        Qualified parameter determines whether players who meet NBA's minimum
        qualifications will be returned, or all players. API defaults to true
        '''
        data = self.http_get(
            self.build_url(sport="nba", method="leaders", id=category),
            params={
                "limit": limit,
                "qualified": qualified,
                "season_type": season_type,
                }
            )
        leaders = Struct(data)
        return leaders

    def get_teams(self, sport):
        data = self.http_get(
            self.build_url(sport=sport, method="teams"),
            )
        teams = Struct(data)
        return teams

    def get_team_results(self, sport, team_id, season=None, since=None,
                         until=None, order=None):
        data = self.http_get(
            self.build_url(sport=sport, method="results", id=team_id),
            params={
                "season": season,
                "since": since,
                "until": until,
                "order": order,
                }
            )
        results = Struct(data)
        return results

    def get_standings(self, sport, date=None):
        data = self.http_get(
            self.build_url(sport=sport, method="standings", date=date)
            )
        standings = Struct(data)
        return standings

    def get_wildcard_standings(self, date):
        data = self.http_get(
            self.build_url(sport="mlb", method="wildcard", date=date)
            )
        wildcard = Struct(data)
        return wildcard
