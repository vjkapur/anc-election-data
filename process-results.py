#!/usr/bin/env python3

import pandas as pd
from os import listdir
from os.path import isfile, join

# for a given results set and SMD identifier, return the total ballot count


def get_smd_ballot_count(result, smd):
    # summing across precincts, candidates, overvotes, undervotes
    return result[result.ContestName.str.contains(smd)].Votes.sum()

# for a given results set, SMD identifier, and candidate list (ordered by preference), return the margin (negative is disfavorable)
# only supporting two-candidate races for now because they're all I care about rn


def get_smd_margin(result, smd, candidates):
    incl = result[result.ContestName.str.contains(
        smd) & result.Candidate.str.contains(candidates[0])].Votes.sum()
    gate = result[result.ContestName.str.contains(
        smd) & result.Candidate.str.contains(candidates[1])].Votes.sum()

    return (incl - gate)

# print out a quick digest of what changed for interesting races
def print_summary_snapshot(old_result, new_result, competitive_races):
    summary = pd.DataFrame(
        columns=['SMD', 'candidates', 'previous_margin', 'new_ballots', 'new_margin'])
    summary.SMD = competitive_races.keys()
    for smd in competitive_races:
        summary.loc[summary.SMD == smd, 'candidates'] = "%s/%s" % (
            competitive_races[smd][0], competitive_races[smd][1])
        summary.loc[summary.SMD == smd, 'previous_margin'] = get_smd_margin(
            old_result, smd, competitive_races[smd])
        summary.loc[summary.SMD == smd, 'new_ballots'] = get_smd_ballot_count(
            new_result, smd) - get_smd_ballot_count(old_result, smd)
        summary.loc[summary.SMD == smd, 'new_margin'] = get_smd_margin(
            new_result, smd, competitive_races[smd])

    summary.sort_values('new_margin', ascending=False, inplace=True)
    print(summary.to_string(index=False))

#revisions = ['tues8', 'wed9', 'thurs10', 'fri11', 'mon14', 'fri18', 'mon21', 'tues22', 'wed30']
revisions = [f for f in listdir('data/2024/') if isfile(join('data/2024/', f))]
results = dict.fromkeys(revisions)

yimbyness = pd.read_csv('data/yimbyness.csv')
Y_grouping = yimbyness.groupby('SMD').sum()
competitive_SMDs_with_Y = Y_grouping[Y_grouping.score > 0].index.values

competitive_races = dict.fromkeys(competitive_SMDs_with_Y, [])

# competitive_races = {'5D06': ['McCray', 'Henderson'],
#                     '5B07': ['Rathore', 'Haynes'],
#                     '5E01': ['Gardiner', 'Rodriguez'],
#                     '5E05': ['Lopez', 'Thompson'],
#                     '5B05': ['Lopez', 'Feeley']}

for revision in revisions:
    results[revision] = pd.read_csv('data/2024/%s' % revision)

print_summary_snapshot(results[revisions[-2:][0]],
                       results[revisions[-1:][0]], competitive_races)

# get a list of ANC SMDs
anc_contests = results[next(iter(results))][results[next(iter(results))].ContestName.str.contains(
    'ANC - ')].ContestName.unique()
smds = [contest.split(' ')[2] for contest in anc_contests]

# sort the list
smds.sort()

# set up a dataframe for counts by SMD per data revision
revision_metrics = []
[revision_metrics.extend(update) for update in [['%s ballots' % revision,
                                                 '%s increase' % revision, '%s pct increase' % revision] for revision in revisions[1:]]]
ballot_counts = pd.DataFrame(
    columns=['SMD'] + ['%s ballots' % revisions[0]] + revision_metrics)
ballot_counts.SMD = smds

# gathering up permutations of margin and margin-pct for each available revision
margins = []
[margins.extend(update) for update in [['margin-' + revision,
                                        'margin-pct-' + revision] for revision in revisions]]

margin_counts = pd.DataFrame(columns=['SMD'] + margins)
margin_counts.SMD = competitive_races.keys()

# for each SMD and revision, calculate the ballot count
for smd in smds:
    competitive_races[smd][0] = yimbyness[yimbyness.SMD == smd].sort_values(by='score', ascending=False).candidate.iloc[0]
    competitive_races[smd][1] = yimbyness[yimbyness.SMD == smd].sort_values(by='score', ascending=False).candidate.iloc[1]
 
    for revision in revisions:
        ballot_counts.loc[ballot_counts.SMD == smd,
                          '%s ballots' % revision] = get_smd_ballot_count(results[revision], smd)
        if revision != revisions[0]:
            ballot_counts.loc[ballot_counts.SMD == smd, '%s increase' % revision] = ballot_counts.loc[ballot_counts.SMD == smd, '%s ballots' %
                                                                                                      revision] - ballot_counts.loc[ballot_counts.SMD == smd, '%s ballots' % revisions[revisions.index(revision) - 1]]
            ballot_counts.loc[ballot_counts.SMD == smd, '%s pct increase' % revision] = '%.2f%%' % (ballot_counts.loc[ballot_counts.SMD == smd, '%s increase' %
                                                                                                                      revision] / ballot_counts.loc[ballot_counts.SMD == smd, '%s ballots' % revisions[revisions.index(revision) - 1]] * 100)
        if smd in competitive_races:
            margin_counts.loc[margin_counts.SMD == smd, 'margin-%s' %
                              revision] = get_smd_margin(results[revision], smd, competitive_races[smd])
            margin_counts.loc[margin_counts.SMD == smd, 'margin-pct-%s' %
                              revision] = get_smd_margin(results[revision], smd, competitive_races[smd])/get_smd_ballot_count(results[revision], smd)

# write it out to a CSV
ballot_counts.to_csv('ballots_by_smd_over_time.csv', index=False, header=True)
margin_counts.to_csv(
    'competitive_race_margins_over_time.csv', index=False, header=True)
