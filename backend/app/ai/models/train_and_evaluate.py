"""
Training and Evaluation Engine for Agricultural Price Forecasting.
Trains Linear Regression, Random Forest, and PyTorch LSTM.
Computes R², MAE, RMSE, MAPE on unseen test data and generates research paper comparison tables.
"""

import os
import time
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
import joblib

from prepare_dataset import load_and_clean_data, engineer_features, PROCESSED_DATA_PATH, OUTPUT_DIR
from model_architectures import get_baseline_model, get_random_forest_model, LSTMPricePredictor

def compute_metrics(y_true, y_pred):
    """Compute standard regression & forecasting metrics"""
    r2 = r2_score(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mape = mean_absolute_percentage_error(y_true, y_pred) * 100.0
    return {
        "R2": round(float(r2), 4),
        "MAE": round(float(mae), 2),
        "RMSE": round(float(rmse), 2),
        "MAPE": round(float(mape), 2)
    }

def create_sequences(X, y, seq_length=7):
    """Create sliding time-series windows for LSTM training"""
    xs, ys = [], []
    for i in range(len(X) - seq_length):
        xs.append(X[i:(i + seq_length)])
        ys.append(y[i + seq_length])
    return np.array(xs), np.array(ys)

def run_training_pipeline():
    print("\n" + "=" * 70)
    print("SMART-AGRI AI: MODEL BUILDING & ACCURACY BENCHMARKING ENGINE")
    print("=" * 70)
    
    # 1. Prepare / Load Data
    if os.path.exists(PROCESSED_DATA_PATH):
        print(f"Loading cached preprocessed dataset from: {PROCESSED_DATA_PATH}")
        df = pd.read_csv(PROCESSED_DATA_PATH)
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
    else:
        raw_df = load_and_clean_data()
        df, feature_cols, target_col = engineer_features(raw_df)
        
    print(f"Dataset Loaded: {len(df):,} total Maharashtra records")
    
    # 2. Time-Series Train/Test Split (Strict Chronological Split - Zero Data Leakage)
    print("\nPerforming Chronological Split for True Out-of-Sample Forecasting:")
    train_mask = df["year"] <= 2021
    val_mask = df["year"].isin([2022, 2023])
    test_mask = df["year"] >= 2024
    
    df_train = df[train_mask]
    df_val = df[val_mask]
    df_test = df[test_mask]
    
    print(f"  • Training Set   (2001 - 2021): {len(df_train):,} records ({len(df_train)/len(df)*100:.1f}%)")
    print(f"  • Validation Set (2022 - 2023): {len(df_val):,} records ({len(df_val)/len(df)*100:.1f}%)")
    print(f"  • Test Set       (2024 Unseen): {len(df_test):,} records ({len(df_test)/len(df)*100:.1f}%)")
    
    X_train, y_train = df_train[feature_cols].values, df_train[target_col].values
    X_val, y_val = df_val[feature_cols].values, df_val[target_col].values
    X_test, y_test = df_test[feature_cols].values, df_test[target_col].values
    
    # Feature Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)
    
    joblib.dump(scaler, os.path.join(OUTPUT_DIR, "feature_scaler.pkl"))
    print("Saved feature scaler to saved/feature_scaler.pkl")
    
    results = {}
    
    # -------------------------------------------------------------
    # MODEL 1: Linear Regression (Baseline)
    # -------------------------------------------------------------
    print("\n" + "-" * 50)
    print("1. TRAINING BASELINE MODEL: Linear Regression")
    print("-" * 50)
    t0 = time.time()
    lr_model = get_baseline_model()
    lr_model.fit(X_train_scaled, y_train)
    lr_train_time = time.time() - t0
    
    lr_preds = lr_model.predict(X_test_scaled)
    lr_metrics = compute_metrics(y_test, lr_preds)
    results["Linear Regression (Baseline)"] = {**lr_metrics, "Training Time (s)": round(lr_train_time, 2)}
    print(f"Linear Regression Completed in {lr_train_time:.2f}s")
    print(f"  -> R² Score: {lr_metrics['R2']} | MAE: ₹{lr_metrics['MAE']}/Qtl | MAPE: {lr_metrics['MAPE']}%")
    
    # -------------------------------------------------------------
    # -------------------------------------------------------------
    # MODEL 2: Random Forest Regressor (ML)
    # -------------------------------------------------------------
    print("\n" + "-" * 50)
    print("2. TRAINING ML MODEL: Random Forest Regressor (100 Trees)")
    print("-" * 50)
    t0 = time.time()
    rf_model = get_random_forest_model()
    rf_model.fit(X_train, y_train)
    rf_train_time = time.time() - t0
    
    print("Evaluating Random Forest across TRAIN, VALIDATION (2022-2023), and TEST (2024 Unseen)...")
    # Evaluate on Train (representative 50,000 subset for fast computation)
    train_sample_n = min(50000, len(X_train))
    rf_train_preds = rf_model.predict(X_train[:train_sample_n])
    rf_train_metrics = compute_metrics(y_train[:train_sample_n], rf_train_preds)
    
    # Evaluate on Validation
    rf_val_preds = rf_model.predict(X_val)
    rf_val_metrics = compute_metrics(y_val, rf_val_preds)
    
    # Evaluate on Test
    rf_test_preds = rf_model.predict(X_test)
    rf_test_metrics = compute_metrics(y_test, rf_test_preds)
    
    results["Random Forest (Train Sample)"] = {**rf_train_metrics, "Training Time (s)": round(rf_train_time, 2)}
    results["Random Forest (Validation 22-23)"] = {**rf_val_metrics, "Training Time (s)": round(rf_train_time, 2)}
    results["Random Forest Regressor (Test 2024)"] = {**rf_test_metrics, "Training Time (s)": round(rf_train_time, 2)}
    
    joblib.dump(rf_model, os.path.join(OUTPUT_DIR, "random_forest_model.pkl"))
    print(f"Random Forest Training Completed in {rf_train_time:.2f}s")
    print(f"  • TRAIN R²:      {rf_train_metrics['R2']} | MAE: ₹{rf_train_metrics['MAE']}/Qtl | RMSE: {rf_train_metrics['RMSE']} | MAPE: {rf_train_metrics['MAPE']}%")
    print(f"  • VALIDATION R²: {rf_val_metrics['R2']} | MAE: ₹{rf_val_metrics['MAE']}/Qtl | RMSE: {rf_val_metrics['RMSE']} | MAPE: {rf_val_metrics['MAPE']}%")
    print(f"  • TEST (2024) R²:{rf_test_metrics['R2']} | MAE: ₹{rf_test_metrics['MAE']}/Qtl | RMSE: {rf_test_metrics['RMSE']} | MAPE: {rf_test_metrics['MAPE']}%")
    print("Saved Random Forest model to saved/random_forest_model.pkl")
    
    # Gaps
    train_val_gap = round(rf_train_metrics['R2'] - rf_val_metrics['R2'], 4)
    train_test_gap = round(rf_train_metrics['R2'] - rf_test_metrics['R2'], 4)
    val_test_diff = round(rf_val_metrics['R2'] - rf_test_metrics['R2'], 4)
    print(f"\nGeneralization Analysis:")
    print(f"  • Train - Validation R² Gap: {train_val_gap:+.4f}")
    print(f"  • Train - Test R² Gap:       {train_test_gap:+.4f}")
    print(f"  • Validation - Test Diff:    {val_test_diff:+.4f}")
    
    # Feature Importance (Top 15)
    importances = pd.Series(rf_model.feature_importances_, index=feature_cols).sort_values(ascending=False)
    print("\nTop 15 Most Influential Features (Random Forest):")
    for i, (feat, imp) in enumerate(importances.head(15).items(), 1):
        print(f"  {i:2d}. {feat:<20}: {imp*100:.2f}%")
        
    # Old vs Corrected Comparison Table
    print("\n" + "=" * 80)
    print("OLD MODEL (WITH LEAKAGE) vs CORRECTED MODEL (STRICT TIME SERIES)")
    print("=" * 80)
    comparison_table = pd.DataFrame([
        {
            "Split": "TRAIN",
            "Old R²": 0.9870,
            "New R²": rf_train_metrics["R2"],
            "Old MAE": 74.87,
            "New MAE": rf_train_metrics["MAE"],
            "Old RMSE": 148.03,
            "New RMSE": rf_train_metrics["RMSE"],
            "Old MAPE": "5.34%",
            "New MAPE": f"{rf_train_metrics['MAPE']}%"
        },
        {
            "Split": "VALIDATION (2022-2023)",
            "Old R²": 0.9240,
            "New R²": rf_val_metrics["R2"],
            "Old MAE": 246.25,
            "New MAE": rf_val_metrics["MAE"],
            "Old RMSE": 583.19,
            "New RMSE": rf_val_metrics["RMSE"],
            "Old MAPE": "8.32%",
            "New MAPE": f"{rf_val_metrics['MAPE']}%"
        },
        {
            "Split": "TEST (2024 Unseen)",
            "Old R²": 0.9687,
            "New R²": rf_test_metrics["R2"],
            "Old MAE": 185.39,
            "New MAE": rf_test_metrics["MAE"],
            "Old RMSE": 300.69,
            "New RMSE": rf_test_metrics["RMSE"],
            "Old MAPE": "7.43%",
            "New MAPE": f"{rf_test_metrics['MAPE']}%"
        }
    ])
    print(comparison_table.to_string(index=False))
    print("=" * 80)
    
    rf_preds = rf_test_preds
        
    # -------------------------------------------------------------
    # MODEL 3: PyTorch LSTM Neural Network (DL)
    # -------------------------------------------------------------
    print("\n" + "-" * 50)
    print("3. TRAINING DEEP LEARNING MODEL: PyTorch 2-Layer LSTM")
    print("-" * 50)
    
    # Device selection (Apple Silicon MPS or CPU)
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    print(f"Using Compute Device: {device}")
    
    # Sequence windows for LSTM
    seq_len = 7
    print(f"Creating time-series sequences (Lookback window = {seq_len} time steps)...")
    
    X_train_seq, y_train_seq = create_sequences(X_train_scaled, y_train, seq_length=seq_len)
    X_test_seq, y_test_seq = create_sequences(X_test_scaled, y_test, seq_length=seq_len)
    
    train_dataset = TensorDataset(torch.tensor(X_train_seq, dtype=torch.float32), torch.tensor(y_train_seq, dtype=torch.float32))
    train_loader = DataLoader(train_dataset, batch_size=256, shuffle=False)
    
    input_dim = len(feature_cols)
    lstm_model = LSTMPricePredictor(input_dim=input_dim).to(device)
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(lstm_model.parameters(), lr=0.005)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=2)
    
    t0 = time.time()
    epochs = 15
    lstm_model.train()
    for epoch in range(1, epochs + 1):
        epoch_loss = 0.0
        for batch_x, batch_y in train_loader:
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)
            optimizer.zero_grad()
            preds = lstm_model(batch_x)
            loss = criterion(preds, batch_y)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item() * len(batch_x)
            
        epoch_loss /= len(train_dataset)
        rmse_loss = np.sqrt(epoch_loss)
        scheduler.step(rmse_loss)
        if epoch % 3 == 0 or epoch == epochs:
            print(f"  Epoch [{epoch:02d}/{epochs:02d}] -> Training RMSE: ₹{rmse_loss:.2f}")
            
    lstm_train_time = time.time() - t0
    
    # LSTM Evaluation
    lstm_model.eval()
    with torch.no_grad():
        test_x_tensor = torch.tensor(X_test_seq, dtype=torch.float32).to(device)
        lstm_preds = lstm_model(test_x_tensor).cpu().numpy()
        
    lstm_metrics = compute_metrics(y_test_seq, lstm_preds)
    results["PyTorch LSTM (Deep Learning)"] = {**lstm_metrics, "Training Time (s)": round(lstm_train_time, 2)}
    
    torch.save(lstm_model.state_dict(), os.path.join(OUTPUT_DIR, "lstm_model.pth"))
    print(f"LSTM Training Completed in {lstm_train_time:.2f}s")
    print(f"  -> R² Score: {lstm_metrics['R2']} | MAE: ₹{lstm_metrics['MAE']}/Qtl | MAPE: {lstm_metrics['MAPE']}%")
    print("Saved LSTM model weights to saved/lstm_model.pth")
    
    # -------------------------------------------------------------
    # 4. FINAL ACCURACY COMPARISON TABLE FOR RESEARCH PAPER & VIVA
    # -------------------------------------------------------------
    print("\n" + "=" * 70)
    print("FINAL ACCURACY COMPARISON TABLE (FOR RESEARCH PAPER & VIVA)")
    print("=" * 70)
    
    results_df = pd.DataFrame(results).T
    print(results_df.to_string())
    
    # Per-Crop Performance Breakdown for Key Commodities
    print("\n" + "=" * 70)
    print("CROP-WISE ACCURACY BREAKDOWN (RANDOM FOREST REGRESSOR)")
    print("=" * 70)
    
    df_test_eval = df_test.copy()
    df_test_eval["pred_modal_price"] = rf_preds
    
    crop_breakdown = []
    for crop_name in df_test_eval["Commodity"].unique():
        sub = df_test_eval[df_test_eval["Commodity"] == crop_name]
        if len(sub) > 10:
            c_metrics = compute_metrics(sub["modal_price"].values, sub["pred_modal_price"].values)
            crop_breakdown.append({
                "Crop": crop_name,
                "Test Records": len(sub),
                "Mean Price": f"₹{sub['modal_price'].mean():.1f}",
                "R² Score": c_metrics["R2"],
                "MAE (₹/Qtl)": f"₹{c_metrics['MAE']}",
                "MAPE (%)": f"{c_metrics['MAPE']}%"
            })
            
    crop_df = pd.DataFrame(crop_breakdown).sort_values(by="R² Score", ascending=False)
    print(crop_df.to_string(index=False))
    
    print("\n" + "=" * 70)
    print("ALL MODELS BUILT, TRAINED, EVALUATED, AND SAVED SUCCESSFULLY!")
    print("=" * 70)
    
    return results_df, crop_df

if __name__ == "__main__":
    run_training_pipeline()
