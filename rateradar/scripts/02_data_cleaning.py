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

def read_excel_file(input_file: str):
    """
    Read the data from the input file.

    Args:
    input_file (str): The input file to read.
    """
    return pd.read_excel(input_file)

def save_to_csv(df: pd.DataFrame, output_file: str):
    """
    Save the DataFrame to the output file.

    Args:
    df (pd.DataFrame): The DataFrame to save.
    output_file (str): The output file to save the DataFrame to.
    """
    df.to_csv(os.path.join(paths.PROCESSED_DIR, output_file))

def clean_cpi(input_file: str, output_file: str) -> None:
    """
    Clean the data in the input file and save it to the output file.

    Args:
    input_file (str): The input file to clean.
    output_file (str): The output file to save the cleaned data to.
    """
    df = read_excel_file(input_file)
    last_col = df.columns[-1]
    clean_df = df[['DATE', last_col]]
    clean_df = clean_df.rename(columns={'DATE': 'Date', last_col: 'Raw'})
    clean_df['Date'] = clean_df['Date'].str.split(':', expand=True)[1] + '/01/' + clean_df['Date'].str.split(':', expand=True)[0]
    clean_df = clean_df.set_index('Date')
    clean_df['Pct'] = clean_df['Raw'].pct_change()

    # Get the CPI difference between this row and 6 rows ago
    clean_df['6m_change'] = clean_df['Raw'].diff(6)

    # Calculate what percentage change that is
    clean_df['6m_pct_change'] = clean_df['6m_change'] / clean_df['Raw'].shift(6)

    # Double the change to get the annualized rate
    clean_df['annualized_change'] = clean_df['6m_pct_change'] * 2

    # Drop the raw change
    clean_df = clean_df.drop(columns=['6m_change'])

    save_to_csv(clean_df, output_file)

def clean_gdp(input_file: str, output_file: str) -> None:
    """
    Clean the data in the GDP file and save it to the output file.

    Args:
    input_file (str): The input file to clean.
    output_file (str): The output file to save the cleaned data to.
    """
    df = pd.read_excel(input_file, sheet_name=1, skiprows=4)
    clean_df = df[['Date', 'First']]
    clean_df = clean_df.set_index('Date')
    clean_df = clean_df.rename(columns={'First': 'GDP'})
    save_to_csv(clean_df, output_file)

def clean_employment(input_file: str, output_file: str) -> None:
    """
    Clean the data in the employment file and save it to the output file.

    Args:
    input_file (str): The input file to clean.
    output_file (str): The output file to save the cleaned data to.
    """
    df = read_excel_file(input_file)
    last_col = df.columns[-1]
    clean_df = df[['DATE', last_col]]
    clean_df = clean_df.rename(columns={'DATE': 'Date', last_col: 'Raw'})
    clean_df['Date'] = clean_df['Date'].str.split(':', expand=True)[1] + '/01/' + clean_df['Date'].str.split(':', expand=True)[0]
    clean_df = clean_df.set_index('Date')
    save_to_csv(clean_df, output_file)

def clean_tradingview(input_file: str, output_file: str) -> None:
    """
    Clean the data in the TradingView file and save it to the output file.

    Args:
    input_file (str): The input file to clean.
    output_file (str): The output file to save the cleaned data to.
    """
    clean_df = pd.read_csv(input_file)
    clean_df['Date'] = pd.to_datetime(clean_df['time'], unit='s')
    
    # Set the day to 1 for each row so it aligns with the other data
    clean_df['Date'] = clean_df['Date'].apply(lambda x: x.replace(day=1))

    clean_df['Date'] = clean_df['Date'].dt.strftime('%Y-%m-%d')
    clean_df = clean_df[['Date', 'close']]
    clean_df = clean_df.set_index('Date')
    save_to_csv(clean_df, output_file)

def main():
    pcpi_filename = os.path.join(paths.RAW_DIR, 'inflation', 'pcpiMvMd.xlsx')
    clean_cpi(pcpi_filename, 'pcpi.csv')

    pcpix_filename = os.path.join(paths.RAW_DIR, 'inflation', 'pcpixMvMd.xlsx')
    clean_cpi(pcpix_filename, 'pcpix.csv')

    gdp_filename = os.path.join(paths.RAW_DIR, 'gdp', 'routput_first_second_third.xlsx')
    clean_gdp(gdp_filename, 'gdp.csv')

    gdp_filename = os.path.join(paths.RAW_DIR, 'employment', 'rucQvMd.xlsx')
    clean_employment(gdp_filename, 'employment.csv')

    # Not including Russell 2000 as it is too new
    tv_files = ['indices/spx_1m.csv', 'indices/dji_1m.csv', 'indices/ndx_1m.csv', 'rates/fedfunds_1m.csv']
    for filepath in tv_files:
        index_filename = os.path.join(paths.RAW_DIR, filepath)
        output_filename = filepath.split('/')[-1]
        clean_tradingview(index_filename, output_filename)

    print("File saved.")

if __name__ == "__main__":
    main()