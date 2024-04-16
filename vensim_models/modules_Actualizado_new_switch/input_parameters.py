"""
Module input_parameters
Translated using PySD version 3.13.4
"""


@component.add(
    name="BIOMASS PRICE",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def biomass_price():
    """
    €/GJ
    """
    return np.interp(time(), [2019.0, 2030.0, 2040.0, 2050.0], [12.0, 11.0, 10.5, 5.0])


@component.add(
    name="CARBON TAX",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def carbon_tax():
    """
    €/tCO2
    """
    return np.interp(time(), [2019, 2030, 2040, 2050], [55, 110, 200, 300])


@component.add(name="DISCOUNT RATE", comp_type="Constant", comp_subtype="Normal")
def discount_rate():
    return 0.08


@component.add(
    name="ELECTRICITY PRICE",
    units="€/kWh",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def electricity_price():
    """
    €/kWh
    """
    return np.interp(time(), [2019.0, 2030.0, 2050.0], [0.038, 0.05, 0.045])


@component.add(name="ELECTRICITY TAX", comp_type="Constant", comp_subtype="Normal")
def electricity_tax():
    """
    €/MWh
    """
    return 0


@component.add(
    name="GAS PRICE",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def gas_price():
    """
    €/GJ
    """
    return np.interp(time(), [2015.0, 2030.0, 2040.0, 2050.0], [6.3, 8.5, 9.3, 10.2])


@component.add(name="INTEREST RATES", comp_type="Constant", comp_subtype="Normal")
def interest_rates():
    return 0.08


@component.add(
    name="OIL PRICE",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def oil_price():
    """
    €/GJ
    """
    return np.interp(time(), [2019.0, 2030.0, 2040.0, 2050.0], [11.3, 14.3, 16.2, 20.2])
