# Developing unit tests for Osdag using PyTest

This repository contains unit tests for the [Osdag](https://github.com/osdag-admin/Osdag) steel structure design software.

# Demo Video

YouTube : [https://youtu.be/gwHn3yF81h8](https://youtu.be/gwHn3yF81h8)

# Report

👉🏻 [Click Here for PDF Report](https://drive.google.com/file/d/1m2sZc41Mk9pl2ICUa8mIY4AwC2PrwqIC/view?usp=sharing)

## Requirements

*   Python 3.10+
*   PyTest
*   Osdag (cloned to `./Osdag`)

## Running Tests

### Summary Run (12 File-based Checks)
```bash
pytest test_osdag.py::test_consolidated_run
```
<img width="688" height="298" alt="image" src="https://github.com/user-attachments/assets/5c78f3aa-629c-4da4-b266-b26621ee2dab" />


### Detailed Run (48 Granular Checks)
```bash
pytest -v test_osdag.py::TestOsdagModules
```
<img width="688" height="410" alt="image" src="https://github.com/user-attachments/assets/6c8baa76-3d27-474e-a632-fc444837b985" />


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
