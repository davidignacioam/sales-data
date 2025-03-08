# Standard Library
import logging
import urllib3
import warnings

# External
import pandas as pd

# project
from config.config import SERVICE


warnings.filterwarnings('ignore')
urllib3.disable_warnings()

logger = logging.getLogger(SERVICE)


def clean_data(df_sales: pd.DataFrame) -> pd.DataFrame:
   """
   Summary:
      This function cleans the sales data by:
      - Handling missing values  (quantity and price)
      - Calculating total_sales
      - Creating a day_of_week column
      - Adding a high_volume flag
   Args:
      df_sales (pd.DataFrame): The input sales data
   Returns:
      pd.DataFrame: The cleaned sales data
   """
   try:
      
      # Check if there is data to clean
      if len(df_sales) == 0:
         logger.error("No data to clean")
         return pd.DataFrame()
      
      # 1. Handle missing values
      # Replace missing quantity with 0
      df_sales['quantity'] = df_sales['quantity'].fillna(0)

      # Replace invalid price values ('not_a_number') with the median price for the same category
      df_sales['price'] = pd.to_numeric(df_sales['price'], errors='coerce')
      median_prices = df_sales.groupby('category')['price'].transform('median')
      df_sales['price'] = df_sales['price'].fillna(median_prices)

      # Drop rows where both quantity and price are invalid or missing
      df_sales = df_sales.dropna(subset=['quantity', 'price'], how='all')

      # Derived Columns
      # Calculate total_sales
      df_sales['total_sales'] = df_sales['quantity'] * df_sales['price']

      # Create a day_of_week column
      df_sales['day_of_week'] = pd.to_datetime(df_sales['date']).dt.day_name()

      # Add a high_volume flag
      df_sales['high_volume'] = df_sales['quantity'] > 10
      
      return df_sales

   except Exception as e:
      logger.error(f"Error cleaning data: {e}")
      return pd.DataFrame()


def transform_data(df_sales_cleaned: pd.DataFrame) -> tuple:
   """
   Summary:
      This function transforms the sales data by:
      - Calculating the average price and total revenue per category
      - Identifying outliers
      - Finding the days with the highest sales for each category
   Args:
      df_sales_cleaned (pd.DataFrame): The cleaned sales data
   Returns:
      tuple: A tuple containing the transformed dataframes: 
         - df_sales_cleaned: The cleaned sales data with an additional 'outlier' column
         - df_category_metrics: Aggregated metrics per category
         - df_outliers: The outliers in the sales data
   """
   try:
      
      # Check if there is data to transform
      if len(df_sales_cleaned) == 0:
         logger.error("No data to transform")
         return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
      
      # Calculate the days with the highest sales for each category
      highest_sales_per_day = (
         df_sales_cleaned.groupby(['category', 'date'])['total_sales'].sum().reset_index()
      )

      # Get all dates with the maximum sales for each category
      max_sales_per_category = highest_sales_per_day.groupby('category')['total_sales'].transform('max')
      highest_sales_dates = highest_sales_per_day[highest_sales_per_day['total_sales'] == max_sales_per_category]

      # Concatenate dates with the same maximum sales
      highest_sales_dates = (
         highest_sales_dates.groupby('category')['date']
         .apply(lambda x: ', '.join(x))
         .reset_index()
      )

      # Merge with the aggregated metrics
      df_category_metrics = (
         df_sales_cleaned.
         groupby('category').
         agg({
            'price': 'mean',
            'total_sales': 'sum'
         }).
         rename(columns={
            'price': 'avg_price',
            'total_sales': 'total_revenue'
         }).
         reset_index().
         merge(highest_sales_dates, on='category').
         rename(columns={'date': 'days_with_highest_sales'})
      )

      # Identify outliers (more than 2 standard deviations from the mean)
      category_means = df_sales_cleaned.groupby('category')['quantity'].transform('mean')
      category_stds = df_sales_cleaned.groupby('category')['quantity'].transform('std')
      df_sales_cleaned['outlier'] = (df_sales_cleaned['quantity'] > (category_means + 2 * category_stds))
      
      # Get the outliers
      df_outliers = df_sales_cleaned[df_sales_cleaned['outlier']]
      
      return (
         df_sales_cleaned, 
         df_category_metrics, 
         df_outliers
      )
   
   except Exception as e:
      logger.error(f"Error transforming data: {e}")
      return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()