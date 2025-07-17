"""
License Updater - A tool for updating package license information in CSV files.

This package provides functionality to query DNF repositories and update
license information for packages listed in CSV files.
"""

from .core import (
    get_package_license,
    is_newer_package,
    update_licenses_from_dnf
)

__version__ = "1.0.0"
__author__ = "License Updater Project"
__email__ = "your.email@example.com"

__all__ = [
    "get_package_license",
    "is_newer_package", 
    "update_licenses_from_dnf"
] 