import pandas as pd
import numpy as np
from exercise_constants import ALL_EXERCISES
from goal_standards import calculate_development_score

class MatrixGenerator:
    def __init__(self):
        self.exercises = ALL_EXERCISES
        self.development_brackets = {
            'Goal Hit': (100, float('inf')),
            'Elite': (90, 99.99),
            'Above Average': (76, 90),
            'Average': (51, 75),
            'Under Developed': (26, 50),
            'Severely Under Developed': (0, 25)
        }

    def generate_user_matrices(self, df, user_name):
        """Generate test instance matrices for a specific user."""
        user_data = df[df['user name'] == user_name].copy()

        # Initialize matrices
        power_matrix = {}
        accel_matrix = {}
        test_instances = {}

        # Get user's sex for development calculations
        user_sex = user_data['sex'].iloc[0].lower() if not user_data.empty else None

        # Process each exercise chronologically
        for _, row in user_data.iterrows():
            exercise = row['full_exercise_name']

            # Find earliest available test instance for this exercise
            target_instance = 1
            while target_instance in test_instances and exercise in test_instances[target_instance]:
                target_instance += 1

            # Initialize new test instance if needed
            if target_instance not in power_matrix:
                power_matrix[target_instance] = {}
                accel_matrix[target_instance] = {}
                test_instances[target_instance] = set()

            # Add exercise data to matrices
            power_matrix[target_instance][exercise] = row['power - high']
            accel_matrix[target_instance][exercise] = row['acceleration - high']
            test_instances[target_instance].add(exercise)

        # Fill empty cells with NaN
        for instance in power_matrix:
            for exercise in self.exercises:
                if exercise not in power_matrix[instance]:
                    power_matrix[instance][exercise] = np.nan
                if exercise not in accel_matrix[instance]:
                    accel_matrix[instance][exercise] = np.nan

        # Convert to DataFrames
        power_df, accel_df = self._convert_to_dataframes(power_matrix, accel_matrix)

        # Generate development matrices if sex is available
        if user_sex:
            power_dev_df = self._calculate_development_matrix(power_df, user_sex, 'power')
            accel_dev_df = self._calculate_development_matrix(accel_df, user_sex, 'acceleration')

            # Calculate overall development categorization
            overall_dev_df = self._calculate_overall_development(power_dev_df, accel_dev_df)

            # Add bracketing information
            power_brackets = self._categorize_development(power_dev_df)
            accel_brackets = self._categorize_development(accel_dev_df)

            return power_df, accel_df, power_dev_df, accel_dev_df, overall_dev_df, power_brackets, accel_brackets

        return power_df, accel_df, None, None, None, None, None

    def _convert_to_dataframes(self, power_matrix, accel_matrix):
        """Convert dictionary matrices to pandas DataFrames."""
        # Create DataFrame for power
        power_df = pd.DataFrame(power_matrix)
        power_df = power_df.reindex(self.exercises)
        power_df.columns = [f"Test {i}" for i in range(1, len(power_df.columns) + 1)]

        # Create DataFrame for acceleration
        accel_df = pd.DataFrame(accel_matrix)
        accel_df = accel_df.reindex(self.exercises)
        accel_df.columns = [f"Test {i}" for i in range(1, len(accel_df.columns) + 1)]

        return power_df, accel_df

    def _calculate_development_matrix(self, metric_df, sex, metric_type):
        """Calculate development scores for each value in the matrix."""
        dev_matrix = metric_df.copy()

        for col in dev_matrix.columns:
            for idx in dev_matrix.index:
                value = metric_df.loc[idx, col]
                dev_matrix.loc[idx, col] = calculate_development_score(
                    value, idx, sex, metric_type
                )

        return dev_matrix

    def _calculate_overall_development(self, power_dev_df, accel_dev_df):
        """Calculate overall development categorization for each test instance."""
        # Initialize a new DataFrame for overall development
        overall_dev = pd.DataFrame(index=['Power Average', 'Acceleration Average', 'Overall Average'])

        # Calculate averages for each test instance
        for col in power_dev_df.columns:
            # Calculate power average (excluding NaN values)
            power_avg = power_dev_df[col].apply(lambda x: min(x, 100) if pd.notnull(x) else x).mean(skipna=True)

            # Calculate acceleration average (excluding NaN values)
            accel_avg = accel_dev_df[col].apply(lambda x: min(x, 100) if pd.notnull(x) else x).mean(skipna=True)

            # Calculate overall average
            overall_avg = np.mean([power_avg, accel_avg])

            # Add to overall development DataFrame
            overall_dev[col] = [power_avg, accel_avg, overall_avg]

        return overall_dev

    def _categorize_development(self, dev_matrix):
        """Categorize development scores into brackets."""
        # Initialize DataFrame for bracketing
        brackets_df = pd.DataFrame(index=dev_matrix.columns, columns=['Category', 'Score'])

        # Calculate overall average for each test instance (capped at 100%)
        test_averages = dev_matrix.apply(
            lambda x: x.apply(lambda y: min(y, 100) if pd.notnull(y) else y).mean(skipna=True)
        )

        # Categorize each test instance
        for test in test_averages.index:
            score = test_averages[test]
            for category, (min_val, max_val) in self.development_brackets.items():
                if pd.notnull(score) and min_val <= score <= max_val:
                    brackets_df.loc[test, 'Category'] = category
                    brackets_df.loc[test, 'Score'] = f"{score:.1f}%"
                    break

        return brackets_df