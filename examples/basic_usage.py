#!/usr/bin/env python3
"""
Basic usage example for license_updater package.
"""

from license_updater import update_licenses_from_dnf

def main():
    """Example of using license_updater to process a CSV file."""
    
    # Example 1: Process CSV and display results in console
    print("Example 1: Processing CSV with console output")
    update_licenses_from_dnf("sample.csv")
    
    print("\n" + "="*50 + "\n")
    
    # Example 2: Process CSV and save to new file
    print("Example 2: Processing CSV and saving to file")
    update_licenses_from_dnf("sample.csv", "updated_licenses.csv")
    print("Results saved to updated_licenses.csv")

if __name__ == "__main__":
    main() 