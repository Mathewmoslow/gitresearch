import pandas as pd

# Load and check structure
baseline = pd.read_csv("outputs/analysis-baseline/weekly_rollup.csv")
print("Data structure:")
print(baseline.head())
print(f"\nShape: {baseline.shape}")

# Calculate weekly totals properly
weekly_totals = baseline.groupby('Week')['duration_hours'].sum()
print(f"\nCorrect average weekly hours: {weekly_totals.mean():.1f}")
print(f"Number of unique weeks: {baseline['Week'].nunique()}")
