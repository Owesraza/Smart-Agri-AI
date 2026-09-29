"""
Data Preparation & Feature Engineering Pipeline for Maharashtra Mandi Prices (2001 - 2024)
Extracts 1.35M Maharashtra records, cleans outliers, and engineers temporal, lag, and statistical features.
"""

import os
import glob
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import joblib

# Dynamically locate Dataset of 20-24 directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
DATASET_DIR = os.path.join(BASE_DIR, "Dataset of 20-24")
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "saved"))
PROCESSED_DATA_PATH = os.path.join(OUTPUT_DIR, "maharashtra_engineered_dataset.csv")

TARGET_CROPS = [
    "Onion.csv",
    "Wheat.csv",
    "Tomato.csv",
    "Cotton.csv",
    "Soyabean.csv",
    "Potato.csv",
    "Rice.csv",
    "Maize.csv"
]

def load_and_clean_data():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    all_frames = []
    
    print("=" * 60)
    print(f"STEP 1: Extracting Maharashtra APMC Mandi Data from: {DATASET_DIR}")
    print("=" * 60)
    
    for crop_file in TARGET_CROPS:
        crop_path = os.path.join(DATASET_DIR, crop_file)
        if not os.path.exists(crop_path):
            print(f"Warning: {crop_file} not found in {DATASET_DIR}, skipping...")
            continue
        
        crop_name = crop_file.replace(".csv", "")
        print(f"Reading {crop_name}...")
        df = pd.read_csv(crop_path)
        
        # Filter for Maharashtra only
        df = df[df["State Name"].astype(str).str.strip().str.lower() == "maharashtra"].copy()
        df["Commodity"] = crop_name
        
        # Standardize column names
        df = df.rename(columns={
            "State Name": "state",
            "District Name": "district",
            "Market Name": "market",
            "Variety": "variety",
            "Group": "group",
            "Arrivals (Tonnes)": "arrivals_tonnes",
            "Min Price (Rs./Quintal)": "min_price",
            "Max Price (Rs./Quintal)": "max_price",
            "Modal Price (Rs./Quintal)": "modal_price",
            "Reported Date": "reported_date"
        })
        
        all_frames.append(df)
        print(f"  -> Extracted {len(df):,} records for {crop_name}")

    combined_df = pd.concat(all_frames, ignore_index=True)
    print(f"\nTotal raw Maharashtra records: {len(combined_df):,}")
    
    # Cleaning
    print("\nSTEP 2: Cleaning Data & Removing Invalid Outliers...")
    combined_df["date"] = pd.to_datetime(combined_df["reported_date"], format="mixed", errors="coerce")
    combined_df = combined_df.dropna(subset=["date", "modal_price"])
    
    # Filter valid non-zero prices (eliminate reporting errors like Rs 0 or Rs 9999999)
    combined_df = combined_df[
        (combined_df["modal_price"] >= 100) & 
        (combined_df["modal_price"] <= 35000)
    ]
    
    # Fill arrival quantities
    combined_df["arrivals_tonnes"] = combined_df["arrivals_tonnes"].fillna(0.0)
    combined_df["min_price"] = combined_df["min_price"].fillna(combined_df["modal_price"] * 0.9)
    combined_df["max_price"] = combined_df["max_price"].fillna(combined_df["modal_price"] * 1.1)
    
    # Sort chronologically per commodity & market for accurate time-series lag calculation
    combined_df = combined_df.sort_values(by=["Commodity", "district", "market", "date"]).reset_index(drop=True)
    print(f"Valid clean records after filtering: {len(combined_df):,}")
    
    return combined_df

def engineer_features(df):
    print("\nSTEP 3: Engineering Temporal, Momentum, Lag & Supply Features...")
    
    # 1. Calendar / Temporal Features
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    df["day_of_week"] = df["date"].dt.dayofweek
    df["day_of_year"] = df["date"].dt.dayofyear
    df["quarter"] = df["date"].dt.quarter
    
    # Crop Seasonality in Maharashtra (Kharif: Jun-Oct, Rabi: Nov-Mar, Zaid: Apr-May)
    df["is_kharif"] = df["month"].isin([6, 7, 8, 9, 10]).astype(int)
    df["is_rabi"] = df["month"].isin([11, 12, 1, 2, 3]).astype(int)
    df["is_zaid"] = df["month"].isin([4, 5]).astype(int)
    
    # 2. Price Spread & Volatility
    df["price_spread"] = (df["max_price"] - df["min_price"]).clip(lower=0)
    df["log_arrivals"] = np.log1p(df["arrivals_tonnes"].clip(lower=0))
    
    # 3. Time-Series Lag & Momentum Features (Grouped strictly by Commodity, District & Market)
    print("Calculating historical lag features (t-1, t-3, t-7, t-14, t-30) per (Commodity, District, Market)...")
    # Ensure strict chronological sorting within each independent time-series
    df = df.sort_values(by=["Commodity", "district", "market", "date"]).reset_index(drop=True)
    grouped = df.groupby(["Commodity", "district", "market"])
    
    df["lag_price_1"] = grouped["modal_price"].shift(1)
    df["lag_price_3"] = grouped["modal_price"].shift(3)
    df["lag_price_7"] = grouped["modal_price"].shift(7)
    df["lag_price_14"] = grouped["modal_price"].shift(14)
    df["lag_price_30"] = grouped["modal_price"].shift(30)
    
    # Rolling Statistics (strictly historical lookbacks shifted by 1)
    df["rolling_mean_7"] = grouped["modal_price"].transform(lambda x: x.shift(1).rolling(7, min_periods=1).mean())
    df["rolling_std_7"] = grouped["modal_price"].transform(lambda x: x.shift(1).rolling(7, min_periods=1).std()).fillna(0.0)
    df["rolling_mean_30"] = grouped["modal_price"].transform(lambda x: x.shift(1).rolling(30, min_periods=1).mean())
    
    # Exponential Moving Averages (EMA 7, 14, 30 strictly historical shifted by 1)
    df["ema_7"] = grouped["modal_price"].transform(lambda x: x.shift(1).ewm(span=7, adjust=False).mean())
    df["ema_14"] = grouped["modal_price"].transform(lambda x: x.shift(1).ewm(span=14, adjust=False).mean())
    df["ema_30"] = grouped["modal_price"].transform(lambda x: x.shift(1).ewm(span=30, adjust=False).mean())
    
    # LEAKAGE-FREE MISSING VALUE HANDLING:
    # NEVER fill lag or rolling features with the current target (modal_price).
    # Drop rows that lack the required 30-day historical context.
    initial_rows = len(df)
    df = df.dropna(subset=["lag_price_30"]).reset_index(drop=True)
    dropped_rows = initial_rows - len(df)
    print(f"Removed {dropped_rows:,} initial time-series records lacking 30-day historical context ({dropped_rows/initial_rows*100:.2f}% of data).")
    print(f"Clean records remaining: {len(df):,}")
    
    # 4. Categorical Encoders
    print("Encoding categorical identifiers (Commodity, District, Market)...")
    encoders = {}
    for col in ["Commodity", "district", "market"]:
        le = LabelEncoder()
        df[f"{col}_encoded"] = le.fit_transform(df[col].astype(str))
        encoders[col] = le
        
    joblib.dump(encoders, os.path.join(OUTPUT_DIR, "label_encoders.pkl"))
    print("Saved label encoders to saved/label_encoders.pkl")
    
    # Final feature set selection
    feature_cols = [
        "Commodity_encoded", "district_encoded", "market_encoded",
        "year", "month", "day", "day_of_week", "day_of_year", "quarter",
        "is_kharif", "is_rabi", "is_zaid",
        "log_arrivals", "price_spread",
        "lag_price_1", "lag_price_3", "lag_price_7", "lag_price_14", "lag_price_30",
        "rolling_mean_7", "rolling_std_7", "rolling_mean_30",
        "ema_7", "ema_14", "ema_30"
    ]
    
    target_col = "modal_price"
    
    print("\n" + "=" * 70)
    print("PHASE 6: ENGINEERED DATASET COMPREHENSIVE AUDIT & SUMMARY")
    print("=" * 70)
    print(f"Total Rows: {len(df):,}")
    print(f"Total Features: {len(feature_cols)}")
    print(f"Feature Columns: {feature_cols}")
    print(f"Target Column: {target_col}")
    print(f"Date Range: {df['date'].min().date()} to {df['date'].max().date()}")
    print(f"Crop Count: {df['Commodity'].nunique()} -> {sorted(df['Commodity'].unique().tolist())}")
    print(f"District Count: {df['district'].nunique()}")
    print(f"Market Count: {df['market'].nunique()}")
    print(f"Missing Values in Features: {df[feature_cols].isna().sum().sum()}")
    print(f"Duplicate Rows (all columns): {df.duplicated().sum()}")
    dup_time_series = df.duplicated(subset=['Commodity', 'district', 'market', 'date']).sum()
    print(f"Duplicate Commodity + district + market + date rows: {dup_time_series:,}")
    
    train_count = (df['year'] <= 2021).sum()
    val_count = df['year'].isin([2022, 2023]).sum()
    test_count = (df['year'] >= 2024).sum()
    print(f"Train Rows      (2001 - 2021): {train_count:,} ({train_count/len(df)*100:.2f}%)")
    print(f"Validation Rows (2022 - 2023): {val_count:,} ({val_count/len(df)*100:.2f}%)")
    print(f"Test Rows       (2024 Unseen): {test_count:,} ({test_count/len(df)*100:.2f}%)")
    print("=" * 70)
    
    # Save clean preprocessed dataset
    df.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"Saved corrected engineered dataset to: {PROCESSED_DATA_PATH}")
    
    return df, feature_cols, target_col

if __name__ == "__main__":
    df = load_and_clean_data()
    engineered_df, features, target = engineer_features(df)
    print("\nData Preparation Complete! Ready for Model Building & Training.")
