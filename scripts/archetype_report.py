import pandas as pd, matplotlib.pyplot as plt, os, json

rollup = pd.read_csv("outputs/analysis-baseline/weekly_rollup.csv")
# example multipliers—adjust as needed
mult = {"Adult_310":1.2,"OBGYN_330":1.3,"Gerontology_315":1.1,"NCLEX_335":1.4}
rollup["adj_hours"] = rollup.apply(lambda r: r["duration_hours"]*mult.get(r["Course"],1), axis=1)

os.makedirs("outputs/analysis-archetypes", exist_ok=True)
rollup.to_csv("outputs/analysis-archetypes/adjusted_rollup.csv", index=False)

summ = rollup.groupby("Course")["adj_hours"].sum().reset_index()
plt.bar(summ["Course"], summ["adj_hours"]); plt.xticks(rotation=45); plt.tight_layout()
plt.savefig("outputs/analysis-archetypes/archetype_chart.png", dpi=300); plt.close()
print("✅ Archetype analysis saved.")
