import plotly.graph_objects as go
import pandas as pd
import numpy as np

def create_body_heat_map(region_scores):
    """
    Create a simplified body heat map visualization with region scores.
    
    Args:
        region_scores: A dictionary with region names as keys and average scores as values.
                      Expected keys: 'Arms', 'Legs', 'Torso', 'Press/Pull'
                      
    Returns:
        A plotly figure object with the heat map visualization
    """
    # Create a simplified body representation
    fig = go.Figure()
    
    # Set up the canvas
    fig.update_layout(
        width=500,
        height=600,
        margin=dict(l=0, r=0, t=30, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title="Body Region Development Scores",
    )
    
    # Define colors based on score values (same scale as development brackets)
    def get_color(score):
        if score >= 100:  # Goal Hit
            return 'rgb(0, 128, 0)'  # Dark Green
        elif score >= 90:  # Elite
            return 'rgb(50, 205, 50)'  # Lime Green
        elif score >= 80:  # Above Average
            return 'rgb(173, 255, 47)'  # GreenYellow
        elif score >= 70:  # Average
            return 'rgb(255, 255, 0)'  # Yellow
        elif score >= 60:  # Under Developed
            return 'rgb(255, 165, 0)'  # Orange
        else:  # Severely Under Developed
            return 'rgb(255, 0, 0)'  # Red
    
    # Extract scores with defaults if any region is missing
    arms_score = region_scores.get('Arms', 0)
    legs_score = region_scores.get('Legs', 0)
    torso_score = region_scores.get('Torso', 0)
    press_pull_score = region_scores.get('Press/Pull', 0)
    
    # Get colors for each region
    arms_color = get_color(arms_score)
    legs_color = get_color(legs_score)
    torso_color = get_color(torso_score)
    press_pull_color = get_color(press_pull_score)
    
    # Draw the body parts
    
    # Torso (rectangle)
    fig.add_shape(
        type="rect",
        x0=0.4, y0=0.3, x1=0.6, y1=0.6,
        line=dict(color="black", width=2),
        fillcolor=torso_color
    )
    
    # Arms (left and right rectangles)
    fig.add_shape(
        type="rect",
        x0=0.2, y0=0.4, x1=0.4, y1=0.5,
        line=dict(color="black", width=2),
        fillcolor=arms_color
    )
    fig.add_shape(
        type="rect",
        x0=0.6, y0=0.4, x1=0.8, y1=0.5,
        line=dict(color="black", width=2),
        fillcolor=arms_color
    )
    
    # Legs (left and right rectangles)
    fig.add_shape(
        type="rect",
        x0=0.4, y0=0.1, x1=0.45, y1=0.3,
        line=dict(color="black", width=2),
        fillcolor=legs_color
    )
    fig.add_shape(
        type="rect",
        x0=0.55, y0=0.1, x1=0.6, y1=0.3,
        line=dict(color="black", width=2),
        fillcolor=legs_color
    )
    
    # Head (circle)
    fig.add_shape(
        type="circle",
        x0=0.45, y0=0.6, x1=0.55, y1=0.7,
        line=dict(color="black", width=2),
        fillcolor="lightgray"
    )
    
    # Press/Pull (upper chest and back area)
    fig.add_shape(
        type="rect",
        x0=0.4, y0=0.5, x1=0.6, y1=0.6,
        line=dict(color="black", width=2),
        fillcolor=press_pull_color
    )
    
    # Add annotations with scores
    # Arms
    fig.add_annotation(
        x=0.3, y=0.45,
        text=f"Arms<br>{arms_score:.1f}%",
        showarrow=False,
        font=dict(size=12, color="black", family="Arial, bold"),
    )
    
    # Legs
    fig.add_annotation(
        x=0.5, y=0.15,
        text=f"Legs<br>{legs_score:.1f}%",
        showarrow=False,
        font=dict(size=12, color="black", family="Arial, bold"),
    )
    
    # Torso
    fig.add_annotation(
        x=0.5, y=0.4,
        text=f"Torso<br>{torso_score:.1f}%",
        showarrow=False,
        font=dict(size=12, color="black", family="Arial, bold"),
    )
    
    # Press/Pull
    fig.add_annotation(
        x=0.5, y=0.55,
        text=f"Press/Pull<br>{press_pull_score:.1f}%",
        showarrow=False,
        font=dict(size=12, color="black", family="Arial, bold"),
    )
    
    # Add legend with development brackets
    legend_items = [
        {"name": "Goal Hit (≥100%)", "color": 'rgb(0, 128, 0)'},
        {"name": "Elite (90-99%)", "color": 'rgb(50, 205, 50)'},
        {"name": "Above Average (80-89%)", "color": 'rgb(173, 255, 47)'},
        {"name": "Average (70-79%)", "color": 'rgb(255, 255, 0)'},
        {"name": "Under Developed (60-69%)", "color": 'rgb(255, 165, 0)'},
        {"name": "Severely Under (≤59%)", "color": 'rgb(255, 0, 0)'}
    ]
    
    # Add legend items as invisible traces with custom names
    for item in legend_items:
        fig.add_trace(
            go.Scatter(
                x=[None], y=[None], 
                mode='markers',
                marker=dict(size=10, color=item["color"]),
                name=item["name"],
                showlegend=True
            )
        )
    
    # Update layout to position the legend
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.1,
            xanchor="center",
            x=0.5,
            font=dict(size=10)
        ),
        xaxis=dict(visible=False, range=[0, 1]),
        yaxis=dict(visible=False, range=[0, 1]),
    )
    
    return fig