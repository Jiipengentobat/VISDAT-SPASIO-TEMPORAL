"""
STEP 1: DATA PREPROCESSING & CLEANING
Gempa Bumi Indonesia - Tugas Akhir Visualisasi Data Spasio-Temporal
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("STEP 1: DATA PREPROCESSING & CLEANING")
print("=" * 70)

# 1. LOAD DATA
print("\n[1/6] Loading data...")
df = pd.read_csv('../data/katalog_gempa_raw.csv')
print(f"✓ Loaded {len(df)} records")
print(f"✓ Columns: {list(df.columns)}")

# 2. PARSE DATETIME
print("\n[2/6] Parsing datetime fields...")
df['tgl'] = pd.to_datetime(df['tgl'], format='%Y/%m/%d')
df['ot'] = pd.to_datetime(df['ot'], format='%H:%M:%S.%f', errors='coerce').dt.time
df['datetime'] = pd.to_datetime(
    df['tgl'].astype(str) + ' ' + df['ot'].astype(str), 
    errors='coerce'
)

# Extract temporal features
df['year'] = df['tgl'].dt.year
df['month'] = df['tgl'].dt.month
df['day'] = df['tgl'].dt.day
df['hour'] = df['datetime'].dt.hour
df['yearmonth'] = df['tgl'].dt.strftime('%Y-%m')
print(f"✓ Date range: {df['tgl'].min()} to {df['tgl'].max()}")

# 3. DATA QUALITY CHECK
print("\n[3/6] Checking data quality...")
print(f"✓ Missing values:")
print(f"  - Latitude: {df['lat'].isna().sum()}")
print(f"  - Longitude: {df['lon'].isna().sum()}")
print(f"  - Magnitude: {df['mag'].isna().sum()}")
print(f"  - Depth: {df['depth'].isna().sum()}")

# Remove rows with missing critical values
df_clean = df.dropna(subset=['lat', 'lon', 'mag', 'depth'])
print(f"✓ After cleaning: {len(df_clean)} records ({100*len(df_clean)/len(df):.1f}%)")

# 4. REMOVE OUTLIERS & VALIDATE COORDINATES
print("\n[4/6] Validating spatial coordinates...")
# Indonesia bounds (with small buffer)
lat_valid = (df_clean['lat'] >= -11) & (df_clean['lat'] <= 7)
lon_valid = (df_clean['lon'] >= 95) & (df_clean['lon'] <= 141)
df_clean = df_clean[lat_valid & lon_valid]
print(f"✓ After spatial validation: {len(df_clean)} records")

# Validate magnitude and depth
df_clean = df_clean[(df_clean['mag'] >= 0) & (df_clean['mag'] <= 10)]
df_clean = df_clean[(df_clean['depth'] >= 0) & (df_clean['depth'] <= 700)]
print(f"✓ After magnitude/depth validation: {len(df_clean)} records")

# 5. ADD DERIVED FEATURES
print("\n[5/6] Engineering features...")

# Magnitude categories
def categorize_magnitude(mag):
    if mag < 3:
        return 'Minor'
    elif mag < 4:
        return 'Light'
    elif mag < 5:
        return 'Moderate'
    elif mag < 6:
        return 'Strong'
    else:
        return 'Major'

df_clean['mag_category'] = df_clean['mag'].apply(categorize_magnitude)

# Depth categories (shallow/intermediate/deep)
def categorize_depth(depth):
    if depth < 70:
        return 'Shallow'
    elif depth < 300:
        return 'Intermediate'
    else:
        return 'Deep'

df_clean['depth_category'] = df_clean['depth'].apply(categorize_depth)

# Add grid cell identifier (for spatial clustering)
df_clean['grid_id'] = (
    (df_clean['lat'].round(1)).astype(str) + '_' + 
    (df_clean['lon'].round(1)).astype(str)
)

print("✓ Added: mag_category, depth_category, grid_id")

# 6. SAVE PROCESSED DATA
print("\n[6/6] Saving processed data...")
output_file = '../data/katalog_gempa_clean.csv'
df_clean.to_csv(output_file, index=False)
print(f"✓ Saved to: {output_file}")

# STATISTICS
print("\n" + "=" * 70)
print("DATA STATISTICS")
print("=" * 70)
print(f"\nTemporal Coverage:")
print(f"  • Years: {df_clean['year'].min():.0f} - {df_clean['year'].max():.0f}")
print(f"  • Total months: {df_clean['yearmonth'].nunique()}")
print(f"  • Average per month: {len(df_clean) / df_clean['yearmonth'].nunique():.1f}")

print(f"\nSpatial Coverage:")
print(f"  • Latitude range: {df_clean['lat'].min():.2f}° to {df_clean['lat'].max():.2f}°")
print(f"  • Longitude range: {df_clean['lon'].min():.2f}° to {df_clean['lon'].max():.2f}°")
print(f"  • Grid cells covered: {df_clean['grid_id'].nunique()}")

print(f"\nMagnitude Statistics:")
print(f"  • Min: {df_clean['mag'].min():.1f}, Max: {df_clean['mag'].max():.1f}")
print(f"  • Mean: {df_clean['mag'].mean():.2f}, Median: {df_clean['mag'].median():.2f}")
print(f"  • Distribution:")
for cat in ['Minor', 'Light', 'Moderate', 'Strong', 'Major']:
    count = (df_clean['mag_category'] == cat).sum()
    pct = 100 * count / len(df_clean)
    print(f"    - {cat}: {count} ({pct:.1f}%)")

print(f"\nDepth Statistics:")
print(f"  • Min: {df_clean['depth'].min():.0f} km, Max: {df_clean['depth'].max():.0f} km")
print(f"  • Mean: {df_clean['depth'].mean():.1f} km")
print(f"  • Distribution:")
for cat in ['Shallow', 'Intermediate', 'Deep']:
    count = (df_clean['depth_category'] == cat).sum()
    pct = 100 * count / len(df_clean)
    print(f"    - {cat}: {count} ({pct:.1f}%)")

print(f"\nTop 5 Earthquake Regions:")
top_regions = df_clean['remark'].value_counts().head(5)
for region, count in top_regions.items():
    print(f"  • {region}: {count} events")

print("\n✓ Data preprocessing complete!")
print("=" * 70)
