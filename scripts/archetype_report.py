import pandas as pd
import matplotlib.pyplot as plt
import os

# === Load weekly rollup ===
rollup = pd.read_csv("outputs/analysis-archetypes/weekly_rollup.csv")

# === Define multipliers for archetypes (example only) ===
multipliers = {
    "Adult_310": 1.2,
    "OBGYN_330": 1.3,
    "Gerontology_315": 1.1,
    "NCLEX_335": 1.4,
}

# === Apply multipliers ===
rollup["adjusted_hours"] = rollup.apply(
    lambda row: row["duration_hours"] * multipliers.get(row["course"], 1.0),
    axis=1
)

# === Save adjusted rollup ===
os.makedirs("outputs/analysis-archetypes", exist_ok=True)
rollup.to_csv("outputs/analysis-archetypes/adjusted_rollup.csv", index=False)

# === Summary chart ===
summary = rollup.groupby("course")["adjusted_hours"].sum().reset_index()

plt.figure(figsize=(10, 6))
plt.bar(summary["course"], summary["adjusted_hours"])
plt.title("Total Adjusted Hours by Course (Archetype)")
plt.ylabel("Adjusted Hours")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("outputs/analysis-archetypes/archetype_chart.png", dpi=300)
plt.close()

print("\n✅ Archetype analysis complete and saved.")
