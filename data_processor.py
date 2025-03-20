import pandas as pd
import numpy as np
from exercise_constants import (
    VALID_EXERCISES,
    EXERCISE_DOMINANCE,
    is_valid_exercise_dominance,
    get_full_exercise_name
)

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

        # Validate exercise names and dominance combinations
        valid_base_exercises = [ex for cat in VALID_EXERCISES.values() for ex in cat]
        invalid_exercises = []

        for _, row in df.iterrows():
            exercise_name = row['exercise name']
            dominance = row['dominance']

            if exercise_name not in valid_base_exercises:
                invalid_exercises.append(f"Invalid exercise: {exercise_name}")
                continue

            if not is_valid_exercise_dominance(exercise_name, dominance):
                invalid_exercises.append(
                    f"Invalid dominance '{dominance}' for exercise '{exercise_name}'"
                )

        if invalid_exercises:
            return False, "Data validation failed:\n" + "\n".join(invalid_exercises[:5])

        return True, "Data validation successful"

    def preprocess_data(self, df):
        """Clean and prepare the data for matrix generation."""
        # Create a copy to avoid modifying original data
        processed_df = df.copy()

        # Filter valid exercises and dominance combinations
        valid_rows = []
        for idx, row in processed_df.iterrows():
            if is_valid_exercise_dominance(row['exercise name'], row['dominance']):
                valid_rows.append(idx)

        processed_df = processed_df.loc[valid_rows].copy()

        # Generate full exercise names
        processed_df['full_exercise_name'] = processed_df.apply(
            lambda row: get_full_exercise_name(row['exercise name'], row['dominance']),
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