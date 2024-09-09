
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


def create_pump(x_mid, y_mid, triangle_size, direction):
    if direction == "down":
        pump = [
            dict(
                type='path',
                path=f'M {x_mid},{y_mid - triangle_size} L {x_mid - triangle_size},{y_mid + triangle_size*2} L {x_mid + triangle_size},{y_mid + triangle_size*2} Z',
                line=dict(color='black'),
                fillcolor='white'
            )
        ]
    else:
        pump = [
            dict(
                type='path',
                path=f'M {x_mid},{y_mid + triangle_size*2} L {x_mid - triangle_size},{y_mid - triangle_size} L {x_mid + triangle_size},{y_mid - triangle_size} Z',
                line=dict(color='black'),
                fillcolor='white'
            )
        ]
    return pump