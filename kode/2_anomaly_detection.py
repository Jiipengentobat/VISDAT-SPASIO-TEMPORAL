"""
STEP 2: MACHINE LEARNING - DETEKSI ANOMALI SEISMIK
Menggunakan Isolation Forest + Z-Score untuk identifikasi aktivitas abnormal
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from scipy import stats
import json
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("STEP 2: DETEKSI ANOMALI AKTIVITAS SEISMIK")
print("=" * 70)

# 1. LOAD CLEANED DATA
print("\n[1/5] Loading cleaned data...")
df = pd.read_csv('../data/katalog_gempa_clean.csv')
print(f"✓ Loaded {len(df)} records")

# 2. AGGREGATE DATA BY GRID & TIME
print("\n[2/5] Aggregating data by spatial grid and temporal units...")

# Monthly aggregation per grid cell
df['datetime'] = pd.to_datetime(df['tgl'])
monthly_grid = df.groupby(['yearmonth', 'grid_id']).agg({
    'mag': ['count', 'mean', 'max', 'std'],
    'depth': 'mean',
    'lat': 'mean',
    'lon': 'mean'
}).reset_index()

monthly_grid.columns = ['yearmonth', 'grid_id', 'event_count', 'mag_mean', 
                        'mag_max', 'mag_std', 'depth_mean', 'lat', 'lon']
monthly_grid['mag_std'] = monthly_grid['mag_std'].fillna(0)

print(f"✓ Created {len(monthly_grid)} monthly grid observations")

# 3. FEATURE ENGINEERING FOR ANOMALY DETECTION
print("\n[3/5] Engineering anomaly detection features...")

# Spatial clustering: events per grid cell per month
grid_month_features = pd.DataFrame()
grid_month_features['event_count'] = monthly_grid['event_count']
grid_month_features['mag_max'] = monthly_grid['mag_max']
grid_month_features['mag_mean'] = monthly_grid['mag_mean']
grid_month_features['depth_mean'] = monthly_grid['depth_mean']

# Normalize features
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_normalized = scaler.fit_transform(grid_month_features)

print(f"✓ Features normalized")

# 4. ANOMALY DETECTION - ISOLATION FOREST
print("\n[4/5] Running Isolation Forest algorithm...")
iso_forest = IsolationForest(
    contamination=0.05,  # Expect ~5% anomalies
    random_state=42,
    n_estimators=100
)

anomaly_labels = iso_forest.fit_predict(X_normalized)
anomaly_scores = iso_forest.score_samples(X_normalized)

# -1 = anomaly, 1 = normal
monthly_grid['anomaly_if'] = (anomaly_labels == -1).astype(int)
monthly_grid['anomaly_score_if'] = anomaly_scores

print(f"✓ Anomalies detected: {(anomaly_labels == -1).sum()} observations")

# 5. ANOMALY DETECTION - Z-SCORE METHOD
print("\n[5/5] Running Z-Score method for validation...")

# Calculate Z-scores for event count and magnitude
monthly_grid['zscore_event_count'] = np.abs(
    stats.zscore(monthly_grid['event_count'], nan_policy='omit')
)
monthly_grid['zscore_mag_max'] = np.abs(
    stats.zscore(monthly_grid['mag_max'], nan_policy='omit')
)
monthly_grid['zscore_max'] = monthly_grid[['zscore_event_count', 'zscore_mag_max']].max(axis=1)

# Anomaly if Z-score > 2 (95% confidence)
monthly_grid['anomaly_zscore'] = (monthly_grid['zscore_max'] > 2).astype(int)

# Combined anomaly score
monthly_grid['anomaly_combined'] = (
    (monthly_grid['anomaly_if'] == 1) | (monthly_grid['anomaly_zscore'] == 1)
).astype(int)

print(f"✓ Z-Score anomalies: {monthly_grid['anomaly_zscore'].sum()}")
print(f"✓ Combined anomalies: {monthly_grid['anomaly_combined'].sum()}")

# 6. SAVE RESULTS
print("\n[6/6] Saving anomaly detection results...")
monthly_grid.to_csv('../data/gempa_anomalies.csv', index=False)
print(f"✓ Saved to: ../data/gempa_anomalies.csv")

# ANOMALY REPORT
print("\n" + "=" * 70)
print("ANOMALY DETECTION REPORT")
print("=" * 70)

anomalies = monthly_grid[monthly_grid['anomaly_combined'] == 1].sort_values(
    'anomaly_score_if'
).head(10)

print(f"\nTop 10 Anomalous Periods/Locations:")
for idx, row in anomalies.iterrows():
    print(f"\n  Period: {row['yearmonth']}, Grid: {row['grid_id']}")
    print(f"    - Events: {row['event_count']:.0f}")
    print(f"    - Max Magnitude: {row['mag_max']:.1f}")
    print(f"    - Avg Depth: {row['depth_mean']:.1f} km")
    print(f"    - Anomaly Score (IF): {row['anomaly_score_if']:.3f}")
    print(f"    - Z-Score Max: {row['zscore_max']:.2f}")

print("\n" + "=" * 70)
print("✓ Machine Learning preprocessing complete!")
print("=" * 70)
