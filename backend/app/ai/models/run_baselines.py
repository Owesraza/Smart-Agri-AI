"""
DAY 1 TASK: Baseline Model Comparison
Runs XGBoost and ARIMA on the same 5-fold walk-forward splits.
Compares against existing Random Forest results.
Runs Wilcoxon significance tests.
Saves results to baseline_comparison_results.json
"""

import pandas as pd
import numpy as np
import json
import time
import warnings
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler
from scipy.stats import wilcoxon

warnings.filterwarnings('ignore')

print("=" * 70)
print("BASELINE MODEL COMPARISON — Smart Agri AI")
print("=" * 70)

# ─── Load Dataset ───────────────────────────────────────────────────────────
CSV_PATH = "/Users/owaisrazaansaralibhati/Desktop/Smart Agri AI/backend/app/ai/models/saved/maharashtra_engineered_dataset.csv"
SAVE_DIR = "/Users/owaisrazaansaralibhati/Desktop/Smart Agri AI/backend/app/ai/models/saved"

print("\n[1/5] Loading dataset...")
df = pd.read_csv(CSV_PATH, parse_dates=['date'])
df = df.dropna(subset=['modal_price'])
df = df.sort_values('date').reset_index(drop=True)
print(f"  Loaded {len(df):,} records | {df['date'].min().date()} to {df['date'].max().date()}")

# ─── Feature Columns (same as production RF) ────────────────────────────────
FEATURE_COLS = [
    'year', 'month', 'day', 'day_of_week', 'day_of_year', 'quarter',
    'is_kharif', 'is_rabi', 'is_zaid',
    'price_spread', 'log_arrivals',
    'lag_price_1', 'lag_price_3', 'lag_price_7', 'lag_price_14', 'lag_price_30',
    'rolling_mean_7', 'rolling_std_7', 'rolling_mean_30',
    'ema_7', 'ema_14', 'ema_30',
    'Commodity_encoded', 'district_encoded', 'market_encoded'
]
TARGET = 'modal_price'

# Keep only available feature cols
available = [c for c in FEATURE_COLS if c in df.columns]
print(f"  Features available: {len(available)}")

# ─── Walk-Forward Fold Definitions (same as RF experiment) ──────────────────
FOLDS = [
    (None,  2010, 2011, 2013),
    (None,  2013, 2014, 2016),
    (None,  2016, 2017, 2018),
    (None,  2018, 2019, 2021),
    (None,  2021, 2022, 2024),
]

def mape(y_true, y_pred):
    mask = y_true != 0
    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100

def get_fold_data(df, train_end_year, val_start_year, val_end_year):
    train = df[df['date'].dt.year <= train_end_year].dropna(subset=available + [TARGET])
    val   = df[(df['date'].dt.year >= val_start_year) & (df['date'].dt.year <= val_end_year)].dropna(subset=available + [TARGET])
    return train, val

# ─── EXISTING RF RESULTS ────────────────────────────────────────────────────
rf_r2   = [0.9354, 0.9527, 0.9660, 0.9408, 0.9495]
rf_mae  = [145.84, 126.85, 111.22, 184.17, 211.68]
rf_rmse = [304.86, 269.78, 239.50, 395.13, 470.56]
rf_mape = [8.33,   7.90,   6.92,   8.16,   7.90  ]

print("\n[2/5] Running XGBoost baseline (5-fold walk-forward)...")
try:
    from xgboost import XGBRegressor
    xgb_r2, xgb_mae, xgb_rmse, xgb_mape = [], [], [], []
    for i, (_, train_end, val_start, val_end) in enumerate(FOLDS):
        t0 = time.time()
        train, val = get_fold_data(df, train_end, val_start, val_end)
        X_train, y_train = train[available].values, train[TARGET].values
        X_val,   y_val   = val[available].values,   val[TARGET].values

        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_val   = scaler.transform(X_val)

        model = XGBRegressor(
            n_estimators=300, max_depth=8, learning_rate=0.05,
            subsample=0.8, colsample_bytree=0.8,
            random_state=42, n_jobs=-1, verbosity=0
        )
        model.fit(X_train, y_train)
        pred = model.predict(X_val)

        xgb_r2.append(round(r2_score(y_val, pred), 4))
        xgb_mae.append(round(mean_absolute_error(y_val, pred), 2))
        xgb_rmse.append(round(np.sqrt(mean_squared_error(y_val, pred)), 2))
        xgb_mape.append(round(mape(y_val, pred), 2))
        elapsed = time.time() - t0
        print(f"  Fold {i+1}: R²={xgb_r2[-1]:.4f}  MAE=Rs.{xgb_mae[-1]:.1f}  MAPE={xgb_mape[-1]:.2f}%  [{elapsed:.1f}s]")

    xgb_ok = True
    print(f"  XGBoost Mean R²={np.mean(xgb_r2):.4f}  Mean MAPE={np.mean(xgb_mape):.2f}%")

except ImportError:
    print("  XGBoost not installed — installing...")
    import subprocess
    subprocess.run(["/Users/owaisrazaansaralibhati/Desktop/Smart Agri AI/backend/venv/bin/pip",
                    "install", "xgboost", "-q"], check=True)
    print("  Installed. Please re-run this script.")
    xgb_ok = False
    xgb_r2 = xgb_mae = xgb_rmse = xgb_mape = []

print("\n[3/5] Running ARIMA baseline (per-commodity aggregate monthly series)...")
from statsmodels.tsa.arima.model import ARIMA

arima_r2, arima_mae, arima_rmse, arima_mape = [], [], [], []

fold_configs = [
    (2010, 2011, 2013),
    (2013, 2014, 2016),
    (2016, 2017, 2018),
    (2018, 2019, 2021),
    (2021, 2022, 2024),
]

for fi, (train_end, val_start, val_end) in enumerate(fold_configs):
    fold_true, fold_pred = [], []
    for commodity in df['Commodity'].unique():
        cdf = df[df['Commodity'] == commodity][['date', TARGET]].dropna()
        cdf = cdf.groupby('date')[TARGET].mean().reset_index()
        cdf = cdf.sort_values('date')
        cdf['ym'] = cdf['date'].dt.to_period('M')
        monthly = cdf.groupby('ym')[TARGET].mean()

        train_ser = monthly[monthly.index.year <= train_end]
        val_ser   = monthly[(monthly.index.year >= val_start) & (monthly.index.year <= val_end)]

        if len(train_ser) < 24 or len(val_ser) < 3:
            continue
        try:
            model = ARIMA(train_ser.values, order=(2, 1, 2))
            fit   = model.fit()
            forecast = fit.forecast(steps=len(val_ser))
            fold_true.extend(val_ser.values)
            fold_pred.extend(forecast)
        except Exception:
            continue

    fold_true = np.array(fold_true)
    fold_pred = np.array(fold_pred)
    if len(fold_true) > 0:
        arima_r2.append(round(r2_score(fold_true, fold_pred), 4))
        arima_mae.append(round(mean_absolute_error(fold_true, fold_pred), 2))
        arima_rmse.append(round(np.sqrt(mean_squared_error(fold_true, fold_pred)), 2))
        arima_mape.append(round(mape(fold_true, fold_pred), 2))
        print(f"  Fold {fi+1}: R²={arima_r2[-1]:.4f}  MAE=Rs.{arima_mae[-1]:.1f}  MAPE={arima_mape[-1]:.2f}%")
    else:
        arima_r2.append(0.0)
        arima_mae.append(9999.0)
        arima_rmse.append(9999.0)
        arima_mape.append(99.0)
        print(f"  Fold {fi+1}: ARIMA failed — insufficient data")

print(f"  ARIMA Mean R²={np.mean(arima_r2):.4f}  Mean MAPE={np.mean(arima_mape):.2f}%")

# ─── STATISTICAL SIGNIFICANCE TESTS ─────────────────────────────────────────
print("\n[4/5] Wilcoxon Signed-Rank Tests (RF vs each baseline)...")

def wilcoxon_test(a, b, label):
    try:
        stat, p = wilcoxon(a, b)
        sig = "SIGNIFICANT (p < 0.05)" if p < 0.05 else "not significant"
        print(f"  RF vs {label}: p-value={p:.4f} → {sig}")
        return round(p, 4)
    except Exception as e:
        print(f"  RF vs {label}: could not compute ({e})")
        return None

p_rf_vs_xgb   = wilcoxon_test(rf_r2, xgb_r2, "XGBoost") if xgb_ok else None
p_rf_vs_arima = wilcoxon_test(rf_r2, arima_r2, "ARIMA")

# ─── SAVE RESULTS ────────────────────────────────────────────────────────────
print("\n[5/5] Saving results...")

results = {
    "random_forest": {
        "r2": rf_r2, "mae": rf_mae, "rmse": rf_rmse, "mape": rf_mape,
        "mean_r2": round(np.mean(rf_r2), 4),
        "mean_mae": round(np.mean(rf_mae), 2),
        "mean_rmse": round(np.mean(rf_rmse), 2),
        "mean_mape": round(np.mean(rf_mape), 2),
        "std_r2": round(np.std(rf_r2), 4),
        "std_mape": round(np.std(rf_mape), 2),
    },
    "xgboost": {
        "r2": xgb_r2, "mae": xgb_mae, "rmse": xgb_rmse, "mape": xgb_mape,
        "mean_r2": round(np.mean(xgb_r2), 4) if xgb_r2 else None,
        "mean_mae": round(np.mean(xgb_mae), 2) if xgb_mae else None,
        "mean_rmse": round(np.mean(xgb_rmse), 2) if xgb_rmse else None,
        "mean_mape": round(np.mean(xgb_mape), 2) if xgb_mape else None,
        "std_r2": round(np.std(xgb_r2), 4) if xgb_r2 else None,
        "std_mape": round(np.std(xgb_mape), 2) if xgb_mape else None,
    },
    "arima": {
        "r2": arima_r2, "mae": arima_mae, "rmse": arima_rmse, "mape": arima_mape,
        "mean_r2": round(np.mean(arima_r2), 4),
        "mean_mae": round(np.mean(arima_mae), 2),
        "mean_rmse": round(np.mean(arima_rmse), 2),
        "mean_mape": round(np.mean(arima_mape), 2),
        "std_r2": round(np.std(arima_r2), 4),
        "std_mape": round(np.std(arima_mape), 2),
    },
    "significance_tests": {
        "rf_vs_xgboost_r2_pvalue": p_rf_vs_xgb,
        "rf_vs_arima_r2_pvalue": p_rf_vs_arima,
    },
    "folds": [
        {"fold": 1, "train_period": "2001-2010", "val_period": "2011-2013"},
        {"fold": 2, "train_period": "2001-2013", "val_period": "2014-2016"},
        {"fold": 3, "train_period": "2001-2016", "val_period": "2017-2018"},
        {"fold": 4, "train_period": "2001-2018", "val_period": "2019-2021"},
        {"fold": 5, "train_period": "2001-2021", "val_period": "2022-2024"},
    ]
}

out_path = f"{SAVE_DIR}/baseline_comparison_results.json"
with open(out_path, 'w') as f:
    json.dump(results, f, indent=2)

print(f"\n  Results saved: {out_path}")
print("\n" + "=" * 70)
print("FINAL COMPARISON SUMMARY")
print("=" * 70)
print(f"{'Model':<22} {'Mean R²':>10} {'Mean MAE':>12} {'Mean MAPE':>12} {'Std R²':>10}")
print("-" * 70)
print(f"{'ARIMA (Baseline)':<22} {np.mean(arima_r2):>10.4f} {'Rs.'+str(round(np.mean(arima_mae),1)):>12} {str(round(np.mean(arima_mape),2))+'%':>12} {np.std(arima_r2):>10.4f}")
if xgb_ok:
    print(f"{'XGBoost (Baseline)':<22} {np.mean(xgb_r2):>10.4f} {'Rs.'+str(round(np.mean(xgb_mae),1)):>12} {str(round(np.mean(xgb_mape),2))+'%':>12} {np.std(xgb_r2):>10.4f}")
print(f"{'Random Forest (Ours)':<22} {np.mean(rf_r2):>10.4f} {'Rs.'+str(round(np.mean(rf_mae),1)):>12} {str(round(np.mean(rf_mape),2))+'%':>12} {np.std(rf_r2):>10.4f}")
print("=" * 70)

improvement_over_arima = round(np.mean(arima_mape) - np.mean(rf_mape), 2)
improvement_over_xgb   = round(np.mean(xgb_mape) - np.mean(rf_mape), 2) if xgb_ok else 0
print(f"\n  RF improvement over ARIMA: -{improvement_over_arima}% MAPE")
if xgb_ok:
    print(f"  RF improvement over XGBoost: -{improvement_over_xgb}% MAPE")
print("\nDONE. Run generate_comparison_pdf.py next.")
