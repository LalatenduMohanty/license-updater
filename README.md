# license-updater

A Python script to update license information in CSV files by querying DNF repositories using the [DNF Python API](https://dnf.readthedocs.io/en/latest/api_queries.html).

The script was created using [cursor](https://cursor.com/)

## Requirements

Before running the script, install the required dependencies:

```bash
pip install -r requirements.txt
```

**Note**: This script requires the DNF Python library and DNF to be installed on your system. It's designed to work on Fedora, RHEL, CentOS, and other RPM-based distributions.

## Features

- Uses the DNF Python API for direct access to package repository information
- Processes CSV files with package information
- Automatically finds the latest version using DNF's built-in `latest()` method
- Proper EVR (Epoch, Version, Release) comparison for accurate version sorting
- Skips packages marked with `UBI? = yes`
- Supports both console output and CSV file output
- Comprehensive error handling for various edge cases
- Efficient single DNF base initialization for processing multiple packages

## Usage

```bash
# Display results in console
python license_updater.py input.csv

# Save results to a new CSV file
python license_updater.py input.csv -o output.csv
```

## CSV Format

The input CSV should have at least these columns:
- `UBI?`: Indicates whether to skip the package (script processes packages with "no")
- `package`: The name of the package to query
- `License`: Will be updated with the license information from DNF

## Testing

The project includes comprehensive unit tests that cover all major functions and edge cases. The tests use mocking to simulate the DNF API without requiring actual DNF installation or network access.

### Running Tests

You can run the tests using either pytest (recommended) or the standard unittest module:

```bash
# Using pytest (recommended for better output)
python -m pytest test_license_updater.py -v

# Using standard unittest module
python test_license_updater.py

# Run tests with coverage (if you have pytest-cov installed)
python -m pytest test_license_updater.py --cov=license_updater --cov-report=html
```

### Test Coverage

The test suite covers:
- **`get_package_license()`**: Success cases, DNF API error handling, multiple package versions
- **`is_newer_package()`**: EVR comparison logic, epoch/version/release comparison 
- **`update_licenses_from_dnf()`**: CSV processing, DNF initialization, file I/O error handling
- **Integration tests**: End-to-end processing with mocked DNF API components

All tests use proper mocking of DNF Base objects, Query objects, and Package objects to ensure they don't require actual DNF installation or network access during testing.

## A sample run
```
$ python license_updater.py sample.csv 
Processing package: boost-atomic.x86_64...
/home/lmohanty/Downloads/license-updater/license_updater.py:180: FutureWarning: Setting an item of incompatible dtype is deprecated and will raise an error in a future version of pandas. Value 'BSL-1.0 AND MIT AND Python-2.0.1' has dtype incompatible with float64, please explicitly cast to a compatible dtype first.
  df.loc[index, 'License'] = new_license
  Updated license for boost-atomic.x86_64: BSL-1.0 AND MIT AND Python-2.0.1
Processing package: boost-chrono.x86_64...
  Updated license for boost-chrono.x86_64: BSL-1.0 AND MIT AND Python-2.0.1
Processing package: boost-container.x86_64...
  Updated license for boost-container.x86_64: BSL-1.0 AND MIT AND Python-2.0.1
Processing package: boost-context.x86_64...
  Updated license for boost-context.x86_64: BSL-1.0 AND MIT AND Python-2.0.1
Processing package: boost-contract.x86_64...
  Updated license for boost-contract.x86_64: BSL-1.0 AND MIT AND Python-2.0.1
Processing package: boost-coroutine.x86_64...
  Updated license for boost-coroutine.x86_64: BSL-1.0 AND MIT AND Python-2.0.1
Processing package: boost-date-time.x86_64...
  Updated license for boost-date-time.x86_64: BSL-1.0 AND MIT AND Python-2.0.1
Processing package: boost-fiber.x86_64...
  Updated license for boost-fiber.x86_64: BSL-1.0 AND MIT AND Python-2.0.1
Processing package: boost-filesystem.x86_64...
  Updated license for boost-filesystem.x86_64: BSL-1.0 AND MIT AND Python-2.0.1
Processing package: boost-graph.x86_64...
  Updated license for boost-graph.x86_64: BSL-1.0 AND MIT AND Python-2.0.1
Processing package: boost-iostreams.x86_64...
  Updated license for boost-iostreams.x86_64: BSL-1.0 AND MIT AND Python-2.0.1

--- Updated DataFrame (first 20 rows) ---
| UBI?   | package                 | License                          |
|:-------|:------------------------|:---------------------------------|
| no     | boost-atomic.x86_64     | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-chrono.x86_64     | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-container.x86_64  | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-context.x86_64    | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-contract.x86_64   | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-coroutine.x86_64  | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-date-time.x86_64  | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-fiber.x86_64      | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-filesystem.x86_64 | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-graph.x86_64      | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-iostreams.x86_64  | BSL-1.0 AND MIT AND Python-2.0.1 |

--- Updated DataFrame (last 20 rows) ---
| UBI?   | package                 | License                          |
|:-------|:------------------------|:---------------------------------|
| no     | boost-atomic.x86_64     | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-chrono.x86_64     | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-container.x86_64  | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-context.x86_64    | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-contract.x86_64   | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-coroutine.x86_64  | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-date-time.x86_64  | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-fiber.x86_64      | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-filesystem.x86_64 | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-graph.x86_64      | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-iostreams.x86_64  | BSL-1.0 AND MIT AND Python-2.0.1 |
```
