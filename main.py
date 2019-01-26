from Betting import *


def main():
	first_day = '2017-01-01'
	#DataCollector().get2(date, date)
	Db_handler.initialize_dbs()
	print('db initializing finished')
	Db_handler.hire_workers()
	print('hiring process finished')
	DataCollector().football(first_day)
	Db_handler.fire_workers()

if __name__ == '__main__':
	main()


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
