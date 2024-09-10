import plotly.graph_objects as go
from shapes import create_pump, create_valve  # Import functions from shapes.py

# Node Class
class Node:
    def __init__(self, node_id, x, y, label, size=0.2):
        self.id = node_id
        self.x = x
        self.y = y
        self.label = label
        self.size = size
        self.prev_node = None
        self.next_node = None
        self.arrow_positions = self.get_arrow_positions()

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
    def __init__(self, start_node, end_node, conn_type='normal'):
        self.start_node = start_node
        self.end_node = end_node
        self.conn_type = conn_type  # Type of connection: 'normal', 'pump', 'valve'
        self.style = dict(color='black', width=2)  # Default style for normal lines

    def draw_connection(self):
        """Create shapes for connecting edges based on connection type."""
        line_shapes = []

        # Get arrow positions around nodes
        start_bottom_left_tip, start_bottom_right_tip = self.start_node.arrow_positions[2], self.start_node.arrow_positions[3]
        end_top_left_tip, end_top_right_tip = self.end_node.arrow_positions[0], self.end_node.arrow_positions[1]

        # Connect the bottom left arrow tip of the start node to the top left arrow tip of the end node
        line_shapes.append(
            dict(
                type='line',
                x0=start_bottom_left_tip[0], y0=start_bottom_left_tip[1],
                x1=end_top_left_tip[0], y1=end_top_left_tip[1],
                line=self.style
            )
        )

        # Connect the bottom right arrow tip of the start node to the top right arrow tip of the end node
        line_shapes.append(
            dict(
                type='line',
                x0=start_bottom_right_tip[0], y0=start_bottom_right_tip[1],
                x1=end_top_right_tip[0], y1=end_top_right_tip[1],
                line=self.style
            )
        )

        # Determine the location for pumps or valves
        if self.conn_type in ['pump', 'valve']:
            # Calculate the positions to place the shape on the edge
            shape_x = (start_bottom_left_tip[0] + end_top_left_tip[0]) / 2
            shape_y = (start_bottom_left_tip[1] + end_top_left_tip[1]) / 2

            # Add the appropriate shape
            if self.conn_type == 'valve':
                valve_shape = create_valve(shape_x, shape_y, 0.05)  # Adjust the size as needed
                line_shapes.extend(valve_shape)

            elif self.conn_type == 'pump':
                direction = 'up' if self.start_node.y > self.end_node.y else 'down'
                pump_shape = create_pump(shape_x, shape_y, 0.05, direction)  # Adjust the size as needed
                line_shapes.extend(pump_shape)

        return line_shapes


# GraphVisualizer Class
class GraphVisualizer:
    def __init__(self, linked_list):
        self.linked_list = linked_list
        self.shapes = []
        self.annotations = []

    def create_shapes(self):
        """Convert nodes and connections to Plotly shapes."""
        # Add node shapes and annotations
        for node in self.linked_list.nodes:
            # Create node shape
            self.shapes.append(
                dict(
                    type='rect',
                    x0=node.x - node.size,
                    y0=node.y - node.size,
                    x1=node.x + node.size,
                    y1=node.y + node.size,
                    line=dict(color='DarkSlateGrey', width=2),
                    fillcolor='LightSkyBlue'
                )
            )

            # Create text annotation for node
            self.annotations.append(
                dict(
                    x=node.x,
                    y=node.y,
                    text=node.label,
                    showarrow=False,
                    font=dict(color='black', size=14)
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
                    ax=node.x + node.size, ay=node.y + node.size / 2,
                    xref='x', yref='y', axref='x', ayref='y',
                    showarrow=True, arrowhead=1, arrowwidth=3, arrowcolor='black'
                )
            )

            # Bottom arrows
            self.annotations.append(
                dict(
                    x=bottom_left_tip[0], y=bottom_left_tip[1],
                    ax=node.x - node.size, ay=node.y - node.size / 2,
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

        # Add connection shapes
        for i in range(len(self.linked_list.nodes) - 1):
            start_node = self.linked_list.nodes[i]
            end_node = self.linked_list.nodes[i + 1]
            conn_type = 'valve' if i == 1 else 'pump' if i == 2 else 'normal'
            conn = Connection(start_node, end_node, conn_type=conn_type)
            self.shapes.extend(conn.draw_connection())

    def display_graph(self):
        """Render the graph using Plotly."""
        layout = go.Layout(
            shapes=self.shapes,
            annotations=self.annotations,
            xaxis=dict(showgrid=False, zeroline=False, visible=False),
            yaxis=dict(showgrid=False, zeroline=False, visible=False),
            showlegend=False,
        )
        fig = go.Figure(layout=layout)
        fig.show()

# Instantiate and use the classes
# Create nodes and doubly linked list
linked_list = DoublyLinkedList()
linked_list.add_node(Node('A', 2, 3, 'Start'))
linked_list.add_node(Node('B', 2, 2, 'Process 1'))
linked_list.add_node(Node('D', 2, 1, 'Process 2'))
linked_list.add_node(Node('E', 2, 0, 'End'))

# Visualize the graph
visualizer = GraphVisualizer(linked_list)
visualizer.create_shapes()
visualizer.display_graph()