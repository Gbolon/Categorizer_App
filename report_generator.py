"""PDF Report generation for group-level analysis."""
import os
import io
import base64
import tempfile
from datetime import datetime
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    Image, PageBreak, ListFlowable, ListItem
)
from PIL import Image as PILImage
from io import BytesIO
from bracket_visualizer import BracketVisualizer


class PDFReportGenerator:
    """Generate PDF reports from analysis data."""
    
    def __init__(self, data_processor, matrix_generator):
        """Initialize with data processing components."""
        self.data_processor = data_processor
        self.matrix_generator = matrix_generator
        self.bracket_visualizer = BracketVisualizer()
        self.doc = None
        self.styles = getSampleStyleSheet()
        self.setup_styles()
        
    def setup_styles(self):
        """Setup custom styles for the report."""
        # Add custom styles
        self.styles.add(ParagraphStyle(
            name='Title',
            parent=self.styles['Heading1'],
            fontSize=24,
            alignment=TA_CENTER,
            spaceAfter=20
        ))
        
        self.styles.add(ParagraphStyle(
            name='Subtitle',
            parent=self.styles['Heading2'],
            fontSize=18,
            spaceAfter=12
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionTitle',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceAfter=8
        ))
        
        self.styles.add(ParagraphStyle(
            name='BodyText',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6
        ))
        
        self.styles.add(ParagraphStyle(
            name='Caption',
            parent=self.styles['Normal'],
            fontSize=9,
            alignment=TA_CENTER,
            textColor=colors.darkgrey
        ))
        
    def generate_report(self, processed_df, filename="exercise_analysis_report.pdf"):
        """Generate a complete PDF report from the processed data."""
        # Create a temporary file for the PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            temp_filename = tmp_file.name
        
        # Setup the document
        self.doc = SimpleDocTemplate(
            temp_filename, 
            pagesize=letter,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )
        
        # Build the document with all elements
        elements = []
        
        # Add cover page
        elements.extend(self._create_cover_page(processed_df))
        elements.append(PageBreak())
        
        # Add executive summary
        elements.extend(self._create_executive_summary(processed_df))
        elements.append(PageBreak())
        
        # Add group analysis sections
        elements.extend(self._create_group_analysis_section(processed_df))
        elements.append(PageBreak())
        
        # Add body region analysis
        elements.extend(self._create_body_region_analysis(processed_df))
        
        # Build and save the document
        self.doc.build(elements)
        
        # Return the path to the generated file
        return temp_filename
        
    def _create_cover_page(self, df):
        """Create the report cover page."""
        elements = []
        
        # Title
        title = Paragraph(
            "Exercise Development Analysis Report", 
            self.styles['Title']
        )
        elements.append(title)
        elements.append(Spacer(1, 0.5*inch))
        
        # Date and Time
        date_time = Paragraph(
            f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
            self.styles['Subtitle']
        )
        elements.append(date_time)
        elements.append(Spacer(1, 0.25*inch))
        
        # Summary Statistics
        total_users = len(df['user name'].unique())
        multi_test_users = self._count_multi_test_users(df)
        single_test_users = total_users - multi_test_users
        
        stats = [
            f"Total Athletes: {total_users}",
            f"Athletes with Multiple Tests: {multi_test_users}",
            f"Athletes with Single Test: {single_test_users}"
        ]
        
        for stat in stats:
            elements.append(Paragraph(stat, self.styles['BodyText']))
        
        return elements
        
    def _create_executive_summary(self, df):
        """Create the executive summary section."""
        elements = []
        
        # Section title
        title = Paragraph("Executive Summary", self.styles['Subtitle'])
        elements.append(title)
        elements.append(Spacer(1, 0.1*inch))
        
        # Generate group analysis data
        (power_counts, accel_counts, single_test_distribution,
         power_transitions_detail, accel_transitions_detail,
         power_average, accel_average,
         avg_power_change_1_2, avg_accel_change_1_2,
         avg_power_change_2_3, avg_accel_change_2_3,
         avg_days_between_tests) = self.matrix_generator.generate_group_analysis(df)
        
        # Key metrics paragraph
        key_metrics = Paragraph(
            f"The group shows an average power development of {power_average:.1f}% and "
            f"acceleration development of {accel_average:.1f}%. "
            f"From test 1 to test 2, power improved by {avg_power_change_1_2:+.1f}% and "
            f"acceleration by {avg_accel_change_1_2:+.1f}%. "
            f"The average time between tests was {avg_days_between_tests:.1f} days.",
            self.styles['BodyText']
        )
        elements.append(key_metrics)
        elements.append(Spacer(1, 0.15*inch))
        
        # Create summary table
        data = [
            ["Metric", "Power", "Acceleration"],
            ["Overall Development", f"{power_average:.1f}%", f"{accel_average:.1f}%"],
            ["Change (Test 1→2)", f"{avg_power_change_1_2:+.1f}%", f"{avg_accel_change_1_2:+.1f}%"],
            ["Change (Test 2→3)", f"{avg_power_change_2_3:+.1f}%", f"{avg_accel_change_2_3:+.1f}%"]
        ]
        
        table = Table(data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 0.25*inch))
        
        # Generate bracket distribution visualization and add to the report
        if power_counts is not None and not power_counts.empty:
            subtitle = Paragraph("Development Bracket Distribution", self.styles['SectionTitle'])
            elements.append(subtitle)
            
            # Create a pie chart for bracket distribution
            bracket_data = []
            for bracket in power_counts.index:
                if bracket != 'Total Users' and 'Test 1' in power_counts.columns:
                    count = power_counts.loc[bracket, 'Test 1']
                    if count > 0:
                        bracket_data.append((bracket, count))
            
            if bracket_data:
                fig = self._create_bracket_pie_chart(bracket_data, "Power Development Bracket Distribution")
                img_path = self._plotly_to_image(fig)
                img = Image(img_path, width=6*inch, height=4*inch)
                elements.append(img)
                elements.append(Paragraph("Power Development Bracket Distribution", self.styles['Caption']))
                elements.append(Spacer(1, 0.1*inch))
                
                # Clean up the temporary image file
                if os.path.exists(img_path):
                    os.remove(img_path)
        
        return elements
        
    def _create_group_analysis_section(self, df):
        """Create the group analysis section with transition matrices."""
        elements = []
        
        # Section title
        title = Paragraph("Group Development Analysis", self.styles['Subtitle'])
        elements.append(title)
        elements.append(Spacer(1, 0.1*inch))
        
        # Generate group analysis data
        (power_counts, accel_counts, single_test_distribution,
         power_transitions_detail, accel_transitions_detail,
         power_average, accel_average,
         avg_power_change_1_2, avg_accel_change_1_2,
         avg_power_change_2_3, avg_accel_change_2_3,
         avg_days_between_tests) = self.matrix_generator.generate_group_analysis(df)
        
        # Add transition matrices section
        subtitle = Paragraph("Transition Matrices", self.styles['SectionTitle'])
        elements.append(subtitle)
        elements.append(Spacer(1, 0.1*inch))
        
        # Add reading guide
        reading_guide = Paragraph(
            "Reading guide: Rows show starting bracket, columns show ending bracket. "
            "Numbers show how many users made each transition. "
            "Diagonal values (blue) show users who remained in the same bracket. "
            "Above diagonal (red) shows regression to lower brackets. "
            "Below diagonal (green) shows improvement to higher brackets.",
            self.styles['BodyText']
        )
        elements.append(reading_guide)
        elements.append(Spacer(1, 0.2*inch))
        
        # Add power transition matrices
        if power_transitions_detail:
            subtitle = Paragraph("Power Transitions", self.styles['SectionTitle'])
            elements.append(subtitle)
            
            for period, matrix in power_transitions_detail.items():
                # Create a flow diagram for this transition period
                fig = self.bracket_visualizer.create_flow_diagram(matrix, period)
                img_path = self._plotly_to_image(fig)
                img = Image(img_path, width=6*inch, height=4*inch)
                elements.append(img)
                elements.append(Paragraph(f"Power Transitions: {period}", self.styles['Caption']))
                elements.append(Spacer(1, 0.2*inch))
                
                # Clean up the temporary image file
                if os.path.exists(img_path):
                    os.remove(img_path)
                
                # Also add the matrix as a table
                elements.append(Paragraph(f"Transition Matrix: {period}", self.styles['SectionTitle']))
                elements.append(self._dataframe_to_table(matrix))
                elements.append(Spacer(1, 0.3*inch))
        
        # Add acceleration transition matrices
        if accel_transitions_detail:
            subtitle = Paragraph("Acceleration Transitions", self.styles['SectionTitle'])
            elements.append(subtitle)
            
            for period, matrix in accel_transitions_detail.items():
                # Create a flow diagram for this transition period
                fig = self.bracket_visualizer.create_flow_diagram(matrix, period)
                img_path = self._plotly_to_image(fig)
                img = Image(img_path, width=6*inch, height=4*inch)
                elements.append(img)
                elements.append(Paragraph(f"Acceleration Transitions: {period}", self.styles['Caption']))
                elements.append(Spacer(1, 0.2*inch))
                
                # Clean up the temporary image file
                if os.path.exists(img_path):
                    os.remove(img_path)
                
                # Also add the matrix as a table
                elements.append(Paragraph(f"Transition Matrix: {period}", self.styles['SectionTitle']))
                elements.append(self._dataframe_to_table(matrix))
                elements.append(Spacer(1, 0.3*inch))
        
        return elements
        
    def _create_body_region_analysis(self, df):
        """Create the body region analysis section."""
        elements = []
        
        # Section title
        title = Paragraph("Body Region Analysis", self.styles['Subtitle'])
        elements.append(title)
        elements.append(Spacer(1, 0.1*inch))
        
        # Get body region averages
        body_region_averages = self.matrix_generator.calculate_body_region_averages(df)
        
        # Create a summary table of all regions
        if body_region_averages:
            subtitle = Paragraph("Body Region Summary", self.styles['SectionTitle'])
            elements.append(subtitle)
            
            # Combine all region data into one dataframe for comparison
            summary_data = {}
            for region, averages in body_region_averages.items():
                if not averages.empty:
                    summary_data[region] = averages['Overall']
            
            if summary_data:
                summary_df = pd.DataFrame(summary_data)
                elements.append(self._dataframe_to_table(summary_df, format_func=lambda x: f"{x:.1f}%"))
                elements.append(Spacer(1, 0.2*inch))
                
                # Create a bar chart for region comparison
                fig = self._create_region_comparison_chart(summary_df)
                img_path = self._plotly_to_image(fig)
                img = Image(img_path, width=6*inch, height=4*inch)
                elements.append(img)
                elements.append(Paragraph("Region Development Comparison", self.styles['Caption']))
                elements.append(Spacer(1, 0.2*inch))
                
                # Clean up the temporary image file
                if os.path.exists(img_path):
                    os.remove(img_path)
        
        # Add detailed analyses for each region
        from exercise_constants import VALID_EXERCISES
        
        for region in VALID_EXERCISES.keys():
            # Add a page break before each new region (except the first one)
            if region != list(VALID_EXERCISES.keys())[0]:
                elements.append(PageBreak())
                
            subtitle = Paragraph(f"{region} Region Analysis", self.styles['SectionTitle'])
            elements.append(subtitle)
            
            # Get detailed metrics for this region
            power_df, accel_df, power_changes, accel_changes, lowest_power_exercise, lowest_power_value, lowest_accel_exercise, lowest_accel_value = (
                self.matrix_generator.get_region_metrics(df, region)
            )
            
            if power_df is not None and accel_df is not None:
                # Power development table
                power_title = Paragraph(f"{region} Region Power Development (%)", self.styles['SectionTitle'])
                elements.append(power_title)
                elements.append(self._dataframe_to_table(power_df, format_func=lambda x: f"{x:.1f}%"))
                elements.append(Spacer(1, 0.1*inch))
                
                # Add power changes
                if power_changes:
                    changes_list = []
                    
                    if 'test1_to_test2_pct' in power_changes and not pd.isna(power_changes['test1_to_test2_pct']):
                        change = power_changes['test1_to_test2_pct']
                        changes_list.append(f"Test 1 → Test 2: {change:+.1f}%")
                    
                    if 'test2_to_test3_pct' in power_changes and not pd.isna(power_changes['test2_to_test3_pct']):
                        change = power_changes['test2_to_test3_pct']
                        changes_list.append(f"Test 2 → Test 3: {change:+.1f}%")
                    
                    if lowest_power_exercise is not None and lowest_power_value is not None:
                        changes_list.append(f"Exercise with lowest change: {lowest_power_exercise} ({lowest_power_value:+.1f}%)")
                    
                    if changes_list:
                        power_changes_title = Paragraph("Power Development Changes:", self.styles['SectionTitle'])
                        elements.append(power_changes_title)
                        
                        # Create a bulleted list
                        bulleted_list = []
                        for item in changes_list:
                            bulleted_list.append(ListItem(Paragraph(item, self.styles['BodyText'])))
                        elements.append(ListFlowable(bulleted_list, bulletType='bullet', leftIndent=20))
                        elements.append(Spacer(1, 0.2*inch))
                
                # Acceleration development table
                accel_title = Paragraph(f"{region} Region Acceleration Development (%)", self.styles['SectionTitle'])
                elements.append(accel_title)
                elements.append(self._dataframe_to_table(accel_df, format_func=lambda x: f"{x:.1f}%"))
                elements.append(Spacer(1, 0.1*inch))
                
                # Add acceleration changes
                if accel_changes:
                    changes_list = []
                    
                    if 'test1_to_test2_pct' in accel_changes and not pd.isna(accel_changes['test1_to_test2_pct']):
                        change = accel_changes['test1_to_test2_pct']
                        changes_list.append(f"Test 1 → Test 2: {change:+.1f}%")
                    
                    if 'test2_to_test3_pct' in accel_changes and not pd.isna(accel_changes['test2_to_test3_pct']):
                        change = accel_changes['test2_to_test3_pct']
                        changes_list.append(f"Test 2 → Test 3: {change:+.1f}%")
                    
                    if lowest_accel_exercise is not None and lowest_accel_value is not None:
                        changes_list.append(f"Exercise with lowest change: {lowest_accel_exercise} ({lowest_accel_value:+.1f}%)")
                    
                    if changes_list:
                        accel_changes_title = Paragraph("Acceleration Development Changes:", self.styles['SectionTitle'])
                        elements.append(accel_changes_title)
                        
                        # Create a bulleted list
                        bulleted_list = []
                        for item in changes_list:
                            bulleted_list.append(ListItem(Paragraph(item, self.styles['BodyText'])))
                        elements.append(ListFlowable(bulleted_list, bulletType='bullet', leftIndent=20))
                        elements.append(Spacer(1, 0.2*inch))
            else:
                info_text = Paragraph(f"Not enough multi-test user data to display detailed {region.lower()} region analysis.", self.styles['BodyText'])
                elements.append(info_text)
        
        return elements
    
    def _count_multi_test_users(self, df):
        """Count the number of users with multiple test instances."""
        multi_test_count = 0
        for user in df['user name'].unique():
            user_df = df[df['user name'] == user]
            if len(user_df['test instance'].unique()) > 1:
                multi_test_count += 1
        return multi_test_count
    
    def _plotly_to_image(self, fig):
        """Convert a plotly figure to an image file for embedding in the PDF."""
        # Create a temporary file for the image
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
            img_path = tmp_file.name
        
        # Export the figure to the temporary file
        fig.write_image(img_path, width=800, height=500)
        
        return img_path
    
    def _dataframe_to_table(self, df, format_func=None):
        """Convert a DataFrame to a formatted ReportLab Table."""
        # Extract data from DataFrame
        data = [df.columns.tolist()]  # Header row
        for i, row in df.iterrows():
            row_data = [i]  # Row header
            for col in df.columns:
                value = row[col]
                if format_func and pd.notna(value):
                    value = format_func(value)
                row_data.append(value)
            data.append(row_data)
        
        # Add row headers as first column
        header_row = [''] + list(df.columns)
        data[0] = header_row
        
        # Create the table
        col_widths = [1.2*inch] + [1*inch for _ in range(len(df.columns))]
        table = Table(data, colWidths=col_widths)
        
        # Style the table
        style = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Header row background
            ('BACKGROUND', (0, 1), (0, -1), colors.lightgrey),  # First column background
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Header text color
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center all text
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),  # Row headers font
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),  # Header bottom padding
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),  # Table grid
        ]
        table.setStyle(TableStyle(style))
        
        return table
    
    def _create_bracket_pie_chart(self, bracket_data, title):
        """Create a pie chart for bracket distribution."""
        labels = [item[0] for item in bracket_data]
        values = [item[1] for item in bracket_data]
        
        # Get colors from bracket visualizer
        colors = [self.bracket_visualizer.colors.get(label, '#CCCCCC') for label in labels]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=colors),
            textinfo='value+percent',
            insidetextorientation='radial',
            hole=0.3
        )])
        
        fig.update_layout(
            title=title,
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1
            )
        )
        
        return fig
    
    def _create_region_comparison_chart(self, df):
        """Create a bar chart comparing all body regions."""
        # Create data for plotting
        regions = df.columns.tolist()
        
        fig = go.Figure()
        
        # Add bars for power
        fig.add_trace(go.Bar(
            x=regions,
            y=df.loc['Power Average'],
            name='Power',
            marker_color='#3498db'
        ))
        
        # Add bars for acceleration
        fig.add_trace(go.Bar(
            x=regions,
            y=df.loc['Acceleration Average'],
            name='Acceleration',
            marker_color='#2ecc71'
        ))
        
        # Layout
        fig.update_layout(
            title="Body Region Development Comparison",
            xaxis_title="Body Region",
            yaxis_title="Development (%)",
            barmode='group',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig