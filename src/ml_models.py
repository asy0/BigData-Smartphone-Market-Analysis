"""
Machine Learning Module
For predictive analytics and ML models (Processing Layer)
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, classification_report
import joblib

def prepare_features(df: pd.DataFrame) -> tuple:
    """
    Feature engineering for ML models
    Extracts and prepares features from raw data
    """
    # Create feature columns
    features_df = df.copy()
    
    # Encode categorical variables
    le_brand = LabelEncoder()
    le_os = LabelEncoder()
    
    if 'brand' in features_df.columns:
        features_df['brand_encoded'] = le_brand.fit_transform(features_df['brand'].astype(str))
    if 'os' in features_df.columns:
        features_df['os_encoded'] = le_os.fit_transform(features_df['os'].astype(str))
    
    # Create derived features
    if 'ram' in features_df.columns and 'storage' in features_df.columns:
        features_df['ram_storage_ratio'] = features_df['ram'] / features_df['storage']
    
    if 'screen_size' in features_df.columns and 'price' in features_df.columns:
        features_df['price_per_inch'] = features_df['price'] / features_df['screen_size']
    
    return features_df, le_brand, le_os

def train_price_prediction_model(df: pd.DataFrame) -> dict:
    """
    Train a Random Forest model to predict device prices
    Returns model and metrics
    """
    # Prepare features
    features_df, le_brand, le_os = prepare_features(df)
    
    # Select feature columns
    feature_cols = ['brand_encoded', 'os_encoded', 'screen_size', 'ram', 'storage', 
                    'ram_storage_ratio', 'price_per_inch']
    feature_cols = [col for col in feature_cols if col in features_df.columns]
    
    X = features_df[feature_cols].fillna(0)
    y = features_df['price'].fillna(df['price'].median())
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
    model.fit(X_train_scaled, y_train)
    
    # Predictions
    y_pred = model.predict(X_test_scaled)
    
    # Metrics
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': feature_cols,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    return {
        'model': model,
        'scaler': scaler,
        'label_encoders': {'brand': le_brand, 'os': le_os},
        'metrics': {
            'mse': mse,
            'rmse': rmse,
            'r2_score': r2
        },
        'feature_importance': feature_importance,
        'feature_columns': feature_cols
    }

def train_category_classification_model(df: pd.DataFrame) -> dict:
    """
    Train a classification model to categorize devices
    Returns model and metrics
    """
    # Prepare features
    features_df, le_brand, le_os = prepare_features(df)
    
    # Create target category (e.g., based on price)
    if 'price_category' not in features_df.columns:
        features_df['price_category'] = pd.cut(
            features_df['price'],
            bins=[0, 500, 1000, float('inf')],
            labels=['Budget', 'Mid-range', 'Premium']
        )
    
    # Select features
    feature_cols = ['brand_encoded', 'os_encoded', 'screen_size', 'ram', 'storage']
    feature_cols = [col for col in feature_cols if col in features_df.columns]
    
    X = features_df[feature_cols].fillna(0)
    y = features_df['price_category'].astype(str)
    
    # Encode target
    le_target = LabelEncoder()
    y_encoded = le_target.fit_transform(y)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
    model.fit(X_train_scaled, y_train)
    
    # Predictions
    y_pred = model.predict(X_test_scaled)
    
    # Metrics
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=le_target.classes_)
    
    return {
        'model': model,
        'scaler': scaler,
        'label_encoders': {'brand': le_brand, 'os': le_os, 'target': le_target},
        'metrics': {
            'accuracy': accuracy,
            'classification_report': report
        },
        'feature_columns': feature_cols
    }

def save_model(model_dict: dict, filepath: str):
    """Save trained model and preprocessors"""
    joblib.dump(model_dict, filepath)
    print(f"SUCCESS: Model saved to {filepath}")

def load_model(filepath: str) -> dict:
    """Load trained model and preprocessors"""
    return joblib.load(filepath)
