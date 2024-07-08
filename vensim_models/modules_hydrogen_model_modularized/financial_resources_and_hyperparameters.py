"""
Module financial_resources_and_hyperparameters
Translated using PySD version 3.14.0
"""

@component.add(
    name="BIOMASS BASE PRICE",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def biomass_base_price():
    """
    €/GJ
    """
    return np.interp(time(), [2019.0, 2030.0, 2040.0, 2050.0], [12.0, 11.0, 10.5, 8.0])


@component.add(
    name="BIOMASS PRICE",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"biomass_base_price": 1, "biomass_demand_saturation": 1},
)
def biomass_price():
    """
    €/GJ
    """
    return biomass_base_price() * biomass_demand_saturation()


@component.add(
    name="CARBON TAX",
    units="€/tCO2",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def carbon_tax():
    """
    €/tCO2
    """
    return np.interp(time(), [2019, 2030, 2040, 2050], [55, 110, 200, 300])


@component.add(
    name="COAL PRICE",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def coal_price():
    """
    €/t. To be updated
    """
    return np.interp(time(), [2015.0, 2030.0, 2050.0], [2.85, 3.5, 3.5])


@component.add(name="CROSS CONVENTIONAL", comp_type="Constant", comp_subtype="Normal")
def cross_conventional():
    return 0.9


@component.add(name="CROSS INNOVATION", comp_type="Constant", comp_subtype="Normal")
def cross_innovation():
    return 1.1


@component.add(
    name="DIESEL PRICE",
    units="€/l",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"oil_price": 1, "oil_price_init": 1},
)
def diesel_price():
    """
    Scale the diesel price with the oil price by assuming that the 2019 oil price corresponds to a diesel price of 1.5€/l.
    """
    return oil_price() / oil_price_init() * 1.5


@component.add(
    name="DISCOUNT RATE", units="percent", comp_type="Constant", comp_subtype="Normal"
)
def discount_rate():
    return 0.08


@component.add(
    name="ELECTRICITY BASE PRICE",
    units="€/kWh",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def electricity_base_price():
    """
    €/kWh Alternative: ([(0,0)-(10,10)],(2019,0.038),(2030,0.05),(2050,0.045) )
    """
    return np.interp(time(), [2019.0, 2030.0, 2050.0], [0.038, 0.038, 0.038])


@component.add(
    name="ELECTRICITY EMISSION FACTOR",
    units="tCO2/kWh",
    comp_type="Constant",
    comp_subtype="Normal",
)
def electricity_emission_factor():
    """
    https://ens.dk/en/our-services/statistics-data-key-figures-and-energy-maps/ key-figures
    """
    return 50 / 10**6


@component.add(
    name="ELECTRICITY PRICE",
    units="€/kWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "electricity_base_price": 1,
        "electricity_emission_factor": 1,
        "carbon_tax": 1,
        "electricity_sensitivity": 1,
    },
)
def electricity_price():
    """
    €/kWh
    """
    return (
        electricity_base_price() + electricity_emission_factor() * carbon_tax()
    ) * electricity_sensitivity()


@component.add(
    name="ELECTRICITY SENSITIVITY", comp_type="Constant", comp_subtype="Normal"
)
def electricity_sensitivity():
    return 0.4


@component.add(
    name="GAS PRICE",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def gas_price():
    """
    €/GJ
    """
    return np.interp(time(), [2015.0, 2030.0, 2040.0, 2050.0], [6.3, 8.5, 9.3, 10.2])


@component.add(
    name="INTEREST RATE", units="percent", comp_type="Constant", comp_subtype="Normal"
)
def interest_rate():
    return 0.08


@component.add(
    name="MODEL SEED",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "seed": 1},
)
def model_seed():
    return time() * seed()


@component.add(
    name="OIL BIOMASS PRICE",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"biomass_price": 1},
)
def oil_biomass_price():
    return biomass_price() * 1.3


@component.add(
    name="OIL PRICE",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def oil_price():
    """
    €/GJ
    """
    return np.interp(time(), [2019.0, 2030.0, 2040.0, 2050.0], [11.3, 14.3, 16.2, 20.2])


@component.add(
    name="OIL PRICE INIT",
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_oil_price_init": 1},
    other_deps={"_initial_oil_price_init": {"initial": {"oil_price": 1}, "step": {}}},
)
def oil_price_init():
    return _initial_oil_price_init()


_initial_oil_price_init = Initial(lambda: oil_price(), "_initial_oil_price_init")


@component.add(name="SEED", comp_type="Constant", comp_subtype="Normal")
def seed():
    return 40


@component.add(name="SLOPE", comp_type="Constant", comp_subtype="Normal")
def slope():
    return 5


@component.add(
    name="SYSTEM NOISE", units="percent", comp_type="Constant", comp_subtype="Normal"
)
def system_noise():
    """
    Standard deviation in percent of flow rate with which each state is changing.
    """
    return 0.03


@component.add(name="USD to EUR", comp_type="Constant", comp_subtype="Normal")
def usd_to_eur():
    """
    https://www.google.com/finance/quote/USD-EUR?sa=X&sqi=2&ved=2ahUKEwjLjIbOkrCGAxUz3wIH HdJaCOAQmY0JegQIJBAw Exchange rate 28/05-2024
    """
    return 0.92
