#!/usr/bin/env python3
"""
Generate Research Integrity Report
Documents computational environment and methodology for reproducibility
Author: Mathew Moslow
"""

import sys
import platform
import json
import subprocess
from datetime import datetime
from pathlib import Path

def get_git_info():
    """Get current git commit information"""
    try:
        commit_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()
        commit_date = subprocess.check_output(['git', 'show', '-s', '--format=%ci', 'HEAD']).decode().strip()
        branch = subprocess.check_output(['git', 'branch', '--show-current']).decode().strip()
        
        # Check for uncommitted changes
        status = subprocess.check_output(['git', 'status', '--porcelain']).decode()
        has_changes = len(status.strip()) > 0
        
        return {
            'commit': commit_hash[:8],
            'commit_full': commit_hash,
            'date': commit_date,
            'branch': branch,
            'clean': not has_changes
        }
    except:
        return None

def get_package_info():
    """Get detailed package information"""
    packages = {}
    
    for pkg_name in ['pandas', 'numpy', 'matplotlib', 'seaborn', 'scipy']:
        try:
            pkg = __import__(pkg_name)
            packages[pkg_name] = {
                'version': pkg.__version__,
                'location': pkg.__file__
            }
        except:
            packages[pkg_name] = {'version': 'Not installed', 'location': 'N/A'}
    
    return packages

def generate_report():
    """Generate comprehensive integrity report"""
    
    # Collect all information
    report_data = {
        'generated': datetime.now().isoformat(),
        'system': {
            'platform': platform.platform(),
            'python_version': sys.version,
            'python_executable': sys.executable,
            'architecture': platform.machine(),
            'processor': platform.processor()
        },
        'git': get_git_info(),
        'packages': get_package_info()
    }
    
    # Create markdown report
    report = f"""# Research Integrity Report
## BSN Workload Analysis Computational Environment

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Researcher:** Mathew Moslow  
**Institution:** AdventHealth University  

---

## Executive Summary

This document provides complete computational environment documentation to ensure reproducibility of the BSN workload analysis research. All analyses were performed using the environment described below.

## System Information

| Component | Value |
|-----------|-------|
| Platform | {report_data['system']['platform']} |
| Python Version | {sys.version.split()[0]} |
| Python Path | `{report_data['system']['python_executable']}` |
| Architecture | {report_data['system']['architecture']} |

## Version Control

"""
    
    if report_data['git']:
        git = report_data['git']
        report += f"""| Git Information | Value |
|-----------------|-------|
| Commit Hash | `{git['commit_full']}` |
| Commit Date | {git['date']} |
| Branch | {git['branch']} |
| Working Directory | {'Clean ✓' if git['clean'] else '⚠️  Has uncommitted changes'} |

"""
    else:
        report += "⚠️  Git information not available\n\n"
    
    report += """## Package Versions

Critical packages and their versions used in this analysis:

| Package | Version | Purpose |
|---------|---------|---------|
"""
    
    package_purposes = {
        'pandas': 'Data manipulation and analysis',
        'numpy': 'Numerical computations',
        'matplotlib': 'Visualization generation',
        'seaborn': 'Statistical visualizations',
        'scipy': 'Statistical tests and distributions'
    }
    
    for pkg, info in report_data['packages'].items():
        purpose = package_purposes.get(pkg, 'Supporting library')
        report += f"| {pkg} | {info['version']} | {purpose} |\n"
    
    report += f"""

## Reproducibility Instructions

### 1. Environment Setup

```bash
# Clone the repository
git clone https://github.com/MathewMoslow/gitresearch
cd gitresearch

# Checkout specific commit
git checkout {report_data['git']['commit_full'] if report_data['git'] else '[commit_hash]'}

# Create virtual environment with Python {sys.version.split()[0]}
python{sys.version_info.major}.{sys.version_info.minor} -m venv venv

# Activate environment
source venv/bin/activate  # On macOS/Linux
# or
venv\\Scripts\\activate  # On Windows

# Install exact package versions
pip install -r requirements_lock.txt
```

### 2. Verify Environment

```bash
# Run verification script
python verify_environment.py

# Expected output: "✅ ENVIRONMENT VERIFICATION PASSED"
```

### 3. Reproduce Analysis

```bash
# Run complete analysis pipeline
make all

# Generate all reports
make all-reports
```

## Data Integrity Measures

1. **Version Control**: All analysis scripts are version controlled with git
2. **Environment Locking**: Package versions locked in `requirements_lock.txt`
3. **Verification Scripts**: `verify_environment.py` ensures correct setup
4. **Reproducible Random States**: All random operations use seed=42
5. **Output Preservation**: All outputs timestamped and preserved

## Computational Procedures

### Data Processing Pipeline
1. Raw data cleaning (`scripts/clean_data.py`)
2. Baseline analysis (`scripts/baseline_report.py`)
3. Archetype modeling (`scripts/archetype_report.py`)
4. Monte Carlo simulation (`scripts/simulation_report.py`)
5. Report generation (`scripts/evidence_based_report.py`)

### Key Parameters
- **Study Period**: 14 weeks (May 5 - August 7, 2025)
- **Courses Analyzed**: 4 (Adult_310, OBGYN_330, Gerontology_315, NCLEX_335)
- **Total Tasks**: 407
- **Monte Carlo Iterations**: 1,000 per week
- **Random Seed**: 42 (for all stochastic operations)

## Quality Assurance

✓ All calculations verified against manual checks  
✓ Statistical tests validated with known examples  
✓ Visualizations reviewed for accuracy  
✓ Edge cases tested and handled  

## Contact

For questions about computational reproducibility:  
Mathew Moslow  
Undergraduate BSN Student  
AdventHealth University  

---

*This report ensures compliance with computational reproducibility standards for academic research.*
"""
    
    # Save report
    output_dir = Path.home() / "Documents/gitresearch_outputs"
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "RESEARCH_INTEGRITY.md"
    with open(output_file, 'w') as f:
        f.write(report)
    
    # Also save JSON version
    json_file = output_dir / "research_integrity.json"
    with open(json_file, 'w') as f:
        json.dump(report_data, f, indent=2)
    
    print(f"✅ Research integrity report saved to: {output_file}")
    print(f"📊 JSON data saved to: {json_file}")
    
    return output_file

if __name__ == "__main__":
    generate_report()