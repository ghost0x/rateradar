"""
07_report_generation.py

Purpose: Compile the analysis results and visualizations into a readable format, 
such as a PDF report or a dashboard.

Tasks: Automate the generation of reports or dashboards, including textual summaries of 
findings, embedding visualizations, and formatting the report.

Output: A final report or dashboard that presents the findings from the economic data analysis.
"""
import os
import warnings
import csv
import json
from pathlib import Path
from ..common import paths

# Remove annoying pandas warnings
warnings.filterwarnings("ignore")

# Specify the file paths for the CSV input and JSON output
csv_file_path = os.path.join(paths.PROCESSED_DIR, 'merged.csv')
json_file_path = os.path.join(paths.PROCESSED_DIR, 'output.json')

data = []

# Open the CSV file for reading
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    
    for row in csv_reader:
        for key, value in row.items():
            if key == "":
                continue
            # If the key is not "Date", convert the value to a float
            if key != "date" and value != "":
                row[key] = float(value)
        data.append(row)

# Open the JSON file for writing
with open(json_file_path, 'w') as json_file:
    json.dump(data, json_file, indent=4)

# Copy the output to the web directory
web_output_path = os.path.join(paths.WEB_DIR, 'output.json')
with open(web_output_path, 'w') as json_file:
    json.dump(data, json_file, indent=4)
