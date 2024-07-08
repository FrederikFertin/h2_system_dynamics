"""
Module meoh_and_biogas_production
Translated using PySD version 3.14.0
"""

@component.add(
    name="biogas price", units="€/GJ", comp_type="Constant", comp_subtype="Normal"
)
def biogas_price():
    return 30


@component.add(
    name="Biomass LHV", units="MJ/kg", comp_type="Constant", comp_subtype="Normal"
)
def biomass_lhv():
    return 12.5


@component.add(
    name="bioMeOH cost without hydrogen",
    units="€/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "meoh_capex": 1,
        "meoh_af": 1,
        "meoh_opex": 1,
        "meoh_operating_hours": 1,
        "meoh_lhv": 2,
        "biomass_price": 1,
        "biomass_lhv": 1,
        "meoh_electricity_usage": 1,
        "meoh_biomass_usage": 1,
        "meoh_excess_heat": 1,
        "heat_cost": 1,
        "electricity_price": 1,
    },
)
def biomeoh_cost_without_hydrogen():
    """
    €/MJ MeOH [ [kgBM/kgMeOH] * [€/GJ] * [MJ/kgBM ] / [MJ/GJ] + [€/kgH2] / [kgMeOH/kgH2] + [€/kWh * kWh/kgMeOH] ] / [MJ/kgMeOH]
    """
    return (
        meoh_capex() * (meoh_af() + meoh_opex()) / (meoh_operating_hours() * meoh_lhv())
        + (
            meoh_biomass_usage() * biomass_price() * (biomass_lhv() / 1000)
            + electricity_price() * meoh_electricity_usage()
            - heat_cost() / 1000 * meoh_excess_heat()
        )
        / meoh_lhv()
    )


@component.add(
    name="Blue bioMeOH price",
    units="€/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biomeoh_cost_without_hydrogen": 1,
        "blue_h2_price": 1,
        "meoh_lhv": 1,
        "meoh_h2_usage": 1,
    },
)
def blue_biomeoh_price():
    return (
        biomeoh_cost_without_hydrogen() + blue_h2_price() / meoh_h2_usage() / meoh_lhv()
    )


@component.add(
    name="Blue eMeOH price",
    units="€/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "emeoh_cost_without_hydrogen": 1,
        "blue_h2_price": 1,
        "meoh_lhv": 1,
        "emeoh_h2_usage": 1,
    },
)
def blue_emeoh_price():
    return (
        emeoh_cost_without_hydrogen() + blue_h2_price() / emeoh_h2_usage() / meoh_lhv()
    )


@component.add(
    name="eMeOH AF",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"discount_rate": 2, "emeoh_lifetime": 1},
)
def emeoh_af():
    return 1 / ((1 - (1 + discount_rate()) ** -emeoh_lifetime()) / discount_rate())


@component.add(
    name="eMeOH CAPEX", units="€/kgMeOH/h", comp_type="Constant", comp_subtype="Normal"
)
def emeoh_capex():
    return 10000


@component.add(
    name="eMeOH CO2 usage",
    units="kgCO2/kgMeOH",
    comp_type="Constant",
    comp_subtype="Normal",
)
def emeoh_co2_usage():
    """
    kg CO2 per kg MeOH
    """
    return 1.374


@component.add(
    name="eMeOH cost without hydrogen",
    units="€/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "emeoh_capex": 1,
        "emeoh_opex": 1,
        "emeoh_af": 1,
        "emeoh_operating_hours": 1,
        "meoh_lhv": 2,
        "emeoh_electricity_usage": 1,
        "ps_cc_cost": 1,
        "emeoh_excess_heat": 1,
        "emeoh_co2_usage": 1,
        "heat_cost": 1,
        "electricity_price": 1,
    },
)
def emeoh_cost_without_hydrogen():
    """
    €/MJ MeOH [ [kgBM/kgMeOH] * [€/GJ] * [MJ/kgBM ] / [MJ/GJ] + [€/kgH2] / [kgMeOH/kgH2] + [€/kWh * kWh/kgMeOH] ] / [MJ/kgMeOH]
    """
    return (
        emeoh_capex()
        * (emeoh_af() + emeoh_opex())
        / (emeoh_operating_hours() * meoh_lhv())
        + (
            emeoh_co2_usage() * (ps_cc_cost() / 1000)
            + electricity_price() * emeoh_electricity_usage()
            - heat_cost() / 1000 * emeoh_excess_heat()
        )
        / meoh_lhv()
    )


@component.add(
    name="eMeOH electricity usage",
    units="kWh/kgMeOH",
    comp_type="Constant",
    comp_subtype="Normal",
)
def emeoh_electricity_usage():
    """
    kWhe/kgMeOH
    """
    return 0.316


@component.add(
    name="eMeOH excess heat",
    units="kWh/kg MeOH",
    comp_type="Constant",
    comp_subtype="Normal",
)
def emeoh_excess_heat():
    return 0.68


@component.add(
    name="eMeOH H2 usage",
    units="kgMeOH/kgH2",
    comp_type="Constant",
    comp_subtype="Normal",
)
def emeoh_h2_usage():
    """
    kg MeOH per kg H2
    """
    return 5.26


@component.add(
    name="eMeOH lifetime", units="years", comp_type="Constant", comp_subtype="Normal"
)
def emeoh_lifetime():
    return 20


@component.add(
    name="eMeOH operating hours", units="h", comp_type="Constant", comp_subtype="Normal"
)
def emeoh_operating_hours():
    return 8000


@component.add(
    name="eMeOH OPEX", units="percent", comp_type="Constant", comp_subtype="Normal"
)
def emeoh_opex():
    """
    Percentage of CAPEX
    """
    return 0.04


@component.add(
    name="Green bioMeOH price",
    units="€/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biomeoh_cost_without_hydrogen": 1,
        "meoh_lhv": 1,
        "meoh_h2_usage": 1,
        "green_h2_price": 1,
    },
)
def green_biomeoh_price():
    return (
        biomeoh_cost_without_hydrogen()
        + green_h2_price() / meoh_h2_usage() / meoh_lhv()
    )


@component.add(
    name="Green eMeOH price",
    units="€/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "emeoh_cost_without_hydrogen": 1,
        "meoh_lhv": 1,
        "emeoh_h2_usage": 1,
        "green_h2_price": 1,
    },
)
def green_emeoh_price():
    return (
        emeoh_cost_without_hydrogen() + green_h2_price() / emeoh_h2_usage() / meoh_lhv()
    )


@component.add(
    name="Grey bioMeOH price",
    units="€/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biomeoh_cost_without_hydrogen": 1,
        "grey_h2_price": 1,
        "meoh_lhv": 1,
        "meoh_h2_usage": 1,
    },
)
def grey_biomeoh_price():
    return (
        biomeoh_cost_without_hydrogen() + grey_h2_price() / meoh_h2_usage() / meoh_lhv()
    )


@component.add(
    name="Grey eMeOH price",
    units="€/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "emeoh_cost_without_hydrogen": 1,
        "grey_h2_price": 1,
        "meoh_lhv": 1,
        "emeoh_h2_usage": 1,
    },
)
def grey_emeoh_price():
    return (
        emeoh_cost_without_hydrogen() + grey_h2_price() / emeoh_h2_usage() / meoh_lhv()
    )


@component.add(
    name="MeOH AF",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"discount_rate": 2, "meoh_lifetime": 1},
)
def meoh_af():
    return 1 / ((1 - (1 + discount_rate()) ** -meoh_lifetime()) / discount_rate())


@component.add(
    name="MeOH biomass usage",
    units="kgBiomass/kgMeOH",
    comp_type="Constant",
    comp_subtype="Normal",
)
def meoh_biomass_usage():
    """
    kg biomass per kg MeOH
    """
    return 1.17


@component.add(
    name="MeOH CAPEX", units="€/kgMeOH/h", comp_type="Constant", comp_subtype="Normal"
)
def meoh_capex():
    return 20000


@component.add(
    name="MeOH electricity usage",
    units="kWh/kgMeOH",
    comp_type="Constant",
    comp_subtype="Normal",
)
def meoh_electricity_usage():
    """
    kWhe/kgMeOH
    """
    return 0.64


@component.add(
    name="MeOH excess heat",
    units="kWh/kgMeOH",
    comp_type="Constant",
    comp_subtype="Normal",
)
def meoh_excess_heat():
    return 0.428


@component.add(
    name="MeOH H2 usage",
    units="kgMeOH/kgH2",
    comp_type="Constant",
    comp_subtype="Normal",
)
def meoh_h2_usage():
    """
    kg MeOH per kg H2
    """
    return 15.7


@component.add(
    name="MeOH LHV", units="MJ/kg", comp_type="Constant", comp_subtype="Normal"
)
def meoh_lhv():
    return 19.9


@component.add(
    name="MeOH lifetime", units="years", comp_type="Constant", comp_subtype="Normal"
)
def meoh_lifetime():
    return 20


@component.add(
    name="MeOH operating hours", units="h", comp_type="Constant", comp_subtype="Normal"
)
def meoh_operating_hours():
    return 8000


@component.add(
    name="MeOH OPEX", units="percent", comp_type="Constant", comp_subtype="Normal"
)
def meoh_opex():
    """
    Percentage of CAPEX
    """
    return 0.04
