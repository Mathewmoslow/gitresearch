import pandas as pd, pathlib, os

RAW  = pathlib.Path("data/Cleaned_Master_text.txt")
OUT  = pathlib.Path("outputs/analysis-baseline")
OUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(RAW)
df["Date"] = pd.to_datetime(df["Date"].str.split("_").str[0], errors="coerce")
df["Week"] = df["Date"].dt.isocalendar().week

def to_hrs(x):
    if pd.isna(x) or str(x).strip().upper() in {"N/A", ""}:
        return pd.NA
    h, m, s = map(float, str(x).split(":"))
    return h + m/60 + s/3600

df["duration_hours"] = df["Duration_Cleaned"].apply(to_hrs)

weekly = (df.groupby(["Week", "Course"], dropna=False)
            .agg(Task_Count=("UniqueID", "size"),
                 duration_hours=("duration_hours", "sum"))
            .reset_index())

tasktype = (df.groupby(["Course", "Type"], dropna=False)
              .agg(Task_Count=("UniqueID", "size"),
                   duration_hours=("duration_hours", "sum"),
                   With_Duration=("duration_hours", "count"))
              .reset_index())

df.to_csv("data/tasks_cleaned.csv", index=False)
weekly.to_csv(OUT/"weekly_rollup.csv", index=False)
tasktype.to_csv(OUT/"tasktype_by_course.csv", index=False)

print("✅ Cleaning + roll‑ups complete.")
