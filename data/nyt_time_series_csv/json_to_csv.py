
import os
import json
import pandas as pd

state = 'pennsylvania'
csv_dir = os.path.dirname(__file__)
json_dir = os.path.join(csv_dir, '..', 'nyt_time_series_json_cleaned')

json_files = [f for f in os.listdir(json_dir) if f.endswith('json')]

for json_file in json_files:

	# Get time series of vote dumps
	json_path = os.path.join(json_dir, json_file)
	if os.path.exists(json_path):
		with open(json_path, 'r') as f:
			data = json.load(f)
			data = data['data']['races'][0]['timeseries']

	# Get all unique candidates in data
	candidates = set()
	for ballot_dump in data:
		for candidate in ballot_dump['vote_shares'].keys():
			candidates.add(candidate)

	# Build data frame
	df_data = list()
	df_index = list()
	for ballot_dump in data:

		datetime = ballot_dump['timestamp']

		percent_by_candidate = {
			c: ballot_dump['vote_shares'].get(c, 0) for c in candidates
		}

		count_by_candidate = {
			c: p * ballot_dump['votes'] for c, p in percent_by_candidate.items()
		}

		df_index.append(datetime)
		row = {
			**{f'{k}_percent': v for k, v in percent_by_candidate.items()},
			**{f'{k}_count': round(v) for k, v in count_by_candidate.items()},
		}
		df_data.append(row)


	df = pd.DataFrame(df_data, index=pd.DatetimeIndex(df_index))
	df.sort_index(inplace=True)

	percent_cols = [f'{c}_percent' for c in candidates]
	delta_cols = [f'{c}_delta' for c in candidates]
	count_cols = [f'{c}_count' for c in candidates]

	# Drop erroneous data where all counts are zero
	zero_count_index = ~(df[count_cols] == 0).all(axis=1)

	# Always keep first row
	zero_count_index.iloc[0] = True

	# Subset
	df = df[zero_count_index]

	for candidate in candidates:
		df[f'{candidate}_delta'] = df[f'{candidate}_count'].diff()

	csv_filename = json_file.replace('.json', '.csv')
	csv_filepath = os.path.join(csv_dir, csv_filename)
	df.to_csv(csv_filepath, index_label='timestamp')

