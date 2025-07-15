import pandas as pd, numpy as np, matplotlib.pyplot as plt, os

np.random.seed(42)
roll = pd.read_csv("outputs/analysis-baseline/weekly_rollup.csv")

sims = []
for i in range(1000):
    tmp = roll.copy()
    tmp["sim"] = np.random.normal(tmp["duration_hours"], 0.1*tmp["duration_hours"])
    tmp["run"] = i; sims.append(tmp)
sims = pd.concat(sims)

summary = (sims.groupby("Week")["sim"]
             .agg(["mean","std"])
             .assign(lo=lambda d:d["mean"]-1.96*d["std"],
                     hi=lambda d:d["mean"]+1.96*d["std"])
             .reset_index())

plt.plot(summary["Week"], summary["mean"]); plt.fill_between(summary["Week"], summary["lo"], summary["hi"], alpha=.3)
plt.axhline(12, color="red", ls="--"); plt.tight_layout()

os.makedirs("outputs/analysis-simulation", exist_ok=True)
plt.savefig("outputs/analysis-simulation/simulation_chart.png", dpi=300); plt.close()
summary.to_csv("outputs/analysis-simulation/weekly_ci.csv", index=False)
print("✅ Simulation complete.")
