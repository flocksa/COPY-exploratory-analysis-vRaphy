import os
import requests
import pandas as pd
        
def download_nhanes_file(cycle, file_desc, category, download_dir="nhanes_data"$
    print(f"DEBUG: Requested -> Cycle: {cycle}, Description: {file_desc}, Categ$
    category = category.lower()
        
    # Mapping cycle name to the correct starting year
    cycle_mapping = {
        "1999-2000": "1999", "2001-2002": "2001", "2003-2004": "2003",
        "2005-2006": "2005", "2007-2008": "2007", "2009-2010": "2009",
        "2011-2012": "2011-2012", "2013-2014": "2013", "2015-2016": "2015", "20$
    }
    cycle_single_year = cycle_mapping.get(cycle)
    if not cycle_single_year:  
        print(f"ERROR: Unrecognized cycle: {cycle}")
        return None
    # NHANES file code mappings
    nhanes_file_mapping = {
        "demographics": {
            "Demographic Variables & Sample Weights": {
                "1999": "DEMO", "2001": "DEMO_B", "2003": "DEMO_C", "2005": "DE$
                "2007": "DEMO_E", "2009": "DEMO_F", "2011": "DEMO_G", "2013": "$
                "2015": "DEMO_I", "2017": "DEMO_J"  
            }
        },
        "questionnaire": {
            "Diabetes": {  
                "1999": "DIQ", "2001": "DIQ_B", "2003": "DIQ_C", "2005": "DIQ_D$
                "2007": "DIQ_E", "2009": "DIQ_F", "2011": "DIQ_G", "2013": "DIQ$
                "2015": "DIQ_I", "2017": "DIQ_J"
            }
        }
    }
    # Get file short name
    file_name = nhanes_file_mapping.get(category, {}).get(file_desc, {}).get(cy$
    if not file_name:
        print(f"ERROR: Could not find mapping for {file_desc} in {cycle_single_$
        return None
    
    # ✅ Fixed URL construction
    url = f"https://wwwn.cdc.gov/Nchs/Data/Nhanes/{cycle_single_year}/{file_nam$
    print(f"DEBUG: Download URL → {url}")
                
    os.makedirs(download_dir, exist_ok=True)
    xpt_path = os.path.join(download_dir, f"{file_name}.XPT")
          
    if not os.path.exists(xpt_path):
    # NHANES file code mappings
   nhanes_file_mapping = {
        "demographics": {
            "Demographic Variables & Sample Weights": {
                "1999": "DEMO", "2001": "DEMO_B", "2003": "DEMO_C", "2005": "DE$
                "2007": "DEMO_E", "2009": "DEMO_F", "2011": "DEMO_G", "2013": "$
                "2015": "DEMO_I", "2017": "DEMO_J"
            }
        },
        "questionnaire": {
            "Diabetes": {  
                "1999": "DIQ", "2001": "DIQ_B", "2003": "DIQ_C", "2005": "DIQ_D$
                "2007": "DIQ_E", "2009": "DIQ_F", "2011": "DIQ_G", "2013": "DIQ$
                "2015": "DIQ_I", "2017": "DIQ_J"
            }
        }
    }
        print(f"Downloading {file_name}...")
        response = requests.get(url)
       if response.status_code != 200:
            print(f"ERROR: Failed to download {url} → {response.status_code} {$ 
            return None
        with open(xpt_path, "wb") as f:
            f.write(response.content)
         
    try:
        df = pd.read_sas(xpt_path, format='xport')
        print(f"Loaded {file_name} successfully, shape: {df.shape}")
        
        if category == "demographics" and file_desc == "Demographic Variables &$
            columns = ["SEQN", "RIDAGEYR", "RIAGENDR", "RIDRETH1"]
            df = df[columns]
            
        if category == "questionnaire" and file_desc == "Diabetes":
            if "DIQ010" in df.columns:
                df = df[["SEQN", "DIQ010"]]
                df.rename(columns={"DIQ010": f"DIQ010_{cycle}"}, inplace=True)
          else:
                print(f"WARNING: DIQ010 not found in {file_name}")
                return None
            
        os.remove(xpt_path)
        return df
            
    except Exception as e:
        print(f"ERROR reading {file_name}.XPT: {e}")
        return None
