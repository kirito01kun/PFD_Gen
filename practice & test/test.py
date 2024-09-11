import plotly.graph_objects as go

# Minimal example shape
direction = 'down'
x_mid = 1
y_mid = 1
triangle_size = 0.5

if direction == "down":
    pump_path = f'M {x_mid},{y_mid - triangle_size} L {x_mid - triangle_size},{y_mid + triangle_size*2} L {x_mid + triangle_size},{y_mid + triangle_size*2} Z'
else:  # Direction is "up"
    pump_path = f'M {x_mid},{y_mid + triangle_size*2} L {x_mid - triangle_size},{y_mid - triangle_size} L {x_mid + triangle_size},{y_mid - triangle_size} Z'

pump_shape = go.layout.Shape(
    type='path',
    path=pump_path,
    line=dict(color='black'),
    fillcolor='white'
)

label_annotation = dict(
    x=x_mid + 1.5 * triangle_size,  # Position label to the right of the pump
    y=y_mid,
    text="COP",
    showarrow=False,
    xanchor='left',
    yanchor='middle',
    font=dict(size=12, color='black')
)

layout = go.Layout(
    shapes=[pump_shape],
    annotations=[label_annotation]  # Add label annotation here
)

fig = go.Figure(layout=layout)
fig.write_image("simple_test_with_label.svg")
