"""
clean_data.py

1.  Reads Cleaned_Master text.txt (tab or csv).
2.  Converts Duration column:
      - HH:MM:SS → decimal hours
      - Blank → NaN
3.  Writes:
     data/tasks_cleaned.csv
     outputs/analysis-baseline/weekly_rollup.csv
     outputs/analysis-baseline/tasktype_by_course.csv
"""

import pandas as pd
import pathlib

RAW = pathlib.Path("data/Cleaned_Master text.txt")
OUT = pathlib.Path("outputs/analysis-baseline")
OUT.mkdir(parents=True, exist_ok=True)

# 1 — load
df = pd.read_csv(RAW, sep=None, engine="python")   # auto‑detect comma/ tab

# 2 — clean duration
def to_hours(x):
    if pd.isna(x) or str(x).strip() == "":
        return pd.NA
    if ":" in str(x):
        h, m, s = map(float, str(x).split(":"))
        return h + m/60 + s/3600
    return float(x)

df["duration_hours"] = df["Duration"].apply(to_hours)

# 3 — weekly & task‑type roll‑ups
weekly = (
    df.groupby(["Week", "Course"])
      .agg(Task_Count=("Task_ID", "size"),
           Hours=("duration_hours", "sum"))
      .reset_index()
)

tasktype = (
    df.groupby(["Course", "Task_Type"])
      .agg(Task_Count=("Task_ID", "size"),
           Hours=("duration_hours", "sum"),
           With_Duration=("duration_hours", "count"))
      .reset_index()
)

# 4 — save
df.to_csv("data/tasks_cleaned.csv", index=False)
weekly.to_csv(OUT / "weekly_rollup.csv", index=False)
tasktype.to_csv(OUT / "tasktype_by_course.csv", index=False)

print("✅ Cleaning + roll‑ups complete.")

