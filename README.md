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