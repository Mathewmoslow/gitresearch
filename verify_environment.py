#!/usr/bin/env python3
"""
Research Environment Verification Script
Ensures computational reproducibility for BSN workload analysis
Author: Mathew Moslo
"""

import sys
import json
import hashlib
from datetime import datetime
from pathlib import Path

def check_python_version():
    """Verify Python version matches requirements"""
    required_major = 3
    required_minor = 13  # Adjust based on your actual Python version
    
    current_major = sys.version_info.major
    current_minor = sys.version_info.minor
    
    if current_major != required_major or current_minor < required_minor:
        return False, f"Python {required_major}.{required_minor}+ required, found {current_major}.{current_minor}"
    return True, f"Python {current_major}.{current_minor}.{sys.version_info.micro}"

def check_package_versions():
    """Verify critical package versions"""
    results = []
    issues = []
    
    # Critical packages for this research
    critical_packages = {
        'pandas': {
            'min_version': '2.0.0',
            'computation_test': lambda pd: pd.DataFrame({'x': [1, 2, 3]})['x'].mean() == 2.0
        },
        'numpy': {
            'min_version': '1.24.0',
            'computation_test': lambda np: np.array([1, 2, 3]).mean() == 2.0
        },
        'matplotlib': {
            'min_version': '3.5.0',
            'computation_test': lambda mpl: True  # Visual library, no computation test
        },
        'seaborn': {
            'min_version': '0.12.0',
            'computation_test': lambda sns: True
        },
        'scipy': {
            'min_version': '1.10.0',
            'computation_test': lambda sp: abs(sp.stats.norm.cdf(0) - 0.5) < 1e-10
        }
    }
    
    for package_name, requirements in critical_packages.items():
        try:
            package = __import__(package_name)
            version = package.__version__
            
            # Version check
            version_ok = version >= requirements['min_version']
            
            # Computation check
            computation_ok = requirements['computation_test'](package)
            
            if version_ok and computation_ok:
                results.append(f"✅ {package_name} {version}")
            else:
                if not version_ok:
                    issues.append(f"{package_name} version {version} < {requirements['min_version']}")
                if not computation_ok:
                    issues.append(f"{package_name} computation test failed")
                    
        except ImportError:
            issues.append(f"{package_name} not installed")
        except Exception as e:
            issues.append(f"{package_name} error: {str(e)}")
    
    return results, issues

def verify_data_processing():
    """Test critical data processing functions"""
    import pandas as pd
    import numpy as np
    
    tests_passed = []
    tests_failed = []
    
    # Test 1: Date parsing
    try:
        test_dates = pd.to_datetime(['2025-05-05', '2025-08-07'])
        if len(test_dates) == 2:
            tests_passed.append("Date parsing")
        else:
            tests_failed.append("Date parsing produced unexpected results")
    except Exception as e:
        tests_failed.append(f"Date parsing: {str(e)}")
    
    # Test 2: Statistical calculations
    try:
        data = pd.DataFrame({
            'hours': [36.6, 31.8, 25.8, 18.1, 38.0, 40.8, 42.1, 46.5, 46.1, 33.9, 35.1, 22.9, 16.8, 8.0]
        })
        mean_val = data['hours'].mean()
        std_val = data['hours'].std()
        
        if abs(mean_val - 31.6) < 0.1 and abs(std_val - 11.7) < 0.2:
            tests_passed.append("Statistical calculations")
        else:
            tests_failed.append(f"Stats mismatch: mean={mean_val:.2f}, std={std_val:.2f}")
    except Exception as e:
        tests_failed.append(f"Statistical calculations: {str(e)}")
    
    # Test 3: Random seed consistency
    try:
        np.random.seed(42)
        random_vals = np.random.rand(3)
        np.random.seed(42)
        random_vals2 = np.random.rand(3)
        
        if np.array_equal(random_vals, random_vals2):
            tests_passed.append("Random seed consistency")
        else:
            tests_failed.append("Random seed not producing consistent results")
    except Exception as e:
        tests_failed.append(f"Random seed test: {str(e)}")
    
    return tests_passed, tests_failed

def generate_environment_hash():
    """Generate a hash of the current environment for verification"""
    import pandas as pd
    import numpy as np
    
    env_string = f"{sys.version}|{pd.__version__}|{np.__version__}"
    return hashlib.sha256(env_string.encode()).hexdigest()[:16]

def save_verification_results(results):
    """Save verification results to file"""
    output_dir = Path.home() / "Documents/gitresearch_outputs"
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "environment_verification.json"
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    return output_file

def main():
    """Main verification routine"""
    print("=" * 60)
    print("RESEARCH ENVIRONMENT VERIFICATION")
    print("BSN Workload Analysis - Mathew Moslo")
    print("=" * 60)
    print()
    
    all_passed = True
    results = {
        'timestamp': datetime.now().isoformat(),
        'environment_hash': None,
        'python_version': None,
        'package_versions': [],
        'computation_tests': [],
        'issues': [],
        'status': 'PENDING'
    }
    
    # Check Python version
    print("Checking Python version...")
    py_ok, py_info = check_python_version()
    results['python_version'] = py_info
    if py_ok:
        print(f"✅ Python version: {py_info}")
    else:
        print(f"❌ Python version: {py_info}")
        results['issues'].append(py_info)
        all_passed = False
    
    # Check package versions
    print("\nChecking package versions...")
    pkg_results, pkg_issues = check_package_versions()
    results['package_versions'] = pkg_results
    
    for result in pkg_results:
        print(result)
    
    if pkg_issues:
        all_passed = False
        for issue in pkg_issues:
            print(f"❌ {issue}")
            results['issues'].append(issue)
    
    # Run computation tests
    print("\nRunning computation tests...")
    tests_passed, tests_failed = verify_data_processing()
    results['computation_tests'] = {
        'passed': tests_passed,
        'failed': tests_failed
    }
    
    for test in tests_passed:
        print(f"✅ {test}")
    
    if tests_failed:
        all_passed = False
        for test in tests_failed:
            print(f"❌ {test}")
            results['issues'].append(test)
    
    # Generate environment hash
    try:
        env_hash = generate_environment_hash()
        results['environment_hash'] = env_hash
        print(f"\nEnvironment hash: {env_hash}")
    except Exception as e:
        print(f"\n⚠️  Could not generate environment hash: {str(e)}")
    
    # Final verdict
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ENVIRONMENT VERIFICATION PASSED")
        print("All requirements met for reproducible research")
        results['status'] = 'PASSED'
    else:
        print("❌ ENVIRONMENT VERIFICATION FAILED")
        print(f"Found {len(results['issues'])} issues that need resolution")
        results['status'] = 'FAILED'
    print("=" * 60)
    
    # Save results
    output_file = save_verification_results(results)
    print(f"\nDetailed results saved to: {output_file}")
    
    # Exit with appropriate code
    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main()
