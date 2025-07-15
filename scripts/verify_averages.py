#!/usr/bin/env python3
import pandas as pd
from pathlib import Path

# Define path
BASE_OUT = Path.home() / "Documents/gitresearch_outputs/analysis-baseline"

# Load and check structure
baseline = pd.read_csv(BASE_OUT / "weekly_rollup.csv")
print("Data structure:")
print(baseline.head())
print(f"\nShape: {baseline.shape}")

# Calculate weekly totals properly
weekly_totals = baseline.groupby('Week')['duration_hours'].sum()
print(f"\nCorrect average weekly hours: {weekly_totals.mean():.1f}")
print(f"Number of unique weeks: {baseline['Week'].nunique()}")

# Show column names
print(f"\nColumn names: {list(baseline.columns)}")

# Check for any data issues
print(f"\nAny null values? {baseline.isnull().sum().sum()}")
print(f"Unique courses: {baseline['Course'].unique()}")