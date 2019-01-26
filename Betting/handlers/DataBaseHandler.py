from multiprocessing import Queue
from threading import Thread
import sqlite3

class Db_handler:

    db_worker_count = 60
    db_base_dir = 'db_cache/'
    db_queue = Queue(db_worker_count * 2)
    workers = []
    @staticmethod
    def configure(worker_count, base_dir):
        Db_handler.db_worker_count = worker_count
        Db_handler.db_base_dir = base_dir
    @staticmethod
    def hire_workers():
        for i in range(Db_handler.db_worker_count):
            t = Thread(target=Db_handler.db_worker, args=(i, ))
            Db_handler.workers.append(t)
            t.start()

    @staticmethod
    def fire_workers():
        for i in range(Db_handler.db_worker_count):
            Db_handler.db_queue.put(None)
        for t in Db_handler.workers:
            t.join()

    @staticmethod
    def db_worker(thread_num):
        conn = sqlite3.connect(f'{Db_handler.db_base_dir}statistics{thread_num}.db')
        cur = conn.cursor()
        while True:
            d = Db_handler.db_queue.get()
            if d is None:
                print('Db_handler exited safely')
                break
            query_string, params = d
            try:
                cur.execute(query_string, params)
            except sqlite3.IntegrityError:
                continue
            except Exception as e:
                print(e)
                continue
            conn.commit()
        conn.close()
    @staticmethod
    def initialize_dbs():
        for i in range(Db_handler.db_worker_count):
            conn = sqlite3.connect(f'{Db_handler.db_base_dir}statistics{i}.db')
            cur = conn.cursor()
            try:
                cur.execute("""
                            CREATE TABLE Player(
                                player_id INTEGER PRIMARY KEY,
                                player_info BLOB
                            );"""
                            )
                cur.execute("""
                            CREATE TABLE Team(
                                team_id INTEGER PRIMARY KEY,
                                team_info BLOB
                            );"""
                            )
                cur.execute("""
                            CREATE TABLE Event(
                                event_id INTEGER PRIMARY KEY,
                                home_team_id INTEGER,
                                away_team_id INTEGER,
                                DATE date,
                                event_info BLOB,
                                FOREIGN KEY(home_team_id) REFERENCES Team,
                                FOREIGN KEY(away_team_id) REFERENCES Team
                            );"""
                            )
                cur.execute("""
                            CREATE TABLE Statistics(
                                player_id INTEGER,
                                event_id INTEGER,
                                stats BLOB,
                                FOREIGN KEY(player_id) REFERENCES Player,
                                FOREIGN KEY(event_id) REFERENCES Event,
                                PRIMARY KEY(player_id, event_id)
                            );"""
                        )
            except sqlite3.OperationalError as e:
                print('Operational error: ', e)
                return

            conn.commit()
            conn.close()
        
