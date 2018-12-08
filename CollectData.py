from concurrent.futures import ProcessPoolExecutor as PPE
from concurrent.futures import ThreadPoolExecutor as TPE
from multiprocessing import cpu_count

from SofaScore import *
from utils.python_utils import *
from handlers import *
from handlers.EventHandler import EventHandler
from handlers.PlayerHandler import PlayerHandler
from handlers.TeamHandler import TeamHandler
from handlers.TournamentHandler import TournamentHandler
from handlers.DateHandler import DateHandler
import os
import json
from sys import stdout


class DataCollector(metaclass=Singleton):
    def __init__(self):
        self.cpu_count = cpu_count()

    def football(self, begin_date="2010-01-01", end_date=None):
        interval = DateHandler(begin_date).create_interval_till(end_date)

        with PPE(max_workers=self.cpu_count) as worker_pool:
            instances_list = worker_pool.map(DataCollector.fetch_day_events, interval)
            for date, instances in instances_list:
                DataCollector.write_content(instances, date)

    def fetch_day_events(date: str):
        day, events = SofaScore().parse_by_date(date)
        tournaments = events['sportItem']['tournaments']
        begin_day(date)
        for tr in tournaments:
            try:
                th = TournamentHandler(date, tr['tournament'])
            except CannotHandled as c:
                continue
            events = tr['events']
            event_ids = list()
            for ev in events:
                event_ids.append(ev['id'])
                home = TeamHandler(date, ev['homeTeam'])
                away = TeamHandler(date, ev['awayTeam'])
                home.add_event(ev['id'])
                away.add_event(ev['id'])
                th.add_participant(home)
                th.add_participant(away)

            event_id_gen = split_into(event_ids, cpu_count() * 5)
            with TPE() as worker_pool:
                event_getter = create_worker(SofaScore().parse_event)
                lineup_getter = create_worker(SofaScore().parse_lineups_event)

                event_info = [x for x in worker_pool.map(event_getter, event_id_gen)]
                lineups_info = [x for x in worker_pool.map(lineup_getter, event_id_gen)]

            stdout.write('all matches of {:40s} played on {} fetched\n'.format(th['uniqueName'], date))
            stdout.flush()
            for x in event_info:
                e_id, event = x[0]
                EventHandler(date, event)

            player_ids = list()
            for lineup in lineups_info:
                event_id, l = lineup[0]
                home, away = l.values()
                EventHandler.get(date, event_id).add_field('lineups', (home, away))
                players = home['lineupsSorted'] + away['lineupsSorted']
                for pl in players:
                    PlayerHandler(date, pl['player'])
                    player_ids.append((event_id, pl['player']['id']))
            player_id_gen = split_into(player_ids, cpu_count() * 5)
            with TPE() as worker_pool:
                player_stats_getter = create_worker(SofaScore().parse_player_stat)
                player_stats = worker_pool.map(player_stats_getter, player_id_gen)

            for s in player_stats:
                e_id, p_id, stat = s[0]
                PlayerHandler.get(date, p_id).add_event(e_id, stat)
        stdout.write('{:50s} {}\n'.format('date has finished:', date))
        stdout.flush()
        return date, instances

    def write_content(instances, date: str, file_name='data/'):
        try:
            os.mkdir(file_name)
        except FileExistsError:
            pass

        if date is None:
            raise (Exception('Date must be not None'))
        data_path = os.path.join(os.getcwd(), file_name)
        for key in instances:
            name = '{}[{}]'.format(key, str(date))
            path = os.path.join(data_path, name)
            with open(path, 'w') as w:
                json.dump(instances[key][date], w, indent=4, sort_keys=True)
        remove_instances(instances, date)
