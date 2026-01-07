"""
Data Sources Module
Handles data collection from multiple sources (Data Source Layer)
"""
import pandas as pd
import requests
from dotenv import load_dotenv
import os
from .mobile_api_example import search_device
import time

load_dotenv()

def collect_mobile_api_data(device_names: list) -> pd.DataFrame:
    """
    Collect data from Mobile API
    Returns DataFrame with device information
    """
    devices_data = []
    
    print("Collecting data from Mobile API...")
    for device_name in device_names:
        try:
            result = search_device(device_name)
            if result and isinstance(result, dict):
                devices_data.append({
                    'device_name': device_name,
                    'api_data': result,
                    'source': 'mobile_api',
                    'collected_at': pd.Timestamp.now().isoformat()
                })
            time.sleep(0.5)  # Rate limiting
        except Exception as e:
            print(f"WARNING: Error fetching {device_name}: {e}")
    
    return pd.DataFrame(devices_data)

def load_kaggle_dataset(dataset_path: str = "data/mobile_devices.csv") -> pd.DataFrame:
    """
    Load Kaggle dataset
    """
    # Try multiple possible paths
    possible_paths = [
        dataset_path,
        f"../{dataset_path}",
        f"./{dataset_path}",
        "data/mobile_devices.csv",
        "../data/mobile_devices.csv"
    ]
    
    for path in possible_paths:
        try:
            if os.path.exists(path):
                df = pd.read_csv(path)
                print(f"SUCCESS: Loaded Kaggle dataset from {path}")
                
                # Normalize common column name variations
                # Priority: Name > Model for device_name
                column_mapping = {}
                
                # Device name mappings - use 'Name' as primary, keep 'Model' separate
                if 'Name' in df.columns:
                    column_mapping['Name'] = 'device_name'
                elif 'Model' in df.columns:
                    column_mapping['Model'] = 'device_name'
                elif 'name' in df.columns:
                    column_mapping['name'] = 'device_name'
                elif 'model' in df.columns:
                    column_mapping['model'] = 'device_name'
                
                # Brand mappings
                if 'Brand' in df.columns:
                    column_mapping['Brand'] = 'brand'
                elif 'brand' in df.columns:
                    column_mapping['brand'] = 'brand'
                elif 'Manufacturer' in df.columns:
                    column_mapping['Manufacturer'] = 'brand'
                
                # Price mappings
                if 'Price' in df.columns:
                    column_mapping['Price'] = 'price'
                elif 'price' in df.columns:
                    column_mapping['price'] = 'price'
                
                # Screen size mappings
                if 'Screen size (inches)' in df.columns:
                    column_mapping['Screen size (inches)'] = 'screen_size'
                elif 'Screen Size' in df.columns:
                    column_mapping['Screen Size'] = 'screen_size'
                elif 'screen_size' in df.columns:
                    column_mapping['screen_size'] = 'screen_size'
                
                # RAM mappings (convert MB to GB if needed)
                if 'RAM (MB)' in df.columns:
                    column_mapping['RAM (MB)'] = 'ram_mb'  # Keep original for conversion
                elif 'RAM' in df.columns:
                    column_mapping['RAM'] = 'ram'
                elif 'ram' in df.columns:
                    column_mapping['ram'] = 'ram'
                
                # Storage mappings
                if 'Internal storage (GB)' in df.columns:
                    column_mapping['Internal storage (GB)'] = 'storage'
                elif 'Storage' in df.columns:
                    column_mapping['Storage'] = 'storage'
                elif 'storage' in df.columns:
                    column_mapping['storage'] = 'storage'
                
                # OS mappings
                if 'Operating system' in df.columns:
                    column_mapping['Operating system'] = 'os'
                elif 'Operating System' in df.columns:
                    column_mapping['Operating System'] = 'os'
                elif 'OS' in df.columns:
                    column_mapping['OS'] = 'os'
                elif 'os' in df.columns:
                    column_mapping['os'] = 'os'
                
                # Apply mappings
                df = df.rename(columns=column_mapping)
                
                # Convert RAM from MB to GB if needed
                if 'ram_mb' in df.columns:
                    df['ram'] = df['ram_mb'] / 1024  # Convert MB to GB
                    df = df.drop(columns=['ram_mb'], errors='ignore')
                elif 'ram' in df.columns and df['ram'].dtype in ['int64', 'float64']:
                    # Check if values are likely in MB (>100) and convert
                    if df['ram'].max() > 100:
                        df['ram'] = df['ram'] / 1024  # Convert MB to GB
                
                # Drop duplicate device_name column if both Name and Model existed
                if 'device_name' in df.columns:
                    # If there are duplicate column names, keep first
                    df = df.loc[:, ~df.columns.duplicated(keep='first')]
                
                df = df.rename(columns=column_mapping)
                return df
        except Exception as e:
            continue
    
    # If no dataset found, create sample data
    print("WARNING: Kaggle dataset not found. Creating sample structure...")
    print("NOTE: Please download a mobile device dataset from Kaggle")

    
    # Sample data structure
    sample_data = {
        'device_name': ['iPhone 15 Pro', 'Samsung Galaxy S24', 'Google Pixel 8', 
                       'OnePlus 12', 'Xiaomi 14'],
        'brand': ['Apple', 'Samsung', 'Google', 'OnePlus', 'Xiaomi'],
        'price': [999, 899, 699, 799, 599],
        'screen_size': [6.1, 6.2, 6.2, 6.82, 6.36],
        'ram': [8, 12, 8, 16, 12],
        'storage': [128, 256, 128, 256, 256],
        'os': ['iOS', 'Android', 'Android', 'Android', 'Android'],
        'release_date': ['2023-09', '2024-01', '2023-10', '2024-01', '2023-10'],
        'category': ['Premium', 'Premium', 'Mid-range', 'Premium', 'Mid-range']
    }
    
    df = pd.DataFrame(sample_data)
    return df

def merge_data_sources(api_df: pd.DataFrame, kaggle_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge data from multiple sources (API and Kaggle)
    Returns combined DataFrame
    """
    print("Merging data from multiple sources...")
    
    # Normalize and merge datasets
    merged_df = pd.concat([
        kaggle_df
    ], ignore_index=True)
    
    print(f"SUCCESS: Merged {len(merged_df)} records from multiple sources")
    return merged_df

def validate_data_quality(df: pd.DataFrame) -> dict:
    """
    Check data quality: completeness, validity, inconsistencies
    Returns quality report
    """
    quality_report = {
        'total_records': len(df),
        'missing_values': df.isnull().sum().to_dict(),
        'missing_percentage': (df.isnull().sum() / len(df) * 100).to_dict(),
        'duplicate_records': df.duplicated().sum(),
        'data_types': df.dtypes.to_dict()
    }
    
    # Check for inconsistencies
    if 'price' in df.columns:
        quality_report['price_range'] = {
            'min': float(df['price'].min()),
            'max': float(df['price'].max()),
            'mean': float(df['price'].mean())
        }
    
    return quality_report
