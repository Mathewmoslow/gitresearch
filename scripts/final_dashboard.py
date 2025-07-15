#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import os

# Define paths
BASE_OUT = Path.home() / "Documents/gitresearch_outputs/analysis-baseline"
SIM_OUT = Path.home() / "Documents/gitresearch_outputs/analysis-simulation"
DASH_OUT = Path.home() / "Documents/gitresearch_outputs"

# Check which files exist before trying to load them
print("Checking available files...")
files_to_check = [
    BASE_OUT / "weekly_rollup.csv",
    BASE_OUT / "tasktype_by_course.csv",
    SIM_OUT / "simulation_results.csv"
]

for f in files_to_check:
    if f.exists():
        print(f"✓ Found: {f}")
    else:
        print(f"✗ Missing: {f}")

try:
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle('Comprehensive Workload Analysis Dashboard', fontsize=16)

    # 1. Baseline weekly hours - aggregated by week
    baseline = pd.read_csv(BASE_OUT / "weekly_rollup.csv")
    weekly_totals = baseline.groupby('Week')['duration_hours'].sum().reset_index()
    weekly_totals.columns = ['Week', 'Total_Hours']
    
    ax1 = axes[0, 0]
    ax1.bar(weekly_totals['Week'], weekly_totals['Total_Hours'], color='skyblue', alpha=0.7)
    ax1.axhline(y=40, color='r', linestyle='--', label='40h limit')
    ax1.axhline(y=20, color='orange', linestyle='--', label='20h limit', alpha=0.5)
    ax1.set_title('Baseline: Actual Weekly Hours')
    ax1.set_xlabel('Week')
    ax1.set_ylabel('Hours')
    ax1.legend()

    # 2. Course distribution
    course_totals = pd.read_csv(BASE_OUT / "tasktype_by_course.csv")
    ax2 = axes[0, 1]
    courses = course_totals.groupby('Course')['duration_hours'].sum().sort_values(ascending=False)
    
    bars = ax2.bar(range(len(courses)), courses.values, tick_label=courses.index)
    # Color code by intensity
    colors = ['red' if v > 100 else 'orange' if v > 50 else 'skyblue' for v in courses.values]
    for bar, color in zip(bars, colors):
        bar.set_color(color)
    ax2.set_title('Total Hours by Course')
    ax2.set_ylabel('Total Hours')
    ax2.axhline(y=100, color='red', linestyle=':', alpha=0.5)
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)

    # 3. Simulation confidence intervals
    sim = pd.read_csv(SIM_OUT / "simulation_results.csv")
    ax3 = axes[1, 0]
    ax3.plot(sim['Week'], sim['mean'], 'b-', linewidth=2, label='Mean')
    ax3.fill_between(sim['Week'], sim['lo'], sim['hi'], alpha=0.3, label='95% CI')
    ax3.axhline(y=40, color='r', linestyle='--', label='40h limit')
    ax3.axhline(y=20, color='orange', linestyle='--', label='20h limit', alpha=0.5)
    ax3.set_title('Monte Carlo: Projected Hours with Uncertainty')
    ax3.set_xlabel('Week')
    ax3.set_ylabel('Hours')
    ax3.legend()

    # 4. Risk heatmap
    ax4 = axes[1, 1]
    risk_data = sim[['Week', 'over_40h_prob']].set_index('Week')
    risk_matrix = risk_data.T
    sns.heatmap(risk_matrix, annot=True, fmt='.0%', cmap='Reds', 
                cbar_kws={'label': 'Probability'}, ax=ax4, vmin=0, vmax=1,
                xticklabels=[f"W{int(w)}" for w in risk_data.index])
    ax4.set_title('Weekly Risk of Exceeding 40h Limit')
    ax4.set_ylabel('')

    plt.tight_layout()
    output_file = DASH_OUT / "final_dashboard.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n✅ Dashboard saved to {output_file}")

    # Generate CORRECTED text summary
    print("\n=== EXECUTIVE SUMMARY ===")
    print(f"Total weeks analyzed: {len(weekly_totals)}")
    print(f"Average weekly hours: {weekly_totals['Total_Hours'].mean():.1f}")
    print(f"Peak workload weeks: {sim.loc[sim['over_40h_prob'] > 0.5, 'Week'].tolist()}")
    print(f"Highest risk week: Week {sim.loc[sim['over_40h_prob'].idxmax(), 'Week']:.0f} ({sim['over_40h_prob'].max():.0%} probability)")
    print(f"Most demanding course: {courses.index[0]} ({courses.iloc[0]:.1f} total hours)")
    print(f"\nWeeks exceeding 40h: {(weekly_totals['Total_Hours'] > 40).sum()}")
    print(f"Maximum weekly hours: {weekly_totals['Total_Hours'].max():.1f}")

except Exception as e:
    print(f"\n❌ Error creating dashboard: {e}")
    import traceback
    traceback.print_exc()