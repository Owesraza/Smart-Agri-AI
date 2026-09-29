"""
Model Stability and Consistency Evaluation via 5-Fold Walk-Forward Time-Series Validation.
Smart Agri AI - Agricultural Price Forecasting System.

IMPORTANT: This is a standalone experiment script.
It does NOT modify or overwrite the production model artifacts.
"""

import os
import sys
import time
import json
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error, mean_absolute_percentage_error

# Set up paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
sys.path.insert(0, os.path.join(BASE_DIR, "backend"))
DATASET_PATH = os.path.join(os.path.dirname(__file__), "saved/maharashtra_engineered_dataset.csv")

FEATURE_COLS = [
    "Commodity_encoded", "district_encoded", "market_encoded",
    "year", "month", "day", "day_of_week", "day_of_year", "quarter",
    "is_kharif", "is_rabi", "is_zaid",
    "log_arrivals", "price_spread",
    "lag_price_1", "lag_price_3", "lag_price_7", "lag_price_14", "lag_price_30",
    "rolling_mean_7", "rolling_std_7", "rolling_mean_30",
    "ema_7", "ema_14", "ema_30"
]
TARGET_COL = "modal_price"

def compute_metrics(y_true, y_pred):
    r2 = float(r2_score(y_true, y_pred))
    mae = float(mean_absolute_error(y_true, y_pred))
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    mape = float(mean_absolute_percentage_error(y_true, y_pred) * 100.0)
    return {
        "R2": round(r2, 4),
        "MAE": round(mae, 2),
        "RMSE": round(rmse, 2),
        "MAPE": round(mape, 2)
    }

def run_stability_evaluation():
    print("=" * 80)
    print("SMART AGRI AI — 5-FOLD CHRONOLOGICAL WALK-FORWARD MODEL STABILITY EVALUATION")
    print("=" * 80)
    
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATASET_PATH}")
        
    print(f"Loading dataset from: {DATASET_PATH}")
    df = pd.read_csv(DATASET_PATH)
    print(f"Dataset Loaded: {len(df):,} records | Date range: {df['date'].min()} to {df['date'].max()}\n")
    
    # Define 5 chronological expanding-window walk-forward folds
    folds = [
        {
            "fold": 1,
            "train_years": (2001, 2010),
            "val_years": (2011, 2013),
            "name": "Fold 1 (Train: 2001-2010 | Val: 2011-2013)"
        },
        {
            "fold": 2,
            "train_years": (2001, 2013),
            "val_years": (2014, 2016),
            "name": "Fold 2 (Train: 2001-2013 | Val: 2014-2016)"
        },
        {
            "fold": 3,
            "train_years": (2001, 2016),
            "val_years": (2017, 2018),
            "name": "Fold 3 (Train: 2001-2016 | Val: 2017-2018)"
        },
        {
            "fold": 4,
            "train_years": (2001, 2018),
            "val_years": (2019, 2021),
            "name": "Fold 4 (Train: 2001-2018 | Val: 2019-2021)"
        },
        {
            "fold": 5,
            "train_years": (2001, 2021),
            "val_years": (2022, 2024),
            "name": "Fold 5 (Train: 2001-2021 | Val: 2022-2024)"
        }
    ]
    
    major_commodities = ["Onion", "Wheat", "Tomato", "Cotton", "Soyabean", "Maize", "Potato", "Rice"]
    
    fold_results = []
    commodity_results = {c: [] for c in major_commodities}
    
    total_start_time = time.time()
    
    for f in folds:
        fold_num = f["fold"]
        tr_start, tr_end = f["train_years"]
        vl_start, vl_end = f["val_years"]
        
        print("-" * 80)
        print(f"RUNNING {f['name']}")
        print("-" * 80)
        
        train_mask = (df["year"] >= tr_start) & (df["year"] <= tr_end)
        val_mask = (df["year"] >= vl_start) & (df["year"] <= vl_end)
        
        df_train = df[train_mask]
        df_val = df[val_mask]
        
        train_count = len(df_train)
        val_count = len(df_val)
        train_dates = f"{df_train['date'].min()} to {df_train['date'].max()}"
        val_dates = f"{df_val['date'].min()} to {df_val['date'].max()}"
        
        print(f"  • Training:   {tr_start}–{tr_end} ({train_count:,} records) | Dates: {train_dates}")
        print(f"  • Validation: {vl_start}–{vl_end} ({val_count:,} records) | Dates: {val_dates}")
        
        X_train, y_train = df_train[FEATURE_COLS].values, df_train[TARGET_COL].values
        X_val, y_val = df_val[FEATURE_COLS].values, df_val[TARGET_COL].values
        
        t0 = time.time()
        rf = RandomForestRegressor(
            n_estimators=100,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            max_features=1.0,
            random_state=42,
            n_jobs=-1,
            verbose=0
        )
        rf.fit(X_train, y_train)
        train_duration = time.time() - t0
        
        val_preds = rf.predict(X_val)
        metrics = compute_metrics(y_val, val_preds)
        
        fold_record = {
            "fold": fold_num,
            "train_period": f"{tr_start}–{tr_end}",
            "train_dates": train_dates,
            "train_records": train_count,
            "val_period": f"{vl_start}–{vl_end}",
            "val_dates": val_dates,
            "val_records": val_count,
            "R2": metrics["R2"],
            "MAE": metrics["MAE"],
            "RMSE": metrics["RMSE"],
            "MAPE": metrics["MAPE"],
            "train_time_sec": round(train_duration, 2)
        }
        fold_results.append(fold_record)
        
        print(f"  ➜ Results: R² = {metrics['R2']} | MAE = ₹{metrics['MAE']}/Qtl | RMSE = {metrics['RMSE']} | MAPE = {metrics['MAPE']}% | Fit time: {train_duration:.1f}s")
        
        # Commodity-level evaluation on this fold
        df_val_eval = df_val.copy()
        df_val_eval["pred"] = val_preds
        
        for c in major_commodities:
            c_sub = df_val_eval[df_val_eval["Commodity"] == c]
            if len(c_sub) > 0:
                c_metrics = compute_metrics(c_sub[TARGET_COL].values, c_sub["pred"].values)
                commodity_results[c].append({
                    "fold": fold_num,
                    "records": len(c_sub),
                    "mean_price": round(float(c_sub[TARGET_COL].mean()), 2),
                    "R2": c_metrics["R2"],
                    "MAE": c_metrics["MAE"],
                    "RMSE": c_metrics["RMSE"],
                    "MAPE": c_metrics["MAPE"]
                })
            else:
                commodity_results[c].append({
                    "fold": fold_num,
                    "records": 0,
                    "mean_price": None,
                    "R2": None,
                    "MAE": None,
                    "RMSE": None,
                    "MAPE": None
                })
                
    total_duration = time.time() - total_start_time
    print("\n" + "=" * 80)
    print(f"ALL 5 FOLDS COMPLETED IN {total_duration:.1f}s ({total_duration/60:.2f} min)")
    print("=" * 80)
    
    # -------------------------------------------------------------
    # STEP 4: STATISTICAL VARIATION & SUMMARY TABLES
    # -------------------------------------------------------------
    results_df = pd.DataFrame(fold_results)
    
    metrics_list = ["R2", "MAE", "RMSE", "MAPE"]
    stats_summary = []
    
    for m in metrics_list:
        vals = results_df[m].values
        m_mean = float(np.mean(vals))
        m_std = float(np.std(vals, ddof=1))
        m_min = float(np.min(vals))
        m_max = float(np.max(vals))
        m_range = float(m_max - m_min)
        m_cv = float((m_std / m_mean) * 100.0) if m_mean != 0 else 0.0
        
        stats_summary.append({
            "Metric": m,
            "Mean": round(m_mean, 4),
            "Std Dev": round(m_std, 4),
            "Min": round(m_min, 4),
            "Max": round(m_max, 4),
            "Range": round(m_range, 4),
            "CV (%)": round(m_cv, 2)
        })
        
    stats_df = pd.DataFrame(stats_summary)
    
    print("\n================================================================================")
    print("TABLE 1: 5-FOLD WALK-FORWARD TIME-SERIES CROSS-VALIDATION RESULTS")
    print("================================================================================")
    disp_cols = ["fold", "train_period", "val_period", "train_records", "val_records", "R2", "MAE", "RMSE", "MAPE"]
    print(results_df[disp_cols].to_string(index=False))
    
    print("\n================================================================================")
    print("TABLE 2: METRIC VARIATION & STABILITY SUMMARY (MEAN, STD, MIN, MAX, RANGE, CV)")
    print("================================================================================")
    print(stats_df.to_string(index=False))
    
    # -------------------------------------------------------------
    # COMMODITY STABILITY SUMMARY
    # -------------------------------------------------------------
    print("\n================================================================================")
    print("TABLE 3: MAJOR COMMODITIES STABILITY BREAKDOWN ACROSS FOLDS")
    print("================================================================================")
    comm_summary_list = []
    for c in major_commodities:
        c_folds = commodity_results[c]
        r2s = [f["R2"] for f in c_folds if f["R2"] is not None]
        maes = [f["MAE"] for f in c_folds if f["MAE"] is not None]
        mapes = [f["MAPE"] for f in c_folds if f["MAPE"] is not None]
        
        if r2s:
            comm_summary_list.append({
                "Commodity": c,
                "Folds Evaluated": len(r2s),
                "Mean R²": round(float(np.mean(r2s)), 4),
                "Std R²": round(float(np.std(r2s, ddof=1)), 4) if len(r2s) > 1 else 0.0,
                "R² Range": f"{min(r2s):.2f} to {max(r2s):.2f}",
                "Mean MAE (₹)": round(float(np.mean(maes)), 2),
                "Mean MAPE (%)": f"{np.mean(mapes):.2f}%",
                "MAPE Range": f"{min(mapes):.2f}% to {max(mapes):.2f}%"
            })
            
    comm_summary_df = pd.DataFrame(comm_summary_list)
    print(comm_summary_df.to_string(index=False))
    
    # Save output to JSON artifact for reporting
    output_payload = {
        "fold_results": fold_results,
        "stats_summary": stats_summary,
        "commodity_results": commodity_results,
        "commodity_summary": comm_summary_list
    }
    
    out_json_path = os.path.join(os.path.dirname(__file__), "saved/stability_evaluation_results.json")
    with open(out_json_path, "w") as f:
        json.dump(output_payload, f, indent=2)
    print(f"\nSaved raw stability experiment results to: {out_json_path}")
    
    return results_df, stats_df, comm_summary_df

if __name__ == "__main__":
    run_stability_evaluation()
