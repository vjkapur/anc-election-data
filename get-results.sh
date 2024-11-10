# this isn't working as intended and will overwrite a previous file on the same day

curl https://electionresults.dcboe.org/Downloads/Reports/November_5_2024_General_Election_Election_Night_Unofficial_Results.csv > data/2024/results-$(date '+%Y-%m-%d').csv

prefix="data/2024"

last=$(ls -t $(echo $prefix) | head -1)
before_last=$(ls -t $(echo $prefix) | head -2 | tail -1)

# echo "comparing $last to $before_last"

if [ $(diff $(echo $prefix)/$(echo $last) $(echo $prefix)/$(echo $before_last)) ]; then
  echo "new results available"
else
  echo "no new results"
  rm $(echo $prefix)/$(echo $last)
fi