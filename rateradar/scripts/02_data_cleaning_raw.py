 #!/usr/bin/env python -W ignore::DeprecationWarning

"""
02_data_cleaning.py

Purpose: Clean the data to ensure it's accurate and consistent.

Tasks: This might include removing or imputing missing values, correcting data types 
(ensuring numerical columns are recognized as such, dates are in datetime format, etc.), 
removing duplicates, and potentially filtering out irrelevant data.

Output: A cleaned DataFrame that's ready for analysis.
"""
# Remove annoying pandas warnings
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

import os
import pandas as pd

from ..common import paths

def clean_file(input_file: str, output_file: str) -> None:
    """
    Clean the data in the input file and save it to the output file.

    Args:
    input_file (str): The input file to clean.
    output_file (str): The output file to save the cleaned data to.
    """

    # read excel file and get second worksheet (by index not name). Skip first 2 rows
    df = pd.read_excel(input_file)

    # Get name of last column in df
    last_col = df.columns[-1]

    # We only want Date and First columns
    clean_df = df[['DATE', last_col]]
    
    # Rename last col to value
    clean_df = clean_df.rename(columns={'DATE': 'Date'})
    clean_df = clean_df.rename(columns={last_col: 'Raw'})
    
    # Split Date into year/month by splitting on colon and set it to the first of the month
    clean_df['Date'] = clean_df['Date'].str.split(':', expand=True)[1] + '/01/' + clean_df['Date'].str.split(':', expand=True)[0]

    # Make Date the column index to ensure unique data
    clean_df = clean_df.set_index('Date')

    # For each row after the first one, get the percentage increase/decrease from the row before it
    clean_df['Pct'] = clean_df['Raw'].pct_change()

    # Save to data/processed/inflation/cpi.csv
    clean_df.to_csv(os.path.join(paths.PROCESSED_DIR, output_file))

pcpi_filename = os.path.join(paths.RAW_DIR, 'inflation', 'pcpiMvMd.xlsx')
clean_file(pcpi_filename, 'pcpi.csv')

pcpix_filename = os.path.join(paths.RAW_DIR, 'inflation', 'pcpixMvMd.xlsx')
clean_file(pcpix_filename, 'pcpix.csv')

print("File saved.")