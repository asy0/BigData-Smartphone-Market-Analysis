"""
Spark Processing Module
For Big Data processing using PySpark (Processing Layer)
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, max as spark_max, min as spark_min, when
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType
import pandas as pd

def create_spark_session(app_name: str = "BigDataAnalytics"):
    """Create and return Spark session. Returns None if Spark is not available (e.g., Windows issues)"""
    import os
    import sys
    
    # Fix for Windows: Handle getSubject error
    if os.name == 'nt':  # Windows
        # Set environment variables to avoid Windows-specific Spark issues
        if 'HADOOP_HOME' not in os.environ:
            # Try to find winutils or set to empty
            os.environ['HADOOP_HOME'] = ''
        if 'HADOOP_USER_NAME' not in os.environ:
            os.environ['HADOOP_USER_NAME'] = os.environ.get('USERNAME', 'user')
        
        # Set Java options to avoid getSubject error
        java_opts = os.environ.get('JAVA_OPTS', '')
        if '-Djava.security.auth.login.config' not in java_opts:
            # Try to bypass the getSubject call
            os.environ['JAVA_OPTS'] = java_opts + ' -Djava.security.auth.login.config='
    
    try:
        spark = SparkSession.builder \
            .appName(app_name) \
            .master("local[*]") \
            .config("spark.driver.memory", "2g") \
            .config("spark.executor.memory", "2g") \
            .config("spark.sql.warehouse.dir", "file:///tmp/spark-warehouse") \
            .getOrCreate()
        
        print("SUCCESS: Spark session created successfully!")
        return spark
    except Exception as e:
        # If getSubject error occurs, try with additional config
        if "getSubject" in str(e) or "UnsupportedOperationException" in str(e):
            print("WARNING: Windows-specific Spark issue detected. Trying alternative configuration...")
            try:
                # Try with minimal config
                spark = SparkSession.builder \
                    .appName(app_name) \
                    .master("local[1]") \
                    .config("spark.driver.memory", "1g") \
                    .config("spark.executor.memory", "1g") \
                    .config("spark.sql.warehouse.dir", "file:///tmp/spark-warehouse") \
                    .config("spark.driver.extraJavaOptions", "-Djava.security.auth.login.config=") \
                    .getOrCreate()
                print("SUCCESS: Spark session created with alternative configuration!")
                return spark
            except Exception as e2:
                print("WARNING: Spark is not available on this system (Windows getSubject error).")
                print("         Using Pandas as fallback for all operations.")
                print("         Note: This is a known Windows/Java compatibility issue.")
                return None
        else:
            raise

def pandas_to_spark_df(spark, pandas_df: pd.DataFrame):
    """Convert pandas DataFrame to Spark DataFrame. Returns pandas DataFrame if spark is None."""
    if spark is None:
        return pandas_df  # Return pandas DataFrame as fallback
    return spark.createDataFrame(pandas_df)

def spark_mapreduce_example(spark, df):
    """
    Example MapReduce operation using Spark or Pandas fallback
    Groups data and performs aggregations (MapReduce pattern)
    """
    print("\nPerforming MapReduce operation...")
    
    # Check if df is Spark DataFrame or pandas DataFrame
    if spark is None or isinstance(df, pd.DataFrame):
        # Pandas fallback: MapReduce pattern with groupby
        print("Using Pandas for MapReduce (Spark not available)")
        
        # Filter out NaN categories
        df_clean = df.dropna(subset=['category'])
        
        if len(df_clean) == 0:
            print("WARNING: No valid categories found. Creating categories from price...")
            if 'price' in df.columns:
                df_clean = df.copy()
                df_clean['category'] = pd.cut(
                    df_clean['price'],
                    bins=[0, 5000, 20000, float('inf')],
                    labels=['Budget', 'Mid-range', 'Premium']
                )
                df_clean = df_clean.dropna(subset=['category'])
        
        if len(df_clean) > 0:
            result = df_clean.groupby("category").agg({
                "price": ["count", "mean", "max", "min"]
            })
            result.columns = ["count", "avg_price", "max_price", "min_price"]
            result = result.reset_index()
        else:
            # Return empty result with correct structure
            result = pd.DataFrame(columns=["category", "count", "avg_price", "max_price", "min_price"])
        
        return result
    else:
        # Spark implementation
        result = df.groupBy("category") \
            .agg(
                count("*").alias("count"),
                avg("price").alias("avg_price"),
                spark_max("price").alias("max_price"),
                spark_min("price").alias("min_price")
            )
        return result

def process_device_data(spark, device_df):
    """
    Process mobile device data using Spark or Pandas fallback
    Includes data cleaning, transformations, and aggregations
    """
    if spark is None:
        # Pandas fallback
        print("Using Pandas for data processing (Spark not available)")
        processed_df = device_df.copy()
        
        # Price category
        processed_df["price_category"] = processed_df["price"].apply(
            lambda x: "Budget" if x < 5000 else ("Mid-range" if x < 20000 else "Premium")
        )
        
        # Extract year from release_date
        if "release_date" in processed_df.columns:
            processed_df["year"] = pd.to_datetime(processed_df["release_date"], errors='coerce').dt.year
        else:
            processed_df["year"] = None
        
        return processed_df
    else:
        # Spark implementation
        spark_df = pandas_to_spark_df(spark, device_df)
        
        # Data transformations
        processed_df = spark_df \
            .withColumn("price_category", 
                       when(col("price") < 5000, "Budget")
                       .when(col("price") < 20000, "Mid-range")
                       .otherwise("Premium")) \
            .withColumn("year", col("release_date").substr(1, 4))
        
        return processed_df

def spark_ml_preprocessing(spark, df):
    """
    Preprocess data for Machine Learning using Spark
    Feature engineering and data preparation
    """
    from pyspark.ml.feature import VectorAssembler, StringIndexer
    
    # Index categorical features
    indexer = StringIndexer(inputCol="brand", outputCol="brand_index")
    indexed_df = indexer.fit(df).transform(df)
    
    # Assemble features for ML
    feature_cols = ["brand_index", "screen_size", "ram", "storage"]
    assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
    ml_df = assembler.transform(indexed_df)
    
    return ml_df
