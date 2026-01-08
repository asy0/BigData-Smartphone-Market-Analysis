# Big Data Analytics Project
## Mobile Device Market Analysis

A comprehensive Big Data Analytics project implementing all 4 layers of Big Data processing: Data Source, Data Storage, Processing, and Data Output.

## Project Overview

This project analyzes mobile device market data using:
- **Multiple Data Sources:** Mobile API, Kaggle datasets
- **Dual Database Storage:** PostgreSQL (SQL) and MongoDB (NoSQL)
- **Big Data Processing:** Apache Spark with MapReduce patterns
- **Machine Learning:** Price prediction and category classification
- **Visualization:** Comprehensive data storytelling with interactive charts

## Project Structure

```
Big-Data-Analytics/
├── notebooks/                    # Jupyter Notebooks for each layer
│   ├── 01_Data_Source_Layer.ipynb
│   ├── 02_Data_Storage_Layer.ipynb
│   ├── 03_Processing_Layer.ipynb
│   ├── 04_Data_Output_Layer.ipynb
│   └── 05_Big_Data_Vs_Analysis.ipynb
├── src/                          # Python source modules
│   ├── __init__.py
│   ├── data_sources.py           # Data collection module
│   ├── db_connect.py             # PostgreSQL connection
│   ├── mongodb_connect.py        # MongoDB connection (NoSQL)
│   ├── spark_processing.py       # Spark/MapReduce processing
│   ├── ml_models.py              # Machine Learning models
│   └── mobile_api_example.py     # Mobile API integration
├── docs/                         # Documentation
│    └── Project Specification.pdf # Project requirements
├── config/                       # Configuration files
│   └── env.example               # Environment variables template
├── data/                         # Data files (CSV, models)
│   └── mobile_devices.csv        # Kaggle dataset
├── queries/                      # SQL queries
│   └── Query.sql
├── main.py                       # Main entry point
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Quick Start

### 1. Prerequisites

- Python 3.7 or higher
- PostgreSQL database (or use Neon's online service)
- MongoDB (optional, for NoSQL storage)
- Java 8+ (required for Spark)

### 2. Installation

```bash
# Clone the repository
cd Big-Data-Analytics

# Install Python dependencies
pip install -r requirements.txt

# Install Java (required for Spark)
# Windows: Download from https://adoptium.net/
# macOS: brew install openjdk@8
# Linux: sudo apt-get install openjdk-8-jdk
```

### 3. Environment Setup

**Quick Setup:**
1. Copy `config/env.example` to `.env` in project root
2. Fill in your credentials (see detailed guides below)

**Detailed Guides:**
- **MobileAPI Key:** get from https://app.mobileapi.dev/
- **Kaggle Dataset:** Download from Kaggle and place in `data/mobile_devices.csv`

Create a `.env` file in the project root:

```env
# PostgreSQL Connection
PGHOST=your_postgres_host
PGPORT=5432
PGUSER=your_username
PGPASSWORD=your_password
PGDATABASE=your_database

# MongoDB Connection (optional)
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB=bigdata_analytics

# Mobile API Key (get from https://app.mobileapi.dev/)
MOBILEAPIKEY=your_mobile_api_key
```

### 4. Database Setup

#### PostgreSQL (SQL Database)

We use a PostgreSQL Database to avoid multiple local database installations.

**Connection Setup:**
1. In **DataGrip** or PyCharm (**DataGrip** preferred) click on the Plus - chose Data Source - chose **PostgreSQL**
2. For **Host** use **PGHOST**
3. For **Port** use **PGPORT**
4. For **User** use **PGUSER**
5. For **Password** use **PGPASSWORD**
6. For **Database** use **PGDATABASE**
7. Open the **SSH/SSL** tab
8. Check **Use SSL**
9. Set **Mode** to **Require**
10. Click **Test Connection** and then **OK**

#### MongoDB (NoSQL Database) 

**Option 1: Local Installation**
```bash
# macOS
brew install mongodb-community

# Linux
sudo apt-get install mongodb

# Windows
# Download from https://www.mongodb.com/try/download/community
```

**Option 2: MongoDB Atlas (Cloud)**
- Sign up at https://www.mongodb.com/cloud/atlas
- Create a free cluster
- Get connection string and add to `.env` as `MONGODB_URI`

### 5. Running the Project

#### Option A: Run Jupyter Notebooks (Recommended)

```bash
# Start Jupyter Notebook
jupyter notebook

# Navigate to notebooks/ folder and run in order:
# 1. 01_Data_Source_Layer.ipynb
# 2. 02_Data_Storage_Layer.ipynb
# 3. 03_Processing_Layer.ipynb
# 4. 04_Data_Output_Layer.ipynb
# 5. 05_Big_Data_Vs_Analysis.ipynb
```

#### Option B: Run Python Scripts

```bash
# Test database connection
python main.py

# Test Mobile API (from src module)
python -c "from src.mobile_api_example import search_device; print(search_device('iPhone 15'))"
```

## Project Components

### 1. Data Source Layer
- **Mobile API:** Fetch device specifications via REST API
- **Kaggle Dataset:** Load mobile device datasets
- **Data Quality:** Validation and quality checks

### 2. Data Storage Layer
- **PostgreSQL (SQL):** Structured relational data storage
- **MongoDB (NoSQL):** Flexible document-based storage 
- **Data Import/Export:** Python scripts for database operations

### 3. Processing Layer
- **Apache Spark:** Distributed data processing
- **MapReduce:** Group and aggregate operations
- **Feature Engineering:** Extract features for ML
- **Machine Learning:**
  - Price Prediction (Regression)
  - Category Classification

### 4. Data Output Layer
- **Visualizations:** Matplotlib, Seaborn, Plotly
- **Storytelling:** Clear presentation of insights
- **Interactive Charts:** Plotly visualizations

##  Dependencies

All dependencies are listed in `requirements.txt`:

- **Database:** `psycopg2-binary`, `pymongo`
- **Data Processing:** `pandas`, `numpy`
- **Big Data:** `pyspark`
- **Machine Learning:** `scikit-learn`
- **Visualization:** `matplotlib`, `seaborn`, `plotly`
- **Jupyter:** `jupyter`, `notebook`, `ipykernel`

Install all dependencies:
```bash
pip install -r requirements.txt
```

## Project Requirements Checklist

### Obligatory Components:
- **NoSQL Database** (MongoDB)
- **Web Scraping or API** (API implemented)
- **Spark** (Apache Spark with PySpark)
- **MapReduce** (Implemented with Spark)
- **Machine Learning** (Price prediction + Classification)
- **Jupyter Notebooks** (Documentation)

### Data Sources:
- **At least 2 different sources** (API, Kaggle)
- **Data quality checks**
- **Data documentation**

### Storage:
- **SQL Database** (PostgreSQL)
- **NoSQL Database** (MongoDB)
- **Import/Export functionality**

### Analysis:
- **Feature extraction**
- **ML models**
- **Statistical analysis**

### Output:
- **Visualizations**
- **Storytelling**
- **Clear presentation**

## Big Data V's Analysis

The project is analyzed according to Big Data criteria:
- **Volume:** Scalable architecture
- **Velocity:** Batch processing with streaming capability
- **Variety:** Multiple data types and sources
- **Veracity:** Quality checks implemented
- **Value:** ML models and insights

See `notebooks/05_Big_Data_Vs_Analysis.ipynb` for detailed analysis.

## Troubleshooting

### Spark Issues
```bash
# Check Java installation
java -version

# Set JAVA_HOME if needed
export JAVA_HOME=/path/to/java
```

### MongoDB Connection Issues
- Ensure MongoDB is running: `mongod` (local) or check Atlas connection string
- Verify `MONGODB_URI` in `.env` file

### Import Errors in Notebooks
- Make sure you're using `from src.module import ...` syntax
- Restart kernel after opening notebook: **Kernel → Restart Kernel**
- Verify `sys.path.append('..')` is executed before imports
- Check that you're running notebooks from the `notebooks/` directory

### PostgreSQL Connection Issues
- Verify credentials in `.env` file
- Check SSL settings (should be "require")
- Ensure database exists
- Copy `config/env.example` to `.env` and fill in your PostgreSQL credentials

## Setup Documentation

For detailed setup instructions, see:
- **MobileAPI:**
  - API Endpoint: https://api.mobileapi.dev/devices/search/
  - Documentation & API Key Registration: https://app.mobileapi.dev/
- **Kaggle Dataset:**
  - Kaggle Datasets Platform: https://www.kaggle.com/datasets
  - Search for: "mobile phone specification"
  - Download CSV and place in `data/mobile_devices.csv`

## Notes

**Kaggle Dataset:**
- Platform: https://www.kaggle.com/datasets
- Search for: "mobile phone specification"
- Download CSV and place in `data/mobile_devices.csv`
- The project includes a sample dataset structure if no file is found.

**API Keys:**
- Keep API keys secure, never commit `.env` file
- **MobileAPI:**
  - API Endpoint: https://api.mobileapi.dev/devices/search/
  - Get API key from: https://app.mobileapi.dev/
  - Copy `config/env.example` to `.env` and fill in your credentials

Project Structure: All Python modules are in `src/` directory. Notebooks use `from src.module import ...` syntax. Configuration files are in `config/` directory.

Data Size: Current implementation handles medium-sized datasets; architecture scales to larger volumes.

## Team

This project is part of the "Big Data Analytics" course.

## License

This project is for educational purposes.

## Next Steps

1. **Get MobileAPI Key:**
   - Register at: https://app.mobileapi.dev/
   - API Documentation: https://api.mobileapi.dev/devices/search/
2. **Download Kaggle Dataset:**
   - Visit: https://www.kaggle.com/datasets
   - Search for: "mobile phone specification"
   - Download CSV and place in `data/mobile_devices.csv`
3. **Configure Environment:**
   - Copy `config/env.example` to `.env` in project root
   - Fill in your credentials (PostgreSQL, MongoDB, MobileAPI key)
4. **Run Notebooks:**
   - Execute notebooks in sequence (01 to 05)
   - Make sure to restart kernel after opening notebooks
   - Use `from src.module import ...` syntax

Use the credentials from the `.env` file in your project root.
