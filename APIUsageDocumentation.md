# NHANES Profile API Usage Documentation

## Overview
The NHANES Profile API is a Flask-based RESTful service that retrieves, processes, and merges NHANES datasets into a single patient profile. Each patient is identified by a unique SEQN, and data from multiple survey cycles are merged into one comprehensive CSV file.

## Features
- **Dynamic Data Retrieval:** Fetch selected NHANES datasets based on user-provided file descriptions and cycles.
- **XPT to CSV Conversion:** Convert SAS XPT files to CSV format for readability.
- **Patient Profile Aggregation:** Merge data on the common patient identifier (SEQN) across different cycles.
- **RESTful API Endpoint:** Exposes a `/profile` endpoint for generating the patient profile via POST requests.
- **Error Handling:** Skips missing files or files that aren’t in valid XPT format, logging warnings as needed.

## Installation

### Prerequisites
- Python 3.7 or higher
- pip

### Steps
1. **Clone the Repository:**
   ```python
   git clone https://github.com/wvddy/nhanes-profile-api.git
   cd nhanes-profile-api
   ```
2. **(Optional) Create a Virtual Environment:
    ```python
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3. Install Dependencies (see requirements.txt):
    Flask
    pandas
    nhanes_pytool_api
4. Run requirements.text to ensure depdendencies install:
    ```python
    pip install -r requirements.txt
    ```
### Running API Locally 
1. **Start the Flask Server**: Ensure your app.py contains:
    ```python
    if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
2. Then run: 
    ```python
    python app.py
    ```
Your server will run on http://0.0.0.0:5000/

3. GitHub Codespaces Port Forwarding:
   
    In Codespaces, open the Ports tab.
    Locate port 5000 and click the "Make public" button to obtain a public URL.

### API Endpoint
### POST /profile

Description:
Generates a merged patient profile CSV file based on the provided selections and cycles.

Request Payload:
A JSON object with:
    selections: A dictionary mapping data categories (e.g., "demographics", "examination") to lists of file descriptions.
    cycles: A list of survey cycle years (e.g., ["1999-2000", "2001-2002", ...]).