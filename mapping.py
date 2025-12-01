# A dictionary mapping cycle years to file mappings for each category.

FILE_MAPPING = {
    "1999-2000": {
        "demographics": {
            "Demographic Variables & Sample Weights": "DEMO"
        },
        "examination": {
            "Blood Pressure": "BPX",
            "Body Measures": "BMX",
            "Cardiovascular Fitness": "CVX"
        },
        "laboratory": {
            "Cholesterol - LDL & Triglycerides": "LAB13AM",
            "Plasma Fasting Glucose & Insulin": "LAB10AM"
        },
        "questionnaire": {
            "Alcohol Use": "ALQ",
            "Diabetes": "DIQ"
        }
    },
    "2001-2002": {
        "demographics": {
            "Demographic Variables & Sample Weights": "DEMO_B"
        },
        "examination": {
            "Blood Pressure": "BPX_B",
            "Body Measures": "BMX_B",
            "Cardiovascular Fitness": "CVX_B"
        },
        "laboratory": {
            "Cholesterol - LDL & Triglycerides": "L13AM_B",
            "Plasma Fasting Glucose & Insulin": "L10AM_B"
        },
        "questionnaire": {
            "Alcohol Use": "ALQ_B",
            "Diabetes": "DIQ_B"
        }
    },
    "2003-2004": {
        "demographics": {
            "Demographic Variables & Sample Weights": "DEMO_C"
        },
        "examination": {
            "Blood Pressure": "BPX_C",
            "Body Measures": "BMX_C",
            "Cardiovascular Fitness": "CVX_C"
        },
        "laboratory": {
            "Cholesterol - LDL & Triglycerides": "L13AM_C",
            "Plasma Fasting Glucose & Insulin": "L10AM_C"
        },
        "questionnaire": {
            "Alcohol Use": "ALQ_C",
            "Diabetes": "DIQ_C"
        }
    },
    "2005-2006": {
        "demographics": {
            "Demographic Variables & Sample Weights": "DEMO_D"
        },
        "examination": {
            "Blood Pressure": "BPX_D",
            "Body Measures": "BMX_D",
            "Cardiovascular Fitness": "CVX_D"
        },
        "laboratory": {
            "Cholesterol - LDL & Triglycerides": "TRIGLY_D",
            "Plasma Fasting Glucose & Insulin": "GLU_D"
        },
        "questionnaire": {
            "Alcohol Use": "ALQ_D",
            "Diabetes": "DIQ_D"
        }
    },
    "2007-2008": {
        "demographics": {
            "Demographic Variables & Sample Weights": "DEMO_E"
        },
        "examination": {
            "Blood Pressure": "BPX_E",
            "Body Measures": "BMX_E",
            "Cardiovascular Fitness": "CVX_E"
        },
        "laboratory": {
            "Cholesterol - LDL & Triglycerides": "TRIGLY_E",
            "Plasma Fasting Glucose & Insulin": "GLU_E"
        },
        "questionnaire": {
            "Alcohol Use": "ALQ_E",
            "Diabetes": "DIQ_E"
        }
    },
    "2009-2010": {
        "demographics": {
            "Demographic Variables & Sample Weights": "DEMO_F"
        },
        "examination": {
            "Blood Pressure": "BPX_F",
            "Body Measures": "BMX_F",
            "Cardiovascular Fitness": "CVX_F"
        },
        "laboratory": {
            "Cholesterol - LDL & Triglycerides": "TRIGLY_F",
            "Plasma Fasting Glucose & Insulin": "GLU_F"
        },
        "questionnaire": {
            "Alcohol Use": "ALQ_F",
            "Diabetes": "DIQ_F"
        }
    },
    "2011-2012": {
        "demographics": {
            "Demographic Variables & Sample Weights": "DEMO_G"
        },
        "examination": {
            "Blood Pressure": "BPX_G",
            "Body Measures": "BMX_G",
            "Cardiovascular Fitness": "CVX_G"
        },
        "laboratory": {
            "Cholesterol - LDL & Triglycerides": "TRIGLY_G",
            "Plasma Fasting Glucose & Insulin": "GLU_G"
        },
        "questionnaire": {
            "Alcohol Use": "ALQ_G",
            "Diabetes": "DIQ_G"
        }
    },
    "2013-2014": {
        "demographics": {
            "Demographic Variables & Sample Weights": "DEMO_H"
        },
        "examination": {
            "Blood Pressure": "BPX_H",
            "Body Measures": "BMX_H",
            "Cardiovascular Fitness": "CVX_H"
        },
        "laboratory": {
            "Cholesterol - LDL & Triglycerides": "TRIGLY_H",
            "Plasma Fasting Glucose & Insulin": "GLU_H"
        },
        "questionnaire": {
            "Alcohol Use": "ALQ_H",
            "Diabetes": "DIQ_H"
        }
    },
    "2015-2016": {
        "demographics": {
            "Demographic Variables & Sample Weights": "DEMO_I"
        },
        "examination": {
            "Blood Pressure": "BPX_I",
            "Body Measures": "BMX_I",
            "Cardiovascular Fitness": "CVX_I"
        },
        "laboratory": {
            "Cholesterol - LDL & Triglycerides": "TRIGLY_I",
            "Plasma Fasting Glucose & Insulin": "GLU_I"
        },
        "questionnaire": {
            "Alcohol Use": "ALQ_I",
            "Diabetes": "DIQ_I"
        }
    },
    "2017-2018": {
        "demographics": {
            "Demographic Variables & Sample Weights": "DEMO_J"
        },
        "examination": {
            "Blood Pressure": "BPX_J",
            "Body Measures": "BMX_J",
            "Cardiovascular Fitness": "CVX_J"
        },
        "laboratory": {
            "Cholesterol - LDL & Triglycerides": "TRIGLY_J",
            "Plasma Fasting Glucose & Insulin": "GLU_J"
        },
        "questionnaire": {
            "Alcohol Use": "ALQ_J",
            "Diabetes": "DIQ_J"
        }
    }
}


def get_file_identifier(cycle, category, file_desc):
    """
    Returns the NHANES file identifier (e.g. 'DIQ_B') for a given cycle, category, and file description.

    Args:
        cycle (str): e.g. "1999-2000", "2001-2002"
        category (str): e.g. "demographics", "examination", "laboratory", "questionnaire"
        file_desc (str): e.g. "Diabetes", "Blood Pressure"

    Returns:
        str or None: The short code for that file (like "DIQ_B") or None if not found.
    """
    cycle_map = FILE_MAPPING.get(cycle)
    if not cycle_map:
        print(f"No file mapping for cycle '{cycle}'")
        return None
    
    category_map = cycle_map.get(category)
    if not category_map:
        print(f"No file mapping for category '{category}' in cycle '{cycle}'")
        return None
    
    short_code = category_map.get(file_desc)
    if not short_code:
        print(f"No file mapping for file_desc '{file_desc}' in category '{category}', cycle '{cycle}'")
        return None
    
    return short_code
