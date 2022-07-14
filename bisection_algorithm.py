def bisection(f,a,b,N):
    '''Approximate solution of f(x)=0 on interval [a,b] by bisection method.

    Parameters
    ----------
    f : function
        The function for which we are trying to approximate a solution f(x)=0.
    a,b : numbers
        The interval in which to search for a solution. The function returns
        None if f(a)*f(b) >= 0 since a solution is not guaranteed.
    N : (positive) integer
        The number of iterations to implement.

    Returns
    -------
    x_N : number
        The midpoint of the Nth interval computed by the bisection method. The
        initial interval [a_0,b_0] is given by [a,b]. If f(m_n) == 0 for some
        midpoint m_n = (a_n + b_n)/2, then the function returns this solution.
        If all signs of values f(a_n), f(b_n) and f(m_n) are the same at any
        iteration, the bisection method fails and return None.

    Examples
    --------
    >>> f = lambda x: x**2 - x - 1
    >>> bisection(f,1,2,25)
    1.618033990263939
    >>> f = lambda x: (2*x - 1)*(x - 3)
    >>> bisection(f,0,1,10)
    0.5
    '''
    if f(a)*f(b) >= 0:
        print("Bisection method fails.")
        return None
    a_n = a
    b_n = b
    for n in range(1,N+1):
        m_n = (a_n + b_n)/2
        f_m_n = f(m_n)
        print(f_m_n)
        if f(a_n)*f_m_n < 0:
            a_n = a_n
            b_n = m_n
        elif f(b_n)*f_m_n < 0:
            a_n = m_n
            b_n = b_n
        elif f_m_n == 0:
            print("Found exact solution.")
            return m_n
        else:
            print("Bisection method fails.")
            return None
    return (a_n + b_n)/2


import numpy as np
from generate_plot import generate_plot
from scipy.stats import wasserstein_distance


# Function to calculate Chi-distance
def chi2_distance(A, B):
    # compute the chi-squared distance using above formula
    chi = 0.5 * np.sum([((a - b) ** 2) / (a + b)
                      for (a, b) in zip(A, B)])
    return chi 


def mse_distance_function(A, B, ax=0):
    mse = (np.square(A - B)).mean(axis=ax)
    return mse

# distance_function = mse_distance_function
# distance_function = chi2_distance
distance_function = wasserstein_distance

distance_function_name = str(distance_function.__name__)

def get_k_and_chi(Cu_location, O_location, input_home="feff_inputs", output_home="outputs", apply_fourier_transform=False):
    k, chi = generate_plot(Cu_location=Cu_location, O_location=O_location, input_home="feff_inputs", output_home="outputs", apply_fourier_transform=False)
    return k, chi


def f(x):
    Cu_location, O_location = [0, 0, 0], [x, 0, 0]
    return distance_function(get_k_and_chi(Cu_location, O_location)[1], get_k_and_chi(Cu_location, O_location=[2, 0, 0])[1])


result = bisection(f, 1.0, 3.5, 50)
print(f"{distance_function_name}: {result}")
