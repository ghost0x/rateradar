"""
03_data_preprocessing.py

Purpose: Prepare the data for analysis, which may involve more nuanced cleaning 
specific to the type of analysis or the requirements of the data.

Tasks: Standardizing or normalizing data, dealing with outliers, encoding 
categorical variables if needed, and possibly creating new variables that might 
be more informative for the analysis.

Output: A preprocessed DataFrame that's structured and formatted appropriately for analysis.
"""
# Remove annoying pandas warnings
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

import os
import pandas as pd

from ..common import paths

from pathlib import Path

pcpi_filename = os.path.join(paths.PROCESSED_DIR, 'pcpi.csv')
pcpix_filename = os.path.join(paths.PROCESSED_DIR, 'pcpix.csv')

df1 = pd.read_csv(pcpi_filename)
df2 = pd.read_csv(pcpix_filename)

merged_df = df1.merge(df2, on='Date', suffixes=('_pcpi', '_pcpix'))

merged_df.to_csv(os.path.join(paths.PROCESSED_DIR, 'merged.csv'))