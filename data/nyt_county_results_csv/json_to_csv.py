import os
import json
import pandas as pd

csv_dir = os.path.dirname(__file__)
json_dir = os.path.join(csv_dir, '..', 'nyt_time_series_json_cleaned')

json_files = [f for f in os.listdir(json_dir) if f.endswith('json')]
source_data_by_filename = dict()

# Load all json files
for json_file in json_files:
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

as_is_columns = [
	'absentee_count_progress',
	'absentee_max_ballots',
	'absentee_method',
	'absentee_outstanding',
	'absentee_votes',
	'eevp',
	'eevp_display',
	'eevp_source',
	'eevp_value',
	'fips',
	'last_updated',
	'leader_margin_display',
	'leader_margin_name_display',
	'leader_margin_value',
	'leader_party_id',
	'name',
	'precincts',
	'provisional_count_progress',
	'provisional_outstanding',
	'reporting',
	'tot_exp_vote',
	'turnout_stage',
	'votes',
]

for json_file, source_data in source_data_by_filename.items():

	# Get time series of vote dumps
	data = list()
	counties = source_data['data']['races'][0]['counties']
	for county in counties:
		row = {c: county[c] for c in as_is_columns}

		for candidate_key, count in county['results'].items():
			row[f'{candidate_key}__total_count'] = count

			party = party_by_candidate_key[candidate_key]
			col_name = f'{party}__total_count'
			if not col_name in row:
				row[col_name] = 0
			row[col_name] += count


		for candidate_key, count in county['results_absentee'].items():
			row[f'{candidate_key}__absentee_count'] = count

			party = party_by_candidate_key[candidate_key]
			col_name = f'{party}__total_count'
			if not col_name in row:
				row[col_name] = 0
			row[col_name] += count

		data.append(row)

	df = pd.DataFrame(data)

	csv_filename = json_file.replace('.json', '.csv')
	csv_filepath = os.path.join(csv_dir, csv_filename)
	df.to_csv(csv_filepath, index=False)




