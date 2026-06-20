"""
STEP 3: DATA CONVERSION TO GEOJSON & AGGREGATED JSON
Format output untuk Leaflet.js dan Chart.js
"""

import pandas as pd
import json
import numpy as np
from datetime import datetime

print("=" * 70)
print("STEP 3: DATA CONVERSION FOR WEB VISUALIZATION")
print("=" * 70)

# 1. LOAD DATA
print("\n[1/4] Loading data...")
df = pd.read_csv('katalog_gempa_clean.csv')
df['tgl'] = pd.to_datetime(df['tgl'])
anomalies = pd.read_csv('gempa_anomalies.csv')
print(f"✓ Loaded {len(df)} earthquake records")
print(f"✓ Loaded {len(anomalies)} anomaly observations")

# 2. CREATE GEOJSON - ALL EARTHQUAKES (sample untuk performance)
print("\n[2/4] Creating GeoJSON for earthquakes...")

# Sample data untuk GeoJSON (100 earthquakes per magnitude category)
features = []

for year in sorted(df['year'].unique()):
    subset_year = df[df['year'] == year]

    subset = subset_year.sample(
        n=min(150, len(subset_year)),
        random_state=42
    )

    for _, row in subset.iterrows():
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(row['lon']), float(row['lat'])]
            },
            "properties": {
                "magnitude": float(row['mag']),
                "mag_category": row['mag_category'],
                "depth": float(row['depth']),
                "depth_category": row['depth_category'],
                "date": str(row['tgl']),
                "time": str(row['ot']),
                "region": row['remark'],
                "year": int(row['year']),
                "month": int(row['month'])
            }
        }
        features.append(feature)
        
geojson_earthquakes = {
    "type": "FeatureCollection",
    "features": features
}

with open('data/earthquakes_sample.geojson', 'w') as f:
    json.dump(geojson_earthquakes, f)
print(f"✓ Created GeoJSON with {len(features)} sample earthquakes")

# 3. CREATE TIMELINE DATA (monthly aggregation)
print("\n[3/4] Creating timeline aggregation data...")

# Monthly statistics
monthly_stats = df.groupby('yearmonth').agg({
    'mag': ['count', 'mean', 'max'],
    'depth': 'mean',
    'lat': 'count'
}).reset_index()

monthly_stats.columns = ['yearmonth', 'event_count', 'mag_mean', 'mag_max', 
                         'depth_mean', 'total_events']
monthly_stats = monthly_stats.sort_values('yearmonth')

# Convert to list for JavaScript
timeline_data = []
for _, row in monthly_stats.iterrows():
    timeline_data.append({
        "month": row['yearmonth'],
        "events": int(row['event_count']),
        "mag_mean": float(row['mag_mean']),
        "mag_max": float(row['mag_max']),
        "depth_mean": float(row['depth_mean'])
    })

with open('data/timeline.json', 'w') as f:
    json.dump(timeline_data, f)
print(f"✓ Created timeline data: {len(timeline_data)} months")

# 4. CREATE SUMMARY & ANOMALY DATA
print("\n[4/4] Creating summary statistics...")

# Overall statistics
summary = {
    "total_earthquakes": len(df),
    "date_range": {
        "start": df['tgl'].min().strftime('%Y-%m-%d'),
        "end": df['tgl'].max().strftime('%Y-%m-%d')
    },
    "magnitude": {
        "min": float(df['mag'].min()),
        "max": float(df['mag'].max()),
        "mean": float(df['mag'].mean()),
        "median": float(df['mag'].median())
    },
    "depth": {
        "min": float(df['depth'].min()),
        "max": float(df['depth'].max()),
        "mean": float(df['depth'].mean()),
        "median": float(df['depth'].median())
    },
    "spatial": {
        "lat_range": [float(df['lat'].min()), float(df['lat'].max())],
        "lon_range": [float(df['lon'].min()), float(df['lon'].max())],
        "grid_cells": int(df['grid_id'].nunique())
    },
    "magnitude_distribution": {
        cat: int(count) 
        for cat, count in df['mag_category'].value_counts().items()
    },
    "depth_distribution": {
        cat: int(count) 
        for cat, count in df['depth_category'].value_counts().items()
    },
    "top_regions": {
        region: int(count) 
        for region, count in df['remark'].value_counts().head(10).items()
    }
}

with open('data/summary.json', 'w') as f:
    json.dump(summary, f)
print(f"✓ Created summary statistics")

# Anomalies top 10
anomalies_top = anomalies[anomalies['anomaly_combined'] == 1].sort_values(
    'anomaly_score_if'
).head(10)

anomaly_features = []
for _, row in anomalies_top.iterrows():
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [float(row['lon']), float(row['lat'])]
        },
        "properties": {
            "period": row['yearmonth'],
            "event_count": int(row['event_count']),
            "mag_max": float(row['mag_max']),
            "mag_mean": float(row['mag_mean']),
            "depth_mean": float(row['depth_mean']),
            "anomaly_score": float(row['anomaly_score_if']),
            "zscore": float(row['zscore_max'])
        }
    }
    anomaly_features.append(feature)

geojson_anomalies = {
    "type": "FeatureCollection",
    "features": anomaly_features
}

with open('data/anomalies.geojson', 'w') as f:
    json.dump(geojson_anomalies, f)
print(f"✓ Created anomalies GeoJSON with {len(anomaly_features)} top anomalies")

print("\n" + "=" * 70)
print("✓ Data conversion complete!")
print("=" * 70)
print(f"\nGenerated files:")
print(f"  • earthquakes_sample.geojson - Sample earthquakes for map")
print(f"  • timeline.json - Monthly aggregation for chart")
print(f"  • summary.json - Overall statistics")
print(f"  • anomalies.geojson - Top anomalous events")
