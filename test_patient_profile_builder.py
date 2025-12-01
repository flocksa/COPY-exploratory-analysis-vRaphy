import pandas as pd
import pytest
from patient_profile_builder import PatientProfileBuilder

class DummyNHANESAPI:
    def list_file_names(self, category, cycle):
        if category == "demographics":
            return ["Demographic Variables & Sample Weights"]
        elif category == "examination":
            return ["Blood Pressure", "Body Measures"]
        elif category == "laboratory":
            return ["Cholesterol - LDL & Triglycerides"]
        elif category == "questionnaire":
            return ["Alcohol Use"]
        return []

    def retrieve_data(self, category, cycle, file_desc):
        # Only return dummy data if the file description is recognized.
        if file_desc not in self.list_file_names(category, cycle):
            return None
        dummy_col = file_desc.replace(' ', '_')
        return pd.DataFrame({"SEQN": [1, 2], dummy_col: [100, 200]})

@pytest.fixture
def dummy_api():
    return DummyNHANESAPI()

@pytest.fixture
def selections():
    # This fixture returns selections for demographics and examination categories.
    return {
        "demographics": ["Demographic Variables & Sample Weights"],
        "examination": ["Blood Pressure", "Body Measures"]
    }

@pytest.fixture
def cycles():
    return ["1999-2000"]

def test_build_profile_single_cycle(dummy_api):
    """
    Test building a profile with only one cycle.
    """
    # Wrap dummy_api.retrieve_data so that it matches the expected signature.
    builder = PatientProfileBuilder(lambda c, fd, cat: dummy_api.retrieve_data(cat, c, fd))
    selections = {
        "examination": ["Blood Pressure"]
    }
    cycles = ["1999-2000"]
    df = builder.build_profile(selections, cycles)
    assert not df.empty, "Profile DataFrame should not be empty for single cycle."
    # Check that the renamed column is present.
    assert "Blood_Pressure_1999-2000" in df.columns, "Expected renamed column not found."

def test_build_profile_multiple_categories(dummy_api, selections, cycles):
    """
    Test building a profile with multiple categories in a single cycle.
    """
    # Use a lambda that wraps dummy_api.retrieve_data, accepting extra kwargs.
    download_func = lambda cycle, file_desc, category, **kwargs: dummy_api.retrieve_data(category, cycle, file_desc)
    builder = PatientProfileBuilder(download_func)
    df = builder.build_profile(selections, cycles)
    assert not df.empty, "Profile DataFrame should not be empty."
    # Check for columns from each file description
    expected_demo_col = "Demographic_Variables_&_Sample_Weights_1999-2000"
    expected_bp_col = "Blood_Pressure_1999-2000"
    expected_bmx_col = "Body_Measures_1999-2000"
    assert expected_demo_col in df.columns, f"Expected column {expected_demo_col} not found, got {list(df.columns)}"
    assert expected_bp_col in df.columns, f"Expected column {expected_bp_col} not found, got {list(df.columns)}"
    assert expected_bmx_col in df.columns, f"Expected column {expected_bmx_col} not found, got {list(df.columns)}"

def test_build_profile_no_data(dummy_api):
    """
    Test that a selection with a nonexistent file description returns an empty DataFrame.
    """
    builder = PatientProfileBuilder(lambda c, fd, cat: dummy_api.retrieve_data(cat, c, fd))
    selections = {
        "examination": ["Nonexistent File Desc"]
    }
    cycles = ["1999-2000"]
    df = builder.build_profile(selections, cycles)
    # Expect an empty DataFrame because retrieve_data returns None
    assert df.empty, "Profile DataFrame should be empty when no data is retrieved."

def test_build_profile_multiple_cycles(dummy_api):
    """
    Test building a profile with multiple cycles and multiple categories.
    """
    builder = PatientProfileBuilder(lambda c, fd, cat, **kwargs: dummy_api.retrieve_data(cat, c, fd))
    selections = {
        "examination": ["Blood Pressure", "Body Measures"]
    }
    cycles = ["1999-2000", "2001-2002"]
    df = builder.build_profile(selections, cycles)
    assert not df.empty, "Profile DataFrame should not be empty."
    # Check that columns for each cycle are present
    expected_bp_1 = "Blood_Pressure_1999-2000"
    expected_bp_2 = "Blood_Pressure_2001-2002"
    expected_bmx_1 = "Body_Measures_1999-2000"
    expected_bmx_2 = "Body_Measures_2001-2002"
    cols = list(df.columns)
    assert expected_bp_1 in cols, f"Expected {expected_bp_1} in columns, got {cols}"
    assert expected_bp_2 in cols, f"Expected {expected_bp_2} in columns, got {cols}"
    assert expected_bmx_1 in cols, f"Expected {expected_bmx_1} in columns, got {cols}"
    assert expected_bmx_2 in cols, f"Expected {expected_bmx_2} in columns, got {cols}"
