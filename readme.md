# Sales API Project

## 📁 Project Structure

```
project-folder/
│
├── app/                         # Application and API Code
│   ├── api.py                   # FastAPI application code
│   ├── main.py                  # Main entry point for the API
│   ├── __init__.py              # Makes the folder a Python module
│
├── config/                      # Configuration and Logging
│   ├── config.py                # Configuration settings
│   ├── logger.py                # Logging configuration
│   ├── __init__.py              # Makes the folder a Python module
│
├── data/                        # Data Files and Database
│   ├── sales_data.csv           # Original sales data
│   ├── sales_data.db            # SQLite database with processed data
│   ├── raw_data.py              # Raw data processing and cleaning
│   ├── __init__.py              # Makes the folder a Python module
│
├── etl/                         # ETL (Extract, Transform, Load) Scripts
│   ├── extract.py               # Data extraction logic
│   ├── transform.py             # Data transformation logic
│   ├── load.py                  # Data loading into SQLite database
│   ├── __init__.py              # Makes the folder a Python module
│
├── requirements.txt             # Project dependencies
└── README.md                    # Project documentation
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone git@github.com:davidignacioam/sales-data.git
cd project-folder
```

### 2. Set Up a Virtual Environment (Optional)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Prepare the Database

- If not already prepared, run the data extraction, transformation, and loading scripts in the following order:

```bash
python app/main.py
```

### 5. Run the API Server

```bash
uvicorn app.api:app --reload
```

### 6. Access the API Documentation

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 📌 API Endpoints

### 1. **GET /sales/product**

- Returns total sales for each product.
- Supports optional filtering by product name or category.

### 2. **GET /sales/day**

- Returns total sales for each day.
- Supports filtering by date range.

### 3. **GET /sales/category**

- Returns aggregated metrics for each category (total revenue, average price, days with highest sales).

### 4. **GET /sales/outliers**

- Returns flagged outlier transactions.

---

## 🧑‍💻 Development & Contribution

1. Fork the repository.
2. Create a feature branch.
3. Commit changes.
4. Open a pull request.

---

## ⚠️ Requirements.txt

```
fastapi
uvicorn
pandas
sqlite3
numpy
python-dotenv
logging
```
