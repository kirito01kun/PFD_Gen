
def create_valve(x_mid, y_mid, triangle_size):
    valve = [
        dict(
                type='path',
                path=f'M {x_mid},{y_mid} L {x_mid - triangle_size/2},{y_mid + triangle_size*2} L {x_mid + triangle_size/2},{y_mid + triangle_size*2} Z',
                line=dict(color='black'),
                fillcolor='white'
            ),
        dict(
                type='path',
                path=f'M {x_mid},{y_mid} L {x_mid - triangle_size/2},{y_mid - triangle_size*2} L {x_mid + triangle_size/2},{y_mid - triangle_size*2} Z',
                line=dict(color='black'),
                fillcolor='white'
            )
    ]
    return valve



def create_pump(x_mid, y_mid, triangle_size, direction, label='COP:'):
    """Create a pump shape with a label beside it."""
    if direction == "down":
        pump = [
            dict(
                type='path',
                path=f'M {x_mid},{y_mid - triangle_size} L {x_mid - triangle_size},{y_mid + triangle_size*2} L {x_mid + triangle_size},{y_mid + triangle_size*2} Z',
                line=dict(color='black'),
                fillcolor='white'
            )
        ]
    else:  # Direction is "up"
        pump = [
            dict(
                type='path',
                path=f'M {x_mid - 0.0025},{y_mid + triangle_size*2} L {x_mid - triangle_size},{y_mid - triangle_size} L {x_mid + triangle_size},{y_mid - triangle_size} Z',
                line=dict(color='black'),
                fillcolor='white'
            )
        ]

    # Create annotation for the label on the right side of the pump
    label_annotation = dict(
        x=x_mid + 1.5 * triangle_size + 0.005*len(label),  # Position to the right of the pump
        y=y_mid,
        text=label,
        showarrow=False,
        font=dict(color='black', size=12),
        xref='x',
        yref='y'
    )

    return pump, label_annotation
