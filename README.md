# license-updater

A Python script to update license information in CSV files by querying DNF repositories using the DNF Python API.

The script was created using [cursor](https://cursor.com/)

## Requirements

Before running the script, install the required dependencies:

```bash
pip install -r requirements.txt
```

**Note**: The `dnf` Python library requires DNF to be installed on your system. This script is designed to work on Fedora, RHEL, CentOS, and other RPM-based distributions.

## Features

- Uses the DNF Python API instead of subprocess calls for better performance and reliability
- Processes CSV files with package information
- Automatically finds the latest version of packages when multiple versions are available
- Skips packages marked with `UBI? = yes`
- Supports both console output and CSV file output

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
