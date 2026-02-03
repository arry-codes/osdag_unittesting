# Osdag Unit Testing

This repository contains unit tests for the [Osdag](https://github.com/osdag-admin/Osdag) steel structure design software.

## Requirements

*   Python 3.10+
*   PyTest
*   Osdag (cloned to `./Osdag`)

## Setup

```bash
# Clone this repo
git clone https://github.com/arry-codes/osdag_unittesting.git
cd osdag_unittesting

# Clone Osdag source
git clone https://github.com/osdag-admin/Osdag.git

# Install dependencies
pip install pytest

# Set PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)/Osdag/src
```

## Running Tests

### Summary Run (12 File-based Checks)
```bash
pytest test_osdag.py::test_consolidated_run
```

### Detailed Run (48 Granular Checks)
```bash
pytest -v test_osdag.py::TestOsdagModules
```

### All Tests
```bash
pytest test_osdag.py
```

## Test Cases

The tests cover three Osdag modules:

1.  **Cleat Angle Connection** (4 test files)
2.  **Fin Plate Connection** (4 test files)
3.  **Tension Member (Welded)** (4 test files)

Each file is verified against expected values from the corresponding CSV files.
