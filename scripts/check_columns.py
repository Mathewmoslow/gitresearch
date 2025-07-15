import pandas as pd
import os

print("=== Checking CSV structures ===")

# Check weekly_rollup.csv
if os.path.exists("outputs/analysis-baseline/weekly_rollup.csv"):
    df = pd.read_csv("outputs/analysis-baseline/weekly_rollup.csv")
    print("\nweekly_rollup.csv columns:", df.columns.tolist())
    print("First few rows:")
    print(df.head())
else:
    print("\nweekly_rollup.csv not found!")

# Check tasktype_by_course.csv
if os.path.exists("outputs/analysis-baseline/tasktype_by_course.csv"):
    df2 = pd.read_csv("outputs/analysis-baseline/tasktype_by_course.csv")
    print("\ntasktype_by_course.csv columns:", df2.columns.tolist())
else:
    print("\ntasktype_by_course.csv not found!")
