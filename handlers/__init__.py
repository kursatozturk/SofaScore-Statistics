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
            del k[ins]
        instances[key][date] = {'MESSAGE': 'THIS DATE HAS ALREADY BEEN WRITTEN!'}
