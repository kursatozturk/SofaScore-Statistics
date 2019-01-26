from .BaseHandler import BaseHandler

from .DataBaseHandler import Db_handler
import pickle

class TeamHandler(BaseHandler):
    """
        CREATE TABLE Team(
            team_id INTEGER PRIMARY KEY,
            team_info BLOB
        );

    """

    def __init__(self, date, team_info):


        unique_id = team_info['id']
        query_string = 'INSERT INTO Team VALUES(?, ?);'
        params = (unique_id, pickle.dumps(team_info))
        Db_handler.db_queue.put((query_string, params))
        