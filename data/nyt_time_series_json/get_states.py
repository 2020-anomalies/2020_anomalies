import wget
import time

state_names = ["Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", "California", "Colorado", "Connecticut", "District of Columbia", "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Virgin Islands", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]

for state in state_names:
	for race in ['president', 'senate']:
		query_name = state.lower().replace(' ', '-')

		url = f'https://static01.nyt.com/elections-assets/2020/data/api/2020-11-03/race-page/{query_name}/{race}.json'
		try:
			print()
			print(f'Trying {query_name}, {race}')
			wget.download(url, f'{query_name}-{race}.json')
		except BaseException as e:
			print(e)
			print(f'Failed to get {query_name}, {race}')

		time.sleep(1)

