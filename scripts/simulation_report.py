#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np

# Ensure output directory exists
output_dir = Path("outputs/analysis-simulation")
output_dir.mkdir(parents=True, exist_ok=True)

# Load baseline data
print("Loading baseline data...")
baseline = pd.read_csv("outputs/analysis-baseline/weekly_rollup.csv")

# CRITICAL: Aggregate to weekly totals first
weekly_totals = baseline.groupby('Week')['Hours'].sum().reset_index()
print(f"Found {len(weekly_totals)} weeks of data")
print(f"Average weekly hours: {weekly_totals['Hours'].mean():.1f}")

# Monte Carlo Simulation on WEEKLY TOTALS
print("\n=== Running Monte Carlo Simulation ===")
n_simulations = 1000
results = []

for _, week_row in weekly_totals.iterrows():
    week = week_row['Week']
    base_hours = week_row['Hours']
    
    # Simulate with 20% variance
    simulated_hours = np.random.normal(base_hours, base_hours * 0.2, n_simulations)
    
    results.append({
        'Week': week,
        'mean': np.mean(simulated_hours),
        'std': np.std(simulated_hours),
        'p5': np.percentile(simulated_hours, 5),
        'p95': np.percentile(simulated_hours, 95),
        'over_40h_prob': np.mean(simulated_hours > 40),
        'over_20h_prob': np.mean(simulated_hours > 20)
    })

# Create summary DataFrame
summary = pd.DataFrame(results)
summary['lo'] = summary['mean'] - 1.96 * summary['std']
summary['hi'] = summary['mean'] + 1.96 * summary['std']

# Save simulation results
summary.to_csv(output_dir / "simulation_results.csv", index=False)
print(f"✅ Saved simulation results to {output_dir}/simulation_results.csv")

# Create visualization
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# Plot 1: Confidence intervals
ax1.plot(summary['Week'], summary['mean'], 'b-', linewidth=2, label='Mean Hours')
ax1.fill_between(summary['Week'], summary['lo'], summary['hi'], alpha=0.3, label='95% CI')
ax1.axhline(y=40, color='r', linestyle='--', label='Federal 40h Limit')
ax1.axhline(y=20, color='orange', linestyle='--', label='Federal 20h Limit')
ax1.set_xlabel('Week')
ax1.set_ylabel('Hours')
ax1.set_title('Monte Carlo Simulation: Weekly Work Hours with Confidence Intervals')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot 2: Probability of exceeding limits
ax2.bar(summary['Week'], summary['over_40h_prob'] * 100, color='red', alpha=0.7, label='>40h')
ax2.bar(summary['Week'], summary['over_20h_prob'] * 100, color='orange', alpha=0.5, label='>20h')
ax2.set_xlabel('Week')
ax2.set_ylabel('Probability (%)')
ax2.set_title('Weekly Probability of Exceeding Federal Limits')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(output_dir / "simulation_chart.png", dpi=300, bbox_inches='tight')
plt.close()

print(f"✅ Saved simulation chart to {output_dir}/simulation_chart.png")

# Print summary statistics
print("\n=== SIMULATION SUMMARY ===")
print(f"Weeks analyzed: {len(summary)}")
print(f"Average weekly hours: {summary['mean'].mean():.1f}")
print(f"Weeks likely over 40h limit (>50% probability): {(summary['over_40h_prob'] > 0.5).sum()}")
print(f"Weeks likely over 20h limit (>50% probability): {(summary['over_20h_prob'] > 0.5).sum()}")
print(f"Max weekly hours (95% CI upper): {summary['hi'].max():.1f}")

print("\n✅ Simulation analysis completed successfully!")
