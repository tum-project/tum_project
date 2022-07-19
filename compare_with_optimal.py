import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import wasserstein_distance

from generate_plot import generate_plot


# Function to calculate Chi-distance
def chi2_distance(A, B):
 
    # compute the chi-squared distance using above formula
    chi = 0.5 * np.sum([((a - b) ** 2) / (a + b)
                      for (a, b) in zip(A, B)])
    return chi 


def mse_distance(A, B, ax=0):
    mse = (np.square(A - B)).mean(axis=ax)
    return mse


# distance_function = wasserstein_distance
# distance_function = chi2_distance
distance_function = mse_distance

distance_function_name = str(distance_function.__name__)


def get_k_and_chi(Cu_location, O_location, input_home="feff_inputs", output_home="outputs", apply_fourier_transform=False):
    k, chi = generate_plot(Cu_location=Cu_location, O_location=O_location, input_home="feff_inputs", output_home="outputs", apply_fourier_transform=False)
    return k, chi


Cu_location = [0, 0, 0]
O_location = [2, 0, 0]
k0, chi0 = generate_plot(Cu_location=Cu_location, O_location=O_location, input_home="feff_inputs", output_home="outputs", apply_fourier_transform=False)

introduce_error = True
error_string = ""
if introduce_error:
    mu, sigma = 0, 0.001 # mean and standard deviation
    error_string = f"_error_{str(mu)}_{str(sigma)}"

    error_array = np.random.normal(mu, sigma, len(chi0))
    chi0 = chi0 + error_array
    print(chi0-error_array)

ks_and_chis = []
x_axis = []
for dx in range(-5, 5):
    O_location = [(2+dx/10), 0, 0]
    x_axis.append((2+dx/10))
    k, chi = get_k_and_chi(Cu_location=Cu_location, O_location=O_location, input_home="feff_inputs", output_home="outputs", apply_fourier_transform=False)
    ks_and_chis.append((k, chi))


distances = []
for i in range(len(ks_and_chis)):
    distance = distance_function(chi0, ks_and_chis[i][1])
    distances.append(distance)


# print(distances)
# print(x_axis)


x = x_axis
y = distances
fig, ax = plt.subplots()

plt.subplots_adjust(left=0.15)
ax.plot(x, y, **{'color': 'lightsteelblue', 'marker': 'o'})

ax.set_title(f"distance: {distance_function_name}")
ax.set_xlabel("O location in x axis")
ax.set_ylabel("Distance from optimal point (x=2.0)")
plots_folder = "plots"
plt.savefig(f"{plots_folder}/{distance_function_name}{error_string}_comparison.jpg")
