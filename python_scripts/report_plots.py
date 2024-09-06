import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import wasserstein_distance
# Define the sigmoid function
def sigmoid(x, L, k, x0):
    """
    Sigmoid function.
    
    Parameters
    ----------
    x : float
        Input value.
    L : float
        Maximum value of the function.
    k : float
        Steepness of the function.
    x0 : float
        Midpoint of the function.
        
    Returns
    -------
    float
        Value of the sigmoid function at x.
    """
    return L / (1 + np.exp(k*(x0-x)))

# Generate two distributions of random numbers and calculate the Wasserstein distance
n = 1000
np.random.seed(0)
a = np.random.normal(3, 4, n)
b = np.random.normal(2, 1, n)

# Calculate the Wasserstein distance
distance = wasserstein_distance(b, a)
print(f"Wasserstein distance between the two distributions: {distance:.2f}")

# Plot the two distributions
plt.hist(a, bins=30, alpha=0.5, label='Distribution A')
plt.hist(b, bins=30, alpha=0.5, label='Distribution B')
plt.legend(loc='best')
plt.title("Two random distributions")
plt.show()

x_values = np.logspace(-10,10,num=100,base=2)
one = 1900
zero = 2500

y = [one*x**(np.log2(1-0.18)) if x > 1 else zero - (zero - one) * x for x in x_values]
"""
# plot y as a function of x
plt.plot(x_values, y)
plt.xscale('log',base=10)
#plt.yscale('log',base=10)
plt.title("Electrolysis CAPEX - learning curve")
plt.xlabel("Installed capacity [GW]")
plt.ylabel("Capital cost [€/kW]")
plt.ylim(0, 3000)
plt.xlim(0.01, 1000)
plt.grid(alpha=0.4)
plt.show()
"""
# Run the sigmoid function with some parameters
x = np.linspace(0.0, 2.2, 100)
L = 1
k = 10
x0 = 0.9
y = sigmoid(x, L, k, x0)
y2 = sigmoid(x, L, 10, 1.1)

# Plot the normal cumulative distribution function
z = np.linspace(-3, 3, 100)
normal_cdf = 1/2 * (1 + np.tanh(z * np.sqrt(np.pi/8)))
plt.plot(z, normal_cdf)
plt.title("Normal cumulative distribution function")
plt.xlabel("z")
plt.ylabel("CDF")
plt.show()


# Plot the sigmoid function
plt.plot(x, y, label="New")
plt.plot(x, y2, label="Conventional")
plt.title("Sigmoid curves for new and conventional technologies")
plt.xlabel("Competitiveness")
plt.ylabel("Investment Level")
plt.legend(loc='best')
plt.show()

y3 = sigmoid(x, L, -5, 0)
plt.plot(x, y3, label="Decommissioning rate")
plt.title("Decommissiong as a function of competitiveness for fossil technologies") 
plt.xlabel("Competitiveness")
plt.ylabel("Decommissioning rate [%]")
plt.legend(loc='best')
plt.show()