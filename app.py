import streamlit as st
import pandas as pd
from data_processor import DataProcessor
from matrix_generator import MatrixGenerator
from exercise_constants import VALID_EXERCISES

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
                power_matrix, accel_matrix = matrix_generator.generate_user_matrices(
                    processed_df, selected_user)

                # Display matrices
                st.subheader("Power Matrix")
                st.dataframe(power_matrix)

                st.subheader("Acceleration Matrix")
                st.dataframe(accel_matrix)

                # Export functionality
                st.subheader("Export Data")

                def download_matrix(matrix, metric):
                    return matrix.to_csv().encode('utf-8')

                st.download_button(
                    label=f"Download Power Matrix CSV",
                    data=download_matrix(power_matrix, "power"),
                    file_name=f"{selected_user}_power_matrix.csv",
                    mime="text/csv"
                )

                st.download_button(
                    label=f"Download Acceleration Matrix CSV",
                    data=download_matrix(accel_matrix, "acceleration"),
                    file_name=f"{selected_user}_acceleration_matrix.csv",
                    mime="text/csv"
                )

        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

    # Display exercise information
    with st.expander("View Tracked Exercises"):
        for category, exercises in VALID_EXERCISES.items():
            st.subheader(category)
            for exercise in exercises:
                st.write(f"• {exercise}")

if __name__ == "__main__":
    main()