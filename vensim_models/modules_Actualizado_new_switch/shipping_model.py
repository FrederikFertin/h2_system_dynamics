"""
Module shipping_model
Translated using PySD version 3.13.4
"""


@component.add(
    name="check",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hfo_shipping_consumption": 1,
        "meoh_shipping_consumption": 1,
        "nh3_shipping_consumption": 1,
    },
)
def check():
    return (
        hfo_shipping_consumption()
        + meoh_shipping_consumption()
        + nh3_shipping_consumption()
    )


@component.add(
    name="ctrl",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"k_p": 1, "error_int": 1, "error": 1},
)
def ctrl():
    return k_p() * (error() + error_int())


@component.add(
    name="demand change",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ctrl": 1},
)
def demand_change():
    return ctrl()


@component.add(
    name="equalizer",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hfo_level": 1, "meoh_level": 1, "nh3_level": 1},
)
def equalizer():
    return 1 / (hfo_level() + meoh_level() + nh3_level())


@component.add(
    name="error",
    units="e",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "int_shipping_consumption": 1,
        "hfo_shipping_consumption": 1,
        "meoh_shipping_consumption": 1,
        "nh3_shipping_consumption": 1,
    },
)
def error():
    return (
        int_shipping_consumption()
        - hfo_shipping_consumption()
        - meoh_shipping_consumption()
        - nh3_shipping_consumption()
    )


@component.add(
    name="error int",
    units="e",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_error_int": 1},
    other_deps={"_integ_error_int": {"initial": {}, "step": {"k_i": 1, "error": 1}}},
)
def error_int():
    return _integ_error_int()


_integ_error_int = Integ(lambda: k_i() * error(), lambda: 0, "_integ_error_int")


@component.add(
    name="fleet reinvestment",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_fleet_reinvestment": 1},
    other_deps={
        "_integ_fleet_reinvestment": {
            "initial": {"int_shipping_consumption": 1, "ship_lifetime": 1},
            "step": {
                "demand_change": 1,
                "hfo_decay": 1,
                "meoh_decay": 1,
                "nh3_decay": 1,
                "hfo_investment": 1,
                "meoh_investment": 1,
                "nh3_investment": 1,
            },
        }
    },
)
def fleet_reinvestment():
    return _integ_fleet_reinvestment()


_integ_fleet_reinvestment = Integ(
    lambda: demand_change()
    + hfo_decay()
    + meoh_decay()
    + nh3_decay()
    - hfo_investment()
    - meoh_investment()
    - nh3_investment(),
    lambda: int_shipping_consumption() / ship_lifetime(),
    "_integ_fleet_reinvestment",
)


@component.add(
    name="HFO competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hfo_cost": 2, "nh3_cost": 1, "meoh_cost": 1},
)
def hfo_competitiveness():
    return np.maximum(hfo_cost() / nh3_cost(), hfo_cost() / meoh_cost())


@component.add(
    name="HFO cost",
    units="€/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"oil_price": 1, "carbon_tax": 1},
)
def hfo_cost():
    """
    €/MJ Oil Emission factor: 0.075 t per GJ
    """
    return oil_price() / 1000 + carbon_tax() * (0.075 / 1000)


@component.add(
    name="HFO decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hfo_shipping_consumption": 1, "ship_lifetime": 1},
)
def hfo_decay():
    return hfo_shipping_consumption() / ship_lifetime()


@component.add(
    name="HFO investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hfo_investment_level": 1, "fleet_reinvestment": 1},
)
def hfo_investment():
    return hfo_investment_level() * fleet_reinvestment()


@component.add(
    name="HFO investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"equalizer": 1, "hfo_level": 1},
)
def hfo_investment_level():
    return equalizer() * hfo_level()


@component.add(
    name="HFO level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hfo_competitiveness": 1,
        "hfo_shipping_consumption": 2,
        "meoh_shipping_consumption": 1,
        "nh3_shipping_consumption": 1,
    },
)
def hfo_level():
    return (
        1
        / (1 + np.exp(10 * (hfo_competitiveness() - 0.9)))
        * hfo_shipping_consumption()
        / (
            hfo_shipping_consumption()
            + meoh_shipping_consumption()
            + nh3_shipping_consumption()
        )
    )


@component.add(
    name="HFO shipping consumption",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_hfo_shipping_consumption": 1},
    other_deps={
        "_integ_hfo_shipping_consumption": {
            "initial": {"int_shipping_consumption": 1},
            "step": {"hfo_investment": 1, "hfo_decay": 1},
        }
    },
)
def hfo_shipping_consumption():
    return _integ_hfo_shipping_consumption()


_integ_hfo_shipping_consumption = Integ(
    lambda: hfo_investment() - hfo_decay(),
    lambda: int_shipping_consumption(),
    "_integ_hfo_shipping_consumption",
)


@component.add(
    name="int shipping consumption",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def int_shipping_consumption():
    """
    Considering an annual growth of 1,79%
    !Year
    """
    return np.interp(time(), [2019, 2050], [501403, 871296])


@component.add(name="k i", comp_type="Constant", comp_subtype="Normal")
def k_i():
    return 0.08


@component.add(name="k p", comp_type="Constant", comp_subtype="Normal")
def k_p():
    return 3


@component.add(
    name="MeOH AF",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"discount_rate": 2, "meoh_lifetime": 1},
)
def meoh_af():
    return 1 / ((1 - (1 + discount_rate()) ** -meoh_lifetime()) / discount_rate())


@component.add(
    name="MeOH bm usage", units="kg/kg", comp_type="Constant", comp_subtype="Normal"
)
def meoh_bm_usage():
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
    name="MeOH competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"meoh_cost": 2, "nh3_cost": 1, "hfo_cost": 1},
)
def meoh_competitiveness():
    return np.maximum(meoh_cost() / nh3_cost(), meoh_cost() / hfo_cost())


@component.add(
    name="MeOH cost",
    units="€/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "meoh_capex": 1,
        "meoh_af": 1,
        "meoh_opex": 1,
        "meoh_operating_hours": 1,
        "meoh_lhv": 2,
        "meoh_bm_usage": 1,
        "hydrogen_price": 1,
        "meoh_el_usage": 1,
        "electricity_price": 1,
        "biomass_price": 1,
        "meoh_h2_usage": 1,
    },
)
def meoh_cost():
    """
    €/MJ MeOH [ [kgBM/kgMeOH] * [€/GJ] * [MJ/kgBM ] / [MJ/GJ] + [€/kgH2] / [kgMeOH/kgH2] + [€/kWh * kWh/kgMeOH] ] / [MJ/kgMeOH]
    """
    return (
        meoh_capex() * (meoh_af() + meoh_opex()) / (meoh_operating_hours() * meoh_lhv())
        + (
            meoh_bm_usage() * biomass_price() * (12.5 / 1000)
            + hydrogen_price() / meoh_h2_usage()
            + electricity_price() * meoh_el_usage()
        )
        / meoh_lhv()
    )


@component.add(
    name="MeOH decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"meoh_shipping_consumption": 1, "ship_lifetime": 1},
)
def meoh_decay():
    return meoh_shipping_consumption() / ship_lifetime()


@component.add(name="MeOH el usage", comp_type="Constant", comp_subtype="Normal")
def meoh_el_usage():
    """
    kWhe/kgMeOH
    """
    return 0.64


@component.add(
    name="MeOH H2 usage",
    units="kg/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"meohh2": 1},
)
def meoh_h2_usage():
    """
    kg MeOH per kg H2
    """
    return meohh2()


@component.add(
    name="MeOH imitators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fleet_reinvestment": 1, "meoh_investment_level": 1},
)
def meoh_imitators():
    return fleet_reinvestment() * meoh_investment_level()


@component.add(
    name="MeOH inno switch",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"meoh_competitiveness": 1},
)
def meoh_inno_switch():
    return if_then_else(meoh_competitiveness() < 2, lambda: 1, lambda: 0)


@component.add(
    name="MeOH innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fleet_reinvestment": 1, "innovators": 1, "meoh_inno_switch": 1},
)
def meoh_innovators():
    return fleet_reinvestment() * innovators() * meoh_inno_switch()


@component.add(
    name="MeOH investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"meoh_imitators": 1, "meoh_innovators": 1},
)
def meoh_investment():
    return meoh_imitators() + meoh_innovators()


@component.add(
    name="MeOH investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"equalizer": 1, "meoh_level": 1},
)
def meoh_investment_level():
    return equalizer() * meoh_level()


@component.add(
    name="MeOH level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "meoh_competitiveness": 1,
        "meoh_shipping_consumption": 2,
        "hfo_shipping_consumption": 1,
        "nh3_shipping_consumption": 1,
    },
)
def meoh_level():
    return (
        1
        / (1 + np.exp(10 * (meoh_competitiveness() - 1.1)))
        * meoh_shipping_consumption()
        / (
            hfo_shipping_consumption()
            + meoh_shipping_consumption()
            + nh3_shipping_consumption()
        )
    )


@component.add(
    name="MeOH LHV", units="MJ/kg", comp_type="Constant", comp_subtype="Normal"
)
def meoh_lhv():
    return 19.9


@component.add(name="MeOH lifetime", comp_type="Constant", comp_subtype="Normal")
def meoh_lifetime():
    return 20


@component.add(
    name="MeOH operating hours",
    units="h/Year",
    comp_type="Constant",
    comp_subtype="Normal",
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


@component.add(
    name="MeOH shipping consumption",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_meoh_shipping_consumption": 1},
    other_deps={
        "_integ_meoh_shipping_consumption": {
            "initial": {},
            "step": {"meoh_investment": 1, "meoh_decay": 1},
        }
    },
)
def meoh_shipping_consumption():
    return _integ_meoh_shipping_consumption()


_integ_meoh_shipping_consumption = Integ(
    lambda: meoh_investment() - meoh_decay(),
    lambda: 0,
    "_integ_meoh_shipping_consumption",
)


@component.add(
    name='"MeOH/H2"', units="kg/kg", comp_type="Constant", comp_subtype="Normal"
)
def meohh2():
    """
    kg MeOH/kg H2
    """
    return 15.7


@component.add(
    name="NH3 AF",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"discount_rate": 2, "nh3_lifetime": 1},
)
def nh3_af():
    return 1 / ((1 - (1 + discount_rate()) ** -nh3_lifetime()) / discount_rate())


@component.add(name="NH3 CAPEX", comp_type="Constant", comp_subtype="Normal")
def nh3_capex():
    return 6700


@component.add(
    name="NH3 competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nh3_cost": 2, "meoh_cost": 1, "hfo_cost": 1},
)
def nh3_competitiveness():
    return np.maximum(nh3_cost() / meoh_cost(), nh3_cost() / hfo_cost())


@component.add(
    name="NH3 cost",
    units="€/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nh3_capex": 1,
        "nh3_af": 1,
        "nh3_opex": 1,
        "nh3_operating_hours": 1,
        "nh3_lhv": 2,
        "nh3_el_usage": 1,
        "hydrogen_price": 1,
        "electricity_price": 1,
        "nh3_h2_usage": 1,
    },
)
def nh3_cost():
    """
    €/MJ NH3 [ [ [€/kgH2] / [kgNH3/kgH2] ] + [kWh/kgNH3 * €/kWh] ] / [MJ/kgNH3] + [kWhe/kWhNH3 * €/kWhe] * [kWh/MJ]
    """
    return (
        nh3_capex() * (nh3_af() + nh3_opex()) / (nh3_operating_hours() * nh3_lhv())
        + (hydrogen_price() / nh3_h2_usage() + nh3_el_usage() * electricity_price())
        / nh3_lhv()
    )


@component.add(
    name="NH3 decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nh3_shipping_consumption": 1, "ship_lifetime": 1},
)
def nh3_decay():
    return nh3_shipping_consumption() / ship_lifetime()


@component.add(name="NH3 el usage", comp_type="Constant", comp_subtype="Normal")
def nh3_el_usage():
    return 0.315


@component.add(
    name="NH3 H2 usage",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nh3h2": 1},
)
def nh3_h2_usage():
    return nh3h2()


@component.add(
    name="NH3 imitators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fleet_reinvestment": 1, "nh3_investment_level": 1},
)
def nh3_imitators():
    return fleet_reinvestment() * nh3_investment_level()


@component.add(
    name="NH3 inno switch",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nh3_competitiveness": 1},
)
def nh3_inno_switch():
    return if_then_else(nh3_competitiveness() < 2, lambda: 1, lambda: 0)


@component.add(
    name="NH3 innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fleet_reinvestment": 1, "innovators": 1, "nh3_inno_switch": 1},
)
def nh3_innovators():
    return fleet_reinvestment() * innovators() * nh3_inno_switch()


@component.add(
    name="NH3 investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nh3_innovators": 1, "nh3_imitators": 1},
)
def nh3_investment():
    return nh3_innovators() + nh3_imitators()


@component.add(
    name="NH3 investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"equalizer": 1, "nh3_level": 1},
)
def nh3_investment_level():
    return equalizer() * nh3_level()


@component.add(
    name="NH3 level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nh3_competitiveness": 1,
        "nh3_shipping_consumption": 2,
        "meoh_shipping_consumption": 1,
        "hfo_shipping_consumption": 1,
    },
)
def nh3_level():
    return (
        1
        / (1 + np.exp(10 * (nh3_competitiveness() - 1.1)))
        * nh3_shipping_consumption()
        / (
            hfo_shipping_consumption()
            + meoh_shipping_consumption()
            + nh3_shipping_consumption()
        )
    )


@component.add(name="NH3 LHV", comp_type="Constant", comp_subtype="Normal")
def nh3_lhv():
    return 18.9


@component.add(name="NH3 lifetime", comp_type="Constant", comp_subtype="Normal")
def nh3_lifetime():
    return 25


@component.add(name="NH3 operating hours", comp_type="Constant", comp_subtype="Normal")
def nh3_operating_hours():
    return 8000


@component.add(name="NH3 OPEX", comp_type="Constant", comp_subtype="Normal")
def nh3_opex():
    return 0.04


@component.add(
    name="NH3 shipping consumption",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_nh3_shipping_consumption": 1},
    other_deps={
        "_integ_nh3_shipping_consumption": {
            "initial": {},
            "step": {"nh3_investment": 1, "nh3_decay": 1},
        }
    },
)
def nh3_shipping_consumption():
    return _integ_nh3_shipping_consumption()


_integ_nh3_shipping_consumption = Integ(
    lambda: nh3_investment() - nh3_decay(), lambda: 0, "_integ_nh3_shipping_consumption"
)


@component.add(name='"NH3/H2"', comp_type="Constant", comp_subtype="Normal")
def nh3h2():
    """
    kg NH3/kg H2
    """
    return 5.56


@component.add(name="ship lifetime", comp_type="Constant", comp_subtype="Normal")
def ship_lifetime():
    return 15


@component.add(
    name="shipping hydrogen demand",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "meoh_shipping_consumption": 1,
        "meohh2": 1,
        "nh3h2": 1,
        "nh3_shipping_consumption": 1,
    },
)
def shipping_hydrogen_demand():
    """
    Convert from GWh to GJ, then from GJ to tons fuel, then from tons fuel to tons H2. Example 1: MeOH cons. [GWh] * 3600 [GJ/GWh] / 19.9 [GJ/t] / 15.7 [t MeOH/t H2] Example 2: NH3 cons. [GWh] * 3600 [GJ/GWh] / 18.6 [GJ/t] / 5.56 [t NH3/t H2]
    """
    return (
        meoh_shipping_consumption() * 3600 / 19.9 / meohh2()
        + nh3_shipping_consumption() * 3600 / 18.9 / nh3h2()
    )
