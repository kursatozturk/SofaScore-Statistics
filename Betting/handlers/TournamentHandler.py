from utils.python_utils import CannotHandled
from handlers.BaseHandler import BaseHandler


class TournamentHandler(BaseHandler):
    # deprecated
    instances = {}

    def __init__(self, date, tourn_info):
        try:
            unique_id = tourn_info['uniqueId']
        except KeyError:
            raise (CannotHandled('No UniqueId', tourn_info))

        if unique_id in TournamentHandler.instances[date]:
            super().__init__(*TournamentHandler.instances[date][unique_id])
            return

            # self.clean_data(tourn_info)
        tourn_info['participants'] = []
        # self.info = tourn_info
        super().__init__(date, tourn_info)
        TournamentHandler.instances[date][unique_id] = (date, self)

    def add_participant(self, participant):
        if not participant in self['participants']:
            self['participants'].append(participant)

    def get(date, tournament_id):
        return TournamentHandler.instances[date][tournament_id][1]