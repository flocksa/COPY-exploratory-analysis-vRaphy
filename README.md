# NHANES-Exploratory-Analysis
The NHANES Profile API is a Flask-based service that builds a comprehensive patient profile by merging data from multiple NHANES survey cycles. Users provide file selections by data category and file description and cycle years, and the API returns a merged CSV file with the data. This API retrieves selected datasets (in SAS XPT format), converts them to CSV for readability, merges them based on the unique patient identifier (SEQN), and returns the final merged profile as a downloadable CSV file. The API is designed to help researchers, data scientists, and healthcare professionals build comprehensive patient profiles across multiple NHANES cycles.

# Features

Dynamic Data Merging:
Merge data from various NHANES data files (e.g., demographics, examination, laboratory, questionnaire) across different cycles.

Mapping-Based Download:
Uses a separate mapping module to translate human-readable file descriptions into the correct NHANES file identifiers.

XPT to CSV Conversion:
Automatically converts SAS XPT files to CSV format without altering blank columns (to allow for future data cleaning strategies).

Patient Profile Aggregation:
Merges data from various NHANES cycles on the common SEQN identifier to create a comprehensive patient profile.

RESTful API Endpoint:
Exposes a /profile endpoint that accepts a JSON payload with user selections and cycle years, and returns a merged CSV file.

Error Handling:
Logs errors and skips files that are unavailable or not in the expected format, ensuring the API continues to function.

# Installation
Prerequisites
Python 3.7 or higher

pip install

## Requirements

The minimal requirements for this project are:

- Flask
- pandas
- requests
- pyreadstat

You can install these dependencies with:

pip install -r requirements.txt

# Contributing
Contributions are welcome! If you have ideas for improvements or bug fixes, please open an issue or submit a pull request.

# License
This project is licensed under the MIT License. See the LICENSE file for details.

# Disclaimer
Please review the NHANES API disclaimer and usage restrictions before using this tool. The NHANES Profile API is designed for use with pre-pandemic cycle data (1999-2000 through 2017-2018) and may require updates for newer cycles.
