# Standard
from logging.config import dictConfig

# External
import pandas as pd

# Project
from config.config import CSV_PATH
from config.logger import LogConfig
from etl.extract import extract_data
from etl.transform import clean_data, transform_data
from etl.load import insert_data

dictConfig(LogConfig().dict())

def main():
   
   extract_data()

   df_sales = pd.read_csv(CSV_PATH)

   df_sales_cleaned = clean_data(df_sales)

   df_sales_cleaned, df_category_metrics, df_outliers = transform_data(df_sales_cleaned)

   insert_data(df_sales_cleaned, df_category_metrics, df_outliers)

if __name__ == "__main__":
   main()