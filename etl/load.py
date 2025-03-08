# Standard Library
import logging
import urllib3
import warnings

# External 
import pandas as pd
import sqlite3

# Project
from config.config import DB_NAME, SERVICE


warnings.filterwarnings('ignore')
urllib3.disable_warnings()

logger = logging.getLogger(SERVICE)


def insert_data(
   df_sales_cleaned: pd.DataFrame, 
   df_category_metrics: pd.DataFrame, 
   df_outliers: pd.DataFrame
) -> None:
   """
   Summary:
      This function inserts the cleaned sales data, aggregated metrics, 
      and outliers into the SQLite database.
   Args:
      df_sales_cleaned (pd.DataFrame): The cleaned sales data
      df_category_metrics (pd.DataFrame): The aggregated metrics per category
      df_outliers (pd.DataFrame): The outliers in the sales data
   """
   try:
      
      # Check if there is any data to insert
      if len(df_sales_cleaned) == 0 and len(df_category_metrics) == 0 and len(df_outliers) == 0:
         logger.info("No data to insert into the database")
         return None
      
      # Create a connection to the SQLite database
      conn = sqlite3.connect(DB_NAME)

      # Save transactions
      if len(df_sales_cleaned) > 0:
         df_sales_cleaned.to_sql('transactions', conn, if_exists='replace', index=False)

      # Save aggregated metrics
      if len(df_category_metrics) > 0:
         df_category_metrics.to_sql('aggregated_metrics', conn, if_exists='replace', index=False)

      # Save outliers
      if len(df_outliers) > 0:
         df_outliers.to_sql('outliers', conn, if_exists='replace', index=False)

      # Close the connection
      conn.close()
   
   except Exception as e:
      logger.error(f"Error inserting data into the database: {e}")