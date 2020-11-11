#### NYT Time Series V2

All time series data of presidential and senate races from Edison Research, reconstructed from NYT sources, aggregated by party.

+ `timestamp` When the update was made (i.e. a vote dump).
+ `democrate__percent`, `republican__percent` Cumulative vote shares for each party. Aggregated in the case of more than two contenders in senate races (i.e. Lousianna)
+ `democrat__count`, `republican__count` Cumulative votes counted for each party. Aggregated the same way as the above.
+ `democrat__delta`, `republican__delta` The change in total vote count from the last period (i.e. the size of the vote dump for each party.)

