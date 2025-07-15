import pandas as pd, matplotlib.pyplot as plt, os

rollup = pd.read_csv("outputs/analysis-baseline/weekly_rollup.csv")
rollup = rollup.rename(columns={"duration_hours": "Hours"})

FED_WEEK = 12; FED_TOTAL = 45

summary = rollup.groupby("Course")["Hours"].sum().reset_index()
summary["over_limit"] = summary["Hours"] > FED_TOTAL
print("\n=== TOTAL HOURS BY COURSE ==="); print(summary)

pivot = rollup.pivot_table(index="Week", columns="Course", values="Hours", aggfunc="sum").fillna(0)
pivot.plot(kind="bar", stacked=True, figsize=(12,6))
plt.axhline(FED_WEEK, color="red", ls="--"); plt.tight_layout()

os.makedirs("outputs/analysis-baseline", exist_ok=True)
plt.savefig("outputs/analysis-baseline/weekly_stack_chart.png", dpi=300); plt.close()
print("✅ Baseline chart saved.")
