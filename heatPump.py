import plotly.graph_objects as go
from shapes import create_pump, create_valve  # Import functions from shapes.py

# Node Class
class Node:
    def __init__(self, node_id, x, y, label, temperatures):
        self.id = node_id
        self.x = x
        self.y = y
        self.label = label
        self.size = 0.2
        self.prev_node = None
        self.next_node = None
        self.arrow_positions = self.get_arrow_positions()
        self.top_left_label = str(temperatures[0]) + ' °C' # Top In
        self.top_right_label = str(temperatures[1]) + ' °C' # Top Out
        self.bottom_right_label = str(temperatures[2]) + ' °C' # Buttom In
        self.bottom_left_label = str(temperatures[3]) + ' °C' # Buttom Out

    def get_arrow_positions(self):
        """Calculate the positions of arrow tips around the node."""
        arrow_length = 0.15
        # Top arrows (left and right tips)
        top_left_tip = (self.x - self.size - arrow_length, self.y + self.size / 2)
        top_right_tip = (self.x + self.size + arrow_length, self.y + self.size / 2)
        # Bottom arrows (left and right tips)
        bottom_left_tip = (self.x - self.size - arrow_length, self.y - self.size / 2)
        bottom_right_tip = (self.x + self.size + arrow_length, self.y - self.size / 2)
        return top_left_tip, top_right_tip, bottom_left_tip, bottom_right_tip

    def connect_to(self, next_node):
        """Connect this node to the next node in the list."""
        self.next_node = next_node
        next_node.prev_node = self


# DoublyLinkedList Class
class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.nodes = []

    def add_node(self, node):
        """Add a node to the end of the linked list."""
        if not self.head:
            self.head = node
            self.tail = node
        else:
            self.tail.connect_to(node)
            self.tail = node
        self.nodes.append(node)

    def find_node_by_id(self, node_id):
        """Find and return a node by its ID."""
        for node in self.nodes:
            if node.id == node_id:
                return node
        return None

class Connection:
    def __init__(self, start_node, end_node, conn_type='normal', side='left', conn_label=''):
        self.start_node = start_node
        self.end_node = end_node
        self.conn_type = conn_type  # Type of connection: 'normal', 'pump', 'valve'
        self.conn_label = conn_label
        self.side = side  # Side of the connection: 'left' or 'right'
        self.style = dict(color='black', width=2)  # Default style for normal lines

    def draw_connection(self):
        """Create shapes for connecting edges based on connection type and side."""
        line_shapes = []
        annotations = []

        # Get arrow positions around nodes
        if self.side == 'left':
            start_tip = self.start_node.arrow_positions[2]  # bottom left tip
            end_tip = self.end_node.arrow_positions[0]  # top left tip
            line_shapes.append(
                dict(
                    type='line',
                    x0=start_tip[0], y0=start_tip[1],
                    x1=end_tip[0] + 0.004, y1=end_tip[1],
                    line=self.style
                )
            )

        else:
            start_tip = self.start_node.arrow_positions[3]  # bottom right tip
            end_tip = self.end_node.arrow_positions[1]  # top right tip
            # Connect the chosen arrow tip of the start node to the end node
            line_shapes.append(
                dict(
                    type='line',
                    x0=start_tip[0] - 0.004, y0=start_tip[1],
                    x1=end_tip[0], y1=end_tip[1],
                    line=self.style
                )
            )

        # Determine the location for pumps or valves
        if self.conn_type in ['pump', 'valve']:
            # Calculate the positions to place the shape on the edge
            shape_x = (start_tip[0] + end_tip[0]) / 2
            shape_y = (start_tip[1] + end_tip[1]) / 2

            # Add the appropriate shape
            if self.conn_type == 'valve':
                valve_shape = create_valve(shape_x, shape_y, 0.05)  # Adjust the size as needed
                line_shapes.extend(valve_shape)

            elif self.conn_type == 'pump':
                direction = 'up' if self.start_node.y > self.end_node.y else 'down'
                pump_shape, pump_label = create_pump(shape_x, shape_y, 0.05, direction, self.conn_label)  # Adjust the size as needed
                line_shapes.extend(pump_shape)
                annotations.append(pump_label)
        

        return line_shapes, annotations


# GraphVisualizer Class
class GraphVisualizer:
    def __init__(self, heatPumpNetwork):
        self.heatPumpNetwork = heatPumpNetwork
        self.shapes = []
        self.annotations = []
        self.connections = []  # To store connections

    # Inside GraphVisualizer class

    def create_shapes(self):
        """Convert nodes and connections to Plotly shapes."""
        # Add node shapes and annotations
        for node in self.heatPumpNetwork.nodes:
            # Create node shape
            self.shapes.append(
                dict(
                    type='rect',
                    x0=node.x - node.size,
                    y0=node.y - node.size,
                    x1=node.x + node.size,
                    y1=node.y + node.size,
                    line=dict(color='DarkSlateGrey', width=2),
                    fillcolor='LightGreen'
                )
            )

            # Create text annotation for node
            self.annotations.append(
                dict(
                    x=node.x,
                    y=node.y,
                    text=node.label,
                    showarrow=False,
                    font=dict(color='black', size=15)
                )
            )

            # Create arrows on top and bottom sides
            top_left_tip, top_right_tip, bottom_left_tip, bottom_right_tip = node.arrow_positions
            # Top arrows
            self.annotations.append(
                dict(
                    x=node.x - node.size, y=top_left_tip[1],
                    ax=top_left_tip[0], ay=node.y + node.size / 2,
                    xref='x', yref='y', axref='x', ayref='y',
                    showarrow=True, arrowhead=1, arrowwidth=3, arrowcolor='black'
                )
            )
            self.annotations.append(
                dict(
                    x=top_right_tip[0], y=top_right_tip[1],
                    ax=node.x + node.size - 0.004, ay=node.y + node.size / 2,
                    xref='x', yref='y', axref='x', ayref='y',
                    showarrow=True, arrowhead=1, arrowwidth=3, arrowcolor='black'
                )
            )

            # Bottom arrows
            self.annotations.append(
                dict(
                    x=bottom_left_tip[0], y=bottom_left_tip[1],
                    ax=node.x - node.size + 0.004, ay=node.y - node.size / 2,
                    xref='x', yref='y', axref='x', ayref='y',
                    showarrow=True, arrowhead=1, arrowwidth=3, arrowcolor='black'
                )
            )
            self.annotations.append(
                dict(
                    x=node.x + node.size, y=bottom_right_tip[1],
                    ax=bottom_right_tip[0], ay=node.y - node.size / 2,
                    xref='x', yref='y', axref='x', ayref='y',
                    showarrow=True, arrowhead=1, arrowwidth=3, arrowcolor='black'
                )
            )

            # Create arrow labels
            self.annotations.append(
                dict(
                    x=(top_left_tip[0] + (node.x - node.size)) / 2,
                    y=(top_left_tip[1] + (node.y + node.size / 2)) / 2 + 0.05,
                    text=node.top_left_label,
                    showarrow=False,
                    font=dict(color='black', size=12),
                    xref='x', yref='y'
                )
            )
            self.annotations.append(
                dict(
                    x=(top_right_tip[0] + (node.x + node.size)) / 2,
                    y=(top_right_tip[1] + (node.y + node.size / 2)) / 2 + 0.05,
                    text=node.top_right_label,
                    showarrow=False,
                    font=dict(color='black', size=12),
                    xref='x', yref='y'
                )
            )
            self.annotations.append(
                dict(
                    x=(bottom_left_tip[0] + (node.x - node.size)) / 2,
                    y=(bottom_left_tip[1] + (node.y - node.size / 2)) / 2 - 0.05,
                    text=node.bottom_left_label,
                    showarrow=False,
                    font=dict(color='black', size=12),
                    xref='x', yref='y'
                )
            )
            self.annotations.append(
                dict(
                    x=(bottom_right_tip[0] + (node.x + node.size)) / 2,
                    y=(bottom_right_tip[1] + (node.y - node.size / 2)) / 2 - 0.05,
                    text=node.bottom_right_label,
                    showarrow=False,
                    font=dict(color='black', size=12),
                    xref='x', yref='y'
                )
            )

        # Initialize connections without setting their types
        for i in range(len(self.heatPumpNetwork.nodes) - 1):
            start_node = self.heatPumpNetwork.nodes[i]
            end_node = self.heatPumpNetwork.nodes[i + 1]
            # Add connections for both left and right sides
            for side in ['left', 'right']:
                conn = Connection(start_node, end_node, side=side)  # Initialize with default connection type
                self.connections.append(conn)  # Store connection object

    def change_connection_type(self, start_node_id, end_node_id, new_type, side, label=''):
        """Change the type of a specific side connection."""
        for conn in self.connections:
            if conn.start_node.id == start_node_id and conn.end_node.id == end_node_id and conn.side == side:
                conn.conn_type = new_type  # Update connection type
                conn.conn_label = label
                return  # Exit after finding and updating the connection
    
    def get_conn_types(self):
        for conn in self.connections:
            print(conn.conn_type)

    def draw_connections(self):
        """Draw the connections based on their current types."""
        for conn in self.connections:
            shapes, annotations = conn.draw_connection()  # Get shapes and annotations for the connection
            self.shapes.extend(shapes)  # Add shapes to the shapes list
            self.annotations.extend(annotations)  # Add annotations to the annotations list

    def display_graph(self):
        """Render the graph using Plotly."""
        self.draw_connections()  # Draw connections after applying changes
        layout = go.Layout(
            shapes=self.shapes,
            annotations=self.annotations,
            xaxis=dict(showgrid=False, zeroline=False, visible=False),
            yaxis=dict(showgrid=False, zeroline=False, visible=False),
            showlegend=False,
        )
        fig = go.Figure(layout=layout)
        fig.show()
    

    def calculate_graph_bounds(self):
        """Calculate the boundaries of the graph for centering and zooming."""
        x_coords = []
        y_coords = []

        # Collect x and y coordinates of all nodes
        for node in self.heatPumpNetwork.nodes:
            x_coords.append(node.x)
            y_coords.append(node.y)

        # Collect x and y coordinates of all annotations
        for annotation in self.annotations:
            if 'x' in annotation:
                x_coords.append(annotation['x'])
            if 'y' in annotation:
                y_coords.append(annotation['y'])

        # Calculate the minimum and maximum coordinates
        min_x = min(x_coords)
        max_x = max(x_coords)
        min_y = min(y_coords)
        max_y = max(y_coords)

        return min_x, max_x, min_y, max_y

    def save_graph(self, file_name):
        """Save the graph as an image."""
        # Draw connections first to ensure all elements are considered
        self.draw_connections()

        # Calculate the graph bounds
        min_x, max_x, min_y, max_y = self.calculate_graph_bounds()


        # Define the width and height based on the bounds
        width = max_x - min_x
        height = max_y - min_y

        # Set the layout
        layout = go.Layout(
            shapes=self.shapes,
            annotations=self.annotations,
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                visible=False,
                range=[min_x - 0.1 * width, max_x + 0.1 * width]  # add margins
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                visible=False,
                range=[min_y - 0.1 * height, max_y + 0.1 * height]  # add margins
            ),
            width=800,  # Set a fixed width for the saved image
            height=800 * (height / 1.5*width),  # Maintain aspect ratio
            showlegend=False,
        )

        # Create figure
        fig = go.Figure(layout=layout)

        # Save the image using kaleido
        fig.write_image(file_name)

        print(f"Graph saved as {file_name}")



temp_values = [[101, 105, 149, 110],
               [59, 59, 70, 60],
               [60, 70, 73, 66]]

# Use the classes
heatPumpNetwork = DoublyLinkedList()
heatPumpNetwork.add_node(Node('A', 2, 2, 'Condensor', temp_values[0]))
heatPumpNetwork.add_node(Node('B', 2, 1, 'Evaporator', temp_values[1]))
heatPumpNetwork.add_node(Node('C', 2, 0, 'TropiCHeat', temp_values[2]))


visualizer = GraphVisualizer(heatPumpNetwork)
visualizer.create_shapes()

# Change a specific side connection type
visualizer.change_connection_type('A', 'B', 'valve', 'left')
visualizer.change_connection_type('A', 'B', 'pump', 'right', 'COP: 3.04')

visualizer.save_graph('my_graph.svg')

visualizer.get_conn_types()
visualizer.display_graph()