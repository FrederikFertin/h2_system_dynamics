"""
Module financial_resources_and_hyperparameters
Translated using PySD version 3.14.0
"""

@component.add(
    name="BIOMASS PRICE",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "biomass_price_lookup": 1, "biomass_price_scaler": 1},
)
def biomass_price():
    """
    €/GJ
    """
    return biomass_price_lookup(time()) * biomass_price_scaler()


@component.add(
    name="BIOMASS PRICE LOOKUP",
    units="€/GJ",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_biomass_price_lookup"},
)
def biomass_price_lookup(x, final_subs=None):
    """
    €/GJ
    """
    return _hardcodedlookup_biomass_price_lookup(x, final_subs)


_hardcodedlookup_biomass_price_lookup = HardcodedLookups(
    [2022.0, 2030.0, 2040.0, 2050.0],
    [12.0, 11.0, 10.5, 8.0],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_biomass_price_lookup",
)


@component.add(
    name="CARBON TAX",
    units="€/tCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "carbon_tax_lookup": 1},
)
def carbon_tax():
    """
    €/tCO2
    !Time
    """
    return carbon_tax_lookup(time())


@component.add(
    name="CARBON TAX LOOKUP",
    units="€/tCO2",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_carbon_tax_lookup"},
)
def carbon_tax_lookup(x, final_subs=None):
    return _hardcodedlookup_carbon_tax_lookup(x, final_subs)


_hardcodedlookup_carbon_tax_lookup = HardcodedLookups(
    [2022, 2030, 2040, 2050],
    [55, 110, 200, 300],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_carbon_tax_lookup",
)


@component.add(
    name="COAL PRICE",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "coal_price_lookup": 1},
)
def coal_price():
    """
    €/t. To be updated
    """
    return coal_price_lookup(time())


@component.add(
    name="COAL PRICE LOOKUP",
    units="€/GJ",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_coal_price_lookup"},
)
def coal_price_lookup(x, final_subs=None):
    return _hardcodedlookup_coal_price_lookup(x, final_subs)


_hardcodedlookup_coal_price_lookup = HardcodedLookups(
    [2015.0, 2030.0, 2050.0],
    [2.85, 3.5, 3.5],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_coal_price_lookup",
)


@component.add(name="CROSS CONVENTIONAL", comp_type="Constant", comp_subtype="Normal")
def cross_conventional():
    return 1.1


@component.add(name="CROSS INNOVATION", comp_type="Constant", comp_subtype="Normal")
def cross_innovation():
    return 0.9


@component.add(
    name="DISCOUNT RATE", units="percent", comp_type="Constant", comp_subtype="Normal"
)
def discount_rate():
    return 0.08


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
    return 0 / 10**6


@component.add(
    name="ELECTRICITY PRICE",
    units="€/kWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "electricity_price_lookup": 1,
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
        electricity_price_lookup(time()) + electricity_emission_factor() * carbon_tax()
    ) * electricity_sensitivity()


@component.add(
    name="ELECTRICITY PRICE LOOKUP",
    units="€/kWh",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_electricity_price_lookup"},
)
def electricity_price_lookup(x, final_subs=None):
    """
    €/kWh Alternative: ([(0,0)-(10,10)],(2019,0.038),(2030,0.05),(2050,0.045) )
    """
    return _hardcodedlookup_electricity_price_lookup(x, final_subs)


_hardcodedlookup_electricity_price_lookup = HardcodedLookups(
    [2019.0, 2030.0, 2050.0],
    [0.038, 0.038, 0.038],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_electricity_price_lookup",
)


@component.add(
    name="ELECTRICITY SENSITIVITY",
    units="scalar",
    comp_type="Constant",
    comp_subtype="Normal",
)
def electricity_sensitivity():
    return 1


@component.add(
    name="GAS PRICE",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "gas_price_lookup": 1},
)
def gas_price():
    """
    €/GJ
    """
    return gas_price_lookup(time())


@component.add(
    name="GAS PRICE LOOKUP",
    units="€/GJ",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_gas_price_lookup"},
)
def gas_price_lookup(x, final_subs=None):
    return _hardcodedlookup_gas_price_lookup(x, final_subs)


_hardcodedlookup_gas_price_lookup = HardcodedLookups(
    [2015.0, 2030.0, 2040.0, 2050.0],
    [6.3, 8.5, 9.3, 10.2],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_gas_price_lookup",
)


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
    """
    Assumed to be similar to Wood Pellets. 1.2 times the average biomass price. Source for wood pellet price: "HRE_D6.1_Appendix_2 1"
    """
    return biomass_price() * 1.2


@component.add(
    name="OIL PRICE",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "oil_price_lookup": 1},
)
def oil_price():
    """
    €/GJ
    """
    return oil_price_lookup(time())


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


@component.add(
    name="OIL PRICE LOOKUP",
    units="€/GJ",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_oil_price_lookup"},
)
def oil_price_lookup(x, final_subs=None):
    return _hardcodedlookup_oil_price_lookup(x, final_subs)


_hardcodedlookup_oil_price_lookup = HardcodedLookups(
    [2019.0, 2030.0, 2040.0, 2050.0],
    [11.3, 14.3, 16.2, 20.2],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_oil_price_lookup",
)


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
