"""Bracket movement visualization module."""
import plotly.graph_objects as go
import pandas as pd
import numpy as np

class BracketVisualizer:
    def __init__(self):
        self.bracket_order = [
            'Goal Hit',
            'Elite',
            'Above Average',
            'Average',
            'Under Developed',
            'Severely Under Developed'
        ]
        self.colors = {
            'Goal Hit': '#2ecc71',
            'Elite': '#3498db',
            'Above Average': '#9b59b6',
            'Average': '#f1c40f',
            'Under Developed': '#e67e22',
            'Severely Under Developed': '#e74c3c'
        }

    def create_animated_transitions(self, transitions_dict, metric_type="Power"):
        """Create an animated visualization of bracket transitions."""
        # Initialize figure
        fig = go.Figure()

        # Get all periods from transitions dict
        periods = list(transitions_dict.keys())
        
        # For each bracket, create a trace showing its population over time
        for bracket in self.bracket_order:
            y_values = []
            
            # Calculate total users in this bracket for each period
            for period in periods:
                matrix = transitions_dict[period]
                # Sum both users staying in bracket and those moving to it
                total_in_bracket = matrix[bracket].sum()
                y_values.append(total_in_bracket)

            # Create trace for this bracket
            fig.add_trace(
                go.Scatter(
                    x=periods,
                    y=y_values,
                    name=bracket,
                    mode='lines+markers',
                    line=dict(color=self.colors[bracket], width=2),
                    marker=dict(size=10),
                )
            )

        # Update layout
        fig.update_layout(
            title=f"{metric_type} Development Bracket Transitions Over Time",
            xaxis_title="Test Period",
            yaxis_title="Number of Users",
            hovermode='x unified',
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )

        # Add animation
        fig.update_layout(
            updatemenus=[
                dict(
                    type="buttons",
                    showactive=False,
                    buttons=[
                        dict(
                            label="Play",
                            method="animate",
                            args=[None, {"frame": {"duration": 1000, "redraw": True},
                                       "fromcurrent": True}]
                        ),
                        dict(
                            label="Pause",
                            method="animate",
                            args=[[None], {"frame": {"duration": 0, "redraw": False},
                                         "mode": "immediate",
                                         "transition": {"duration": 0}}]
                        )
                    ]
                )
            ]
        )

        return fig

    def create_flow_diagram(self, transition_matrix, period):
        """Create a Sankey diagram showing flows between brackets."""
        # Prepare source, target, and value lists for Sankey diagram
        source = []
        target = []
        value = []
        
        # Create node labels with counts
        node_labels = self.bracket_order.copy()
        
        # First, ensure we have a DataFrame, not a Styler
        if hasattr(transition_matrix, 'data'):
            df = transition_matrix.data
        else:
            df = transition_matrix
        
        # Calculate flows
        for i, from_bracket in enumerate(self.bracket_order):
            for j, to_bracket in enumerate(self.bracket_order):
                flow = df.loc[from_bracket, to_bracket]
                if flow > 0:
                    source.append(i)
                    target.append(j)
                    value.append(flow)
        
        # Create Sankey diagram
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=node_labels,
                color=[self.colors[bracket] for bracket in self.bracket_order]
            ),
            link=dict(
                source=source,
                target=target,
                value=value
            )
        )])
        
        fig.update_layout(
            title_text=f"Bracket Transitions for {period}",
            font_size=12
        )
        
        return fig
