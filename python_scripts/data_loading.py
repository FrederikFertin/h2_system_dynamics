import pandas as pd
import os


class data_loading_class:
    """Class to load data from Excel files and add future data points to the data.
    All prices are in 2020 EUR. """

    cwd = os.getcwd()
    ### ------- Load data from Excel files ------- ###
    # Format is a pd.Series with years as index and values as data

    # Loads fossil fuel forecast prices
    fuel_prices = pd.read_excel(cwd + "\\data\\fuel_prices.xlsx", sheet_name="Forecast_prices")

    # Loads biomass forecast prices
    biomass_prices = pd.read_excel(cwd + "\\data\\biomass_prices.xlsx",skiprows=1)

    # Loads the inflation rates
    inflation = pd.read_excel(cwd + "\\data\\european_inflation_rates_data.xlsx", sheet_name="european_inflation_rates", index_col=0)
    
    # Function which pads the data with a new data point 20 years later which is the same as the last data point
    # and a data point 20 years before which is the same as the first data point
    def _pad_data(self, series):
        # Pre data padding:
        first_year = series.index[0]
        new_first_year = first_year - 20
        new_first_value = series.iloc[0]
        # Post data padding:
        last_year = series.index[-1]
        new_last_year = last_year + 20
        new_last_years = list(range(last_year+1,new_last_year+1))
        new_last_value = series.iloc[-1]
        new_last_values = [new_last_value] * len(new_last_years)
        return pd.Series(data=[new_first_value], index=[new_first_year])._append(series)._append(pd.Series(data=new_last_values, index=new_last_years))
    
    # Function which loads the carbon taxes from self
    def load_carbon_taxes(self, *args, **kwargs):
        args = list(args)
        kwargs = dict(kwargs)

        # Loads forecasted carbon taxes
        if "seamaps" in args:
            self.carbon_tax = pd.read_excel(self.cwd + "\\data\\marine_fuel_costs_and_emissions.xlsx", sheet_name="CO2-Price")
            self.carbon_taxes = pd.Series(
                                index=self.carbon_tax["Year"].values,
                                data=self.carbon_tax["CO2-tax /tonne"].values,
                                dtype=float)
        else:
            self.carbon_tax = pd.read_excel(self.cwd + "\\data\\co2_tax.xlsx")
            self.carbon_taxes = pd.Series(
                                index=self.carbon_tax["Year"].values,
                                data=self.carbon_tax["EUR2015/tCO2"].values * self.inflation.loc[2015]['Inflation Multiplier'],
                                dtype=float)
        
        if "sensitivity" in kwargs:
            self.carbon_taxes = self.carbon_taxes * kwargs["sensitivity"]
        if "discount_rate" in kwargs:
            first_year = self.carbon_taxes.index[0]
            last_year = self.carbon_taxes.index[-1]
            c = self._pad_data(self.carbon_taxes)
            discount_index = [1/(1 + kwargs["discount_rate"])**i for i in range(20)]
            c_npv = []
            for i in range(first_year, last_year + 1):
                c_d = sum(c[year]*discount_index[j] for j, year in enumerate(range(i, i + 20))) / sum(discount_index)
                c_npv.append(c_d)
            c.loc[first_year:last_year] = c_npv
            self.carbon_taxes = c
            return self.carbon_taxes
        
        return self._pad_data(self.carbon_taxes)
    
    # Function which loads the gas prices from self
    def load_gas_prices(self, *args, **kwargs):
        args = list(args)
        kwargs = dict(kwargs)

        # Loads forecasted gas prices
        self.gas_prices = pd.Series(
                                index=self.fuel_prices.columns[1:].astype(int),
                                data=self.fuel_prices.loc[self.fuel_prices["[EUR/GJ]"] == "Gas"].values[0][1:] * self.inflation.loc[2015]['Inflation Multiplier'], # €/GJ
                                dtype=float)

        if "sensitivity" in kwargs:
            self.gas_prices = self.gas_prices * kwargs["sensitivity"]

        return self._pad_data(self.gas_prices)
    
    # Function which loads the oil prices from self
    def load_oil_prices(self, *args, **kwargs):
        args = list(args)
        kwargs = dict(kwargs)

        # Loads forecasted oil prices
        self.oil_prices = pd.Series(
                                index=self.fuel_prices.columns[1:].astype(int),
                                data=self.fuel_prices.loc[self.fuel_prices["[EUR/GJ]"] == "Oil"].values[0][1:] * self.inflation.loc[2015]['Inflation Multiplier'], # €/GJ
                                dtype=float)
        
        if "sensitivity" in kwargs:
            self.oil_prices = self.oil_prices * kwargs["sensitivity"]
        
        return self._pad_data(self.oil_prices)
    
    # Function which loads the coal prices from self
    def load_coal_prices(self, *args, **kwargs):
        args = list(args)
        kwargs = dict(kwargs)

        self.coal_prices = pd.Series(
                                index=self.fuel_prices.columns[1:].astype(int),
                                data=self.fuel_prices.loc[self.fuel_prices["[EUR/GJ]"] == "Coal"].values[0][1:] * self.inflation.loc[2015]['Inflation Multiplier'], # €/GJ
                                dtype=float)

        if "sensitivity" in kwargs:
            self.coal_prices = self.coal_prices * kwargs["sensitivity"]

        return self._pad_data(self.coal_prices)
    
    # Function which loads the woodchip prices from self
    def load_woodchip_prices(self, *args, **kwargs):
        args = list(args)
        kwargs = dict(kwargs)
        
        self.woodchip_prices = pd.Series(
                                index=self.biomass_prices["Euro/GJ"].values[1:].astype(int),
                                data=self.biomass_prices["Wood Chips"].values[1:].astype(float) * self.inflation.loc[2015]['Inflation Multiplier'], # €/GJ
                                dtype=float)

        if "sensitivity" in kwargs:
            self.woodchip_prices = self.woodchip_prices * kwargs["sensitivity"]

        return self._pad_data(self.woodchip_prices)
    
    # Function which loads the straw prices from self
    def load_straw_prices(self, *args, **kwargs):
        args = list(args)
        kwargs = dict(kwargs)

        self.straw_prices = pd.Series(
                                index=self.biomass_prices["Euro/GJ"].values[1:].astype(int),
                                data=self.biomass_prices["Straw"].values[1:].astype(float) * self.inflation.loc[2015]['Inflation Multiplier'], # €/GJ
                                dtype=float)

        if "sensitivity" in kwargs:
            self.straw_prices = self.straw_prices * kwargs["sensitivity"]
        
        return self._pad_data(self.straw_prices)
    
    # Function which loads the woodpellet prices from self
    def load_woodpellet_prices(self, *args, **kwargs):
        args = list(args)
        kwargs = dict(kwargs)

        self.woodpellet_prices = pd.Series(
                                index=self.biomass_prices["Euro/GJ"].values[1:].astype(int),
                                data=self.biomass_prices["Wood Pellets"].values[1:].astype(float) * self.inflation.loc[2015]['Inflation Multiplier'], # €/GJ
                                dtype=float)

        if "sensitivity" in kwargs:
            self.woodpellet_prices = self.woodpellet_prices * kwargs["sensitivity"]
        
        return self._pad_data(self.woodpellet_prices)
    
    # Function which loads the electricity prices from self
    def load_electricity_prices(self, *args, **kwargs):
        args = list(args)
        kwargs = dict(kwargs)

        self.electricity_prices = pd.Series(
                                index=[2020, 2030, 2040, 2050],
                                data=[40, 35, 30, 25], # €_2020/MWh (example data)
                                dtype=float)

        if "sensitivity" in kwargs:
            self.electricity_prices = self.electricity_prices * kwargs["sensitivity"]

        return self._pad_data(self.electricity_prices)

if __name__ == "__main__":
    data = data_loading_class()
    print(data.load_carbon_taxes(**{"discount_rate": 0.08}))
    print(data.load_gas_prices())
    print(data.load_oil_prices())
    print(data.load_woodchip_prices())
    print(data.load_straw_prices())
    print(data.load_woodpellet_prices())
    print(data.load_coal_prices())
    print(data.load_electricity_prices())