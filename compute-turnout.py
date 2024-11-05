#!/usr/bin/env python3

import pandas as pd
import numpy as np

voters_2024 = pd.read_csv('data/voter-roll-20240904.csv', encoding='iso-8859-1')
voters_2022 = pd.read_csv('data/voter-roll-20221019.csv')
votes_2022 = pd.read_csv('data/certified-votes-20221108.csv')
votes_2022.ContestName = votes_2022.ContestName.str.replace('8F0', '6/8F0')
voters_2022.SMD = voters_2022.SMD.str.replace('8F0', '6/8F0')

# initialize a Dataframe with one row per SMD
voter_counts = pd.DataFrame()
voter_counts['SMD'] = voters_2024.SMD.unique()
voter_counts = voter_counts.sort_values('SMD')

# populate voter registration count, 2022 votes cast, computed turnout
voter_counts['2022-10-19 reg'] = voters_2022.SMD.value_counts()[voter_counts.SMD].values
voter_counts['2024-09-04 reg'] = voters_2024.SMD.value_counts()[voter_counts.SMD].values
voter_counts['2022-11-08 cast'] = [votes_2022[votes_2022.ContestName.str.contains(smd)].Votes.sum() for smd in voter_counts.SMD]
all_2022 = votes_2022.Votes.sum()
voter_counts['2022-11-08 pct of whole'] = voter_counts['2022-11-08 cast'] / all_2022 * 100
voter_counts['2022 turnout'] = voter_counts['2022-11-08 cast'] / voter_counts['2022-10-19 reg'] * 100

# write it out to a CSV
voter_counts.to_csv('voter_counts_by_smd.csv', index=False, header=True)
