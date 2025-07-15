import pandas as pd
import matplotlib.pyplot as plt
import os

# === Load cleaned data ===
rollup = pd.read_csv("outputs/analysis-baseline/weekly_rollup.csv")

# Column names in weekly_rollup.csv are:  Week, Course, Task_Count, Hours
# We renamed Hours → duration_hours in the cleaner for consistency:
rollup = rollup.rename(columns={"Hours": "duration_hours"})

# === Config ===
FEDERAL_WEEKLY_LIMIT = 12
FEDERAL_TOTAL_LIMIT = 45

# === 1. Summarize hours per course ===
total_by_course = (
    rollup.groupby("Course")["duration_hours"]
          .sum()
          .reset_index()
          .rename(columns={"Course": "Course", "duration_hours": "Total_Hours"})
)
total_by_course["over_limit"] = total_by_course["Total_Hours"] > FEDERAL_TOTAL_LIMIT

print("\n=== TOTAL HOURS BY COURSE ===")
print(total_by_course.sort_values("Total_Hours", ascending=False))

# === 2. Weekly stacked bar chart ===
pivot = (
    rollup.pivot_table(index="Week", columns="Course",
                       values="duration_hours", aggfunc="sum")
          .fillna(0)
          .sort_index()
)

plt.figure(figsize=(12, 6))
pivot.plot(kind="bar", stacked=True, colormap="tab20", figsize=(12, 6))
plt.axhline(FEDERAL_WEEKLY_LIMIT, color="red", linestyle="--",
            label="Federal Limit (12h/week)")
plt.title("Weekly Workload by Course")
plt.ylabel("Total Hours")
plt.xlabel("Week")
plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()

# Save chart
os.makedirs("outputs/analysis-baseline", exist_ok=True)
plt.savefig("outputs/analysis-baseline/weekly_stack_chart.png", dpi=300)
plt.close()

print("\n✅ Weekly workload chart saved to:")
print("   outputs/analysis-baseline/weekly_stack_chart.png")

# === 3. Optional: Print overload weeks ===
rollup_summary = (
    rollup.groupby("Week")["duration_hours"]
          .sum()
          .reset_index()
)
overload_weeks = rollup_summary[rollup_summary["duration_hours"] > FEDERAL_WEEKLY_LIMIT]

if not overload_weeks.empty:
    print("\n⚠️  Weeks exceeding federal weekly limit:")
    print(overload_weeks)
else:
    print("\n✅ All weeks under federal weekly threshold.")
