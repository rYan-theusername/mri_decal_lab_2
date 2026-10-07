import numpy as np
import matplotlib.pyplot as plt
import pyvista as pv
import ipywidgets as widgets
from IPython.display import display

# Render Plotter() inside VS Code / Jupyter instead of a desktop VTK window.
try:
    pv.set_jupyter_backend("trame")
except Exception:
    pass


def plot_3D_vectors(vectors, vector_origins=None, colors=None, labels=None):

    tips = np.array(vectors, dtype=np.float32)
    tails = np.zeros_like(vectors, dtype=np.float32) if vector_origins is None \
        else np.array(vector_origins, dtype=np.float32)

    directions = tips - tails  # (N, 3)
    lengths = np.linalg.norm(directions, axis=1)  # (N,)
    directions = directions / lengths[:, None]

    pl = pv.Plotter()

    SHAFT_RADIUS = 0.02  # Thickness of the line/shaft
    HEAD_RADIUS = 0.06  # Thickness of the base of the arrowhead
    HEAD_LENGTH = 0.15  # Constant length of the arrowhead

    for i in range(len(tails)):
        if lengths[i] <= HEAD_LENGTH:  # If the vector is shorter than the arrowhead itself, just draw a small cone
            if lengths[i] == 0: continue
            arrow_mesh = pv.Cone(center=tips[i], direction=directions[i], height=lengths[i], radius=HEAD_RADIUS)
            pl.add_mesh(arrow_mesh, color=colors[i] if colors else 'white')
            continue

        # 1. Create the Shaft (Cylinder)
        # Calculate exactly how long the shaft should be (total length minus arrowhead)
        shaft_len = lengths[i] - HEAD_LENGTH
        shaft_center = tails[i] + directions[i] * (shaft_len / 2.0)

        shaft = pv.Cylinder(
            center=shaft_center,
            direction=directions[i],
            radius=SHAFT_RADIUS,
            height=shaft_len
        )

        # 2. Create the Head (Cone)
        # Place the base of the cone right at the end of the cylinder shaft
        head_center = tails[i] + directions[i] * (shaft_len + HEAD_LENGTH / 2.0)

        head = pv.Cone(
            center=head_center,
            direction=directions[i],
            radius=HEAD_RADIUS,
            height=HEAD_LENGTH
        )

        # 3. Combine both parts into a single mesh
        custom_arrow = shaft.merge(head)

        color = colors[i] if colors is not None else 'white'
        label = labels[i] if labels is not None else f'vector {i+1}'
        pl.add_mesh(custom_arrow, color=color, label=label)

    # Find the bounding limits of vectors
    all_points = np.vstack([tails, tips])
    max_val = np.max(np.abs(all_points)) * 1.2  # 20% buffer

    # Draw light gray X, Y, and Z axis lines through the origin
    pl.add_lines(np.array([[-max_val, 0, 0], [max_val, 0, 0]]), color='gray', width=1)
    pl.add_lines(np.array([[0, -max_val, 0], [0, max_val, 0]]), color='gray', width=1)
    pl.add_lines(np.array([[0, 0, -max_val], [0, 0, max_val]]), color='gray', width=1)

    # Add text strings positioned right at the far edges of axis lines
    pl.add_point_labels([max_val, 0, 0], ["X"])
    pl.add_point_labels([0, max_val, 0], ["Y"])
    pl.add_point_labels([0, 0, max_val], ["Z"])

    pl.add_legend() if labels is not None else None
    pl.show()

def plot_vector_components(v, t, title='Vector Components over Time', labels=('$x$', '$y$', '$z$'),
                           linestyles=('b-', 'r-', 'g-')):

    plt.figure(figsize=(8, 4))

    for i in range(v.shape[0]):
        label = labels[i] if i < len(labels) else f'Component {i+1}'
        plt.plot(t, v[i, :], linestyles[i], label=label, linewidth=2)

    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.show()

def animate_vector_motion(vector, fps=30, dts_per_frame=1, show_path=True, dt=None):

    num_frames = int(vector.shape[1] / dts_per_frame)
    dt = 1/fps if dt is None else dt
    play = widgets.Play(
        value=0,
        min=0,
        max=num_frames - 1,
        step=1,
        interval=1000 // fps,  # fps -> ms per frame
        description="Play",
        disabled=False
    )
    slider = widgets.IntSlider(
        value=0,
        min=0,
        max=num_frames - 1,
        step=1,
        description='Frame:'
    )
    widgets.jslink((play, 'value'), (slider, 'value')) # links play button to slider
    time_label = widgets.Label(value=f"Time: {0} s") # to show the actual time corresponding to frame number

    pl = pv.Plotter()
    tail = np.array([0.0, 0.0, 0.0])
    max_val = np.max(np.abs(vector)) * 1.2  # 20% buffer

    # Draw light gray X, Y, and Z axis lines through the origin
    pl.add_lines(np.array([[-max_val, 0, 0], [max_val, 0, 0]]), color='gray', width=1)
    pl.add_lines(np.array([[0, -max_val, 0], [0, max_val, 0]]), color='gray', width=1)
    pl.add_lines(np.array([[0, 0, -max_val], [0, 0, max_val]]), color='gray', width=1)

    # Add text strings positioned right at the far edges of axis lines
    pl.add_point_labels([max_val, 0, 0], ["X"])
    pl.add_point_labels([0, max_val, 0], ["Y"])
    pl.add_point_labels([0, 0, max_val], ["Z"])

    def update_frame(change):

        i = change['new']   # 'new' holds the new ipywidget slider value
        i *= dts_per_frame
        time_label.value = f"Time: {i*dt:.2f} s"

        direction = vector[:, i] - tail
        length = np.linalg.norm(direction)
        direction = direction / length

        SHAFT_RADIUS = max_val / 80
        HEAD_RADIUS = max_val / 24
        HEAD_LENGTH = max_val / 8

        if length <= HEAD_LENGTH:
            # If the vector is shorter than the arrowhead itself, just draw a small cone
            cone_center = tail + direction * (length / 2.0)
            arrow_mesh = pv.Cone(center=cone_center, direction=direction, height=length, radius=HEAD_RADIUS)
        else:
            # 1. Create the Shaft (Cylinder)
            shaft_len = length - HEAD_LENGTH
            shaft_center = tail + direction * (shaft_len / 2.0)
            shaft = pv.Cylinder(
                center=shaft_center,
                direction=direction,
                radius=SHAFT_RADIUS,
                height=shaft_len
            )

            # 2. Create the Head (Cone)
            head_center = tail + direction * (shaft_len + HEAD_LENGTH / 2.0)
            head = pv.Cone(
                center=head_center,
                direction=direction,
                radius=HEAD_RADIUS,
                height=HEAD_LENGTH
            )

            # 3. Combine both parts into a single mesh
            arrow_mesh = shaft.merge(head)

        pl.add_mesh(arrow_mesh, name='vector', color='red')

        # Update or clear the path trail depending on the frame
        if show_path:
            if i > 0:
                path_points = vector[:, :i+1].T
                path_line = pv.lines_from_points(path_points)
                pl.add_mesh(path_line, name='path', color='blue', line_width=3)
            else:
                if 'path' in pl.actors:
                    pl.remove_actor('path')

    slider.observe(update_frame, names='value') # calls update_frame whenever the slider changes
    update_frame({'new': 0}) # start at time step 0

    ui = widgets.HBox([play, slider, time_label])
    display(ui)
    pl.show()