import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

np.random.seed(42)  # reproducibility

# Load base data
rollup = pd.read_csv("outputs/analysis-simulation/weekly_rollup.csv")

# Monte Carlo: simulate variation per course
def simulate_hours(row):
    # assume ±10% normal variation
    return np.random.normal(loc=row["duration_hours"], scale=0.1 * row["duration_hours"])

simulations = []

for i in range(1000):
    sim = rollup.copy()
    sim["sim_hours"] = sim.apply(simulate_hours, axis=1)
    sim["run"] = i
    simulations.append(sim)

all_sims = pd.concat(simulations)

# Summary: mean + 95% CI by week
summary = (
    all_sims.groupby("week")["sim_hours"]
    .agg(["mean", "std"])
    .assign(
        ci_lower=lambda df: df["mean"] - 1.96 * df["std"],
        ci_upper=lambda df: df["mean"] + 1.96 * df["std"]
    )
    .reset_index()
)

# Plot
plt.figure(figsize=(12, 6))
plt.plot(summary["week"], summary["mean"], label="Mean Hours")
plt.fill_between(summary["week"], summary["ci_lower"], summary["ci_upper"], alpha=0.3, label="95% CI")
plt.axhline(12, color="red", linestyle="--", label="Federal Limit")
plt.title("Simulated Weekly Hours with 95% CI")
plt.xlabel("Week")
plt.ylabel("Simulated Hours")
plt.legend()
plt.tight_layout()
os.makedirs("outputs/analysis-simulation", exist_ok=True)
plt.savefig("outputs/analysis-simulation/simulation_chart.png", dpi=300)
plt.close()

print("\n✅ Simulation analysis complete and saved.")
