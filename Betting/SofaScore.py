import requests
from Betting.handlers.DateHandler import DateHandler
from Betting.utils.python_utils import Singleton
from time import sleep

class SofaScore(metaclass=Singleton):

    def __init__(self):
        # not generic, will give a hand for it, if it become necessary
        self.by_date_url = "https://www.sofascore.com/football//{date}/json"  # yyyy-mm-dd
        self.event_url = "https://www.sofascore.com/event/{event_id}/json"
        self.lineups_url = "https://www.sofascore.com/event/{event_id}/lineups/json"
        self.player_statistics = "https://www.sofascore.com/event/{event_id}/player/{player_id}/statistics/json"
        # self.get = lambda url: requests.get(url).json()

    def get(self, url):
        try:
            json_val = requests.get(url).json()
            return json_val
        except Exception as e:
            # TODO: correct exception handling avoid unwanted behaviour
            print(e)
            sleep(60)
            return self.get(url)
    def parse_by_date(self, e_date):
        # Generator creator
        # all events are generated btw begin_date and end_date
        url = self.by_date_url.format(date=e_date)
        return e_date, self.get(url)

    def parse_event(self, event_id):
        url = self.event_url.format(event_id=event_id)
        return event_id, self.get(url)

    def parse_lineups_event(self, event_id):
        url = self.lineups_url.format(event_id=event_id)
        return event_id, self.get(url)

    def parse_player_stat(self, ids):
        event_id, player_id = ids
        url = self.player_statistics.format(event_id=event_id, player_id=player_id)
        return event_id, player_id, self.get(url)
