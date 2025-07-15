import pandas as pd
import numpy as np
from pathlib import Path

def to_hrs(x):
    """Convert duration string to hours."""
    if pd.isna(x) or x == "":
        return 0
    try:
        parts = str(x).split(":")
        if len(parts) == 3:
            return int(parts[0]) + int(parts[1])/60 + int(parts[2])/3600
        elif len(parts) == 2:
            return int(parts[0]) + int(parts[1])/60
        else:
            return float(x)
    except:
        return 0

# File paths
RAW = Path("data/Cleaned_Master_text.txt")
OUT = Path.home() / "Documents/gitresearch_outputs/analysis-baseline"
OUT.mkdir(parents=True, exist_ok=True)

# Load and process data
df = pd.read_csv(RAW, sep=None, engine="python")

# Fix date format - replace underscore with space
df["Date"] = df["Date"].str.replace('_', ' ')
df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d %H:%M:%S", errors="coerce")

# Add week number
df["Week"] = df["Date"].dt.isocalendar().week

# Convert duration to hours
df["duration_hours"] = df["Duration_Cleaned"].apply(to_hrs)

# Create weekly rollup
weekly = (df.groupby(["Week", "Course"])
          .agg(Task_Count=("UniqueID", "count"),
               duration_hours=("duration_hours", "sum"))
          .reset_index())

# Create task type by course summary
tasktype = (df.groupby(["Course", "Type"])
            .agg(Task_Count=("UniqueID", "count"),
                 duration_hours=("duration_hours", "sum"),
                 With_Duration=("duration_hours", "count"))
            .reset_index())

# Print summary
print("✅ Cleaning + roll‑ups complete.")

# Save outputs
df.to_csv("data/tasks_cleaned.csv", index=False)
weekly.to_csv(OUT / "weekly_rollup.csv", index=False)
tasktype.to_csv(OUT / "tasktype_by_course.csv", index=False)

# Print output locations
print(f"   - data/tasks_cleaned.csv")
print(f"   - {OUT}/weekly_rollup.csv")
print(f"   - {OUT}/tasktype_by_course.csv")

# Verify column names for consistency
assert 'duration_hours' in weekly.columns, "Column name mismatch: expected 'duration_hours'"
print(f"   Weekly rollup columns: {list(weekly.columns)}")