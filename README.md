# license-updater

A Python package for updating license information in CSV files by querying DNF repositories using the [DNF Python API](https://dnf.readthedocs.io/en/latest/api_queries.html).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)


## Installation

### Option 1: Development Installation (Recommended)
```bash
# Clone the repository
git clone https://github.com/yourusername/license-updater.git
cd license-updater

# Install in development mode with all dependencies
pip install -e ".[dev]"
```

### Option 2: Production Installation
```bash
# Install production dependencies only
pip install -e .
```

### Option 3: Manual Installation
```bash
# Install required dependencies
pip install -r requirements.txt
```

**System Requirements**: 
- Python 3.8+
- DNF package manager installed on your system
- Works on Fedora, RHEL, CentOS, and other RPM-based distributions

## Usage

### 1. Command Line Interface

```bash
# Process CSV and display results in console
python -m license_updater examples/sample.csv

# Process CSV and save to new file
python -m license_updater examples/sample.csv -o updated_licenses.csv

# Alternative: using the CLI module directly
python license_updater/cli.py examples/sample.csv
```

### 2. Python Library Usage

```python
from license_updater import update_licenses_from_dnf, get_package_license

# Process entire CSV file
update_licenses_from_dnf("input.csv", "output.csv")

# Get license for a single package
license_info = get_package_license("boost-atomic.x86_64")
print(f"License: {license_info}")
```

### 3. Development Automation

```bash
# Run all tests
make test

# Run tests with coverage
make test-cov

# Format code
make format

# Run linting
make lint

# Full development workflow (format + lint + test)
make dev

# Clean build artifacts
make clean

# Build distribution packages
make build
```

## Project Structure

```
license-updater/
├── examples/                 # Usage examples and sample data
│   ├── basic_usage.py       # Programming examples
│   └── sample.csv           # Test data
├── license_updater/         # Main package
│   ├── __init__.py          # Package exports and metadata
│   ├── __main__.py          # Module entry point (python -m)
│   ├── cli.py               # Command line interface
│   └── core.py              # Core functionality
├── tests/                   # Test suite
│   ├── __init__.py          # Test package
│   └── test_license_updater.py # Comprehensive tests
├── LICENSE                  # MIT license
├── Makefile                 # Development automation
├── pyproject.toml          # Modern Python packaging configuration  
├── README.md               # This file
└── requirements.txt        # Production dependencies
```

## CSV Format

The input CSV should contain at least these columns:

| Column | Description | Example |
|--------|-------------|---------|
| `UBI?` | Skip indicator ("no" = process, "yes" = skip) | `no` |
| `package` | Package name (with or without architecture) | `boost-atomic.x86_64` |
| `License` | License field to be updated | *(will be filled)* |

**Example CSV:**
```csv
UBI?,package,License
no,boost-atomic.x86_64,
no,boost-chrono.x86_64,
yes,ubi-package,
```

## Testing

The project includes comprehensive unit tests covering all functionality:

### Running Tests

```bash
# Using make (recommended)
make test

# Using pytest directly
python -m pytest tests/ -v

# With coverage report
make test-cov

# Run specific test
python -m pytest tests/test_license_updater.py::TestGetPackageLicense -v
```

## Development

### Setting Up Development Environment

```bash
# 1. Clone and install
git clone https://github.com/yourusername/license-updater.git
cd license-updater
make install-dev

# 2. Run development workflow
make dev

# 3. Make changes and test
make test
```

### Available Make Commands

| Command | Description |
|---------|-------------|
| `make help` | Show all available commands |
| `make install` | Install production dependencies |
| `make install-dev` | Install development dependencies |
| `make test` | Run test suite |
| `make test-cov` | Run tests with coverage report |
| `make lint` | Run code linting (flake8, mypy) |
| `make format` | Format code (black, isort) |
| `make clean` | Clean build artifacts |
| `make build` | Build distribution packages |
| `make dev` | Full development workflow |

### Code Quality

The project uses modern Python development tools:

- **Black**: Code formatting
- **isort**: Import sorting  
- **flake8**: Linting
- **mypy**: Type checking
- **pytest**: Testing framework

## Example Output

```bash
$ python -m license_updater examples/sample.csv

Initializing DNF base and loading repository metadata...
DNF initialization complete.
Processing package: boost-atomic.x86_64...
  Updated license for boost-atomic.x86_64: BSL-1.0 AND MIT AND Python-2.0.1
Processing package: boost-chrono.x86_64...
  Updated license for boost-chrono.x86_64: BSL-1.0 AND MIT AND Python-2.0.1

--- Updated DataFrame (first 20 rows) ---
| UBI?   | package                 | License                          |
|:-------|:------------------------|:---------------------------------|
| no     | boost-atomic.x86_64     | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-chrono.x86_64     | BSL-1.0 AND MIT AND Python-2.0.1 |
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run the development workflow (`make dev`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built using [Cursor](https://cursor.com/) AI-assisted development
- Uses the [DNF Python API](https://dnf.readthedocs.io/en/latest/api_queries.html) for package queries
- Inspired by the need for automated license compliance in container environments
