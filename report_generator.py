"""Report generator module for exercise data visualization."""
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import io

class ReportGenerator:
    """Generates reports for exercise data analysis."""
    
    def __init__(self):
        """Initialize the report generator with default settings."""
        pass
    
    def generate_distribution_report(self, power_counts, accel_counts):
        """
        Generate a report with distribution tables and a bar chart visualization.
        
        Args:
            power_counts (DataFrame): Power development distribution counts
            accel_counts (DataFrame): Acceleration development distribution counts
            
        Returns:
            bytes: PDF report as bytes
        """
        # Create a report buffer
        report_buffer = io.BytesIO()
        
        # Create an HTML string for the report
        html_content = self._generate_html_report(power_counts, accel_counts)
        
        # Return the HTML content as bytes
        report_buffer.write(html_content.encode())
        report_buffer.seek(0)
        
        return report_buffer.getvalue()
    
    def create_distribution_chart(self, power_counts, accel_counts):
        """
        Create a bar chart visualization for distribution data.
        
        Args:
            power_counts (DataFrame): Power development distribution
            accel_counts (DataFrame): Acceleration development distribution
            
        Returns:
            plotly.graph_objects.Figure: Plotly figure object
        """
        # Extract categories and test values
        categories = power_counts.index.tolist()
        
        # Set up the data for plotting
        test_columns = [col for col in power_counts.columns if 'Test' in col]
        
        # Create a figure with a single subplot for both power and acceleration
        fig = make_subplots(rows=1, cols=1)
        
        # Add bars for power data
        for i, col in enumerate(test_columns):
            fig.add_trace(
                go.Bar(
                    x=categories,
                    y=power_counts[col],
                    name=f"Power {col}",
                    marker_color='blue',
                    opacity=0.7,
                    showlegend=True
                )
            )
        
        # Add bars for acceleration data
        for i, col in enumerate(test_columns):
            fig.add_trace(
                go.Bar(
                    x=categories,
                    y=accel_counts[col],
                    name=f"Acceleration {col}",
                    marker_color='green',
                    opacity=0.7,
                    showlegend=True
                )
            )
        
        # Update layout
        fig.update_layout(
            title="Distribution of Users by Development Category",
            xaxis_title="Development Category",
            yaxis_title="Number of Users",
            barmode='group',
            bargap=0.15,
            bargroupgap=0.1,
            height=500,
            width=800,
            legend=dict(
                x=0.01,
                y=0.99,
                bgcolor='rgba(255, 255, 255, 0.5)',
                bordercolor='rgba(0, 0, 0, 0.1)',
                borderwidth=1
            )
        )
        
        return fig
    
    def _generate_html_report(self, power_counts, accel_counts):
        """
        Generate HTML report content.
        
        Args:
            power_counts (DataFrame): Power development distribution
            accel_counts (DataFrame): Acceleration development distribution
            
        Returns:
            str: HTML content
        """
        # Create a chart and convert to HTML
        fig = self.create_distribution_chart(power_counts, accel_counts)
        chart_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
        
        # Convert dataframes to HTML tables
        power_table = power_counts.to_html(classes='table table-striped', index=True)
        accel_table = accel_counts.to_html(classes='table table-striped', index=True)
        
        # Create HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Exercise Development Distribution Report</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    padding: 0;
                    color: #333;
                }}
                h1, h2 {{
                    color: #2c3e50;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                }}
                .table {{
                    border-collapse: collapse;
                    margin: 25px 0;
                    font-size: 0.9em;
                    width: 100%;
                    box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
                }}
                .table thead tr {{
                    background-color: #2c3e50;
                    color: #ffffff;
                    text-align: left;
                }}
                .table th,
                .table td {{
                    padding: 12px 15px;
                }}
                .table tbody tr {{
                    border-bottom: 1px solid #dddddd;
                }}
                .table tbody tr:nth-of-type(even) {{
                    background-color: #f3f3f3;
                }}
                .table tbody tr:last-of-type {{
                    border-bottom: 2px solid #2c3e50;
                }}
                .chart-container {{
                    width: 100%;
                    margin: 25px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Exercise Development Distribution Report</h1>
                
                <h2>Power Development Distribution</h2>
                {power_table}
                
                <h2>Acceleration Development Distribution</h2>
                {accel_table}
                
                <h2>Distribution Visualization</h2>
                <div class="chart-container">
                    {chart_html}
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_content
    
    def generate_downloadable_html(self, power_counts, accel_counts):
        """
        Generate downloadable HTML report.
        
        Args:
            power_counts (DataFrame): Power development distribution
            accel_counts (DataFrame): Acceleration development distribution
            
        Returns:
            bytes: HTML report as bytes
        """
        html_content = self._generate_html_report(power_counts, accel_counts)
        return html_content.encode('utf-8')