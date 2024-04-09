import numpy as np
import matplotlib.pyplot as plt
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
    return L / (1 + np.exp(k*(x-x0)))

# Run the sigmoid function with some parameters
x = np.linspace(0.0, 2.2, 100)
L = 1
k = 10
x0 = 0.9
y = sigmoid(x, L, k, x0)
y2 = sigmoid(1/x, L, k, 0.9)
y3 = y + y2

# Plot the sigmoid function
plt.plot(x, y3)
plt.title("Sigmoid function")
plt.show()