
import json
import os

this_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(
	this_dir,
	'..',
	'nyt_time_series_json',
)
out_dir = this_dir

json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]

for json_file in json_files:
	json_path = os.path.join(data_dir, json_file)
	with open(json_path, 'r') as f:
		data = json.load(f)

	out_path = os.path.join(this_dir, json_file)
	with open(out_path, 'w') as f:
		json.dump(data, f, indent=4, sort_keys=True)

