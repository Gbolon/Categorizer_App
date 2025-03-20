import pandas as pd
import numpy as np
from exercise_constants import (
    VALID_EXERCISES,
    EXERCISE_DOMINANCE,
    is_valid_exercise_dominance,
    get_full_exercise_name,
    standardize_dominance
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

        # Get base exercises list
        valid_base_exercises = [ex for cat in VALID_EXERCISES.values() for ex in cat]

        # Pre-filter to remove variations we want to ignore
        df = self._filter_standard_exercises(df, valid_base_exercises)

        # Validate remaining exercise names and dominance combinations
        invalid_exercises = []
        for _, row in df.iterrows():
            exercise_name = row['exercise name']
            dominance = standardize_dominance(row['dominance'])

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

    def _filter_standard_exercises(self, df, valid_exercises):
        """Filter out non-standard exercise variations."""
        # Create a series of boolean masks for each valid exercise
        masks = []
        for valid_exercise in valid_exercises:
            # Match exact exercise names or remove known variations
            mask = (df['exercise name'] == valid_exercise) | \
                   (~df['exercise name'].str.contains('Plyo', case=False, na=False))
            masks.append(mask)

        # Combine all masks
        final_mask = pd.concat(masks, axis=1).all(axis=1)
        return df[final_mask].copy()

    def preprocess_data(self, df):
        """Clean and prepare the data for matrix generation."""
        # Create a copy to avoid modifying original data
        processed_df = df.copy()

        # Get valid base exercises
        valid_base_exercises = [ex for cat in VALID_EXERCISES.values() for ex in cat]

        # Pre-filter to remove variations we want to ignore
        processed_df = self._filter_standard_exercises(processed_df, valid_base_exercises)

        # Standardize dominance values
        processed_df['dominance'] = processed_df['dominance'].apply(standardize_dominance)

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

        # Debug logging
        print("Processed data shape:", processed_df.shape)
        print("Unique exercises:", processed_df['full_exercise_name'].unique())

        return processed_df

    def get_user_list(self, df):
        """Get list of unique users in the dataset."""
        return sorted(df['user name'].unique())