import pandas as pd
import numpy as np
from exercise_constants import VALID_EXERCISES, REQUIRES_DOMINANCE, get_full_exercise_name

class DataProcessor:
    def __init__(self):
        self.required_columns = [
            'user name', 'exercise name', 'dominance', 'exercise createdAt',
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
        # Create a copy to avoid modifying original data
        processed_df = df.copy()

        # Validate exercise names
        valid_base_exercises = [ex for cat in VALID_EXERCISES.values() for ex in cat]
        mask = processed_df['exercise name'].isin(valid_base_exercises)

        # Filter only valid exercises
        processed_df = processed_df[mask].copy()

        # Generate full exercise names
        processed_df['full_exercise_name'] = processed_df.apply(
            lambda row: get_full_exercise_name(
                row['exercise name'],
                row['dominance'] if REQUIRES_DOMINANCE[row['exercise name']] else None
            ),
            axis=1
        )

        # Convert timestamp
        processed_df['exercise createdAt'] = pd.to_datetime(processed_df['exercise createdAt'])

        # Sort by user and timestamp
        processed_df = processed_df.sort_values(['user name', 'exercise createdAt'])

        return processed_df

    def get_user_list(self, df):
        """Get list of unique users in the dataset."""
        return sorted(df['user name'].unique())