"""
Command Line Interface for License Updater.
"""

import argparse
from .core import update_licenses_from_dnf


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description=("Update 'License' column in a CSV based on "
                     "DNF API queries.")
    )
    parser.add_argument(
        "input_csv",
        type=str,
        help=("Path to the input CSV file (e.g., 'AIPCC base containers "
              "(2025-06-17) - CUDA 12.8 _ RHEL 9.4.csv')")
    )
    parser.add_argument(
        "-o", "--output_csv",
        type=str,
        help=("Optional: Path to save the updated CSV file. If not "
              "provided, the updated data will be printed to console.")
    )

    args = parser.parse_args()

    # Call the main function with provided arguments
    update_licenses_from_dnf(args.input_csv, args.output_csv)


if __name__ == "__main__":
    main() 