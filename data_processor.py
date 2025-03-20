import pandas as pd
import numpy as np
from exercise_constants import ALL_EXERCISES

class DataProcessor:
    def __init__(self):
        self.required_columns = [
            'user name', 'exercise name', 'exercise createdAt',
            'power - high', 'acceleration - high'
        ]

    def validate_data(self, df):
        """Validate the uploaded data format and content."""
        # Check required columns
        missing_cols = [col for col in self.required_columns if col not in df.columns]
        if missing_cols:
            return False, f"Missing required columns: {', '.join(missing_cols)}"
        
        # Check for empty values in required columns
        empty_cols = [col for col in self.required_columns if df[col].isna().any()]
        if empty_cols:
            return False, f"Empty values found in columns: {', '.join(empty_cols)}"
        
        return True, "Data validation successful"

    def preprocess_data(self, df):
        """Clean and prepare the data for matrix generation."""
        # Filter only valid exercises
        df = df[df['exercise name'].isin(ALL_EXERCISES)].copy()
        
        # Convert timestamp
        df['exercise createdAt'] = pd.to_datetime(df['exercise createdAt'])
        
        # Sort by user and timestamp
        df = df.sort_values(['user name', 'exercise createdAt'])
        
        return df

    def get_user_list(self, df):
        """Get list of unique users in the dataset."""
        return sorted(df['user name'].unique())
