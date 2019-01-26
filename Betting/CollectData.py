from concurrent.futures import ProcessPoolExecutor as PPE
from concurrent.futures import ThreadPoolExecutor as TPE
from multiprocessing import cpu_count
from .SofaScore import SofaScore 
from Betting.utils import *
from Betting.handlers import *
import os
import json
from sys import stdout


class DataCollector(metaclass=Singleton):
    def __init__(self):
        self.cpu_count = cpu_count()

    def football(self, begin_date="2010-01-01", end_date=None):
        interval = DateHandler(begin_date).create_interval_till(end_date)

        with PPE(self.cpu_count) as worker_pool:
            worker_pool.map(DataCollector.fetch_day_events, interval)
            
    @staticmethod
    def fetch_day_events(date: str):
        try:
            day, events = SofaScore().parse_by_date(date)
            tournaments = events['sportItem']['tournaments']
        except Exception as e:
            print(e)
        for tr in tournaments:
            try:
                events = tr['events']
            except KeyError:
                print('events of tournament cannot be fetched')
                continue
            event_ids = list()
            for ev in events:
                try:
                    event_ids.append(ev['id'])
                    home = TeamHandler(date, ev['homeTeam'])
                    away = TeamHandler(date, ev['awayTeam'])
                except KeyError:
                    print('Key Error occured in adding teams to event')
                    continue
                except Exception as e:
                    print(e)
            event_id_gen = split_into(event_ids, cpu_count() * 5)
            with TPE() as worker_pool:
                event_getter = create_worker(SofaScore().parse_event)
                lineup_getter = create_worker(SofaScore().parse_lineups_event)

                event_info = [x for x in worker_pool.map(event_getter, event_id_gen)]
                lineups_info = [x for x in worker_pool.map(lineup_getter, event_id_gen)]

            stdout.write('all matches of {:40s} played on {} fetched\n'.format(tr['tournament']['uniqueName'], date))
            stdout.flush()
            player_ids = list()
            try:
                for ev, lineup in zip(event_info, lineups_info):
                    e_id, event = ev[0]
                    event_id, l = lineup[0]
                    home, away = l.values()
                    try:
                        home = [h['player'] for h in home['lineupsSorted']]
                        away = [a['player'] for a in away['lineupsSorted']]
                    except KeyError:
                        continue
                    EventHandler(date, event, (home, away))
                    players = home + away
                    for pl in players:
                        PlayerHandler(date, pl)
                        player_ids.append((event_id, pl['id']))
            except Exception as e:
                print(e)
                continue
            player_id_gen = split_into(player_ids, cpu_count() * 5)
            with TPE() as worker_pool:
                player_stats_getter = create_worker(SofaScore().parse_player_stat)
                player_stats = worker_pool.map(player_stats_getter, player_id_gen)
            for s in player_stats:
                try:
                    e_id, p_id, stat = s[0]
                except Exception as e:
                    print(e)
                    continue
                PlayerHandler.add_event(p_id, e_id, stat)
        stdout.write('{:50s} {}\n'.format('date has finished:', date))
        stdout.flush()
        
    