"""
Spark Processing Module
For Big Data processing using PySpark (Processing Layer)
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, max as spark_max, min as spark_min, when
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType
import pandas as pd

def create_spark_session(app_name: str = "BigDataAnalytics"):
    """Create and return Spark session"""
    spark = SparkSession.builder \
        .appName(app_name) \
        .master("local[*]") \
        .config("spark.driver.memory", "2g") \
        .config("spark.executor.memory", "2g") \
        .getOrCreate()
    
    print("SUCCESS: Spark session created successfully!")
    return spark

def pandas_to_spark_df(spark, pandas_df: pd.DataFrame):
    """Convert pandas DataFrame to Spark DataFrame"""
    return spark.createDataFrame(pandas_df)

def spark_mapreduce_example(spark, df):
    """
    Example MapReduce operation using Spark
    Groups data and performs aggregations (MapReduce pattern)
    """
    print("\nPerforming MapReduce operation...")
    
    # Map: Group by category
    # Reduce: Aggregate statistics
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
    Process mobile device data using Spark
    Includes data cleaning, transformations, and aggregations
    """
    spark_df = pandas_to_spark_df(spark, device_df)
    
    # Data transformations
    processed_df = spark_df \
        .withColumn("price_category", 
                   when(col("price") < 500, "Budget")
                   .when(col("price") < 1000, "Mid-range")
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
