from handlers.BaseHandler import BaseHandler


class TeamHandler(BaseHandler):
    instances = {}

    def __init__(self, date, team_info):
        unique_id = team_info['id']
        if unique_id in TeamHandler.instances[date]:
            super().__init__(*TeamHandler.instances[date][unique_id])
            return
        team_info['eventList'] = []
        # self.info = team_info
        super().__init__(date, team_info)
        TeamHandler.instances[date][unique_id] = (date, self)

    def add_event(self, event_id):
        self['eventList'].append(event_id)

    def get(date, event_id):
        return TeamHandler.instances[date][event_id][1]