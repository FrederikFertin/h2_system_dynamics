import pysd
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import data_loading


def plot_stocks(stocks):
    fig, axs = plt.subplots(int(len(stocks)/2), 2, figsize=(10, 5*len(stocks)))

    for i, stock in enumerate(stocks):
        ax = axs[int(np.round(i/4+0.1)), np.round(i%2) ]
        ax.plot(stock.index, stock["SMR Users"], label="SMR Users (LT={})".format(1/stock["Green Hydrogen Demand"].iloc[0]))
        ax.plot(stock.index, stock["Adopters"], label="Adopters (LT={})".format(1/stock["Green Hydrogen Demand"].iloc[0]))
        ax.plot(stock.index, stock["EC Users"], label="EC Users (LT={})".format(1/stock["Green Hydrogen Demand"].iloc[0]))
        ax2 = ax.twinx()
        ax2.plot(stock.index, stock["EC price"], label="EC price (LT={})".format(1/stock["Green Hydrogen Demand"].iloc[0]), color='black')
        
        h, l = ax.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        ax.legend(h+h2, l+l2, loc='best')
        
        
    plt.show()

### ------- Load model from Vensim mdl file ------- ###
cwd = os.getcwd()

# Specify the file path of the Vensim model
model_file = os.path.join(cwd,"vensim_models/Actualizado_new_flow.mdl")

# Load the model using the `load` function from `pysd`
model = pysd.read_vensim(model_file)

# Now you can use the `model` object to interact with the Vensim model
# For example, you can access model variables, run simulations, etc.
run1 = model.run(return_columns=["carbon_tax", "int shipping consumption", "int shipping fossil energy consumption", "ammonia shipping consumption", "methanol shipping consumption", "shipping hydrogen demand"])

### ------- Load new data at run time ------- ###
dl = data_loading.data_loading_class()
carbon_taxes = dl.load_carbon_taxes()
gas_prices = dl.load_gas_prices()
oil_prices = dl.load_oil_prices()
woodchip_prices = dl.load_woodchip_prices()

### ------- Run model with new data ------- ###
model.set_components({"carbon_tax": carbon_taxes})
model.set_components({"gas_price": gas_prices, "oil_price": oil_prices})
model.set_components({"biomass_price": woodchip_prices})

run2 = model.run(return_columns=["carbon_tax", "int shipping consumption", "int shipping fossil energy consumption", "ammonia shipping consumption", "methanol shipping consumption", "shipping hydrogen demand"])

### ------- Plot results ------- ###
# Plot run and run2 together
fig, ax1 = plt.subplots(figsize=(10, 5))
ax2 = ax1.twinx()
ax1.plot(run1.index, run1["int shipping consumption"], label="int shipping consumption", linestyle='-', color='grey')
ax1.plot(run1.index, run1["int shipping fossil energy consumption"], label="fossil", linestyle='--', color='blue')
ax1.plot(run1.index, run1["ammonia shipping consumption"], label="ammonia", linestyle=':', color='blue')
ax1.plot(run1.index, run1["methanol shipping consumption"], label="methanol", linestyle='-.', color='blue')

ax1.plot(run2.index, run2["int shipping fossil energy consumption"], label="fossil", linestyle='--', color='red')
ax1.plot(run2.index, run2["ammonia shipping consumption"], label="ammonia", linestyle=':', color='red')
ax1.plot(run2.index, run2["methanol shipping consumption"], label="methanol", linestyle='-.', color='red')

ax2.plot(run1.index, run1["shipping hydrogen demand"], label="hydrogen shipping demand", linestyle='-', color='blue',alpha=0.5)
ax2.plot(run2.index, run2["shipping hydrogen demand"], label="hydrogen shipping demand", linestyle='-', color='red', alpha=0.5)

# set same y limits
ax1.set_ylim(0, 10**6)
ax2.set_ylim(0, 2*10**7)

ax1.set_xlabel("Time")
ax1.set_ylabel("Shipping consumption [GWh]")
ax2.set_ylabel("Hydrogen shipping demand [t H2]")

# collect legend handles and labels
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
# merge legends
ax1.legend(h1+h2, l1+l2, loc='best')
ax1.grid(alpha=0.5)

plt.show()

fig, ax1 = plt.subplots(figsize=(10, 5))
ax2 = ax1.twinx()
ax1.plot(run1.index, run1["carbon_tax"], label="carbon tax", linestyle='--', color='blue')
ax1.plot(run2.index, run2["carbon_tax"], label="carbon tax", linestyle='--', color='red')

ax2.plot(run1.index, run1["shipping hydrogen demand"], label="hydrogen shipping demand", linestyle='-', color='blue',alpha=0.5)
ax2.plot(run2.index, run2["shipping hydrogen demand"], label="hydrogen shipping demand", linestyle='-', color='red', alpha=0.5)

# set same y limits
ax1.set_ylim(0, 400)
ax2.set_ylim(0, 2*10**7)

ax1.set_xlabel("Time")
ax1.set_ylabel("Shipping consumption [GWh]")
ax2.set_ylabel("Hydrogen shipping demand [t H2]")

# collect legend handles and labels
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
# merge legends
ax1.legend(h1+h2, l1+l2, loc='best')
ax1.grid(alpha=0.5)

plt.show()
