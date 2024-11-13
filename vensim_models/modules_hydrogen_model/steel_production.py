"""
Module steel_production
Translated using PySD version 3.14.0
"""

@component.add(
    name="BF CCS cost",
    units="€/tsteel",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "bf_coal_cost": 1,
        "bf_coal_emission_factor": 1,
        "ccs_cost": 1,
        "carbon_tax": 1,
        "cc_capture_rate": 1,
    },
)
def bf_ccs_cost():
    return bf_coal_cost() + bf_coal_emission_factor() * (
        ccs_cost() - carbon_tax() * cc_capture_rate()
    )


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
        "coal_lhv": 1,
        "coal_to_steel": 1,
        "coal_price": 1,
        "grid_electricity_price": 1,
        "el_to_steel_bf_coal": 1,
        "bf_coal_capex": 1,
        "foundry_proxy_af": 1,
    },
)
def bf_coal_cost():
    """
    Variable costs - CAPEX and OPEX as well as iron ore/steel raw material costs are assumed identical across technologies.
    """
    return (
        carbon_tax() * bf_coal_emission_factor()
        + coal_price() * (coal_to_steel() * coal_lhv())
        + grid_electricity_price() * el_to_steel_bf_coal()
        + bf_coal_capex() * foundry_proxy_af()
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
    name="Coal LHV", units="MJ/kg", comp_type="Constant", comp_subtype="Unchangeable"
)
def coal_lhv():
    """
    https://www.engineeringtoolbox.com/fuels-higher-calorific-values-d_169.html
    """
    return 29


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
    name="Foundry proxy AF",
    units="scalar",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"discount_rate": 2, "foundry_lifetime": 2},
)
def foundry_proxy_af():
    """
    The assumption that the original source uses 8% discount rate for its capex calculations is made. With this the CAPEX of steel production is sensitive to discount rate variations.
    """
    return (
        1 / ((1 - (1 + discount_rate()) ** -foundry_lifetime()) / discount_rate())
    ) / (1 / ((1 - (1 + 0.08) ** -foundry_lifetime()) / 0.08))


@component.add(
    name="HDRI CAPEX",
    units="€/tsteel",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hdri_learning_curve": 1, "hdri_capex_base": 1, "foundry_proxy_af": 1},
)
def hdri_capex():
    return hdri_learning_curve() * hdri_capex_base() * foundry_proxy_af()


@component.add(
    name="HDRI CAPEX BASE",
    units="€/tsteel",
    comp_type="Constant",
    comp_subtype="Normal",
)
def hdri_capex_base():
    """
    https://doi.org/10.1016/j.jclepro.2023.136391 Table 2 average
    """
    return (945 + 635 + 670) / 3


@component.add(
    name="HDRI CAPEX subsidy",
    units="€/tsteel",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hdri_capex_subsidy_length": 1,
        "time": 1,
        "hdri_capex_subsidy_size": 1,
        "hdri_capex": 1,
    },
)
def hdri_capex_subsidy():
    return (
        pulse(__data["time"], 2025, width=hdri_capex_subsidy_length())
        * hdri_capex_subsidy_size()
        * hdri_capex()
    )


@component.add(
    name="HDRI CAPEX subsidy length",
    units="years",
    comp_type="Constant",
    comp_subtype="Normal",
)
def hdri_capex_subsidy_length():
    return 10


@component.add(
    name="HDRI CAPEX subsidy size",
    units="percent",
    comp_type="Constant",
    comp_subtype="Normal",
)
def hdri_capex_subsidy_size():
    return 0


@component.add(
    name="HDRI cost",
    units="€/tsteel",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"steel_h2_cost": 1, "h2_to_steel": 1, "hdri_cost_without_h2": 1},
)
def hdri_cost():
    return (steel_h2_cost() * 1000) * h2_to_steel() + hdri_cost_without_h2()


@component.add(
    name="HDRI cost without H2",
    units="€/tsteel",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "renewable_electricity_price": 1,
        "el_to_steel_hdri": 1,
        "hdri_capex": 1,
        "hdri_capex_subsidy": 1,
    },
)
def hdri_cost_without_h2():
    return (
        (renewable_electricity_price() * 1000) * (el_to_steel_hdri() / 3.6)
        + hdri_capex()
        - hdri_capex_subsidy()
    )


@component.add(
    name="HDRI learning curve",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hdri_plant_size": 2, "hdri_eaf": 1, "hdri_learning_rate": 1},
)
def hdri_learning_curve():
    return (np.maximum(hdri_plant_size(), hdri_eaf()) / hdri_plant_size()) ** (
        np.log(1 - hdri_learning_rate()) / np.log(2)
    )


@component.add(
    name="HDRI learning rate",
    units="percent",
    comp_type="Constant",
    comp_subtype="Normal",
)
def hdri_learning_rate():
    return 0.12


@component.add(
    name="HDRI plant size", units="MT", comp_type="Constant", comp_subtype="Normal"
)
def hdri_plant_size():
    """
    Common capacity found in https://globalenergymonitor.org/projects/global-steel-plant-tracker/tracker -map/
    """
    return 2


@component.add(
    name="new HDRI capacity",
    units="Mtsteel/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hdri_eaf_investment": 1},
)
def new_hdri_capacity():
    return hdri_eaf_investment()


@component.add(
    name="steel H2 price break",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "bf_ccs_cost": 1,
        "bf_coal_cost": 1,
        "hdri_cost_without_h2": 1,
        "h2_to_steel": 1,
    },
)
def steel_h2_price_break():
    return (
        (np.minimum(bf_ccs_cost(), bf_coal_cost()) - hdri_cost_without_h2())
        / 1000
        / h2_to_steel()
    )


@component.add(
    name="steel H2 price break marginal",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "bf_ccs_cost": 1,
        "bf_coal_cost": 1,
        "el_to_steel_hdri": 1,
        "renewable_electricity_price": 1,
        "h2_to_steel": 1,
    },
)
def steel_h2_price_break_marginal():
    return (
        (
            np.minimum(bf_ccs_cost(), bf_coal_cost())
            - (renewable_electricity_price() * 1000) * (el_to_steel_hdri() / 3.6)
        )
        / 1000
        / h2_to_steel()
    )


@component.add(
    name="total HDRI CAPEX subsidy",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_total_hdri_capex_subsidy": 1},
    other_deps={
        "_integ_total_hdri_capex_subsidy": {
            "initial": {},
            "step": {
                "hdri_capex_subsidy": 1,
                "foundry_lifetime": 1,
                "new_hdri_capacity": 1,
            },
        }
    },
)
def total_hdri_capex_subsidy():
    return _integ_total_hdri_capex_subsidy()


_integ_total_hdri_capex_subsidy = Integ(
    lambda: hdri_capex_subsidy() * foundry_lifetime() * new_hdri_capacity(),
    lambda: 0,
    "_integ_total_hdri_capex_subsidy",
)
