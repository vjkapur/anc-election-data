# historical notes:
- SMDs are redrawn every ten years; the current boundaries were first used in the (midterm) 2022 election
- in 2020, DC BOE's election statistics reflect 517,890 registered voters and 346,491 ballots cast
- (not sure how many registrations were removed in 2021)
- in 2022, DC BOE's election statistics reflect 504,815 registered voters and 205,774 ballots cast
- ignoring registrations and looking only at ballots cast, 2020 had ~1.684 as many ballot cast
- in 2023, during the routine voter roll maintenance, [65,544 registrations were removed](https://dcboe.org/data,-maps,-forms/voter-registration-list-maintenance)
- the November 2022 registrations, minus the purged records from 2023, brings the total to 439,271 without accounting for other organic removals/additions
- as of the city-wide September 4, 2024 voter roll, there are 436,357 voter registrations

## usage
To run:
1. download data from Google Drive (BOE keeps overwriting the CSVs, at least as far as the public links go)
2. either use the included conda environment (requires Anaconda or [miniconda](https://docs.conda.io/en/latest/miniconda.html)) to pull package dependencies through an environment:

   ```shell
   conda env create
   conda activate election-data
   ```

   or use `pip` (assumes python is already installed)

   ```shell
   pip install pandas
   ```

3. run `process-results.py`

   ```shell
   python process_results.py
   ```
   
   or, within a Python terminal:

   ```python
    exec(open('process-results.py').read())
    ```

