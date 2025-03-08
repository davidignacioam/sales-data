# Standard Library
import logging
import urllib3
import warnings

# External
import pandas as pd

# Project
from config.config import CSV_PATH, SERVICE
from data.raw_data import raw_data

warnings.filterwarnings('ignore')
urllib3.disable_warnings()

logger = logging.getLogger(SERVICE)


def extract_data():
   """
   Summary:
      This function extracts the raw sales data and saves it as a CSV file
   """
   try:
      # Create a DataFrame with all columns as strings
      df = pd.DataFrame(raw_data, dtype=str)

      # Save the DataFrame as a CSV file
      df.to_csv(CSV_PATH, index=False)
   
   except Exception as e:
      logger.error(f"Error extracting data: {e}")