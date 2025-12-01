import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

class NHANESDataCleaner:
    def __init__(self, impute=False, impute_method="mean"):
        """
        Initialize the NHANES data cleaner.

        Parameters:
        - impute (bool): Whether to perform imputation (True) or leave missing values as is (False).
        - impute_method (str): The method for imputation ("mean", "median", "mode", "knn", "mice").
        """
        self.impute = impute
        self.impute_method = impute_method
        self.nhanes_missing_codes = {
            "numeric": [".", 7, 77, 777, 9, 99, 999],  # NHANES missing codes for numbers
            "categorical": ["", 7, 77, 777, 9, 99, 999]  # NHANES missing codes for text
        }

    def clean_data(self, df):
        """
        Cleans the dataset based on the chosen option (leave as is or impute).

        Parameters:
        - df (DataFrame): The NHANES dataset
        
        Returns:
        - DataFrame: Processed dataset
        """
        df = df.copy()

        # Step 1: Convert NHANES missing codes to NaN
        for col in df.columns:
            if df[col].dtype in [np.float64, np.int64]:
                df[col] = df[col].replace(self.nhanes_missing_codes["numeric"], np.nan)
            else:
                df[col] = df[col].replace(self.nhanes_missing_codes["categorical"], np.nan)

        # Step 2: Apply imputation if selected
        if self.impute:
            df = self.impute_missing_values(df)

        return df

    def impute_missing_values(self, df):
        """
        Imputes missing values in the dataset.
        """
        for col in df.columns:
            if df[col].isnull().sum() > 0:  # Only process columns with missing values
                if df[col].dtype in [np.float64, np.int64]:  # Numeric columns
                    df[col] = self.impute_numeric(df[col])
                else:  # Categorical columns
                    df[col] = df[col].fillna(df[col].mode()[0])  # Mode imputation for categorical

        return df

    def impute_numeric(self, series):
        """
        Imputes missing numeric values based on the selected method.
        """
        if self.impute_method == "mean":
            return series.fillna(series.mean())
        elif self.impute_method == "median":
            return series.fillna(series.median())
        elif self.impute_method == "mode":
            return series.fillna(series.mode()[0])
        elif self.impute_method == "knn":
            imputer = KNNImputer(n_neighbors=5)
            return imputer.fit_transform(series.values.reshape(-1, 1)).flatten()
        elif self.impute_method == "mice":
            imputer = IterativeImputer(max_iter=10, random_state=0)
            return imputer.fit_transform(series.values.reshape(-1, 1)).flatten()
        else:
            raise ValueError("Invalid imputation method. Choose from 'mean', 'median', 'mode', 'knn', or 'mice'.")