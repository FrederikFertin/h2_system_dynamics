"""
Module steel_production
Translated using PySD version 3.14.0
"""

@component.add(
    name="BF CCS CAPEX", units="€/tsteel", comp_type="Constant", comp_subtype="Normal"
)
def bf_ccs_capex():
    """
    https://doi.org/10.1016/j.jclepro.2023.136391 Table 2 average
    """
    return (265 + 590) / 2


@component.add(
    name="BF CCS cost",
    units="€/tsteel",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "carbon_tax": 1,
        "bf_ccs_emission_factor": 1,
        "gas_price": 1,
        "gas_to_steel": 1,
        "bf_ccs_capex": 1,
    },
)
def bf_ccs_cost():
    """
    Option currently excluded from model
    """
    return (
        carbon_tax() * bf_ccs_emission_factor()
        + gas_price() * gas_to_steel()
        + bf_ccs_capex()
    ) * 5


@component.add(
    name="BF CCS emission factor",
    units="tCO2/tsteel",
    comp_type="Constant",
    comp_subtype="Normal",
)
def bf_ccs_emission_factor():
    """
    Table 2 https://doi.org/10.1016/j.jclepro.2023.136391
    """
    return 1.1


@component.add(
    name="BF Coal CAPEX", units="€/tsteel", comp_type="Constant", comp_subtype="Normal"
)
def bf_coal_capex():
    """
    https://doi.org/10.1016/j.jclepro.2023.136391 Table 2 average
    """
    return (600 + 311) / 2


@component.add(
    name="BF Coal cost",
    units="€/tsteel",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "carbon_tax": 1,
        "bf_coal_emission_factor": 1,
        "lhv_coal": 1,
        "coal_price": 1,
        "coal_to_steel": 1,
        "el_to_steel_bf_coal": 1,
        "electricity_price": 1,
        "bf_coal_capex": 1,
    },
)
def bf_coal_cost():
    """
    Variable costs - CAPEX and OPEX as well as iron ore/steel raw material costs are assumed identical across technologies.
    """
    return (
        carbon_tax() * bf_coal_emission_factor()
        + coal_price() * (coal_to_steel() * lhv_coal())
        + electricity_price() * el_to_steel_bf_coal()
        + bf_coal_capex()
    )


@component.add(
    name="BF Coal emission factor",
    units="tCO2/tsteel",
    comp_type="Constant",
    comp_subtype="Normal",
)
def bf_coal_emission_factor():
    """
    https://doi.org/10.1016/j.jclepro.2023.136391
    """
    return 1.815


@component.add(
    name="Coal to Steel",
    units="tCoal/tsteel",
    comp_type="Constant",
    comp_subtype="Normal",
)
def coal_to_steel():
    """
    ton Coal per ton steel https://doi.org/10.1016/j.jclepro.2023.136391
    """
    return 0.8


@component.add(
    name="EL to Steel BF Coal",
    units="kWh/tsteel",
    comp_type="Constant",
    comp_subtype="Normal",
)
def el_to_steel_bf_coal():
    """
    https://www.globalccsinstitute.com/archive/hub/publications/15671/global-te chnology-roadmap-ccs-industry-steel-sectoral-report.pdf
    """
    return 250


@component.add(
    name="EL to Steel HDRI",
    units="GJ/tsteel",
    comp_type="Constant",
    comp_subtype="Normal",
)
def el_to_steel_hdri():
    """
    https://doi.org/10.1016/j.jclepro.2023.136391 Table 2 - energy consumption minus an assumed H2 consumption of 6.7 GJ H2 per ton Steel.
    """
    return 5.8


@component.add(
    name="Gas to Steel", units="GJ/tsteel", comp_type="Constant", comp_subtype="Normal"
)
def gas_to_steel():
    """
    https://doi.org/10.1016/j.jclepro.2023.136391 Table 2 - all energy consumption is assumed to be NG.
    """
    return 15.12


@component.add(
    name="HDRI CAPEX", units="€/tsteel", comp_type="Constant", comp_subtype="Normal"
)
def hdri_capex():
    """
    https://doi.org/10.1016/j.jclepro.2023.136391 Table 2 average
    """
    return (945 + 635 + 670) / 3


@component.add(
    name="HDRI cost",
    units="€/tsteel",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "green_h2_price": 1,
        "h2_to_steel": 1,
        "el_to_steel_hdri": 1,
        "electricity_price": 1,
        "hdri_capex": 1,
    },
)
def hdri_cost():
    return (
        (green_h2_price() * 1000) * h2_to_steel()
        + (electricity_price() * 1000) * (el_to_steel_hdri() / 3.6)
        + hdri_capex()
    )


@component.add(
    name="LHV Coal", units="MJ/kg", comp_type="Constant", comp_subtype="Normal"
)
def lhv_coal():
    """
    https://www.engineeringtoolbox.com/fuels-higher-calorific-values-d_169.html
    """
    return 30
