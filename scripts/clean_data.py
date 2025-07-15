"""
clean_data.py  –  Baseline pipeline for Paper 1
------------------------------------------------
1. Reads  data/Cleaned_Master_text.txt
   (comma‑separated, columns: UniqueID, Course, Date, Item, Type, Duration_Cleaned)
2. Adds:
     - duration_hours  (HH:MM:SS → decimal; NaN → <NA>)
     - Week            (ISO week number derived from Date)
3. Writes cleaned and roll‑ups:
     data/tasks_cleaned.csv
     outputs/analysis-baseline/weekly_rollup.csv
     outputs/analysis-baseline/tasktype_by_course.csv
"""

import pandas as pd
import pathlib

RAW  = pathlib.Path("data/Cleaned_Master_text.txt")
OUT  = pathlib.Path("outputs/analysis-baseline")
OUT.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# 1 — load
df = pd.read_csv(RAW)

# 2 — tidy date + week
df["Date"] = pd.to_datetime(df["Date"].str.split("_").str[0], errors="coerce")  # keep YYYY-MM-DD
df["Week"] = df["Date"].dt.isocalendar().week

# 3 — duration to hours
def to_hours(x):
    if pd.isna(x) or str(x).strip().upper() in {"N/A", ""}:
        return pd.NA
    h, m, s = map(float, str(x).split(":"))
    return h + m/60 + s/3600

df["duration_hours"] = df["Duration_Cleaned"].apply(to_hours)

# 4 — roll‑ups
weekly = (
    df.groupby(["Week", "Course"], dropna=False)
      .agg(Task_Count=("UniqueID", "size"),
           Hours=("duration_hours", "sum"))
      .reset_index()
      .sort_values(["Week", "Course"])
)

tasktype = (
    df.groupby(["Course", "Type"], dropna=False)
      .agg(Task_Count=("UniqueID", "size"),
           Hours=("duration_hours", "sum"),
           With_Duration=("duration_hours", "count"))
      .reset_index()
      .sort_values(["Course", "Type"])
)

# 5 — save
df.to_csv("data/tasks_cleaned.csv", index=False)
weekly.to_csv(OUT / "weekly_rollup.csv", index=False)
tasktype.to_csv(OUT / "tasktype_by_course.csv", index=False)

print("✅ Cleaning + roll‑ups complete.")
print("   - data/tasks_cleaned.csv")
print("   - outputs/analysis-baseline/weekly_rollup.csv")
print("   - outputs/analysis-baseline/tasktype_by_course.csv")
