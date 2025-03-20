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

        # Track exercises in each test instance
        test_instances = {}  # Dictionary to track exercises in each test instance

        # Process each exercise chronologically
        for _, row in user_data.iterrows():
            exercise = row['full_exercise_name']

            # Find earliest available test instance for this exercise
            target_instance = self._find_earliest_available_instance(
                exercise, test_instances)

            # Initialize new test instance if needed
            if target_instance not in power_matrix:
                power_matrix[target_instance] = {}
                accel_matrix[target_instance] = {}
                test_instances[target_instance] = set()

            # Add exercise data to matrices
            power_matrix[target_instance][exercise] = row['power - high']
            accel_matrix[target_instance][exercise] = row['acceleration - high']
            test_instances[target_instance].add(exercise)

        return self._convert_to_dataframes(power_matrix, accel_matrix)

    def _find_earliest_available_instance(self, exercise, test_instances):
        """Find the earliest test instance that doesn't have this exercise."""
        instance = 1
        while True:
            # If instance doesn't exist or exercise not in instance, use this instance
            if (instance not in test_instances or 
                exercise not in test_instances[instance]):
                return instance
            instance += 1

    def _convert_to_dataframes(self, power_matrix, accel_matrix):
        """Convert dictionary matrices to pandas DataFrames."""
        # Create DataFrame for power
        power_df = pd.DataFrame(power_matrix)
        power_df = power_df.reindex(self.exercises)

        # Create DataFrame for acceleration
        accel_df = pd.DataFrame(accel_matrix)
        accel_df = accel_df.reindex(self.exercises)

        return power_df, accel_df