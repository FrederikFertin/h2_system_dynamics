"""
Module nh3_production
Translated using PySD version 3.14.0
"""

@component.add(
    name="Blue NH3 price",
    units="€/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nh3_cost_without_hydrogen_costs": 1,
        "blue_h2_price": 1,
        "nh3_lhv": 1,
        "nh3_h2_usage": 1,
    },
)
def blue_nh3_price():
    return (
        nh3_cost_without_hydrogen_costs() + blue_h2_price() / nh3_h2_usage() / nh3_lhv()
    )


@component.add(
    name="Green NH3 price",
    units="€/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nh3_cost_without_hydrogen_costs": 1,
        "nh3_lhv": 1,
        "nh3_h2_usage": 1,
        "green_h2_price": 1,
    },
)
def green_nh3_price():
    return (
        nh3_cost_without_hydrogen_costs()
        + green_h2_price() / nh3_h2_usage() / nh3_lhv()
    )


@component.add(
    name="Grey NH3 price",
    units="€/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nh3_cost_without_hydrogen_costs": 1,
        "grey_h2_price": 1,
        "nh3_lhv": 1,
        "nh3_h2_usage": 1,
    },
)
def grey_nh3_price():
    return (
        nh3_cost_without_hydrogen_costs() + grey_h2_price() / nh3_h2_usage() / nh3_lhv()
    )


@component.add(
    name="NH3 AF",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"discount_rate": 2, "nh3_lifetime": 1},
)
def nh3_af():
    return 1 / ((1 - (1 + discount_rate()) ** -nh3_lifetime()) / discount_rate())


@component.add(
    name="NH3 CAPEX", units="€/(kgNH3/h)", comp_type="Constant", comp_subtype="Normal"
)
def nh3_capex():
    return 6700


@component.add(
    name="NH3 cost without hydrogen costs",
    units="€/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nh3_capex": 1,
        "nh3_af": 1,
        "nh3_opex": 1,
        "nh3_lhv": 2,
        "nh3_operating_hours": 1,
        "nh3_el_usage": 1,
        "electricity_price": 1,
    },
)
def nh3_cost_without_hydrogen_costs():
    """
    €/MJ NH3 [ [ [€/kgH2] / [kgNH3/kgH2] ] + [kWh/kgNH3 * €/kWh] ] / [MJ/kgNH3] + [kWhe/kWhNH3 * €/kWhe] * [kWh/MJ]
    """
    return (
        nh3_capex() * (nh3_af() + nh3_opex()) / (nh3_operating_hours() * nh3_lhv())
        + nh3_el_usage() * electricity_price() / nh3_lhv()
    )


@component.add(
    name="NH3 el usage", units="kWh/kgNH3", comp_type="Constant", comp_subtype="Normal"
)
def nh3_el_usage():
    return 0.315


@component.add(
    name="NH3 H2 usage", units="kgNH3/kgH2", comp_type="Constant", comp_subtype="Normal"
)
def nh3_h2_usage():
    return 5.56


@component.add(
    name="NH3 LHV", units="MJ/kgNH3", comp_type="Constant", comp_subtype="Normal"
)
def nh3_lhv():
    return 18.9


@component.add(
    name="NH3 lifetime", units="years", comp_type="Constant", comp_subtype="Normal"
)
def nh3_lifetime():
    return 25


@component.add(
    name="NH3 operating hours", units="h", comp_type="Constant", comp_subtype="Normal"
)
def nh3_operating_hours():
    return 8000


@component.add(
    name="NH3 OPEX", units="percent", comp_type="Constant", comp_subtype="Normal"
)
def nh3_opex():
    return 0.04
