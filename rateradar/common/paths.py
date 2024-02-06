import os
import sys

# Get parent directory of current directory
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
data_dir = os.path.join(os.path.dirname(parent_dir), 'data')
raw_dir = os.path.join(data_dir, 'raw')
processed_dir = os.path.join(data_dir, 'processed')

RAW_DIR = raw_dir
PROCESSED_DIR = processed_dir