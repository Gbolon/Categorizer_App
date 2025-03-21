import streamlit as st
import pandas as pd
from data_processor import DataProcessor
from matrix_generator import MatrixGenerator
from exercise_constants import VALID_EXERCISES
from goal_standards import POWER_STANDARDS, ACCELERATION_STANDARDS

# Configure the page at the very beginning
st.set_page_config(
    page_title="Exercise Test Instance Matrix Generator",
    page_icon="📊",
    layout="wide",  # This will make the page wider
    initial_sidebar_state="auto"
)

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

            # Show data preview in collapsed expander
            with st.expander("Data Preview", expanded=False):
                st.dataframe(processed_df.head())

            # Generate group-level analysis
            (power_counts, accel_counts, single_test_distribution,
             power_transitions_detail, accel_transitions_detail) = matrix_generator.generate_group_analysis(processed_df)

            # Display group-level analysis
            st.subheader("Group Development Analysis")

            # Create two columns for side-by-side layout
            col1, col2 = st.columns(2)

            # Display Single Test Users Distribution in left column
            with col1:
                st.write("Single Test Users Distribution")
                styled_single_test = single_test_distribution.style.format("{:.0f}")
                st.dataframe(styled_single_test)

            # Display average metrics in right column
            with col2:
                st.write("Single Test Users Averages")
                # Define bracket midpoints for weighted average calculation
                bracket_scores = {
                    'Goal Hit': 100,
                    'Elite': 95,
                    'Above Average': 83,
                    'Average': 63,
                    'Under Developed': 38,
                    'Severely Under Developed': 12.5
                }

                # Calculate weighted averages for Power and Acceleration
                def calculate_weighted_average(column):
                    total_users = single_test_distribution.loc['Total Users', column]
                    if total_users == 0:
                        return 0

                    weighted_sum = sum(
                        single_test_distribution.loc[bracket, column] * score
                        for bracket, score in bracket_scores.items()
                        if bracket in single_test_distribution.index
                    )
                    return weighted_sum / total_users

                power_avg = calculate_weighted_average('Power')
                accel_avg = calculate_weighted_average('Acceleration')

                # Create metrics
                st.metric("Average Overall Power Development", f"{power_avg:.1f}%")
                st.metric("Average Overall Acceleration Development", f"{accel_avg:.1f}%")

            # Display distribution tables full width
            st.write("Multi-Test Users Power Development Distribution")
            styled_power_counts = power_counts.style.format("{:.0f}")
            st.dataframe(styled_power_counts, use_container_width=True)

            st.write("Multi-Test Users Acceleration Development Distribution")
            styled_accel_counts = accel_counts.style.format("{:.0f}")
            st.dataframe(styled_accel_counts, use_container_width=True)

            # Display detailed transition analysis
            st.subheader("Detailed Transition Analysis")

            # Display reading guide once at the top
            st.write("Reading guide: Rows show starting bracket, columns show ending bracket. Numbers show how many users made each transition.")
            st.write("Diagonal values (blue) show users who remained in the same bracket.")
            st.write("Above diagonal (red) shows regression to lower brackets.")
            st.write("Below diagonal (green) shows improvement to higher brackets.")

            # Create tabs for Power and Acceleration transitions
            power_tab, accel_tab = st.tabs(["Power Transitions", "Acceleration Transitions"])

            # Power transitions tab
            with power_tab:
                for period, matrix in power_transitions_detail.items():
                    st.write(f"Period: {period}")
                    st.dataframe(matrix, use_container_width=True)
                    st.write("---")

            # Acceleration transitions tab
            with accel_tab:
                for period, matrix in accel_transitions_detail.items():
                    st.write(f"Period: {period}")
                    st.dataframe(matrix, use_container_width=True)
                    st.write("---")

            # User selection for individual analysis
            st.subheader("Individual User Analysis")
            users = data_processor.get_user_list(processed_df)
            selected_user = st.selectbox("Select User", users)

            if selected_user:
                # Generate matrices
                matrices = matrix_generator.generate_user_matrices(
                    processed_df, selected_user)

                power_matrix, accel_matrix, power_dev_matrix, accel_dev_matrix, overall_dev_matrix, power_brackets, accel_brackets = matrices

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

                    # Display overall development categorization
                    if overall_dev_matrix is not None:
                        st.subheader("Overall Development Categorization")
                        styled_overall_dev = overall_dev_matrix.style.format("{:.1f}%")
                        st.dataframe(styled_overall_dev)

                    # Display development brackets
                    if power_brackets is not None and accel_brackets is not None:
                        st.subheader("Development Brackets")

                        col1, col2 = st.columns(2)

                        with col1:
                            st.write("Power Development Brackets")
                            st.dataframe(power_brackets)

                        with col2:
                            st.write("Acceleration Development Brackets")
                            st.dataframe(accel_brackets)

                # Export functionality
                st.subheader("Export Data")

                def download_matrix(matrix, name):
                    return matrix.to_csv().encode('utf-8')

                for matrix, name in [
                    (power_matrix, "power"),
                    (accel_matrix, "acceleration"),
                    (power_dev_matrix, "power_development"),
                    (accel_dev_matrix, "acceleration_development"),
                    (overall_dev_matrix, "overall_development"),
                    (power_brackets, "power_brackets"),
                    (accel_brackets, "acceleration_brackets"),
                    (power_counts, "power_group_analysis"),
                    (accel_counts, "acceleration_group_analysis"),
                    (single_test_distribution, "single_test_distribution")
                ]:
                    if matrix is not None:
                        st.download_button(
                            label=f"Download {name.replace('_', ' ').title()} Matrix CSV",
                            data=download_matrix(matrix, name),
                            file_name=f"{selected_user}_{name}_matrix.csv",
                            mime="text/csv"
                        )

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

        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

if __name__ == "__main__":
    main()