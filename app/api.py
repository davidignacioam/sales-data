# External
from fastapi import FastAPI, Query
from typing import Optional, List
import sqlite3

# Project
from config.config import DB_NAME


app = FastAPI()

# Utility function to execute SQL queries
def execute_query(query: str, params: tuple = ()) -> List[dict]:
   conn = sqlite3.connect(DB_NAME)
   conn.row_factory = sqlite3.Row
   cursor = conn.cursor()
   cursor.execute(query, params)
   rows = cursor.fetchall()
   conn.close()
   return [dict(row) for row in rows]

# 1. GET /sales/product
@app.get('/sales/product')
def get_sales_by_product(
   product_name: Optional[str] = Query(None, description="Filter by product name"),
   category: Optional[str] = Query(None, description="Filter by category")
):
   query = '''
      SELECT product, SUM(total_sales) AS total_sales
      FROM transactions
      WHERE (? IS NULL OR product = ?)
      AND (? IS NULL OR category = ?)
      GROUP BY product;
   '''
   params = (product_name, product_name, category, category)
   return execute_query(query, params)

# 2. GET /sales/day
@app.get('/sales/day')
def get_sales_by_day(
   start_date: Optional[str] = Query(None, description="Filter by start date (YYYY-MM-DD)"),
   end_date: Optional[str] = Query(None, description="Filter by end date (YYYY-MM-DD)")
):
   query = '''
      SELECT date, SUM(total_sales) AS total_sales
      FROM transactions
      WHERE (? IS NULL OR date >= ?)
      AND (? IS NULL OR date <= ?)
      GROUP BY date;
   '''
   params = (start_date, start_date, end_date, end_date)
   return execute_query(query, params)

# 3. GET /sales/category
@app.get('/sales/category')
def get_aggregated_metrics_by_category():
   query = '''
      SELECT * FROM aggregated_metrics;
   '''
   return execute_query(query)

# 4. GET /sales/outliers
@app.get('/sales/outliers')
def get_outliers():
   query = '''
      SELECT * FROM outliers;
   '''
   return execute_query(query)