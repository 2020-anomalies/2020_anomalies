#### NYT Time Series V2

All time series data of presidential and senate races from Edison Research, reconstructed from NYT sources, by candidate.

+ `timestamp` When the update was made (i.e. a vote dump).
+ `<candidate>_percent`, `<candidate>_percent` Cumulative vote shares for each party. Aggregated in the case of more than two contenders in senate races (i.e. Lousianna)
+ `<candidate>_count`, `<candidate>_count` Cumulative votes counted for each party. Aggregated the same way as the above.
+ `<candidate>_delta`, `<candidate>_delta` The change in total vote count from the last period (i.e. the size of the vote dump for each party.)

