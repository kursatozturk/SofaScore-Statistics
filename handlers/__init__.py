from . import DateHandler, EventHandler, PlayerHandler, TeamHandler, TournamentHandler
instances = {
    'EventHandler': EventHandler.EventHandler.instances,
    'PlayerHandler': PlayerHandler.PlayerHandler.instances,
    'TeamHandler': TeamHandler.TeamHandler.instances,
    'TournamentHandler': TournamentHandler.TournamentHandler.instances,
}
def begin_day(date):
    for key in instances:
        instances[key][date] = dict()
def remove_instances(instances, date):

    for key in instances:
        k = instances[key][date]
        for ins in k:
            t = k[ins]
            k[ins] = None
            del t
        instances[key][date] = dict(msg='This Date Has been written to persistent memory!')
