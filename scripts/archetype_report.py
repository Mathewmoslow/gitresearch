#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

# Load baseline data
baseline = pd.read_csv("outputs/analysis-archetypes/weekly_rollup.csv")

# Define archetype multipliers
multipliers = {
    "struggling": 1.3,    # Takes 30% longer
    "average": 1.0,       # Baseline
    "efficient": 0.8      # 20% faster
}

# Apply multipliers and create scenarios
scenarios = {}
for archetype, mult in multipliers.items():
    df = baseline.copy()
    df['duration_hours'] = df['duration_hours'] * mult
    df['archetype'] = archetype
    scenarios[archetype] = df

# Combine all scenarios
all_scenarios = pd.concat(scenarios.values())

# Calculate weekly totals for each archetype
plt.figure(figsize=(12, 6))
for archetype, mult in multipliers.items():
    data = scenarios[archetype]
    weekly = data.groupby('Week')['duration_hours'].sum()
    plt.plot(weekly.index, weekly.values, marker='o', label=f'{archetype.title()} (×{mult})')

plt.axhline(y=40, color='r', linestyle='--', label='Federal 40h limit')
plt.axhline(y=20, color='orange', linestyle='--', label='Federal 20h limit', alpha=0.7)
plt.xlabel('Week')
plt.ylabel('Total Hours')
plt.title('Weekly Hours by Student Archetype')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Save outputs
output_dir = Path("outputs/analysis-archetypes")
plt.savefig(output_dir / "archetype_chart.png", dpi=300, bbox_inches='tight')

# Rename Hours to duration_hours for consistency in saved file
all_scenarios = all_scenarios.rename(columns={'Hours': 'duration_hours'})
all_scenarios.to_csv(output_dir / "adjusted_rollup.csv", index=False)

# Print summary
print("\n=== ARCHETYPE ANALYSIS SUMMARY ===")
for archetype in multipliers:
    scenario_data = scenarios[archetype]
    weekly_totals = scenario_data.groupby('Week')['duration_hours'].sum()
    print(f"\n{archetype.upper()} students:")
    print(f"  Average weekly hours: {weekly_totals.mean():.1f}")
    print(f"  Weeks over 40h: {(weekly_totals > 40).sum()}")
    print(f"  Max weekly hours: {weekly_totals.max():.1f}")

print("\n✅ Archetype analysis saved.")
plt.close()
