#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import os

# Check which files exist before trying to load them
print("Checking available files...")
for f in ['outputs/analysis-baseline/weekly_rollup.csv',
          'outputs/analysis-baseline/tasktype_by_course.csv',
          'outputs/analysis-simulation/simulation_results.csv']:
    if os.path.exists(f):
        print(f"✓ Found: {f}")
    else:
        print(f"✗ Missing: {f}")

try:
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle('Comprehensive Workload Analysis Dashboard', fontsize=16)

    # 1. Baseline weekly hours
    baseline = pd.read_csv("outputs/analysis-baseline/weekly_rollup.csv")
    ax1 = axes[0, 0]
    ax1.bar(baseline['Week'], baseline['duration_hours'], color='skyblue', alpha=0.7)
    ax1.axhline(y=40, color='r', linestyle='--', label='40h limit')
    ax1.set_title('Baseline: Actual Weekly Hours')
    ax1.set_xlabel('Week')
    ax1.set_ylabel('Hours')
    ax1.legend()

    # 2. Course distribution
    course_totals = pd.read_csv("outputs/analysis-baseline/tasktype_by_course.csv")
    ax2 = axes[0, 1]
    courses = course_totals.groupby('Course')['duration_hours'].sum().sort_values(ascending=False)
    ax2.bar(range(len(courses)), courses.values, tick_label=courses.index)
    ax2.set_title('Total Hours by Course')
    ax2.set_ylabel('Total Hours')
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)

    # 3. Simulation confidence intervals
    sim = pd.read_csv("outputs/analysis-simulation/simulation_results.csv")
    ax3 = axes[1, 0]
    ax3.plot(sim['Week'], sim['mean'], 'b-', linewidth=2, label='Mean')
    ax3.fill_between(sim['Week'], sim['lo'], sim['hi'], alpha=0.3, label='95% CI')
    ax3.axhline(y=40, color='r', linestyle='--')
    ax3.set_title('Monte Carlo: Projected Hours with Uncertainty')
    ax3.set_xlabel('Week')
    ax3.set_ylabel('Hours')
    ax3.legend()

    # 4. Risk heatmap
    ax4 = axes[1, 1]
    risk_data = sim[['Week', 'over_40h_prob']].set_index('Week')
    risk_matrix = risk_data.T
    sns.heatmap(risk_matrix, annot=True, fmt='.0%', cmap='Reds', 
                cbar_kws={'label': 'Probability'}, ax=ax4, vmin=0, vmax=1)
    ax4.set_title('Weekly Risk of Exceeding 40h Limit')
    ax4.set_ylabel('')

    plt.tight_layout()
    plt.savefig('outputs/final_dashboard.png', dpi=300, bbox_inches='tight')
    print("\n✅ Dashboard saved to outputs/final_dashboard.png")

    # Generate text summary
    print("\n=== EXECUTIVE SUMMARY ===")
    print(f"Total weeks analyzed: {len(baseline)}")
    print(f"Average weekly hours: {baseline['duration_hours'].mean():.1f}")
    print(f"Peak workload weeks: {sim.loc[sim['over_40h_prob'] > 0.5, 'Week'].tolist()}")
    print(f"Highest risk week: Week {sim.loc[sim['over_40h_prob'].idxmax(), 'Week']:.0f} ({sim['over_40h_prob'].max():.0%} probability)")
    print(f"Most demanding course: {courses.index[0]} ({courses.iloc[0]:.1f} total hours)")

except Exception as e:
    print(f"\n❌ Error creating dashboard: {e}")
    print("\nMake sure to run 'make all' first to generate all required files.")
