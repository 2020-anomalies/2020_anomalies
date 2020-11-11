#### New York Times Time Series Data

A company called Edison research runs web scapers against state election results websites to create a time series of vote count changes in order to chart the election progress. This data set is pretty difficult to assemble. It requires a lot of software developer effort to set up this data pipeline. The NYT exposes a lot of Edison's data to make their election-night charts. This data was downloaded from a NYT webiste.

This data will allow us to recreate the famous "jump chart" or "F chart" where the blue vote count crosses the red in one sharp jump.

Further, this data set contains numerous singular vote deltas (otherwise called "ballot dumps") along with their timestamps. This is potentially very valuable for anomaly analysis.

