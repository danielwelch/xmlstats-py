import json
import os
import unittest
from xmlstats import xmlstats

access_token = os.getenv("XML_STATS_ACCESS_TOKEN")
user_agent = os.getenv("XML_STATS_USER_AGENT")


class TestXmlStats(unittest.TestCase):

    s = xmlstats.Xmlstats(access_token, user_agent, objectify=True)
    s_native = xmlstats.Xmlstats(access_token, user_agent, objectify=False)

    with open('tests/test_boxscore.json', 'r') as f:
        boxscore = json.load(f)

    def test_build_url(self):
        event_id = "20120621-oklahoma-city-thunder-at-miami-heat"
        self.assertEqual(
            self.s.build_url(method="boxscore", sport="nba", id=event_id),
            "https://erikberg.com/nba/boxscore/20120621-oklahoma-city-thunder-at-miami-heat.json"
        )
        self.assertEqual(
            self.s.build_url(method="standings", sport="nba", date="20151031"),
            "https://erikberg.com/nba/standings/20151031.json"
        )

    def test_http_get(self):
        url = "https://erikberg.com/nba/boxscore/20120621-oklahoma-city-thunder-at-miami-heat.json"
        result = self.s.http_get(url)
        print(result)
        self.assertEqual(
            self.boxscore["home_period_scores"],
            result["home_period_scores"]
        )
        self.assertEqual(self.boxscore.keys(), result.keys())

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
            result = self.s.http_get(url)
            self.assertEqual(result["away_team"]["team_id"], team_id)
