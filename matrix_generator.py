import pandas as pd
import numpy as np
from exercise_constants import ALL_EXERCISES

class MatrixGenerator:
    def __init__(self):
        self.exercises = ALL_EXERCISES

    def generate_user_matrices(self, df, user_name):
        """Generate test instance matrices for a specific user."""
        user_data = df[df['user name'] == user_name].copy()
        
        # Initialize matrices for power and acceleration
        power_matrix = {}
        accel_matrix = {}
        test_instance = 1
        
        # Track filled exercises
        filled_exercises = set()
        
        # Process each exercise chronologically
        for _, row in user_data.iterrows():
            exercise = row['exercise name']
            
            # Skip if exercise already in earlier test instance
            if exercise in filled_exercises:
                continue
                
            # Initialize new test instance if needed
            if test_instance not in power_matrix:
                power_matrix[test_instance] = {}
                accel_matrix[test_instance] = {}
            
            # Add exercise data to matrices
            power_matrix[test_instance][exercise] = row['power - high']
            accel_matrix[test_instance][exercise] = row['acceleration - high']
            filled_exercises.add(exercise)
            
            # Check if current test instance is full
            if len(power_matrix[test_instance]) == len(self.exercises):
                test_instance += 1
        
        return self._convert_to_dataframes(power_matrix, accel_matrix)

    def _convert_to_dataframes(self, power_matrix, accel_matrix):
        """Convert dictionary matrices to pandas DataFrames."""
        # Create DataFrame for power
        power_df = pd.DataFrame(power_matrix)
        power_df = power_df.reindex(self.exercises)
        
        # Create DataFrame for acceleration
        accel_df = pd.DataFrame(accel_matrix)
        accel_df = accel_df.reindex(self.exercises)
        
        return power_df, accel_df
