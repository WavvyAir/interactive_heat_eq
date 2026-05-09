import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

print("##############################################################")
print("# Interactive Heat Equation Solver with Plotly Visualization #")
print("##############################################################")

plate_length = 25
max_iter_time = 2000

alpha = 2
delta_x = 1

delta_t = (delta_x ** 2) / (4 * alpha) # calculate time step explicitly to ensure stability
gamma = (alpha * delta_t) / (delta_x ** 2)

####################################

boundary_type = np.zeros((plate_length, plate_length))
boundary_value = np.zeros((plate_length, plate_length))

mode = "dirichlet"
value = 100.0

#################################### Matplotlib interactive boundary drawing

print("Use mouse to draw on the edges of the plate. Press 'd' for Dirichlet mode, 'r' for insulated (neumann), '+' or '-' to adjust value, and 'Enter' to start the simulation.")

dpi = 100
fig, ax = plt.subplots(figsize=(1280/dpi, 720/dpi), dpi=dpi)
grid = np.zeros((plate_length, plate_length))
img = ax.imshow(grid, cmap="coolwarm", vmin=-100, vmax=100)

ax.set_title("Draw boundary on edges (d=Dirichlet, i=insulated, r=reset boundaries, Enter=start)")

started_by_user = False # Flag to detect if user closed the setup window without starting the simulation
drawing = False

def paint(i, j):
    if 0 <= i < plate_length and 0 <= j < plate_length: # Only allow drawing on boundary cells
        if i in [0, plate_length-1] or j in [0, plate_length-1]:
            if mode == "dirichlet":
                boundary_type[i, j] = 1
                boundary_value[i, j] = value
                grid[i, j] = value
            elif mode == "neumann":
                boundary_type[i, j] = 2
                grid[i, j] = -100  # Indicator value for insulated boundaries


def onclick(event):
    global drawing
    drawing = True
    onmove(event)

def onrelease(event):
    global drawing
    drawing = False

def onmove(event):
    if not drawing:
        return
    if event.xdata is None or event.ydata is None:
        return

    i = int(event.ydata)
    j = int(event.xdata)

    paint(i, j)

    img.set_data(grid)
    fig.canvas.draw_idle()

def onkey(event):
    global mode, value, started_by_user

    if event.key == 'd':
        mode = "dirichlet"
        print("Dirichlet mode")

    elif event.key == 'i':
        mode = "neumann"
        print("Neumann mode (Insulated)")

    elif event.key == '+':
        value += 10
        print("Value:", value)

    elif event.key == '-':
        if value == 0:
            print("Value cannot be negative.")
            return
        
        value -= 10
        print("Value:", value)

    elif event.key == 'r': # Reset boundaries to default state
        boundary_type.fill(0)
        boundary_value.fill(0)
        grid.fill(0)
        img.set_data(grid)
        fig.canvas.draw_idle()
        mode = "dirichlet"
        print("Boundaries reset.")

    elif event.key == 'enter':
        started_by_user = True
        plt.close()
        print("Starting visualization with Plotly, look for browser window popup...")

def force_close(event):
    if not started_by_user:
        print("Setup closed by user. Exiting.")
        exit(0)


fig.canvas.mpl_connect('button_press_event', onclick)
fig.canvas.mpl_connect('button_release_event', onrelease)
fig.canvas.mpl_connect('motion_notify_event', onmove)
fig.canvas.mpl_connect('key_press_event', onkey)
fig.canvas.mpl_connect('close_event', force_close)

plt.show()

#################################### Heat equation solver and boundary condition application

u = np.zeros((max_iter_time, plate_length, plate_length))

def apply_boundary(u_k):
    #Neumann
    
    # Top and Bottom edges
    for j in range(plate_length):
        if boundary_type[0, j] == 2: # Top
            u_k[0, j] = u_k[1, j]
        if boundary_type[plate_length-1, j] == 2: # Bottom
            u_k[plate_length-1, j] = u_k[plate_length-2, j]
            
    # Left and Right edges
    for i in range(plate_length):
        if boundary_type[i, 0] == 2: # Left
            u_k[i, 0] = u_k[i, 1]
        if boundary_type[i, plate_length-1] == 2: # Right
            u_k[i, plate_length-1] = u_k[i, plate_length-2]

    # Dirichlet
    for i in range(plate_length):
        for j in range(plate_length):
            if boundary_type[i, j] == 1:
                u_k[i, j] = boundary_value[i, j]


# Explicit finite difference method for heat equation
def calculate(u):
    for k in range(max_iter_time - 1):
        u[k+1, 1:-1, 1:-1] = (
            u[k, 1:-1, 1:-1] +
            gamma * (
                u[k, 2:, 1:-1] +
                u[k, :-2, 1:-1] +
                u[k, 1:-1, 2:] +
                u[k, 1:-1, :-2] -
                4 * u[k, 1:-1, 1:-1]
            )
        )

        apply_boundary(u[k+1])

    return u

u = calculate(u)

#################################### Plotly visualization

# No deep logic here, just mostly beautification stuff

frames = []

for k in range(max_iter_time): # Plotly animation frames
    frames.append(
        go.Frame(
            data=[
                go.Surface(
                    z=u[k],
                    colorscale="BlueRed",
                    cmin=0,
                    cmax=100,
                )
            ],
            name=str(k)
        )
    )


fig = go.Figure( 
    data=[
        go.Surface(
            z=u[0],
            colorscale="BlueRed",
            cmin=0,
            cmax=100,
        )
    ],
    frames=frames
)


# Adds contours while mouse hovers over the surface and changes default surface lighting
fig.update_traces(
    contours_z=dict(
        show=True, 
        usecolormap=False,
        highlightcolor="white", 
        highlightwidth=8, 
        project_z=False
        ),
        lighting=dict(
        ambient=0.9,
        diffuse=0.8,
        fresnel=0.2,
        specular=0.1,
        roughness=1.0
    ),
    selector=dict(type='surface')
        )



fig.update_layout(
    title=dict(text="<b>Heat Equation Visualization</b>", x=0.5, font=dict(size=32, color="#212121", family=' "Roboto", "Arial" ')),
    scene=dict(
        xaxis_title="x",
        yaxis_title="y",
        zaxis_title="Temperature",
        xaxis=dict(range=[0, plate_length - 1], autorange=False), # Fixes axes ranges to data range
        yaxis=dict(range=[0, plate_length - 1], autorange=False),
        zaxis=dict(range=[0, 100], autorange=False),
        uirevision="keep",
        dragmode="turntable",
        aspectmode='cube'
    ),

    updatemenus=[
        {
            "type": "buttons",
            "font": {
                "size": 20,
                "color": "#212121",
            },
            "pad": {"r": 20, "t": 20, "b": 10, "l": 10},
            "buttons": [
                {
                    "label": "  Play  ",
                    "method": "animate",
                    "args": [None, {"frame": {"duration": 16, "redraw": True}, "fromcurrent": True, "transition": {"duration": 0}}]
                },
                {

                    "label": "  Stop  ",
                    "method": "animate",
                    "args": [None, {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}]
                } 
            ]
        }
    ]
)

fig.show()