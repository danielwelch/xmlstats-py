import json
import os
import unittest
from xmlstats import xmlstats

access_token = os.getenv("XML_STATS_ACCESS_TOKEN")
user_agent = os.getenv("XML_STATS_USER_AGENT")


class TestXmlStats(unittest.TestCase):

    s = xmlstats.Xmlstats(access_token, user_agent)

    with open('tests/test_boxscore.json', 'r') as f:
        boxscore = json.load(f)

    def test_build_url(self):
        event_id = "20120621-oklahoma-city-thunder-at-miami-heat"
        self.assertEqual(
            self.s._build_url(method="boxscore", sport="nba", id=event_id),
            "https://erikberg.com/nba/boxscore/20120621-oklahoma-city-thunder-at-miami-heat.json"
        )
        self.assertEqual(
            self.s._build_url(method="standings", sport="nba", date="20151031"),
            "https://erikberg.com/nba/standings/20151031.json"
        )

    # def test_http_get(self):
    #     url = "https://erikberg.com/nba/boxscore/20120621-oklahoma-city-thunder-at-miami-heat.json"
    #     result = self.s._http_get(url)
    #     self.assertEqual(self.boxscore, result)

    def test_http_get_timeout(self):
        urls = [
            (
                "https://erikberg.com/nba/boxscore/20141028-orlando-magic-at-new-orleans-pelicans.json",
                "orlando-magic"
            ),
            (
                "https://erikberg.com/nba/boxscore/20141030-washington-wizards-at-orlando-magic.json",
                "washington-wizards"
            ),
            (
                "https://erikberg.com/nba/boxscore/20141101-toronto-raptors-at-orlando-magic.json",
                "toronto-raptors"
            ),
            (
                "https://erikberg.com/nba/boxscore/20141104-orlando-magic-at-chicago-bulls.json",
                "orlando-magic"
            ),
            (
                "https://erikberg.com/nba/boxscore/20141111-orlando-magic-at-toronto-raptors.json",
                "orlando-magic"
            ),
            (
                "https://erikberg.com/nba/boxscore/20141115-orlando-magic-at-washington-wizards.json",
                "orlando-magic"
            ),
            (
                "https://erikberg.com/nba/boxscore/20141117-orlando-magic-at-detroit-pistons.json",
                "orlando-magic"
            )
        ]
        for url, team_id in urls:
            result = self.s._http_get(url)
            self.assertEqual(json.loads(result)["away_team"]["team_id"], team_id)

    def test_roster(self):
        result = self.s.roster(sport="nba", team_id="detroit-pistons")
        self.assertEqual(result.team.abbreviation, "DET")

    def test_events(self):
        ok = False
        result = self.s.events(sport="nba", date="2013-01-31")
        for e in result.event:
            if e.event_id == "20130131-memphis-grizzlies-at-oklahoma-city-thunder":
                ok = True
                self.assertEqual(e.away_team.team_id, "memphis-grizzlies")
        if not ok:
            raise

    def test_standings(self):
        result = self.s.standings(sport="nba", date="20170317")
        self.assertEqual(result.standing[0].team_id, "cleveland-cavaliers")

    def test_teams(self):
        result = self.s.teams(sport="nba")
        self.assertEqual(result[0].team_id, "atlanta-hawks")

    def test_team_results(self):
        result = self.s.team_results(sport="nba", team_id="atlanta-hawks")
        self.assertEqual(result[0].team.team_id, "atlanta-hawks")

    # def test_get_boxscore(self):
    #     event_id = "20120621-oklahoma-city-thunder-at-miami-heat"
    #     box = self.s.get_boxscore("nba", event_id)
    #     self.assertEqual(box.away_team.full_name, "Oklahoma City Thunder")

    # def test_get_events(self):
    #     date = "20130131"
    #     events = self.s.get_events(date, "nba")
    #     self.assertEqual(events.events_date, "2013-01-31T00:00:00-05:00")
