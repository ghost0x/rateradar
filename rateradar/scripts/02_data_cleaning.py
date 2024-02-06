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
    clean_df = clean_df.rename(columns={'DATE': 'date', last_col: 'raw'})
    clean_df['date'] = clean_df['date'].str.split(':', expand=True)[1] + '/01/' + clean_df['date'].str.split(':', expand=True)[0]
    clean_df = clean_df.set_index('date')
    clean_df['pct'] = clean_df['raw'].pct_change() * 100

    # Get the CPI difference between this row and 6 rows ago
    clean_df['6m_change'] = clean_df['raw'].diff(6)

    # Calculate what percentage change that is
    clean_df['6m_pct_change'] = clean_df['6m_change'] / clean_df['raw'].shift(6) * 100

    # Double the change to get the annualized rate
    clean_df['annualized_change'] = clean_df['6m_pct_change'] * 2

    # Drop unnecessary columns
    clean_df = clean_df[['pct', '6m_pct_change', 'annualized_change']]

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
    clean_df = clean_df.rename(columns={'Date': 'date'})
    clean_df = clean_df.rename(columns={'First': 'gdp'})
    clean_df = clean_df.set_index('date')
    convert_to_numeric(clean_df, 'gdp')
    
    # Drop unnecessary columns
    clean_df = clean_df[['gdp']]

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
    convert_to_numeric(clean_df, last_col)
    clean_df = clean_df.rename(columns={'DATE': 'date', last_col: 'pct'})
    clean_df['date'] = clean_df['date'].str.split(':', expand=True)[1] + '/01/' + clean_df['date'].str.split(':', expand=True)[0]
    clean_df = clean_df.set_index('date')
    clean_df = clean_df[['pct']]
    save_to_csv(clean_df, output_file)

def convert_to_numeric(df: pd.DataFrame, column: str) -> None:
    """
    Convert the column in the DataFrame to a numeric value.

    Args:
    df (pd.DataFrame): The DataFrame to convert.
    column (str): The column to convert to a numeric value.
    """
    df.loc[:, column] = pd.to_numeric(df[column], errors='coerce')
    

def clean_tradingview(input_file: str, output_file: str) -> None:
    """
    Clean the data in the TradingView file and save it to the output file.

    Args:
    input_file (str): The input file to clean.
    output_file (str): The output file to save the cleaned data to.
    """
    clean_df = pd.read_csv(input_file)
    clean_df['date'] = pd.to_datetime(clean_df['time'], unit='s')
    
    # Set the day to 1 for each row so it aligns with the other data
    clean_df['date'] = clean_df['date'].apply(lambda x: x.replace(day=1))

    clean_df['date'] = clean_df['date'].dt.strftime('%Y-%m-%d')
    clean_df = clean_df[['date', 'close']]
    convert_to_numeric(clean_df, 'close')
    clean_df = clean_df.set_index('date')
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