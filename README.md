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

## Installation & Setup

1.  **Clone the Osdag Repository**:
    ```bash
    git clone https://github.com/osdag-org/Osdag.git
    ```
    *Note: Ensure you are on the correct branch compatible with these tests if applicable.*

2.  **Clone this Test Repository**:
    ```bash
    git clone https://github.com/arry-codes/osdag_unittesting.git
    ```

3.  **Set up the Environment**:
    It is recommended to use a virtual environment.
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install pytest
    ```
    
    Ensure `Osdag` is in your Python path. If you cloned Osdag into a separate directory, add it to `PYTHONPATH`:
    ```bash
    export PYTHONPATH=$PYTHONPATH:/path/to/Osdag
    ```
    (Or install Osdag dependencies as per its documentation).

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
