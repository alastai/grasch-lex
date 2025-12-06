#!/usr/bin/env python3
"""
Run regression tests from Phase A through Phase E locations
to verify the GraphSchemaContent fix works correctly.
"""

import subprocess
import sys

# Define test scripts in order
TESTS = [
    ("Phase A", "validate_phase_a.py"),
    ("Phase B", "validate_phase_b.py"),
    ("Phase C", "validate_phase_c.py"),
    ("Phase D", "validate_phase_d.py"),
    ("Phase E", "validate_phase_e.py"),
    ("Phase E Locations 2-3", "validate_phase_e_locations_2_3.py"),
    ("Phase E Locations 4-5", "validate_phase_e_locations_4_5.py"),
]

def run_test(name, script):
    """Run a single test script"""
    print(f"\n{'='*60}")
    print(f"Running: {name}")
    print(f"Script: {script}")
    print('='*60)
    
    try:
        result = subprocess.run(
            ["python", script],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            print(f"✓ {name} PASSED")
            return True
        else:
            print(f"✗ {name} FAILED (exit code {result.returncode})")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"✗ {name} TIMEOUT")
        return False
    except FileNotFoundError:
        print(f"✗ {name} - Script not found: {script}")
        return False
    except Exception as e:
        print(f"✗ {name} ERROR: {e}")
        return False

def main():
    """Run all regression tests"""
    print("="*60)
    print("REGRESSION TEST SUITE")
    print("Testing GraphSchemaContent fix (Location 1)")
    print("="*60)
    
    results = []
    for name, script in TESTS:
        passed = run_test(name, script)
        results.append((name, passed))
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n🎉 All regression tests PASSED!")
        return 0
    else:
        print(f"\n⚠️  {total_count - passed_count} test(s) FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())
