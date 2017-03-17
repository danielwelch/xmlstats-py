from collections import namedtuple
from datetime import datetime
import json
import requests
import time


__version__ = "1.0.0"


# class Struct:
#     def __init__(self, data):
#         for name, value in data.items():
#             setattr(self, name, self._wrap(value))

#     def _wrap(self, value):
#         if isinstance(value, (tuple, list, set, frozenset)):
#             return type(value)([self._wrap(v) for v in value])
#         else:
#             return Struct(value) if isinstance(value, dict) else value


class Xmlstats:

    def __init__(self, access_token, user_agent, objectify=True):
        self.access_token = access_token
        self.user_agent = user_agent
        # self.objectify = objectify

    # def objectify_off(self):
        # self.objectify = False
        # return

    # def objectify_on(self):
        # self.objectify = True
        # return

    def _format_result(self, name, data_str):
        # http://stackoverflow.com/a/15882054/7164290
        return json.loads(
                data_str,
                object_hook=lambda d: namedtuple(name, d.keys())(*d.values())
        )

    # def format_result(self, data, objectify):
    #     if objectify:
    #         return Struct(data)
    #     else:
    #         return data

    def _build_url(self, method, sport=None, date=None, id=None, format="json"):
        host = "https://erikberg.com/"
        path = "/".join(filter(None, (sport, method, date, id)))
        url = host + path + "." + format
        return url

    def _http_get(self, url, params=None):
        headers = {
            "Authorization": "Bearer " + self.access_token,
            "User-Agent": "xmlstats-py/" + __version__ + " " + self.user_agent
        }
        r = requests.get(url, headers=headers, params=params)
        if r.status_code == requests.codes.ok:
            return r.text
        elif r.status_code == 429:
            xmlstats_reset = int(r.headers["xmlstats-api-reset"])
            now = int(datetime.now().strftime('%s'))
            delta = xmlstats_reset - now
            if delta < 0:  # the API seems to sometimes return -1 sec
                return self._http_get(url, params)
            print(
                '''Requests limit reached.
                Waiting {} seconds to make new request'''.format(delta)
            )
            time.sleep(delta)
            return self._http_get(url, params)
        else:
            r.raise_for_status()

    def roster(self, sport, team_id, expanded=False):
        data = self._http_get(
                self._build_url(sport=sport, method="roster", id=team_id),
                params={
                    "status": ("expanded" if expanded else "")
                }
        )
        return self._format_result("Roster", data)

    def events(self, sport=None, date=None):
        data = self._http_get(
                self._build_url(method="events"),
                params={
                    "date": date,
                    "sport": sport
                }
        )
        return self._format_result("Events", data)

    def standings(self, sport, date=None):
        data = self._http_get(
                self._build_url(method="standings", sport=sport, date=date),
        )
        return self._format_result("Standings", data)

    def teams(self, sport):
        data = self._http_get(
                self._build_url(method="teams", sport=sport),
        )
        return self._format_result("Teams", data)

    def team_results(self, sport, team_id, season=None, opponent=None,
                     location_type=None, event_status=None, since=None,
                     until=None, last=None, next=None, order=None):
        data = self._http_get(
                self._build_url(method="results", sport=sport, id=team_id),
                params={
                    season: season,
                    opponent: opponent,
                    location_type: location_type,
                    event_status: event_status,
                    since: since,
                    until: until,
                    last: last,
                    next: next,
                    order: order
                }
        )
        return self._format_result("TeamResults", data)

    ################
    # NBA METHODS  #
    ################

    def nba_box_score(self, event_id):
        data = self._http_get(
            self._build_url(sport="nba", method="boxscore", id=event_id),
        )
        return self._format_result("NBABoxscore", data)

    def nba_draft(self, season=None, team_id=None):
        data = self._http_get(
                self._build_url(sport="nba", method="draft"),
                params={
                    season: season,
                    team_id: team_id
                }
        )
        return self._format_result("NBADraft", data)

    # def nba_leaders(self, category_id, limit, qualified, season_type):
    #     # need to pull in / look at category_ids defined for this method

    def nba_daily_leaders(self, date=None, sort=None):
        data = self._http_get(
                self._build_url(sport="nba", method="daily-leaders", date=date),
                params={
                    sort: sort
                }
        )
        return self._format_result("NBADailyLeaders", data)

    def nba_team_stats(self, date=None, team_id=None, season_type=None):
        data = self._http_get(
                self._build_url(sport="nba", method="team-stats", date=date),
                params={
                    season_type: season_type,
                    team_id: team_id
                }
        )
        return self._format_result("NBATeamStats", data)

    ################
    # MLB METHODS  #
    ################

    def mlb_box_score(self, event_id):
        data = self._http_get(
            self._build_url(sport="mlb", method="boxscore", id=event_id),
        )
        return self._format_result("MLBBoxscore", data)

    def mlb_wild_card_standings(self, date=None):
        data = self._http_get(
                self._build_url(sport="mlb", method="wildcard", date=date)
        )
        return self._format_result("MLBWildcardStandings", data)
