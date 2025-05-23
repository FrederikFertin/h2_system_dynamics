"""
Module ammonia_production
Translated using PySD version 3.14.0
"""

@component.add(
    name="Blue NH3 cost",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "grey_nh3_cost_without_h2": 1,
        "blue_h2_cost": 1,
        "nh3_h2_usage": 1,
        "nh3_lhv": 1,
    },
)
def blue_nh3_cost():
    return (
        grey_nh3_cost_without_h2() + blue_h2_cost() / nh3_h2_usage() / nh3_lhv() * 1000
    )


@component.add(
    name="fertilizer CO2 WTP",
    units="€/tCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fertilizer_nh3_cost": 1,
        "grey_nh3_cost_without_co2": 1,
        "nh3_lhv": 1,
        "nh3_el_usage": 1,
        "nh3_h2_usage": 1,
        "smr_emission_factor": 1,
        "electricity_emission_factor": 1,
    },
)
def fertilizer_co2_wtp():
    """
    €/tNH3 / (tCO2/tNH3)
    """
    return (
        (fertilizer_nh3_cost() - grey_nh3_cost_without_co2())
        * nh3_lhv()
        / (
            smr_emission_factor() / nh3_h2_usage()
            + electricity_emission_factor() * nh3_el_usage()
        )
    )


@component.add(
    name="fertilizer H2 marginal WTP",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "min_alternative_nh3_cost": 1,
        "nh3_el_usage": 1,
        "nh3_lhv": 2,
        "renewable_electricity_price": 1,
        "nh3_h2_usage": 1,
    },
)
def fertilizer_h2_marginal_wtp():
    return (
        (
            min_alternative_nh3_cost()
            - nh3_el_usage() * renewable_electricity_price() / nh3_lhv()
        )
        / 1000
        * nh3_lhv()
        * nh3_h2_usage()
    )


@component.add(
    name="fertilizer H2 WTP",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "min_alternative_nh3_cost": 1,
        "green_nh3_cost_without_h2": 1,
        "nh3_h2_usage": 1,
        "nh3_lhv": 1,
    },
)
def fertilizer_h2_wtp():
    return (
        (min_alternative_nh3_cost() - green_nh3_cost_without_h2())
        * (nh3_lhv() * nh3_h2_usage())
        / 1000
    )


@component.add(
    name="fertilizer NH3 cost",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "green_nh3_cost_without_h2": 1,
        "nh3_h2_usage": 1,
        "nh3_lhv": 1,
        "fertilizer_h2_cost": 1,
    },
)
def fertilizer_nh3_cost():
    return (
        green_nh3_cost_without_h2()
        + fertilizer_h2_cost() / nh3_h2_usage() / nh3_lhv() * 1000
    )


@component.add(
    name="Green NH3 cost without H2",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nh3_capex": 1,
        "nh3_af": 1,
        "nh3_opex": 1,
        "green_nh3_operating_hours": 1,
        "nh3_lhv": 2,
        "nh3_el_usage": 1,
        "renewable_electricity_price": 1,
    },
)
def green_nh3_cost_without_h2():
    """
    €/GJ NH3 [ [ [€/kgH2] / [kgNH3/kgH2] ] + [kWh/kgNH3 * €/kWh] ] / [MJ/kgNH3] + [kWhe/kWhNH3 * €/kWhe] * [kWh/MJ]
    """
    return (
        nh3_capex()
        * (nh3_af() + nh3_opex())
        / (green_nh3_operating_hours() * nh3_lhv())
        * 1000
        + nh3_el_usage() * renewable_electricity_price() / nh3_lhv()
    )


@component.add(
    name="Green NH3 operating hours",
    units="h",
    comp_type="Constant",
    comp_subtype="Normal",
)
def green_nh3_operating_hours():
    return 4000


@component.add(
    name="Grey NH3 cost",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "grey_nh3_cost_without_h2": 1,
        "grey_h2_cost": 1,
        "nh3_h2_usage": 1,
        "nh3_lhv": 1,
    },
)
def grey_nh3_cost():
    return (
        grey_nh3_cost_without_h2() + grey_h2_cost() / nh3_h2_usage() / nh3_lhv() * 1000
    )


@component.add(
    name="Grey NH3 cost without CO2",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "grey_nh3_cost_without_h2": 1,
        "nh3_h2_usage": 1,
        "nh3_lhv": 2,
        "grey_h2_cost_wo_co2": 1,
        "nh3_el_usage": 1,
        "carbon_tax": 1,
        "electricity_emission_factor": 1,
    },
)
def grey_nh3_cost_without_co2():
    return (
        grey_nh3_cost_without_h2()
        + grey_h2_cost_wo_co2() / nh3_h2_usage() / nh3_lhv() * 1000
        - nh3_el_usage() * electricity_emission_factor() * carbon_tax() / nh3_lhv()
    )


@component.add(
    name="Grey NH3 cost without H2",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nh3_capex": 1,
        "nh3_af": 1,
        "nh3_opex": 1,
        "grey_nh3_operating_hours": 1,
        "nh3_lhv": 2,
        "grid_electricity_price": 1,
        "nh3_el_usage": 1,
    },
)
def grey_nh3_cost_without_h2():
    return (
        nh3_capex()
        * (nh3_af() + nh3_opex())
        / (grey_nh3_operating_hours() * nh3_lhv())
        * 1000
        + nh3_el_usage() * grid_electricity_price() / nh3_lhv()
    )


@component.add(
    name="Grey NH3 operating hours",
    units="h",
    comp_type="Constant",
    comp_subtype="Normal",
)
def grey_nh3_operating_hours():
    return 8000


@component.add(
    name="min alternative NH3 cost",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"blue_nh3_cost": 1, "grey_nh3_cost": 1},
)
def min_alternative_nh3_cost():
    return np.minimum(blue_nh3_cost(), grey_nh3_cost())


@component.add(
    name="NH3 AF",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"discount_rate": 2, "nh3_plant_lifetime": 1},
)
def nh3_af():
    return 1 / ((1 - (1 + discount_rate()) ** -nh3_plant_lifetime()) / discount_rate())


@component.add(
    name="NH3 CAPEX", units="€/(kgNH3/h)", comp_type="Constant", comp_subtype="Normal"
)
def nh3_capex():
    return 6700


@component.add(
    name="NH3 el usage", units="MWh/tNH3", comp_type="Constant", comp_subtype="Normal"
)
def nh3_el_usage():
    return 0.315


@component.add(
    name="NH3 H2 usage", units="tNH3/tH2", comp_type="Constant", comp_subtype="Normal"
)
def nh3_h2_usage():
    return 5.56


@component.add(
    name="NH3 LHV", units="GJ/tNH3", comp_type="Constant", comp_subtype="Unchangeable"
)
def nh3_lhv():
    return 18.6


@component.add(
    name="NH3 OPEX", units="percent", comp_type="Constant", comp_subtype="Normal"
)
def nh3_opex():
    return 0.04


@component.add(
    name="NH3 plant lifetime",
    units="years",
    comp_type="Constant",
    comp_subtype="Normal",
)
def nh3_plant_lifetime():
    return 25


@component.add(
    name="shipping NH3 cost",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "green_nh3_cost_without_h2": 1,
        "shipping_nh3_h2_cost": 1,
        "nh3_h2_usage": 1,
        "nh3_lhv": 1,
    },
)
def shipping_nh3_cost():
    return (
        green_nh3_cost_without_h2()
        + shipping_nh3_h2_cost() / nh3_h2_usage() / nh3_lhv() * 1000
    )
