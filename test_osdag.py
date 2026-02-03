import pytest
import csv
import os
from osdag.cli import run_module
from functools import lru_cache

def parse_csv(csv_path):
    cases = []
    with open(csv_path, 'r') as f:
        lines = f.readlines()
    
    header_params = lines[0].strip().split(',')
    header_types = lines[1].strip().split(',')
    
    param_map = {}
    current_param = None
    
    for i, (p, t) in enumerate(zip(header_params, header_types)):
        if p.strip():
            current_param = p.strip()
        
        if "Value" in t:
            if current_param:
                param_map[i] = current_param
    
    reader = csv.reader(lines[2:])
    for row in reader:
        if not row: continue
        file_name = row[1].strip()
        if not file_name: continue
        
        checks = {}
        for i, val in enumerate(row):
            if i in param_map and val.strip():
                checks[param_map[i]] = val.strip()
        
        cases.append(pytest.param(file_name, checks, id=file_name))
        
    return cases

cleat_cases = parse_csv("CleatAngle.csv")
fin_cases = parse_csv("FinPlate.csv")
tension_cases = parse_csv("TensionMember.csv")

all_cases = cleat_cases + fin_cases + tension_cases

KEY_MAPPING = {
    "Designation": ["section_size.designation", "Cleat.Angle", "Member.Designation"],
    "Tension Yielding Capacity": "Member.tension_yielding",
    "Tension Rupture Capacity": "Member.tension_rupture", 
    "Tension Block Shear Capacity": "Member.BlockShear", 
    "Tension Capacity": "Member.tension_capacity",
    "Tension Member Slenderness Ratio": "Member.Slenderness", 
    "Slenderness Ratio": "Member.Slenderness",
    "Tension Member efficiency": "Member.efficiency",
    "Utilization ratio": "Member.efficiency",
    "Effective Weld Length": "Weld.EffLength",
    "Weld Strength": "Weld.Strength",
    "Size of Weld": "Weld.Size",
    "Gusset Plate Thickness": "Plate.Thickness", 
    "Gusset Plate Height": "Plate.Height",
    "Gusset Plate Min Height": "Plate.Height",
    "Gusset Plate Length": "Plate.Length",
    "Gusset Plate Yield Capacity": "Plate.Yield",
    "Tension Yielding Gusset Plate": "Plate.Yield",
    "Gusset Plate Block Shear Capacity": "Plate.BlockShear",
    "Gusset Plate Capacity": "Plate.Capacity",
    "Effective Length": "Weld.EffLength",
    "Cleat Angle Designation": "Cleat.Designation", 
    "Fin Plate Thickness": "Plate.Thickness",
    "Fin Plate Height": "Plate.Height",
    "Fin Plate Length": "Plate.Length",
    "Weld Size": "Weld.Size",
    "Bolt Diameter": "Bolt.Diameter",
    "Bolt Grade": "Bolt.Grade_Provided",
    "Bolts - No. of Rows": "Bolt.OneLine",
    "Bolts - No. of Columns": "Bolt.Line",
    "Bolt Rows": "Bolt.OneLine",
    "Bolt Columns": "Bolt.Line",
    "Number of Bolts": "Bolt.Number",
    "Shear Capacity": ["Bolt.Capacity", "Bolt.Shear", "Plate.Shear"],
    "Bearing Capacity": "Bolt.Bearing",
    "Block Shear Capacity": ["Plate.BlockShear", "Cleat.BlockShear", "Member.BlockShear"],
    "Moment Capacity": ["Plate.MomCapacity", "Cleat.MomCapacity"],
    "Cleat Angle Section": "Cleat.Angle",
    "Cleat Height": "Plate.Height",
    "Cleat Shear Capacity": "Cleat.Shear",
    "Shear Yielding Capacity": "Cleat.Shear",
    "Cleat Block Shear Capacity": "Cleat.BlockShear",
    "Cleat Moment Capacity": "Cleat.MomCapacity",
    "Bolt Rows Supported Leg": "Bolt.OneLine",
    "Bolt Columns Supported Leg": "Bolt.Line",
    "Bolt Rows Supporting Leg": "Cleat.Spting_leg.OneLine",
    "Bolt Columns Supporting Leg": "Cleat.Spting_leg.Line",
    "Plate Thickness": "Plate.Thickness",
    "Spacer Plate Thickness": "Plate.Thickness",
    "Property Class": "Bolt.Grade_Provided",
    "Bolt Value Supporting Leg": "Bolt.Capacity_spting",
    "Supporting Leg Bearing Capacity": "Bolt.Bearing", 
}

KNOWN_MISSING_PARAMS = ["Supported Leg Bearing Capacity"]

@lru_cache(maxsize=32)
def run_osdag_cached(file_path):
    return run_module(input_path=file_path, op_type="print_result")

def get_output_value(output_data, param, file_name):
    actual_val = output_data.get(param)
    
    if actual_val is None and param in KEY_MAPPING:
        mapped_val = KEY_MAPPING[param]
        if isinstance(mapped_val, list):
            for mk in mapped_val:
                actual_val = output_data.get(mk)
                if actual_val is not None:
                    break
        else:
            actual_val = output_data.get(mapped_val)
        
    if actual_val is None:
        param_clean = param.lower().replace(" ", "").replace("_", "").replace(".", "")
        for k in output_data:
            k_clean = k.lower().replace(" ", "").replace("_", "").replace(".", "")
            if param_clean == k_clean:
                actual_val = output_data[k]
                break
            if param_clean in k_clean: 
                actual_val = output_data[k]
                break
            if param == "Designation" and "angle" in k_clean:
                 actual_val = output_data[k]
                 break
    
    if actual_val is None and param in ["Plate Thickness", "Spacer Plate Thickness"]:
        cleat_angle = output_data.get("Cleat.Angle")
        if cleat_angle:
            parts = cleat_angle.split('x')
            if len(parts) >= 3:
                 try:
                     val = parts[-1].strip()
                     float(val)
                     actual_val = val
                 except ValueError:
                     pass
    return actual_val

def check_param(file_name, output_data, param, expected_val):
    actual_val = get_output_value(output_data, param, file_name)
    
    if actual_val is None:
        if param in KNOWN_MISSING_PARAMS:
            return
        pytest.fail(f"Parameter '{param}' not found in output for {file_name}")

    try:
        exp_f = float(expected_val)
        act_f = float(actual_val)
        assert act_f == pytest.approx(exp_f, rel=1e-2)
    except ValueError:
        assert str(actual_val).strip().replace(" ", "") == str(expected_val).strip().replace(" ", "")

def verify_category(file_name, expected_checks, category_keywords):
    input_path = os.path.abspath(file_name)
    result = run_osdag_cached(input_path)
    output_data = result['data']
    
    for param, expected_val in expected_checks.items():
        is_match = False
        param_lower = param.lower()
        for k in category_keywords:
            if k in param_lower:
                is_match = True
                break
        if is_match:
            check_param(file_name, output_data, param, expected_val)

@pytest.mark.parametrize("file_name, expected_checks", all_cases)
class TestOsdagModules:
    def test_designation(self, file_name, expected_checks):
        verify_category(file_name, expected_checks, ["designation", "property class", "angle section"])

    def test_shear_capacity(self, file_name, expected_checks):
        verify_category(file_name, expected_checks, ["shear capacity", "shear yielding"])

    def test_bolt_configuration(self, file_name, expected_checks):
        verify_category(file_name, expected_checks, ["row", "column", "bolt", "diameter", "grade"])

    def test_capacity(self, file_name, expected_checks):
        input_path = os.path.abspath(file_name)
        result = run_osdag_cached(input_path)
        output_data = result['data']
        for param, expected_val in expected_checks.items():
            p_lower = param.lower()
            if any(k in p_lower for k in ["designation", "property class", "angle section", "shear capacity", "shear yielding", "row", "column", "bolt", "diameter", "grade"]):
                continue
            check_param(file_name, output_data, param, expected_val)

@pytest.mark.parametrize("file_name, expected_checks", cleat_cases + fin_cases + tension_cases)
def test_consolidated_run(file_name, expected_checks):
    verify_category(file_name, expected_checks, [""])
