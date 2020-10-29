import matplotlib.pyplot as plt
import numpy as np


def plot_graph(inputs_and_cycles):
    x_coors, y_coors = get_coors(inputs_and_cycles)
    x_np, y_np = convert_to_np(x_coors, y_coors)

    plt.plot(x_np, y_np, "o", ms=1)
    plt.xlabel("Input value")
    plt.ylabel("Number of cycles taken")
    plt.show()


def get_coors(inputs_and_cycles):
    x_coors = tuple(inputs_and_cycles.keys())
    y_coors = tuple(inputs_and_cycles.values())
    return x_coors, y_coors


def convert_to_np(x_coors, y_coors):
    x_np = np.array(x_coors)
    y_np = np.array(y_coors)
    return x_np, y_np
