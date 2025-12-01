import json
import pytest
from io import StringIO
import pandas as pd
from nhanes_api import app

# Automatically set the DUMMY_DOWNLOAD environment variable for all tests.
@pytest.fixture(autouse=True)
def set_dummy_download(monkeypatch):
    monkeypatch.setenv("DUMMY_DOWNLOAD", "1")

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_profile_endpoint_success(client):
    payload = {
        "selections": {
            "demographics": ["Demographic Variables & Sample Weights"],
            "examination": ["Blood Pressure", "Body Measures"],
            "laboratory": ["Cholesterol - LDL & Triglycerides"],
            "questionnaire": ["Alcohol Use"]
        },
        "cycles": ["1999-2000", "2001-2002"]
    }
    
    response = client.post("/profile", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    assert "attachment" in response.headers.get("Content-Disposition", ""), "Response does not contain an attachment."

def test_profile_endpoint_missing_payload(client):
    response = client.post("/profile", data=json.dumps({}), content_type="application/json")
    assert response.status_code == 400, f"Expected 400 Bad Request, got {response.status_code}"

def test_profile_endpoint_single_cycle(client):
    """
    Test using only one cycle to ensure the API handles single-cycle data merges.
    """
    payload = {
        "selections": {
            "examination": ["Blood Pressure"]
        },
        "cycles": ["1999-2000"]
    }
    response = client.post("/profile", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    assert "attachment" in response.headers.get("Content-Disposition", ""), "Response does not contain an attachment."

def test_profile_endpoint_invalid_cycle(client):
    """
    Test what happens when we pass an invalid cycle.
    """
    payload = {
        "selections": {
            "examination": ["Blood Pressure"]
        },
        "cycles": ["9999-9999"]  # An invalid cycle
    }
    response = client.post("/profile", data=json.dumps(payload), content_type="application/json")
    # Depending on how the code handles unknown cycles, expect 404 or 500.
    assert response.status_code in [404, 500], f"Expected 404 or 500 for invalid cycle, got {response.status_code}"

def test_profile_endpoint_invalid_file_description(client):
    """
    Test what happens when we pass an invalid file description.
    """
    payload = {
        "selections": {
            "examination": ["Nonexistent File Desc"]
        },
        "cycles": ["1999-2000"]
    }
    response = client.post("/profile", data=json.dumps(payload), content_type="application/json")
    # If the mapping function raises an exception, expect 500 (or 404 if no data is retrieved)
    assert response.status_code in [404, 500], f"Expected 404 or 500 for invalid file description, got {response.status_code}"

def test_profile_endpoint_empty_selections(client):
    """
    Test what happens when we pass an empty dictionary for selections.
    """
    payload = {
        "selections": {},
        "cycles": ["1999-2000"]
    }
    response = client.post("/profile", data=json.dumps(payload), content_type="application/json")
    # Our API returns 400 when selections are empty.
    assert response.status_code == 400, f"Expected 400 Bad Request, got {response.status_code}"

def test_profile_endpoint_with_filters(client):
    """
    Test the /profile endpoint with a demographics filter.
    The dummy demographics DataFrame (from dummy mode) is:
      - SEQN: [1,2,3,4]
      - RIDAGEYR: [25,35,45,85]
      - RIAGENDR: [1,2,2,1]    (1 = Male, 2 = Female)
      - RIDRETH1: [3,3,4,5]     (3 = Non-Hispanic White, etc.)
    
    With filters:
      - age_range: "20-39" selects rows with RIDAGEYR between 20 and 39.
      - gender: "Female" maps to 2.
      - race: "Non-Hispanic White" maps to 3.
    
    Only row with SEQN 2 (age=35, RIAGENDR=2, RIDRETH1=3) should match.
    """
    payload = {
        "selections": {
            "demographics": {
                "file": "Demographic Variables & Sample Weights",
                "filters": {
                    "age_range": "20-39",
                    "gender": "Female",
                    "race": "Non-Hispanic White"
                }
            }
        },
        "cycles": ["1999-2000"]
    }
    
    response = client.post("/profile", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    
    # Read the CSV content from the response.
    csv_data = response.data.decode("utf-8")
    df = pd.read_csv(StringIO(csv_data))
    assert not df.empty, "Profile DataFrame should not be empty."
    # You might also want to check that only one row is returned and that its SEQN is 2.
    assert len(df) == 1, "Expected only one row after filtering."
    assert df["SEQN"].iloc[0] == 2, "Expected SEQN 2 after filtering."
