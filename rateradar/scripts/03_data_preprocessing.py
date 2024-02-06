"""
03_data_preprocessing.py

Purpose: Prepare the data for analysis, which may involve more nuanced cleaning 
specific to the type of analysis or the requirements of the data.

Tasks: Standardizing or normalizing data, dealing with outliers, encoding 
categorical variables if needed, and possibly creating new variables that might 
be more informative for the analysis.

Output: A preprocessed DataFrame that's structured and formatted appropriately for analysis.
"""
import os
import pandas as pd
import warnings
from pathlib import Path
from ..common import paths

# Remove annoying pandas warnings
warnings.filterwarnings("ignore")

def parse_quarterly_date(date_str: str) -> str:
    """
    Converts a date string in the format 'Year:Quarter' to a date string in the format 'YYYY-MM-DD'.
    The returned date string represents the first day of the given quarter.

    Args:
        date_str (str): A string in the format 'Year:Quarter', where Year is a 4-digit year and Quarter is a number from 1 to 4.

    Returns:
        str: A string representing the first day of the quarter in 'YYYY-MM-DD' format.
    """
    date_str = str(date_str)
    year, quarter = date_str.split(':')
    quarter_month = (int(quarter[-1]) - 1) * 3 + 1  
    return f"{year}-{quarter_month:02d}-01"  

def interpolate_gdp(gdp_data: pd.DataFrame) -> pd.DataFrame:
    """
    Interpolates GDP data from quarterly to monthly frequency.

    Args:
        gdp_data (pd.DataFrame): A DataFrame containing GDP data with a 'Date' column.

    Returns:
        pd.DataFrame: The input DataFrame resampled to monthly frequency, with missing values interpolated.
    """
    gdp_data['Date'] = pd.to_datetime(gdp_data['Date'])
    gdp_data.set_index('Date', inplace=True)
    
    monthly_df = gdp_data.resample('M').first()
    new_index = monthly_df.index.map(lambda d: pd.Timestamp(year=d.year, month=d.month, day=1))
    monthly_df.index = new_index
    
    return monthly_df.interpolate(method='linear')

def load_and_process_data(filename: str, date_parser=None) -> pd.DataFrame:
    """
    Loads a CSV file into a DataFrame and processes the 'Date' column.

    Args:
        filename (str): The path to the CSV file to load.
        date_parser (function, optional): A function to apply to the 'Date' column. Defaults to None.

    Returns:
        pd.DataFrame: The loaded and processed DataFrame.
    """
    df = pd.read_csv(filename)
    if date_parser:
        df['Date'] = df['Date'].apply(date_parser)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def add_suffix(df, suffix, on):
    # Add suffix to all columns except the merge key
    df = df.rename(columns={col: col + suffix if col != on else col for col in df.columns})
    return df
    
def merge_dataframes(dataframes: list, on: str, suffixes: list):
    """
    Merge multiple DataFrames on a common column.
    
    Args:
    dataframes (list): A list of DataFrames to merge.
    on (str): The name of the common column to merge on.
    suffixes (tuple): A tuple of suffixes to add to overlapping columns.
    
    Returns:
    pd.DataFrame: The merged DataFrame.
    """

    # Check if the number of suffixes matches the number of DataFrames
    assert len(dataframes) == len(suffixes), "The number of suffixes must match the number of DataFrames."

    # Apply suffixes to each DataFrame
    suffixed_dfs = [add_suffix(df, suffix, on) for df, suffix in zip(dataframes, suffixes)]

    # Start with the first suffixed DataFrame
    merged_df = suffixed_dfs[0]

    # Iterate over the remaining suffixed DataFrames and merge them
    for df in suffixed_dfs[1:]:
        merged_df = pd.merge(merged_df, df, on=on, how='outer')

    return merged_df

def remove_na_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows with missing values from the DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: The input DataFrame with rows containing missing values removed.
    """
    return df.dropna()

def main():
    gdp_filename = os.path.join(paths.PROCESSED_DIR, 'gdp.csv')
    gdp_df = load_and_process_data(gdp_filename, parse_quarterly_date)
    gdp_df = interpolate_gdp(gdp_df)
    gdp_df.to_csv(os.path.join(paths.PROCESSED_DIR, 'gdp_interpolated.csv'))

    pcpi_filename = os.path.join(paths.PROCESSED_DIR, 'pcpi.csv')
    pcpix_filename = os.path.join(paths.PROCESSED_DIR, 'pcpix.csv')
    employment_filename = os.path.join(paths.PROCESSED_DIR, 'employment.csv')
    gdp_filename = os.path.join(paths.PROCESSED_DIR, 'gdp_interpolated.csv')

    pcpi_df = load_and_process_data(pcpi_filename)
    pcpix_df = load_and_process_data(pcpix_filename)
    employment_df = load_and_process_data(employment_filename)
    gdp_df = load_and_process_data(gdp_filename)
    
    df_to_merge = [pcpi_df, pcpix_df, gdp_df, employment_df]
    suffixes = ['_pcpi', '_pcpix', '_gdp', '_unemploymentrate']

    tv_files = ['spx_1m.csv', 'dji_1m.csv', 'ndx_1m.csv', 'fedfunds_1m.csv']
    for filepath in tv_files:
        index_filename = os.path.join(paths.PROCESSED_DIR, filepath)
        df_to_merge.append(load_and_process_data(index_filename))
        suffixes.append('_' + filepath.split('_')[0])

    merged_df = merge_dataframes(df_to_merge, on='Date', suffixes=tuple(suffixes))

    #merged_df = remove_na_rows(merged_df)

    # Only rows after 'Date' is 7/1/1957 which is when GDP starts coming in
    merged_df = merged_df[merged_df['Date'] >= '1957-07-01']

    merged_df.to_csv(os.path.join(paths.PROCESSED_DIR, 'merged.csv'))

if __name__ == "__main__":
    main()