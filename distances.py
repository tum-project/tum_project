from pprint import pprint

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import wasserstein_distance

from generate_plot import generate_plot


def mse_distance_function(A, B, ax=0):
    mse = (np.square(A - B)).mean(axis=ax)
    return mse


# Function to calculate Chi-distance
def chi2_distance(A, B):
    # compute the chi-squared distance using above formula
    chi = 0.5 * np.sum([((a - b) ** 2) / (a + b)
                      for (a, b) in zip(A, B)])
    return chi 


Cu_location = [0, 0, 0]
O_location = [2.1, 0, 0]

def six_positions(Cu_location, O_location):
    positions = []
    for i in range(3):
        for d in [0.1, -0.1]:
            vector = O_location[:]
            vector[i] += d
            vector[i] = round(vector[i], 1)
            positions.append(vector)
    return positions


def get_k_and_chi(Cu_location, O_location, input_home="feff_inputs", output_home="outputs", apply_fourier_transform=False):
    k, chi = generate_plot(Cu_location=Cu_location, O_location=O_location, input_home="feff_inputs", output_home="outputs", apply_fourier_transform=False)
    return k, chi


def six_distances(Cu_location, O_location):
    positions = six_positions(Cu_location, O_location)
    print(positions)
    positions = positions
    k0, chi0 = generate_plot(Cu_location=Cu_location, O_location=O_location, input_home="feff_inputs", output_home="outputs", apply_fourier_transform=False)
    
    ks_and_chis = []
    for i in range(len(positions)):
        k, chi = get_k_and_chi(Cu_location=Cu_location, O_location=positions[i], input_home="feff_inputs", output_home="outputs", apply_fourier_transform=False)
        ks_and_chis.append((k, chi))
    
    distances = []
    for i in range(len(positions)):
        distance = distance_function(chi0, ks_and_chis[i][1])
        distances.append(distance)
    position_distance_mapping = {tuple(positions[i]): distances[i] for i in range(len(positions))}
    return positions, distances, position_distance_mapping

 
Cu_location = [0, 0, 0]
O_location = [2.0, 0, 0]
k0, chi0 = generate_plot(Cu_location=Cu_location, O_location=O_location, input_home="feff_inputs", output_home="outputs", apply_fourier_transform=False)


introduce_error = True
error_string = ""
if introduce_error:
    mu, sigma = 0, 0.001 # mean and standard deviation
    error_string = f"_error_{str(mu)}_{str(sigma)}"

    error_array = np.random.normal(mu, sigma, len(chi0))
    chi0 = chi0 + error_array
    print(chi0-error_array)

test_positions = {0: [], 1:[], 2:[]}

for i in range(3):
    for d in range(-5, 6):
        vector = O_location[:]
        vector[i] += d/10
        vector[i] = round(vector[i], 1)
        test_positions[i].append(vector)

index_to_coordinate = {
    0: "x",
    1: "y",
    2: "z"
}

# pprint(test_positions)

distance_functions = [mse_distance_function, chi2_distance, wasserstein_distance]
# distance_function = distance_functions[0]
for distance_function in distance_functions:
    distance_function_name = str(distance_function.__name__)

    for i in range(3):
        x_axis = []
        y_axis = []
        for position in test_positions[i]:
            x = position[i]
            x_axis.append(x)
            k, chi = get_k_and_chi(Cu_location=Cu_location, O_location=position, input_home="feff_inputs", output_home="outputs", apply_fourier_transform=False)
            distance = distance_function(chi, chi0)
            y = distance
            y_axis.append(y)

        fig, ax = plt.subplots()

        plt.subplots_adjust(left=0.15)
        ax.plot(x_axis, y_axis, **{'color': 'black', 'marker': '.'})

        ax.set_title(f"{distance_function_name} from Cu: {str(Cu_location)} and O: {str(O_location)}")
        ax.set_xlabel(f"position in the co-ordinate {index_to_coordinate[i]}")
        ax.set_ylabel(f"distance from {str(O_location)}")

        figure_path = f"{index_to_coordinate[i]}_co-ordinate_{distance_function_name}{error_string}.png"
        plt.savefig(figure_path)
        plt.close(fig)
