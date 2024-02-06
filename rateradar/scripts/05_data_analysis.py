"""
05_data_analysis.py

Purpose: Conduct the core analysis on the economic data.
Tasks: Depending on your goals, this might involve statistical tests, time series analysis, 
modeling, trend analysis, etc. You might have multiple scripts or functions 
for different types of analysis.

Output: Results of the analysis, which could be statistical summaries, model outputs, 
identified trends, etc.
"""
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

import os
import pandas as pd

from ..common import paths

from pathlib import Path

filename = os.path.join(paths.PROCESSED_DIR, 'merged.csv')

df = pd.read_csv(filename)

# Convert 'Date' column to datetime format and set as index
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
df.set_index('Date', inplace=True)

# Drop the unnamed index column as it's redundant
df.drop(columns=['Unnamed: 0'], inplace=True)

# Calculate 6-month percentage change for 'Raw_pcpi' and 'Raw_pcpix'
df['6m_change_pcpi'] = df['Raw_pcpi'].pct_change(periods=6) * 100  # Convert to percentage
df['6m_change_pcpix'] = df['Raw_pcpix'].pct_change(periods=6) * 100  # Convert to percentage

# Filter for periods where the 6-month change in 'Raw_pcpi' or 'Raw_pcpix' exceeded 1%
inflation_increase = df[(df['6m_change_pcpi'] > 1) | (df['6m_change_pcpix'] > 1)]

# Display the results
inflation_increase.head()

inflation_increase.to_csv(os.path.join(paths.PROCESSED_DIR, '6mo_windows.csv'))