import os
import json
import pandas as pd

csv_dir = os.path.dirname(__file__)
json_dir = os.path.join(csv_dir, '..', 'nyt_time_series_json_cleaned')

json_files = [f for f in os.listdir(json_dir) if f.endswith('json')]
source_data_by_filename = dict()

# Load all json files
for json_file in json_files:
	# Get time series of vote dumps
	json_path = os.path.join(json_dir, json_file)
	if os.path.exists(json_path):
		with open(json_path, 'r') as f:
			source_data_by_filename[json_file] = json.load(f)

# Collect all information about candidates
party_by_candidate_key = dict()
for json_file, source_data in source_data_by_filename.items():
	for d in source_data['data']['races'][0]['candidates']:
		party_by_candidate_key[d['candidate_key']] = d['party_id']

def convert_candidate_to_party(x):
	candidate, stat = x.split('__')
	return f'{party_by_candidate_key[candidate]}__{stat}'


for json_file, source_data in source_data_by_filename.items():

	# Get time series of vote dumps
	data = source_data['data']['races'][0]['timeseries']

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
			**{f'{k}__percent': v for k, v in percent_by_candidate.items()},
			**{f'{k}__count': round(v) for k, v in count_by_candidate.items()},
		}
		df_data.append(row)


	df = pd.DataFrame(df_data, index=pd.DatetimeIndex(df_index))
	df.sort_index(inplace=True)

	percent_cols = [f'{c}__percent' for c in candidates]
	delta_cols = [f'{c}__delta' for c in candidates]
	count_cols = [f'{c}__count' for c in candidates]

	# Drop erroneous data where all counts are zero, except first row
	zero_count_index = ~(df[count_cols] == 0).all(axis=1)
	zero_count_index.iloc[0] = True
	df = df[zero_count_index]

	# Get vote dump deltas
	for candidate in candidates:
		df[f'{candidate}__delta'] = df[f'{candidate}__count'].diff()

	# Map candidates to parties
	df.rename(columns=convert_candidate_to_party, inplace=True)

	# Combine by party is multi-challenger races
	# Should only happen for louisiana-senate.json
	if not df.columns.is_unique:
		df = df.groupby(level=0, axis=1).sum()

	csv_filename = json_file.replace('.json', '.csv')
	csv_filepath = os.path.join(csv_dir, csv_filename)
	df.to_csv(csv_filepath, index_label='timestamp')

