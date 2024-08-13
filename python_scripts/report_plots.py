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
    return L / (1 + np.exp(k*(x0-x)))

x_values = np.logspace(-10,10,num=100,base=2)
one = 1900
zero = 2500

y = [one*x**(np.log2(1-0.18)) if x > 1 else zero - (zero - one) * x for x in x_values]

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

# Run the sigmoid function with some parameters
x = np.linspace(0.0, 2.2, 100)
L = 1
k = 10
x0 = 0.9
y = sigmoid(x, L, k, x0)
y2 = sigmoid(x, L, 10, 1.1)

# Plot the sigmoid function
plt.plot(x, y, label="New")
plt.plot(x, y2, label="Conventional")
plt.title("Sigmoid curves for new and conventional technologies")
plt.xlabel("Competitiveness")
plt.ylabel("Investment Level")
plt.legend(loc='best')
plt.show()

print(2000/33.33)
print(1/15.7*1000)
print()
print(1/5.56*1000)
print(177)