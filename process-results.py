#!/usr/bin/env python3

import pandas as pd

# for a given results set and SMD identifier, return the total ballot count
def get_smd_ballot_count(result, smd):
    # summing across precincts, candidates, overvotes, undervotes
    return result[result.ContestName.str.contains(smd)].Votes.sum()

revisions = ['tues8', 'wed9', 'thurs10', 'fri11']
results = dict.fromkeys(revisions)

for revision in revisions:
    results[revision] = pd.read_csv('data/%s.csv' % revision)

# get a list of ANC SMDs
anc_contests = results['tues8'][results['tues8'].ContestName.str.contains(
    'ANC - ')].ContestName.unique()
smds = [contest.split(' ')[2] for contest in anc_contests]

# sort the list
smds.sort()

# set up a dataframe for counts by SMD per data revision
ballot_counts = pd.DataFrame(columns=['SMD'] + revisions)
ballot_counts.SMD = smds

# for each SMD and revision, calculate the ballot count
for smd in smds:
    for revision in revisions:
        print('calculating ballot count for SMD %s and revision %s' %
              (smd, revision))
        ballot_counts.loc[ballot_counts.SMD == smd,
                          revision] = get_smd_ballot_count(results[revision], smd)

# write it out to a CSV
ballot_counts.to_csv('ballots_by_smd_over_time.csv', index=False, header=True)