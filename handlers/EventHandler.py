from handlers.BaseHandler import BaseHandler


class EventHandler(BaseHandler):
    instances = {}

    def __init__(self, date, event_info):
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
        if unique_id in EventHandler.instances[date]:
            super().__init__(*EventHandler.instances[date][unique_id])
            return
            # teamsForm can be used from here, or be extracted from another source
        unnecessary = [
            'incidents', 'matchInfo', 'groupedIncidents',
            'innings', 'vote', 'odds', 'highlights', 'liveForm',
            'scoreGraph', 'standingsAvailable', 'pointByPoint',
        ]
        for un in unnecessary:
            del event_info[un]

        super().__init__(date, event_info)
        EventHandler.instances[date][unique_id] = (date, self)

    """
    def clean_data(self, event_info):
        del_me = []
        if type(event_info) is list:
            for key in event_info:
                self.clean_data(key)
        else:
            for key in event_info:
                if type(event_info[key]) is dict:
                    self.clean_data(event_info[key])
                elif type(event_info[key]) is bool:
                    del_me.append(key)

        for key in del_me:
            del event_info[key]

    def __getitem__(self, key):
        return self.info[key]
    """

    def add_field(self, field, value):
        self[field] = value

    def get(date, unique_id):
        return EventHandler.instances[date][unique_id][1]
