import streamlit as st
import pandas as pd
from data_processor import DataProcessor
from matrix_generator import MatrixGenerator
from exercise_constants import VALID_EXERCISES
from goal_standards import POWER_STANDARDS, ACCELERATION_STANDARDS

def main():
    st.title("Exercise Test Instance Matrix Generator")

    # Initialize processors
    data_processor = DataProcessor()
    matrix_generator = MatrixGenerator()

    # File upload
    uploaded_file = st.file_uploader("Upload your exercise data (CSV or Excel)", 
                                   type=['csv', 'xlsx'])

    if uploaded_file is not None:
        try:
            # Load and validate data
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            # Validate data
            is_valid, message = data_processor.validate_data(df)

            if not is_valid:
                st.error(message)
                return

            # Process data
            processed_df = data_processor.preprocess_data(df)

            # Show data preview
            st.subheader("Data Preview")
            st.dataframe(processed_df.head())

            # User selection
            users = data_processor.get_user_list(processed_df)
            selected_user = st.selectbox("Select User", users)

            if selected_user:
                # Generate matrices
                matrices = matrix_generator.generate_user_matrices(
                    processed_df, selected_user)

                power_matrix, accel_matrix, power_dev_matrix, accel_dev_matrix = matrices

                # Display raw value matrices
                st.subheader("Raw Value Matrices")

                st.write("Power Matrix (Raw Values)")
                st.dataframe(power_matrix)

                st.write("Acceleration Matrix (Raw Values)")
                st.dataframe(accel_matrix)

                # Display development matrices if available
                if power_dev_matrix is not None and accel_dev_matrix is not None:
                    st.subheader("Development Score Matrices (%)")

                    st.write("Power Development Matrix")
                    styled_power_dev = power_dev_matrix.style.format("{:.1f}%")
                    st.dataframe(styled_power_dev)

                    st.write("Acceleration Development Matrix")
                    styled_accel_dev = accel_dev_matrix.style.format("{:.1f}%")
                    st.dataframe(styled_accel_dev)

                # Export functionality
                st.subheader("Export Data")

                def download_matrix(matrix, name):
                    return matrix.to_csv().encode('utf-8')

                for matrix, name in [
                    (power_matrix, "power"),
                    (accel_matrix, "acceleration"),
                    (power_dev_matrix, "power_development"),
                    (accel_dev_matrix, "acceleration_development")
                ]:
                    if matrix is not None:
                        st.download_button(
                            label=f"Download {name.replace('_', ' ').title()} Matrix CSV",
                            data=download_matrix(matrix, name),
                            file_name=f"{selected_user}_{name}_matrix.csv",
                            mime="text/csv"
                        )

        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

    # Display exercise information with standards
    with st.expander("View Tracked Exercises and Goal Standards"):
        for category, exercises in VALID_EXERCISES.items():
            st.subheader(category)

            # Create a DataFrame to display standards
            standards_data = []
            for exercise in exercises:
                male_power = POWER_STANDARDS['male'][exercise]
                male_accel = ACCELERATION_STANDARDS['male'][exercise]
                female_power = POWER_STANDARDS['female'][exercise]
                female_accel = ACCELERATION_STANDARDS['female'][exercise]

                standards_data.append({
                    'Exercise': exercise,
                    'Male Power': male_power,
                    'Male Acceleration': male_accel,
                    'Female Power': female_power,
                    'Female Acceleration': female_accel
                })

            # Display standards table
            if standards_data:
                df_standards = pd.DataFrame(standards_data)
                styled_standards = df_standards.style.format({
                    'Male Power': '{:.0f}',
                    'Male Acceleration': '{:.0f}',
                    'Female Power': '{:.0f}',
                    'Female Acceleration': '{:.0f}'
                })
                st.dataframe(styled_standards, use_container_width=True)

if __name__ == "__main__":
    main()