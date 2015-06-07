#xmlstats-py
A library for interacting with the xmlstats API -- https://erikberg.com/api

Method calls return instances that mirror the structure of the xmlstats API


##Installing
```pip install xmlstats-py```

##Usage

##Examples

####Get Boxscores for a given date -  *yyyymmdd*


```python
stats = Xmlstats(access_token=MY_ACCESS_TOKEN, user_agent=MY_USER_AGENT)
events = stats.get_events(date=20141028, sport="nba")  # returns event objects for all nba events on given date
event_ids = [event.event_id for event in events.event]
boxscores = []
for event_id in event_ids:
    boxscores.append(stats.get_boxscore(sport="nba", event_id))
```
Note: As in the xmlstats API, the `get_events()` method returns an instance with 2 attributes: `events_date` is a date string; `event` is an array of event objects