#xmlstats-py
[![Build Status](https://travis-ci.org/danielwelch/xmlstats-py.svg?branch=master)](https://travis-ci.org/danielwelch/xmlstats-py)

A python module for interacting with the [xmlstats API](https://erikberg.com/api)

This module aims to closely mirror the methods provided by the xmlstats API in terms of parameters and output structure.


##Installing
```pip install xmlstats-py```

Tested against Python 2.7, 3.2-3.6

##Usage
Instantiate an XmlStats object using a valid access token and user agent, obtained from the [xmlstats API](https://erikberg.com/api).

```python
stats = Xmlstats(access_token=MY_ACCESS_TOKEN, user_agent=MY_USER_AGENT)
```
This object exposes a number of methods (one for each API endpoint) that return a NamedTuple representation of the data provided by the API. The JSON response is processed with ```json.loads```, and a custom ```object_hook``` is used to convert JSON objects into NamedTuples when they are encountered. This means fields can be accessed using dot notation.

####Methods
Each method exposed by the Xmlstats class aims to mirror an the endpoint provided by the API. See the [API documentation](https://erikberg.com/api/methods) for a complete explanation of parameters and results.

|API Endpoint|Class Method|
|------------|------------|
|[Events](https://erikberg.com/api/endpoints/events)|events|
|[Roster](https://erikberg.com/api/endpoints/roster)|roster|
|[Standings](https://erikberg.com/api/endpoints/standings)|standings|
|[Teams](https://erikberg.com/api/endpoints/teams)|teams|
|[Team Schedule/Results](https://erikberg.com/api/endpoints/team-results)|team_results|
|[NBA Box Score](https://erikberg.com/api/endpoints/nba-box-score)|nba_box_score|
|[NBA Draft](https://erikberg.com/api/endpoints/nba-draft)|nba_draft|
|[NBA Daily Leaders](https://erikberg.com/api/endpoints/nba-daily-leaders)|nba_daily_leaders|
|[NBA Team Stats](https://erikberg.com/api/endpoints/nba-team-stats)|nba_team_stats|
|[MLB Box Score](https://erikberg.com/api/endpoints/mlb-box-score)|mlb_box_score|
|[MLB Wild Card Standings](https://erikberg.com/api/endpoints/mlb-wild-card-standings)|mlb_wild_card_standings|

##Examples

####Get Boxscores for a given date -  *yyyymmdd*

```python
stats = Xmlstats(access_token=MY_ACCESS_TOKEN, user_agent=MY_USER_AGENT)
events = stats.events(date="20141028", sport="nba")  # returns NamedTuple "Events" which mirrors data structure explained in API documentation, containing all NBA events on given date
event_ids = [event.event_id for event in events.event]
boxscores = [
        stats.nba_box_score(eid) for eid in event_ids
]
```
