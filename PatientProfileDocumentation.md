# Patient Profile Builder Documentation

## Overview

The `PatientProfileBuilder` is a custom Python class that creates a comprehensive patient profile by retrieving and merging NHANES datasets. For each survey cycle and each selected data file (or attribute) in various categories, it:
- Retrieves the dataset using an NHANES API instance.
- Renames columns (except for the unique patient identifier, `SEQN`) by appending the cycle year. This prevents column name conflicts when the same attribute appears in multiple cycles.
- Merges the datasets within each cycle on the `SEQN` key.
- Finally, merges the cycle-specific profiles across all cycles into one unified DataFrame.

This document breaks down the builder’s structure, its key methods, and provides an example of how to use it.

## Class Structure

The builder is defined in a Python class named `PatientProfileBuilder`. Its key components are:

1. **Initialization**  
2. **Building the Profile (`build_profile` method)**  
3. **A Helper Function to Simplify Usage**

## 1. Class Initialization

```python
import pandas as pd

class PatientProfileBuilder:
    def __init__(self, api):
        """
        Initialize the PatientProfileBuilder with an instance of NHANESDataAPI.
        
        Args:
            api (NHANESDataAPI): An instance of the NHANESDataAPI class.
        """
        self.api = api
```