"""
Creates a scatter graph relating input values to number of cycles taken.
"""

import matplotlib.pyplot as plt
import numpy as np


def plot_graph(inputs_and_cycles):
    """Plots the graph and shows it to the user."""
    x_np, y_np = get_np_coors(inputs_and_cycles)

    plt.plot(x_np, y_np, "o", ms=1)
    plt.xlabel("Input value")
    plt.ylabel("Number of cycles taken")
    plt.show()


def get_np_coors(inputs_and_cycles):
    """Converts dictionary into arrays of coordinates"""
    # convert dict keys and values into tuples
    x_coors = tuple(inputs_and_cycles.keys())
    y_coors = tuple(inputs_and_cycles.values())

    for item in x_coors:
        if isinstance(item, tuple):
            raise TypeError("More than one input given for a single run of the program. Cannot be graphed.")

    # convert resulting tuples into numpy arrays
    x_np = np.array(x_coors)
    y_np = np.array(y_coors)

    return x_np, y_np
