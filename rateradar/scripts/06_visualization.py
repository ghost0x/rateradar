"""
06_visualization.py

Purpose: Create visual representations of the economic data and analysis results.
Tasks: Generate charts, graphs, and other visualizations to illustrate the 
findings. This could include time series plots, histograms, scatter plots, or 
more complex visualizations like heat maps.

Output: A set of visualizations that can be used in reports or presentations.
"""
# Remove annoying pandas warnings
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

import os
import pandas as pd
import matplotlib.pyplot as plt

from ..common import paths

filepath = os.path.join(paths.PROCESSED_DIR, 'pcpi.csv')
df = pd.read_csv(filepath)

print(df)
# Convert the 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Set the 'Date' column as the index of the DataFrame
df.set_index('Date', inplace=True)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(df.index, df['Pct'], marker='o', linestyle='-')
plt.title('Monthly Data Series')
plt.xlabel('Date')
plt.ylabel('Pct')
plt.grid(True)
plt.xticks(rotation=45)  # Rotate date labels for better readability
plt.tight_layout()  # Adjust layout to not cut off labels
plt.show()