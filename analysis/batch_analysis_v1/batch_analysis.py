import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


this_dir = os.path.dirname(__file__)
csv_dir = os.path.join(this_dir, '..', '..', 'data', 'nyt_time_series_csv_v2')



def plot_dump_chart(csv_filename):
	print(f'Plotting {csv_filename} ...')
	csv_path = os.path.join(csv_dir, csv_filename)
	df = pd.read_csv(csv_path, index_col='timestamp', parse_dates=['timestamp'])

	df['timestamp_copy'] = df.index.copy()
	df['numeric_index'] = list(range(df.shape[0]))

	if (
		not 'democrat__delta' in df.columns or 
		not 'republican__delta' in df.columns
		):
		return

	df['d_to_r_ratio'] = df['democrat__delta'] / df['republican__delta']
	filter_extreme_values = (0 <= df.d_to_r_ratio) & (df.d_to_r_ratio <= 2)
	_df = df[filter_extreme_values]

	filebase = csv_filename.rstrip('.csv')
	_split = filebase.split('-')
	state = ' '.join(_split[:-1])
	race_type = _split[-1]


	### First chart
	fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 12))
	ax1.title.set_text(
		f'Ballot dumps from {state.title()} {race_type.title()} Race'
	)

	ax1.plot_date(
		_df.index, 
		_df.d_to_r_ratio, 
		color='black',
		marker='o', 
		markersize=1.5,
	)
	ax1.set_ylabel('Ratio of D to R votes')
	ax1.grid()

	ax2.set_yscale('log')
	ax2.set_ylabel('Size of vote dump')
	ax2.set_xlabel('Timestamp of vote dump')
	ax2.plot_date(
		_df.index, 
		_df.democrat__delta.abs() + _df.republican__delta.abs(), 
		color='black',
		marker='o', 
		markersize=1.5,
	)
	ax2.grid()
	# plt.show()
	plt.savefig(f'{filebase}.png')
	plt.close()

	### Second chart
	fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 12))
	ax1.title.set_text(
		f'Ballot dumps from {state.title()} {race_type.title()} Race'
	)

	ax1.plot(
		_df.numeric_index, 
		_df.d_to_r_ratio, 
		color='black',
		linestyle='None',
		marker='o', 
		markersize=1.5,
	)
	ax1.set_ylabel('Ratio of D to R votes')
	ax1.grid()

	ax2.set_yscale('log')
	ax2.set_ylabel('Size of vote dump')
	ax2.set_xlabel('Vote dump #')
	ax2.plot(
		_df.numeric_index, 
		_df.democrat__delta.abs() + _df.republican__delta.abs(), 
		color='black',
		linestyle='None',
		marker='o', 
		markersize=1.5,
	)
	ax2.grid()
	# plt.show()
	plt.savefig(f'{filebase}-v2.png')
	plt.close()



if __name__ == '__main__':

	filenames = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]
	for filename in filenames:
		plot_dump_chart(filename)





