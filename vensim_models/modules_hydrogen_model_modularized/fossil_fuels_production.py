"""
Module fossil_fuels_production
Translated using PySD version 3.14.0
"""

@component.add(
    name="Blue NG cost",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "gas_price": 1,
        "ccs_cost": 1,
        "gas_emission_factor": 1,
        "carbon_tax": 1,
        "cc_capture_rate": 1,
    },
)
def blue_ng_cost():
    return gas_price() + gas_emission_factor() * (
        (1 - cc_capture_rate()) * carbon_tax() + ccs_cost()
    )


@component.add(
    name="Crude oil LHV", units="MJ/kg", comp_type="Constant", comp_subtype="Normal"
)
def crude_oil_lhv():
    return 44


@component.add(
    name="GAS EMISSION FACTOR",
    units="tCO2/GJ",
    comp_type="Constant",
    comp_subtype="Normal",
)
def gas_emission_factor():
    """
    https://www.eia.gov/environment/emissions/co2_vol_mass.php
    """
    return 52.91 / 1000 / 1.0551


@component.add(
    name="Grey NG cost",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gas_price": 1, "gas_emission_factor": 1, "carbon_tax": 1},
)
def grey_ng_cost():
    return gas_price() + carbon_tax() * gas_emission_factor()


@component.add(
    name="HFO cost",
    units="€/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"oil_price": 1, "carbon_tax": 1, "hfo_emission_factor": 1},
)
def hfo_cost():
    """
    €/MJ Oil
    """
    return oil_price() / 1000 + carbon_tax() * (hfo_emission_factor() / 1000)


@component.add(
    name="HFO emission factor",
    units="tCO2/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"crude_oil_lhv": 1},
)
def hfo_emission_factor():
    """
    Emission factor: 0.075 t per GJ
    """
    return 3.15 / crude_oil_lhv()


@component.add(
    name="Jetfuel cost",
    units="€/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "carbon_tax": 1,
        "jetfuel_emission_factor": 1,
        "jetfuel_crack_spread": 1,
        "oil_price": 1,
    },
)
def jetfuel_cost():
    return (
        carbon_tax() * jetfuel_emission_factor()
        + (1 + jetfuel_crack_spread()) * oil_price()
    ) / 1000


@component.add(
    name="Jetfuel crack spread",
    units="percent",
    comp_type="Constant",
    comp_subtype="Normal",
)
def jetfuel_crack_spread():
    """
    30 % of crude oil price
    """
    return 0.3


@component.add(
    name="Jetfuel emission factor",
    units="tCO2/GJ",
    comp_type="Constant",
    comp_subtype="Normal",
)
def jetfuel_emission_factor():
    """
    https://www.eia.gov/environment/emissions/co2_vol_mass.php
    """
    return 73.19 / 1000 / 1.0551


@component.add(
    name="Jetfuel LHV", units="MJ/kg", comp_type="Constant", comp_subtype="Normal"
)
def jetfuel_lhv():
    """
    https://en.wikipedia.org/wiki/Jet_fuel
    """
    return 43


@component.add(
    name="Naphtha cost",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "naphtha_crack_spread": 1,
        "oil_price": 1,
        "carbon_tax": 1,
        "naphtha_emission_factor": 1,
    },
)
def naphtha_cost():
    """
    Per energy content it is assumed that the cost of naphtha is 10% higher than the crude oil cost. Based on average market price difference observed the last 12 months (anno May 2024). Source: https://tradingeconomics.com/commodity/naphtha
    """
    return (
        1 + naphtha_crack_spread()
    ) * oil_price() + carbon_tax() * naphtha_emission_factor()


@component.add(
    name="Naphtha crack spread",
    units="percent",
    comp_type="Constant",
    comp_subtype="Normal",
)
def naphtha_crack_spread():
    """
    10 % of crude oil price
    """
    return 0.1


@component.add(
    name="Naphtha emission factor",
    units="tCO2/GJ",
    comp_type="Constant",
    comp_subtype="Normal",
)
def naphtha_emission_factor():
    """
    https://www.eia.gov/environment/emissions/co2_vol_mass.php Source of carbon emission factor is in kgCO2/MMBtu. Converted to usable unit.
    """
    return 68.02 / 1000 / 1.0551
