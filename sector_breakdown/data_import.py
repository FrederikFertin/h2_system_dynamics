import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

cwd = os.getcwd()
MainFolder = cwd + '\sector_breakdown'

SectorFolders = [f.path for f in os.scandir(MainFolder) if f.is_dir()]
SectorNames = [f.name for f in os.scandir(MainFolder) if f.is_dir()]

sector_data = {}
for ix, sector_path in enumerate(SectorFolders):
    SubsectorFolders = [f.path for f in os.scandir(sector_path) if f.is_dir()]
    SubsectorNames = [f.name for f in os.scandir(sector_path) if f.is_dir()]
    subsector_data = {}
    for jx, subsector_path in enumerate(SubsectorFolders):
        data_file = [f.path for f in os.scandir(subsector_path) if f.is_file()]
        if len(data_file) > 0:
            xls = pd.ExcelFile(data_file[0])
            subsector_data[SubsectorNames[jx]] = pd.read_excel(xls, 'Sheet 1', skiprows=9)
    sector_data[SectorNames[ix]] = subsector_data



for k1, v1 in sector_data.items():
    for k2, v2 in v1.items():
        years = v2.iloc[0,1:].index.astype(int).values
        values = v2.iloc[1,1:].values.astype(float)
        # Perform linear regression
        lambda_ = 0.96
        weights = lambda_ ** (years[-1] - years)
        
        reg = LinearRegression()
        reg.fit(years.reshape(-1, 1), values.reshape(-1, 1), sample_weight=weights)
        # reg.fit(years.reshape(-1, 1), values.reshape(-1, 1))

        # Predict values using the linear regression model
        predicted_values = reg.predict(years.reshape(-1, 1))
        future_years = np.arange(2023, 2051)
        future_predicted_values = reg.predict(future_years.reshape(-1, 1))

        # Plot the future predicted values
        plt.plot(future_years, future_predicted_values, linestyle='dashed', label='WLS Forecast')

        # Plot the original values and the predicted values
        plt.plot(years, values, label='Original')
        plt.plot(years, predicted_values, label='W. Linear model')
        plt.xlabel('Year')
        plt.ylabel('Energy demand [GWh]')
        ticks = np.arange(years[0], future_years[-1] + 5, 5)
        plt.xticks(ticks, rotation=30)
        plt.title(k2)
        plt.grid(alpha=0.5)
        plt.legend()
        # plt.savefig(cwd + "\\sector_breakdown\\sector_usage\\" + f'{k1}_{k2}.png')
        plt.show()

