# Developing unit tests for Osdag using PyTest

This repository contains a comprehensive unit testing suite for verifying the output of Osdag modules (Cleat Angle Connection, Fin Plate Connection, and Tension Member Welded). It ensures the computational accuracy of the software by comparing module outputs against validated reference values derived from manual calculations and standard design examples.

## Demo Video

<a href="https://youtu.be/gwHn3yF81h8" target="_blank">
  <img src="https://img.youtube.com/vi/gwHn3yF81h8/maxresdefault.jpg" alt="Watch the Osdag Unit Testing Demo" width="600" />
</a>

*(Click the image to watch the demo on YouTube in a new tab)*

## Report

<a href="./report.pdf" target="_blank">👉🏻 Click Here for detailed PDF Report (Opens in new tab)</a>

## Technical Implementation

### Methodology
The testing framework utilizes **PyTest** to drive a data-driven verification process. The core logic involves:
1.  **Input Injection**: Reading standard Osdag input files (e.g., `CleatAngleTest1`) containing design parameters.
2.  **Module Execution**: Invoking the Osdag CLI runner (`osdag.cli.run_module`) to process these inputs.
3.  **Output Capture**: Intercepting the results returned by the module as a Python dictionary.
4.  **Assertion**: Comparing specific output keys against expected values defined in external CSV files.

### Key Components
*   **Test Driver (`test_osdag.py`)**: The main script that orchestrates the tests. It includes a `KEY_MAPPING` dictionary to resolve naming inconsistencies between the raw CSV headers (e.g., "Bolt Rows") and the internal Osdag output keys (e.g., `Bolt.Rows`).
*   **Reference Data (CSVs)**: Files like `CleatAngle.csv` serve as the "Ground Truth". They map each input file to a set of mandatory checks (e.g., Shear Capacity, Moment Capacity, Efficiency).
*   **Granular Reporting**: The suite supports both a high-level file-based check (did the file pass?) and a detailed property-based check (did the specific shear capacity match?).

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
    source venv/bin/activate    # On Windows: venv\Scripts\activate
    pip install pytest
    ```
    
    Ensure Osdag is in your Python path. If you cloned Osdag into a separate directory, add it to your current folder or `PYTHONPATH`.

## Running Tests

### Summary Run (12 File-based Checks)
Executes a consolidated check where each input file counts as one test case.
```bash
pytest test_osdag.py::test_consolidated_run
```
<img width="688" height="298" alt="image" src="https://github.com/user-attachments/assets/5c78f3aa-629c-4da4-b266-b26621ee2dab" />

### Detailed Run (48 Granular Checks)
Expands the test suite to verify individual parameters (e.g., weld strength, bolt capacity) separately for each file.
```bash
pytest -v test_osdag.py::TestOsdagModules
```
<img width="688" height="410" alt="image" src="https://github.com/user-attachments/assets/6c8baa76-3d27-474e-a632-fc444837b985" />

### All Tests
```bash
pytest test_osdag.py
```

## Test Cases Coverage
The tests cover three primary Osdag modules:

| Module | Test Files | Key Checks |
| :--- | :--- | :--- |
| **Cleat Angle** | 4 Files | Shear Capacity, Moment Capacity, Efficiency, Geometric Checks |
| **Fin Plate** | 4 Files | Bolt Shear, Plate Bearing, Weld Strength, Block Shear |
| **Tension Member** | 4 Files | Gross Yielding, Net Rupture, Block Shear Strength |

Each file is verified against expected values from the corresponding CSV files (`CleatAngle.csv`, `FinPlate.csv`, etc.).
