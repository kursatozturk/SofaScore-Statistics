from .BaseHandler import BaseHandler
from .DataBaseHandler import Db_handler
import pickle

class EventHandler(BaseHandler):
    """
        CREATE TABLES Event(
            event_id INTEGER PRIMARY KEY,
            home_team_id INTEGER,
            away_team_id INTEGER,
            DATE date,
            event_info BLOB,
            FOREIGN KEY(home_team_id) REFERENCES Team,
            FOREIGN KEY(away_team_id) REFERENCES Team
        );
    """
    def __init__(self, date, event_info, lineups):
        """
        [
            'event', 'matchInfo', 'teamsForm', 'winningOdds',
            'incidents', 'groupedIncidents', 'innings', 'vote',
            'odds', 'highlights', 'statistics', 'liveForm',
            'scoreGraph', 'standingsAvailable', 'pointByPoint',
            'managerDuel', 'h2hDuel',
        ]
        """

        unique_id = event_info['event']['id']
        home_team = event_info['event']['homeTeam']
        away_team = event_info['event']['awayTeam']
        ht_id = home_team['id']
        at_id = away_team['id']
        score = {
            'home_score': event_info['event']['homeScore'],
            'away_score': event_info['event']['awayScore'],
        }
        #statistics = {
        #    'period1': event_info['event']['statistics']['perod1'],
        #    'period2': event_info['event']['statistics']['perod2'],
        #}
        event_info = {
            'lineups': lineups,
            'score': score,
            #'stats': statistics
        }
        query_string = 'INSERT INTO Event Values(?, ?, ?, ?, ?);'
        params = (unique_id, ht_id, at_id, date, pickle.dumps(event_info))
        Db_handler.db_queue.put((query_string, params))
    