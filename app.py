import streamlit as st
import pandas as pd
import numpy as np
from data_processor import DataProcessor
from matrix_generator import MatrixGenerator
from report_generator import ReportGenerator
from exercise_constants import VALID_EXERCISES
from goal_standards import POWER_STANDARDS, ACCELERATION_STANDARDS

# Configure the page at the very beginning
st.set_page_config(
    page_title="Site Development Bracketer",
    page_icon="📊",
    layout="wide",  # This will make the page wider
    initial_sidebar_state="auto"
)

def main():
    st.markdown("<h1 style='font-size: 3em;'>Site Development Bracketer</h1>", unsafe_allow_html=True)

    # Initialize processors
    data_processor = DataProcessor()
    matrix_generator = MatrixGenerator()
    report_generator = ReportGenerator()

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
             power_transitions_detail, accel_transitions_detail,
             power_average, accel_average,
             avg_power_change_1_2, avg_accel_change_1_2,
             avg_power_change_2_3, avg_accel_change_2_3,
             avg_days_between_tests) = matrix_generator.generate_group_analysis(processed_df)

            # Display group-level analysis
            st.markdown("<h2 style='font-size: 1.875em;'>Group Development Analysis</h2>", unsafe_allow_html=True)

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
                st.metric("Average Overall Power Development", f"{power_average:.1f}%")
                st.metric("Average Overall Acceleration Development", f"{accel_average:.1f}%")

            # Display Multi-Test User Averages
            st.markdown("<h2 style='font-size: 1.875em;'>Multi-Test User Averages</h2>", unsafe_allow_html=True)
            st.metric("Average Days Between Tests", f"{avg_days_between_tests:.1f}")

            # Display Power development distribution and changes
            st.write("Multi-Test Users Power Development Distribution")
            styled_power_counts = power_counts.style.format("{:.0f}")
            st.dataframe(styled_power_counts, use_container_width=True)

            # Display Power changes directly below power distribution
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Power Change (Test 1→2)", f"{avg_power_change_1_2:+.1f}%",
                         delta_color="normal")
            with col2:
                st.metric("Power Change (Test 2→3)", f"{avg_power_change_2_3:+.1f}%",
                         delta_color="normal")

            # Display Acceleration development distribution
            st.write("Multi-Test Users Acceleration Development Distribution")
            styled_accel_counts = accel_counts.style.format("{:.0f}")
            st.dataframe(styled_accel_counts, use_container_width=True)

            # Display Acceleration changes directly below acceleration distribution
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Acceleration Change (Test 1→2)", f"{avg_accel_change_1_2:+.1f}%",
                         delta_color="normal")
            with col2:
                st.metric("Acceleration Change (Test 2→3)", f"{avg_accel_change_2_3:+.1f}%",
                         delta_color="normal")

            # Display detailed transition analysis
            st.markdown("<h2 style='font-size: 1.875em;'>Detailed Transition Analysis</h2>", unsafe_allow_html=True)

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

            # Body Region Meta Analysis
            st.markdown("<h2 style='font-size: 1.875em;'>Body Region Meta Analysis</h2>", unsafe_allow_html=True)
            st.write("Group averages by body region for multi-test users")

            # Calculate body region averages
            body_region_averages = matrix_generator.calculate_body_region_averages(processed_df)

            # Create columns for each body region
            region_cols = st.columns(len(VALID_EXERCISES))

            # Display each region's data
            for i, (region, averages) in enumerate(body_region_averages.items()):
                with region_cols[i]:
                    st.write(f"**{region}**")
                    styled_averages = averages.style.format("{:.1f}%")
                    st.dataframe(styled_averages)
            
            # Detailed Body Region Analysis
            st.markdown("<h2 style='font-size: 1.875em;'>Detailed Body Region Analysis</h2>", unsafe_allow_html=True)
            st.write("Detailed exercise metrics by body region (multi-test users only)")
            
            # Create tabs for each body region
            region_tabs = st.tabs(list(VALID_EXERCISES.keys()))
            
            # Process each region in its own tab
            for i, region in enumerate(VALID_EXERCISES.keys()):
                with region_tabs[i]:
                    st.markdown(f"<h3 style='font-size: 1.5em;'>{region} Region Analysis</h3>", unsafe_allow_html=True)
                    st.write(f"Separate power and acceleration metrics for {region.lower()} region movements (multi-test users only)")
                    
                    # Get detailed region metrics using the generalized function for all regions
                    power_df, accel_df, power_changes, accel_changes, lowest_power_exercise, lowest_power_value, lowest_accel_exercise, lowest_accel_value = matrix_generator.get_region_metrics(processed_df, region)
            
                    if power_df is not None and accel_df is not None:
                        # Create two columns for power and acceleration
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**{region} Region Power Development (%)**")
                            styled_power = power_df.style.format("{:.1f}%")
                            st.dataframe(styled_power)
                            
                            # Display power changes if available
                            if power_changes:
                                st.write("**Average Changes in Power Development:**")
                                metrics_col1, metrics_col2 = st.columns(2)
                                
                                # Test 1 to Test 2 changes
                                if 'test1_to_test2_pct' in power_changes and not pd.isna(power_changes['test1_to_test2_pct']):
                                    change = power_changes['test1_to_test2_pct']
                                    with metrics_col1:
                                        st.write("**Test 1 → Test 2**")
                                        if change < 0:
                                            st.markdown(f"<span style='color:red; font-size:1.2em;'>{change:.1f}%</span>", unsafe_allow_html=True)
                                        else:
                                            st.markdown(f"<span style='color:green; font-size:1.2em;'>{change:.1f}%</span>", unsafe_allow_html=True)
                                
                                # Test 2 to Test 3 changes
                                if 'test2_to_test3_pct' in power_changes and not pd.isna(power_changes['test2_to_test3_pct']):
                                    change = power_changes['test2_to_test3_pct']
                                    with metrics_col2:
                                        st.write("**Test 2 → Test 3**")
                                        if change < 0:
                                            st.markdown(f"<span style='color:red; font-size:1.2em;'>{change:.1f}%</span>", unsafe_allow_html=True)
                                        else:
                                            st.markdown(f"<span style='color:green; font-size:1.2em;'>{change:.1f}%</span>", unsafe_allow_html=True)
                                
                                # Display exercise with lowest change (if available)
                                if lowest_power_exercise is not None and lowest_power_value is not None:
                                    st.write("**Exercise with Lowest Change:**")
                                    if lowest_power_value < 0:
                                        st.markdown(f"**{lowest_power_exercise}**: <span style='color:red'>{lowest_power_value:.1f}%</span>", unsafe_allow_html=True)
                                    else:
                                        st.markdown(f"**{lowest_power_exercise}**: <span style='color:green'>{lowest_power_value:.1f}%</span>", unsafe_allow_html=True)
                        
                        with col2:
                            st.write(f"**{region} Region Acceleration Development (%)**")
                            styled_accel = accel_df.style.format("{:.1f}%")
                            st.dataframe(styled_accel)
                            
                            # Display acceleration changes if available
                            if accel_changes:
                                st.write("**Average Changes in Acceleration Development:**")
                                metrics_col1, metrics_col2 = st.columns(2)
                                
                                # Test 1 to Test 2 changes
                                if 'test1_to_test2_pct' in accel_changes and not pd.isna(accel_changes['test1_to_test2_pct']):
                                    change = accel_changes['test1_to_test2_pct']
                                    with metrics_col1:
                                        st.write("**Test 1 → Test 2**")
                                        if change < 0:
                                            st.markdown(f"<span style='color:red; font-size:1.2em;'>{change:.1f}%</span>", unsafe_allow_html=True)
                                        else:
                                            st.markdown(f"<span style='color:green; font-size:1.2em;'>{change:.1f}%</span>", unsafe_allow_html=True)
                                
                                # Test 2 to Test 3 changes
                                if 'test2_to_test3_pct' in accel_changes and not pd.isna(accel_changes['test2_to_test3_pct']):
                                    change = accel_changes['test2_to_test3_pct']
                                    with metrics_col2:
                                        st.write("**Test 2 → Test 3**")
                                        if change < 0:
                                            st.markdown(f"<span style='color:red; font-size:1.2em;'>{change:.1f}%</span>", unsafe_allow_html=True)
                                        else:
                                            st.markdown(f"<span style='color:green; font-size:1.2em;'>{change:.1f}%</span>", unsafe_allow_html=True)
                                        
                                # Display exercise with lowest change (if available)
                                if lowest_accel_exercise is not None and lowest_accel_value is not None:
                                    st.write("**Exercise with Lowest Change:**")
                                    if lowest_accel_value < 0:
                                        st.markdown(f"**{lowest_accel_exercise}**: <span style='color:red'>{lowest_accel_value:.1f}%</span>", unsafe_allow_html=True)
                                    else:
                                        st.markdown(f"**{lowest_accel_exercise}**: <span style='color:green'>{lowest_accel_value:.1f}%</span>", unsafe_allow_html=True)
                    else:
                        st.info(f"Not enough multi-test user data to display detailed {region.lower()} region analysis.")


            # User selection for individual analysis
            st.markdown("<h2 style='font-size: 1.875em;'>Individual User Analysis</h2>", unsafe_allow_html=True)
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
                        
            # Report Generator Section
            st.markdown("<h2 style='font-size: 1.875em;'>Report Generator</h2>", unsafe_allow_html=True)
            st.write("Generate reports with visualizations of distribution data for easy sharing")
            
            report_tab1, report_tab2 = st.tabs(["Distribution Reports", "Custom Reports (Coming Soon)"])
            
            with report_tab1:
                st.write("Generate a report with power and acceleration distribution data")
                
                # Create columns for buttons
                report_col1, report_col2, report_col3 = st.columns(3)
                
                with report_col1:
                    # HTML Report button with transition matrices (complete report)
                    complete_report = report_generator.generate_downloadable_html(
                        power_counts, 
                        accel_counts,
                        power_transitions_detail,
                        accel_transitions_detail
                    )
                    st.download_button(
                        label="Download Complete HTML Report",
                        data=complete_report,
                        file_name="complete_report.html",
                        mime="text/html",
                    )
                
                with report_col2:
                    # Simple report with just distribution data
                    simple_report = report_generator.generate_downloadable_html(
                        power_counts, 
                        accel_counts
                    )
                    st.download_button(
                        label="Download Simple Report",
                        data=simple_report,
                        file_name="distribution_report.html",
                        mime="text/html",
                    )
                
                # Display a preview of the chart
                fig = report_generator.create_distribution_chart(power_counts, accel_counts)
                st.plotly_chart(fig, use_container_width=True)
                st.caption("Preview of distribution chart included in both reports")
                
                # Add an explanation about the reports
                st.write("**Complete Report**: Includes distribution data, visualization, and transition tables")
                st.write("**Simple Report**: Includes only distribution data and visualization")
            
            with report_tab2:
                st.info("Custom report generation will be available in a future update.")

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