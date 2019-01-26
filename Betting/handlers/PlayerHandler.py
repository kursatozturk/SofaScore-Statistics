from .BaseHandler import BaseHandler
from .DataBaseHandler import Db_handler
import pickle
import re

class PlayerHandler(BaseHandler):
    """
        CREATE TABLES Player(
            player_id INTEGER PRIMARY KEY,
            player_info BLOB,
        );
        CREATE TABLES Statistics(
            player_id INTEGER,
            event_id INTEGER,
            stats BLOB,
            FOREIGN KEY(player_id) REFERENCES Player,
            FOREIGN KEY(event_id) REFERENCES Event,
            PRIMARY KEY(player_id, event_id)
        );
    """
    def __init__(self, date, player_info):

        unique_id = player_info['id']
        query_string = 'INSERT INTO Player VALUES(?, ?);'
        params = (unique_id, pickle.dumps(player_info))
        Db_handler.db_queue.put((query_string, params))
        # self.info = player_info
        super().__init__(date, player_info)
    
    @staticmethod
    def add_event(player_id, event_id, statistics):
        # add to db
        query_string = 'INSERT INTO Statistics VALUES(?, ?, ?);'
        statistics = PlayerHandler.parse_statistics(statistics)
        params = (player_id, event_id, pickle.dumps(statistics))
        Db_handler.db_queue.put((query_string, params))

    @staticmethod
    def parse_value(d, key):
        name_val_pair = d.get(key)
        if name_val_pair is None:
            return [0]
        if 'raw' in name_val_pair.keys():
            val = name_val_pair['raw']
            return val
        name, val = name_val_pair.values()
        val = re.findall(r'\d+', val)
        if val == []:
            return [0, 0] if '(' in name else [0]
        return_val = list()
        for v in val:
            return_val.append(int(v))
        return return_val

    @staticmethod
    def parse_statistics(stat_dict):

        """
            # Parse statistics for players from Event
            'lineupsSorted': idx : 'player':'eventList': 'eventInfo'=>eventId
                                                    : 'statistics' : 'groups' : ['attack' : 'items' :['goalAssist', 'goals', 'notes', 'shotsBlocked', 'shotsOffTarget', 'shotsOnTarget', 'totalContest']
                                                                                    'defence' : 'items' :['challengeLost', 'interceptionWon', 'notes', 'outfielderBlock', 'totalClearance', 'totalTackle']
                                                                                    'duels' : 'items' :['dispossessed', 'fouls', 'totalDuels', 'wasFouled']
                                                                                    'goalkeeper' : 'items' :['goodHighClaim', 'notes', 'punches', 'runsOut', 'saves']
                                                                                    'passing' : 'items' :['accuratePass', 'keyPass', 'notes', 'totalCross', 'totalLongBalls']
                                                                                    'summary' : 'items' :['minutesPlayed']
                                                                                    ] 
                                                                                                                            : 'name', 'value'
        """
        try:
            gr = stat_dict['groups']
        except KeyError:
            return {
                "msg": "No statistics"
            }
        if len(gr) == 6:
            # goalkeeper

            stats = {
                    'goodHighClaim': PlayerHandler.parse_value(gr['goalkeeper']['items'], 'goodHighClaim'), 
                    'punches': PlayerHandler.parse_value(gr['goalkeeper']['items'], 'punches'), 
                    'runsOut': PlayerHandler.parse_value(gr['goalkeeper']['items'], 'runsOut'), 
                    'saves': PlayerHandler.parse_value(gr['goalkeeper']['items'], 'saves'),
            }
        else:
            # normal player
            stats = {
                    'goalAssist':PlayerHandler.parse_value(gr['summary']['items'], 'goalAssist'), 
                    'goals':PlayerHandler.parse_value(gr['summary']['items'],'goals'), 
                    'shotsBlocked':PlayerHandler.parse_value(gr['attack']['items'], 'shotsBlocked'), 
                    'shotsOffTarget':PlayerHandler.parse_value(gr['attack']['items'], 'shotsOffTarget'), 
                    'shotsOnTarget':PlayerHandler.parse_value(gr['attack']['items'], 'shotsOnTarget'), 
                    'totalContest':PlayerHandler.parse_value(gr['attack']['items'], 'totalContest'),
                    'challengeLost':PlayerHandler.parse_value(gr['defence']['items'], 'challengeLost'), 
                    'interceptionWon':PlayerHandler.parse_value(gr['defence']['items'], 'interceptionWin'), 
                    'outfielderBlock':PlayerHandler.parse_value(gr['defence']['items'], 'outfielderBlock'), 
                    'totalClearance':PlayerHandler.parse_value(gr['defence']['items'], 'totalClearance'), 
                    'totalTackle':PlayerHandler.parse_value(gr['defence']['items'], 'totalTackle'),
                    'dispossessed':PlayerHandler.parse_value(gr['duels']['items'], 'dispossessed'),
                    'fouls':PlayerHandler.parse_value(gr['duels']['items'], 'fouls'), 
                    'totalDuels':PlayerHandler.parse_value(gr['duels']['items'], 'totalDuels'), 
                    'wasFouled':PlayerHandler.parse_value(gr['duels']['items'], 'wasFouled'),
                    'accuratePass':PlayerHandler.parse_value(gr['passing']['items'], 'accuratePass'), 
                    'keyPass':PlayerHandler.parse_value(gr['passing']['items'], 'keyPass'),  
                    'totalCross':PlayerHandler.parse_value(gr['passing']['items'], 'totalCross'), 
                    'totalLongBalls':PlayerHandler.parse_value(gr['passing']['items'], 'totalLongBalls'),
                    'minutesPlayed':PlayerHandler.parse_value(gr['summary']['items'], 'minutesPlayed')
            }
        return stats