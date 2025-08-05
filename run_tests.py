#!/usr/bin/env python3
"""
Comprehensive Test Runner for TechScope Search Engine
Runs all tests with detailed reporting and coverage analysis.
"""

import unittest
import sys
import os
import time
import argparse
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def run_unit_tests():
    """Run unit tests."""
    print("\n" + "="*60)
    print("🧪 RUNNING UNIT TESTS")
    print("="*60)
    
    loader = unittest.TestLoader()
    start_dir = os.path.join(project_root, 'Tests', 'unit')
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

def run_integration_tests():
    """Run integration tests."""
    print("\n" + "="*60)
    print("🔗 RUNNING INTEGRATION TESTS")
    print("="*60)
    
    loader = unittest.TestLoader()
    start_dir = os.path.join(project_root, 'Tests', 'integration')
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

def run_edge_case_tests():
    """Run edge case tests."""
    print("\n" + "="*60)
    print("⚠️  RUNNING EDGE CASE TESTS")
    print("="*60)
    
    loader = unittest.TestLoader()
    start_dir = os.path.join(project_root, 'Tests', 'edge_cases')
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

def run_performance_tests():
    """Run performance tests."""
    print("\n" + "="*60)
    print("⚡ RUNNING PERFORMANCE TESTS")
    print("="*60)
    
    loader = unittest.TestLoader()
    start_dir = os.path.join(project_root, 'Tests', 'performance')
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

def run_all_tests():
    """Run all test categories."""
    print("🚀 TECH SCOPE SEARCH ENGINE - COMPREHENSIVE TEST SUITE")
    print("="*60)
    
    start_time = time.time()
    
    # Run all test categories
    unit_success = run_unit_tests()
    integration_success = run_integration_tests()
    edge_success = run_edge_case_tests()
    performance_success = run_performance_tests()
    
    end_time = time.time()
    total_time = end_time - start_time
    
    # Print summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    print(f"Unit Tests:        {'✅ PASSED' if unit_success else '❌ FAILED'}")
    print(f"Integration Tests: {'✅ PASSED' if integration_success else '❌ FAILED'}")
    print(f"Edge Case Tests:   {'✅ PASSED' if edge_success else '❌ FAILED'}")
    print(f"Performance Tests: {'✅ PASSED' if performance_success else '❌ FAILED'}")
    print(f"Total Time:        {total_time:.2f} seconds")
    
    all_passed = unit_success and integration_success and edge_success and performance_success
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED! Your search engine is ready for production!")
    else:
        print("\n⚠️  Some tests failed. Please review the output above.")
    
    return all_passed

def run_specific_test(test_path):
    """Run a specific test file."""
    print(f"🧪 Running specific test: {test_path}")
    
    loader = unittest.TestLoader()
    suite = loader.discover(os.path.dirname(test_path), pattern=os.path.basename(test_path))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

def main():
    """Main function with command line argument parsing."""
    parser = argparse.ArgumentParser(description='TechScope Search Engine Test Runner')
    parser.add_argument('--unit', action='store_true', help='Run only unit tests')
    parser.add_argument('--integration', action='store_true', help='Run only integration tests')
    parser.add_argument('--edge', action='store_true', help='Run only edge case tests')
    parser.add_argument('--performance', action='store_true', help='Run only performance tests')
    parser.add_argument('--file', type=str, help='Run a specific test file')
    parser.add_argument('--all', action='store_true', help='Run all tests (default)')
    
    args = parser.parse_args()
    
    # Default to all tests if no specific category is selected
    if not any([args.unit, args.integration, args.edge, args.performance, args.file]):
        args.all = True
    
    success = True
    
    if args.file:
        success = run_specific_test(args.file)
    elif args.all:
        success = run_all_tests()
    else:
        if args.unit:
            success = run_unit_tests()
        if args.integration:
            success = success and run_integration_tests()
        if args.edge:
            success = success and run_edge_case_tests()
        if args.performance:
            success = success and run_performance_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main() 