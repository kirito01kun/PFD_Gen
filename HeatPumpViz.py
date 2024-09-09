import plotly.graph_objects as go
import numpy as np
from shapes import create_pump, create_valve  # Import functions from shapes.py

node_count = 5
# Define nodes
nodes = {
    'A': {'x': 2, 'y': node_count - 1, 'label': 'Start'},
    'B': {'x': 2, 'y': node_count - 2, 'label': 'Decision'},
    'C': {'x': 2, 'y': node_count - 3, 'label': 'Process 1'},
    'D': {'x': 2, 'y': node_count - 4, 'label': 'Process 2'},
    'E': {'x': 2, 'y': node_count - 5, 'label': 'End'}
}

# Define edges
edges = [
    ('A', 'B'),
    ('B', 'C'),
    ('C', 'D'),
    ('D', 'E'),
]

# Define edges where shapes should be added
edges_with_pump = [
    ('B', 'C'),
    ('C', 'D')
]
edges_with_valve = [
    ('D', 'E')
]

# Create square shapes for nodes
node_shapes = []
annotations = []
node_positions = {}
for node_id, node_data in nodes.items():
    # Calculate square size dynamically based on label length
    size = 0.2
    
    # Store node positions for later use
    node_positions[node_id] = {
        'x': node_data['x'],
        'y': node_data['y'],
        'size': size
    }

    # Define square shape for each node
    node_shapes.append(
        dict(
            type='rect',
            x0=node_data['x'] - size,
            y0=node_data['y'] - size,
            x1=node_data['x'] + size,
            y1=node_data['y'] + size,
            line=dict(color='DarkSlateGrey', width=2),
            fillcolor='LightSkyBlue'
        )
    )

    # Add text annotation for each node
    annotations.append(
        dict(
            x=node_data['x'],
            y=node_data['y'],
            text=node_data['label'],
            showarrow=False,
            font=dict(color='black', size=12)
        )
    )

# Function to calculate the edge start and end points based on square outlines
def get_edge_coords(start_node, end_node):
    size_start = node_positions[start_node]['size']
    size_end = node_positions[end_node]['size']
    x0, y0 = node_positions[start_node]['x'], node_positions[start_node]['y']
    x1, y1 = node_positions[end_node]['x'], node_positions[end_node]['y']

    # Calculate the direction of the edge
    angle = np.arctan2(y1 - y0, x1 - x0)
    
    # Calculate the edge points from the square outlines
    x0_edge = x0 + size_start * np.cos(angle)
    y0_edge = y0 + size_start * np.sin(angle)
    x1_edge = x1 - size_end * np.cos(angle)
    y1_edge = y1 - size_end * np.sin(angle)

    return x0_edge, y0_edge, x1_edge, y1_edge

# Create line shapes for edges
line_shapes = []
triangle_shapes = []
for edge in edges:
    x0_edge, y0_edge, x1_edge, y1_edge = get_edge_coords(edge[0], edge[1])
    
    # Add line shape for edge
    line_shapes.append(
        dict(
            type='line',
            x0=x0_edge, y0=y0_edge, x1=x1_edge, y1=y1_edge,
            line=dict(color='black', width=2)
        )
    )

    # Calculate the midpoint of the line
    x_mid = (x0_edge + x1_edge) / 2
    y_mid = (y0_edge + y1_edge) / 2

    # Define the size of the triangles
    triangle_size = 0.05
    direction = "down"

    # Add custom shapes based on edge type
    if edge in edges_with_pump:
        pump_shapes = create_pump(x_mid, y_mid, triangle_size, direction)
        triangle_shapes.extend(pump_shapes)
    
    if edge in edges_with_valve:
        valve_shapes = create_valve(x_mid, y_mid, triangle_size)
        triangle_shapes.extend(valve_shapes)

# Add annotations
annotations.extend(
    dict(
        x=x1_edge,  # End point of the arrow
        y=y1_edge,
        ax=x0_edge,  # Start point of the arrow
        ay=y0_edge,
        xref='x', yref='y', axref='x', ayref='y',
        showarrow=True,
        arrowhead=2,  # Arrow style
        arrowsize=1,  # Size of the arrow
        arrowwidth=2,
        arrowcolor='black'
    ) for edge in edges
)

# Combine all shapes
all_shapes = node_shapes + line_shapes + triangle_shapes

# Create layout with shapes and annotations
layout = go.Layout(
    shapes=all_shapes,
    annotations=annotations,
    xaxis=dict(showgrid=False, zeroline=False, visible=False),
    yaxis=dict(showgrid=False, zeroline=False, visible=False),
    showlegend=False,
)

# Create figure
fig = go.Figure(layout=layout)

# Show the figure
fig.show()
