"""
Main entry point for running license_updater as a module.

Usage: python -m license_updater input.csv [-o output.csv]
"""

from .cli import main

if __name__ == "__main__":
    main() 