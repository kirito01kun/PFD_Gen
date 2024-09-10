import plotly.graph_objects as go
from shapes import create_pump, create_valve  # Import functions from shapes.py

node_count = 5
# Define nodes with 'size' attribute
nodes = {
    'A': {'x': 2, 'y': node_count - 1, 'label': 'Start', 'size': 0.2},
    'B': {'x': 2, 'y': node_count - 2, 'label': 'Decision', 'size': 0.2},
    'C': {'x': 2, 'y': node_count - 3, 'label': 'Process 1', 'size': 0.2},
    'D': {'x': 2, 'y': node_count - 4, 'label': 'Process 2', 'size': 0.2},
    'E': {'x': 2, 'y': node_count - 5, 'label': 'End', 'size': 0.2}
}

# Define edges
edges = [
    ('A', 'B'),
    ('B', 'C'),
    ('C', 'D'),
    ('D', 'E'),
]

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
arrow_length = 0.15

# Function to get arrow positions around a node
def get_arrow_positions(x, y, size):
    """Get coordinates for arrow tips around a node."""
    # Top arrows (left and right tips)
    top_left_tip = (x - size - arrow_length, y + size / 2)
    top_right_tip = (x + size + arrow_length, y + size / 2)
    
    # Bottom arrows (left and right tips)
    bottom_left_tip = (x - size - arrow_length, y - size / 2)
    bottom_right_tip = (x + size + arrow_length, y - size / 2)
    
    return top_left_tip, top_right_tip, bottom_left_tip, bottom_right_tip

# Populate node shapes and annotations
for node_id, node_data in nodes.items():
    size = node_data['size']
    x, y = node_data['x'], node_data['y']
    
    # Store node positions and arrow positions for later use
    node_positions[node_id] = {'x': x, 'y': y, 'size': size}
    
    # Create node shape
    node_shapes.append(
        dict(
            type='rect',
            x0=x - size,
            y0=y - size,
            x1=x + size,
            y1=y + size,
            line=dict(color='DarkSlateGrey', width=2),
            fillcolor='LightSkyBlue'
        )
    )

    # Create text annotation for node
    annotations.append(
        dict(
            x=x,
            y=y,
            text=node_data['label'],
            showarrow=False,
            font=dict(color='black', size=14)
        )
    )

    # Get the arrow positions around the node
    top_left_tip, top_right_tip, bottom_left_tip, bottom_right_tip = get_arrow_positions(x, y, size)
    
    # Create arrows on top and bottom sides
    # Top arrows
    annotations.append(
        dict(
            x=top_left_tip[0], y=top_left_tip[1],
            ax=x - size, ay=y + size / 2,
            xref='x', yref='y', axref='x', ayref='y',
            showarrow=True, arrowhead=1, arrowwidth=3, arrowcolor='black'
        )
    )
    annotations.append(
        dict(
            x=top_right_tip[0], y=top_right_tip[1],
            ax=x + size, ay=y + size / 2,
            xref='x', yref='y', axref='x', ayref='y',
            showarrow=True, arrowhead=1, arrowwidth=3, arrowcolor='black'
        )
    )

    # Bottom arrows
    annotations.append(
        dict(
            x=bottom_left_tip[0], y=bottom_left_tip[1],
            ax=x - size, ay=y - size / 2,
            xref='x', yref='y', axref='x', ayref='y',
            showarrow=True, arrowhead=1, arrowwidth=3, arrowcolor='black'
        )
    )
    annotations.append(
        dict(
            x=bottom_right_tip[0], y=bottom_right_tip[1],
            ax=x + size, ay=y - size / 2,
            xref='x', yref='y', axref='x', ayref='y',
            showarrow=True, arrowhead=1, arrowwidth=3, arrowcolor='black'
        )
    )

# Function to connect edges between arrows
def connect_arrows_between_nodes(start_node, end_node):
    """Connect the tips of the bottom arrows of the start node to the tips of the top arrows of the end node."""
    # Get positions of the arrow tips
    _, _, start_bottom_left_tip, start_bottom_right_tip = get_arrow_positions(
        node_positions[start_node]['x'],
        node_positions[start_node]['y'],
        node_positions[start_node]['size']
    )
    end_top_left_tip, end_top_right_tip, _, _ = get_arrow_positions(
        node_positions[end_node]['x'],
        node_positions[end_node]['y'],
        node_positions[end_node]['size']
    )

    # Connect the bottom left arrow tip of the start node to the top left arrow tip of the end node
    line_shapes.append(
        dict(
            type='line',
            x0=start_bottom_left_tip[0], y0=start_bottom_left_tip[1],
            x1=end_top_left_tip[0], y1=end_top_left_tip[1],
            line=dict(color='black', width=2)
        )
    )

    # Connect the bottom right arrow tip of the start node to the top right arrow tip of the end node
    line_shapes.append(
        dict(
            type='line',
            x0=start_bottom_right_tip[0], y0=start_bottom_right_tip[1],
            x1=end_top_right_tip[0], y1=end_top_right_tip[1],
            line=dict(color='black', width=2)
        )
    )

# Create line shapes for connecting edges
line_shapes = []
for start, end in edges:
    connect_arrows_between_nodes(start, end)

# Create edge-specific custom shapes (pumps and valves)
triangle_shapes = []
for edge in edges:
    start, end = edge
    # Get the midpoint of the connecting lines
    start_x = node_positions[start]['x']
    start_y = node_positions[start]['y']
    end_x = node_positions[end]['x']
    end_y = node_positions[end]['y']
    x_mid = (start_x + end_x) / 2
    y_mid = (start_y + end_y) / 2
    triangle_size = 0.05
    direction = "down"

    if edge in edges_with_pump:
        pump_shapes = create_pump(x_mid, y_mid, triangle_size, direction)
        triangle_shapes.extend(pump_shapes)
    
    if edge in edges_with_valve:
        valve_shapes = create_valve(x_mid, y_mid, triangle_size)
        triangle_shapes.extend(valve_shapes)

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
