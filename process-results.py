#!/usr/bin/env python3

import pandas as pd

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


revisions = ['tues8', 'wed9', 'thurs10', 'fri11']
results = dict.fromkeys(revisions)

competitive_races = {'5D06': ['Carrie', 'Kathy'],
                     '5C04': ['Shawn', 'Jacque'],
                     '5F07': ['Michele', 'Sylvia'],
                     '5B07': ['Justine', 'Gail'],
                     '5E02': ['Nicole', 'Karla']}

for revision in revisions:
    results[revision] = pd.read_csv('data/%s.csv' % revision)

# get a list of ANC SMDs
anc_contests = results['tues8'][results['tues8'].ContestName.str.contains(
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
