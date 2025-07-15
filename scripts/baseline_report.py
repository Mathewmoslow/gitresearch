#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Define paths
BASE_OUT = Path.home() / "Documents/gitresearch_outputs/analysis-baseline"

# Load data
rollup = pd.read_csv(BASE_OUT / "weekly_rollup.csv")
tasktype = pd.read_csv(BASE_OUT / "tasktype_by_course.csv")

# Calculate total hours by course
print("\n=== TOTAL HOURS BY COURSE ===")
total_by_course = rollup.groupby("Course")["duration_hours"].sum().reset_index()
total_by_course.columns = ["Course", "Total_Hours"]
total_by_course["over_limit"] = total_by_course["Total_Hours"] > 50  # reasonable limit per course
total_by_course = total_by_course.sort_values("Total_Hours", ascending=False)
print(total_by_course)

# Calculate weekly totals (sum across all courses)
weekly_totals = rollup.groupby("Week")["duration_hours"].sum().reset_index()
weekly_totals.columns = ["Week", "duration_hours"]  # Keep consistent naming
print(f"\n=== WEEKLY SUMMARY ===")
print(f"Average weekly hours (across all courses): {weekly_totals['duration_hours'].mean():.1f}")
print(f"Min weekly hours: {weekly_totals['duration_hours'].min():.1f}")
print(f"Max weekly hours: {weekly_totals['duration_hours'].max():.1f}")

# Create stacked bar chart showing breakdown by course
plt.figure(figsize=(12, 6))
pivot_data = rollup.pivot(index='Week', columns='Course', values='duration_hours').fillna(0)
pivot_data.plot(kind='bar', stacked=True, figsize=(12, 6))
plt.axhline(y=40, color='r', linestyle='--', label='Federal 40h limit')
plt.axhline(y=20, color='orange', linestyle='--', label='Federal 20h limit', alpha=0.7)
plt.title('Weekly Workload by Course')
plt.xlabel('Week')
plt.ylabel('Total Hours')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

output_path = BASE_OUT / "weekly_stack_chart.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()

print(f"\n✅ Weekly workload chart saved to:\n   {output_path}")

# Report weeks exceeding limits
over_limit = weekly_totals[weekly_totals["duration_hours"] > 40]
if not over_limit.empty:
    print(f"\n⚠️  Weeks exceeding federal 40h weekly limit:")
    print(over_limit)
else:
    print(f"\n✅ No weeks exceed the federal 40h limit")

# Save weekly totals for other analyses
weekly_totals.to_csv(BASE_OUT / "weekly_totals.csv", index=False)