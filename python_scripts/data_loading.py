import pandas as pd
import os


class data_loading_class:
    """Class to load data from Excel files and add future data points to the data."""

    cwd = os.getcwd()
    ### ------- Load data from Excel files ------- ###
    # Format is a pd.Series with years as index and values as data

    # Loads forecasted carbon taxes
    carbon_tax = pd.read_excel(cwd + "\\data\\co2_tax.xlsx")
    carbon_taxes = pd.Series(index=carbon_tax["Year"].values, data=carbon_tax["EUR2015/tCO2"].values, dtype=float)

    # Loads fossil fuel forecast prices
    fuel_prices = pd.read_excel(cwd + "\\data\\fuel_prices.xlsx", sheet_name="Forecast_prices")
    gas_prices = pd.Series(index=fuel_prices.columns[1:].astype(int), data=fuel_prices.loc[fuel_prices["[EUR/GJ]"] == "Gas"].values[0][1:], dtype=float)
    oil_prices = pd.Series(index=fuel_prices.columns[1:].astype(int), data=fuel_prices.loc[fuel_prices["[EUR/GJ]"] == "Oil"].values[0][1:], dtype=float)
    coal_prices = pd.Series(index=fuel_prices.columns[1:].astype(int), data=fuel_prices.loc[fuel_prices["[EUR/GJ]"] == "Coal"].values[0][1:], dtype=float)

    # Loads biomass forecast prices
    biomass_prices = pd.read_excel(cwd + "\\data\\biomass_prices.xlsx",skiprows=1)
    woodchip_prices = pd.Series(index=biomass_prices["Euro/GJ"].values[1:].astype(int), data=biomass_prices["Wood Chips"].values[1:], dtype=float)
    straw_prices = pd.Series(index=biomass_prices["Euro/GJ"].values[1:].astype(int), data=biomass_prices["Straw"].values[1:], dtype=float)
    woodpellet_prices = pd.Series(index=biomass_prices["Euro/GJ"].values[1:].astype(int), data=biomass_prices["Wood Pellets"].values[1:], dtype=float)

    # Function which adds a new data point to a Series which is 20 years later than the last data point, but copies the last data point
    def add_future_data_point(self, series):
        last_year = series.index[-1]
        new_year = last_year + 20
        new_value = series.iloc[-1]
        return series._append(pd.Series(data=[new_value], index=[new_year]))
    
    # Function which loads the carbon taxes from self
    def load_carbon_taxes(self):
        return self.add_future_data_point(self.carbon_taxes)
    
    # Function which loads the gas prices from self
    def load_gas_prices(self):
        return self.add_future_data_point(self.gas_prices)
    
    # Function which loads the oil prices from self
    def load_oil_prices(self):
        return self.add_future_data_point(self.oil_prices)
    
    # Function which loads the woodchip prices from self
    def load_woodchip_prices(self):
        return self.add_future_data_point(self.woodchip_prices)
    
    # Function which loads the straw prices from self
    def load_straw_prices(self):
        return self.add_future_data_point(self.straw_prices)
    
    # Function which loads the woodpellet prices from self
    def load_woodpellet_prices(self):
        return self.add_future_data_point(self.woodpellet_prices)
    
    # Function which loads the coal prices from self
    def load_coal_prices(self):
        return self.add_future_data_point(self.coal_prices)
