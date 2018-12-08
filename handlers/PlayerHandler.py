from handlers.BaseHandler import BaseHandler


class PlayerHandler(BaseHandler):
    instances = {}

    def __init__(self, date, player_info):

        unique_id = player_info['id']
        if unique_id in PlayerHandler.instances[date]:
            super().__init__(*PlayerHandler.instances[date][unique_id])
            return
        player_info['eventList'] = [
            # eventInfo: same as Team
            # statistics: specific to player
        ]
        # self.info = player_info
        super().__init__(date, player_info)

        PlayerHandler.instances[self.date][unique_id] = (self.date, self)

    def add_event(self, event, statistics):
        self['eventList'].append(dict(eventInfo=event, statistics=statistics))

    def get(date, unique_id):
        return PlayerHandler.instances[date][unique_id][1]