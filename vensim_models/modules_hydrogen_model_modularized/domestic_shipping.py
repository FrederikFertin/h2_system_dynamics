"""
Module domestic_shipping
Translated using PySD version 3.14.0
"""

@component.add(
    name="ctrl dom shipping",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"k_p": 1, "error_dom_shipping": 1, "error_int_dom_shipping": 1},
)
def ctrl_dom_shipping():
    return k_p() * error_dom_shipping() + error_int_dom_shipping()


@component.add(
    name="demand change dom shipping",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ctrl_dom_shipping": 1},
)
def demand_change_dom_shipping():
    return ctrl_dom_shipping()


@component.add(
    name="Domestic battery competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "h2_propulsion_cost": 1,
        "electrical_propulsion_cost": 3,
        "meoh_propulsion_cost": 1,
        "hfo_propulsion_cost": 1,
    },
)
def domestic_battery_competitiveness():
    return np.minimum(
        h2_propulsion_cost() / electrical_propulsion_cost(),
        np.minimum(
            hfo_propulsion_cost() / electrical_propulsion_cost(),
            meoh_propulsion_cost() / electrical_propulsion_cost(),
        ),
    )


@component.add(
    name="Domestic battery decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"domestic_battery_shipping_consumption": 1, "ship_lifetime": 1},
)
def domestic_battery_decay():
    return domestic_battery_shipping_consumption() / ship_lifetime()


@component.add(
    name="Domestic battery imitators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_shipping_reinvestment": 1,
        "domestic_battery_investment_level": 1,
    },
)
def domestic_battery_imitators():
    return domestic_shipping_reinvestment() * domestic_battery_investment_level()


@component.add(
    name="Domestic battery inno switch",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"domestic_battery_competitiveness": 1},
)
def domestic_battery_inno_switch():
    return if_then_else(domestic_battery_competitiveness() > 0.5, lambda: 1, lambda: 0)


@component.add(
    name="Domestic battery innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_shipping_reinvestment": 1,
        "innovators": 1,
        "domestic_battery_inno_switch": 1,
        "sum_dom_shipping": 2,
        "domestic_battery_shipping_consumption": 1,
    },
)
def domestic_battery_innovators():
    return (
        domestic_shipping_reinvestment()
        * innovators()
        * domestic_battery_inno_switch()
        * (sum_dom_shipping() - domestic_battery_shipping_consumption())
        / sum_dom_shipping()
    )


@component.add(
    name="Domestic battery investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"domestic_battery_innovators": 1, "domestic_battery_imitators": 1},
)
def domestic_battery_investment():
    return domestic_battery_innovators() + domestic_battery_imitators()


@component.add(
    name="Domestic battery investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"domestic_shipping_equalizer": 1, "domestic_battery_level": 1},
)
def domestic_battery_investment_level():
    return domestic_shipping_equalizer() * domestic_battery_level()


@component.add(
    name="Domestic battery level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "domestic_battery_competitiveness": 1,
        "cross_innovation": 1,
        "domestic_battery_shipping_consumption": 1,
        "sum_dom_shipping": 1,
    },
)
def domestic_battery_level():
    return (
        1
        / (
            1
            + np.exp(
                slope() * (cross_innovation() - domestic_battery_competitiveness())
            )
        )
        * domestic_battery_shipping_consumption()
        / sum_dom_shipping()
    )


@component.add(
    name="Domestic battery shipping consumption",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_domestic_battery_shipping_consumption": 1},
    other_deps={
        "_integ_domestic_battery_shipping_consumption": {
            "initial": {},
            "step": {"domestic_battery_investment": 1, "domestic_battery_decay": 1},
        }
    },
)
def domestic_battery_shipping_consumption():
    return _integ_domestic_battery_shipping_consumption()


_integ_domestic_battery_shipping_consumption = Integ(
    lambda: domestic_battery_investment() - domestic_battery_decay(),
    lambda: 0,
    "_integ_domestic_battery_shipping_consumption",
)


@component.add(
    name="Domestic H2 competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "meoh_propulsion_cost": 1,
        "h2_propulsion_cost": 3,
        "electrical_propulsion_cost": 1,
        "hfo_propulsion_cost": 1,
    },
)
def domestic_h2_competitiveness():
    return np.minimum(
        meoh_propulsion_cost() / h2_propulsion_cost(),
        np.minimum(
            hfo_propulsion_cost() / h2_propulsion_cost(),
            electrical_propulsion_cost() / h2_propulsion_cost(),
        ),
    )


@component.add(
    name="Domestic H2 decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"domestic_h2_shipping_consumption": 1, "ship_lifetime": 1},
)
def domestic_h2_decay():
    return domestic_h2_shipping_consumption() / ship_lifetime()


@component.add(
    name="Domestic H2 imitators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"domestic_h2_investment_level": 1, "domestic_shipping_reinvestment": 1},
)
def domestic_h2_imitators():
    return domestic_h2_investment_level() * domestic_shipping_reinvestment()


@component.add(
    name="Domestic H2 inno switch",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"domestic_h2_competitiveness": 1},
)
def domestic_h2_inno_switch():
    return if_then_else(domestic_h2_competitiveness() > 0.5, lambda: 1, lambda: 0)


@component.add(
    name="Domestic H2 innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "innovators": 1,
        "domestic_h2_inno_switch": 1,
        "domestic_shipping_reinvestment": 1,
        "domestic_h2_shipping_consumption": 1,
        "sum_dom_shipping": 2,
    },
)
def domestic_h2_innovators():
    return (
        innovators()
        * domestic_h2_inno_switch()
        * domestic_shipping_reinvestment()
        * (sum_dom_shipping() - domestic_h2_shipping_consumption())
        / sum_dom_shipping()
    )


@component.add(
    name="Domestic H2 investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"domestic_h2_imitators": 1, "domestic_h2_innovators": 1},
)
def domestic_h2_investment():
    return domestic_h2_imitators() + domestic_h2_innovators()


@component.add(
    name="Domestic H2 investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"domestic_h2_level": 1, "domestic_shipping_equalizer": 1},
)
def domestic_h2_investment_level():
    return domestic_h2_level() * domestic_shipping_equalizer()


@component.add(
    name="Domestic H2 level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "domestic_h2_competitiveness": 1,
        "cross_innovation": 1,
        "domestic_h2_shipping_consumption": 1,
        "sum_dom_shipping": 1,
    },
)
def domestic_h2_level():
    return (
        1
        / (1 + np.exp(slope() * (cross_innovation() - domestic_h2_competitiveness())))
        * domestic_h2_shipping_consumption()
        / sum_dom_shipping()
    )


@component.add(
    name="Domestic H2 shipping consumption",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_domestic_h2_shipping_consumption": 1},
    other_deps={
        "_integ_domestic_h2_shipping_consumption": {
            "initial": {},
            "step": {"domestic_h2_investment": 1, "domestic_h2_decay": 1},
        }
    },
)
def domestic_h2_shipping_consumption():
    return _integ_domestic_h2_shipping_consumption()


_integ_domestic_h2_shipping_consumption = Integ(
    lambda: domestic_h2_investment() - domestic_h2_decay(),
    lambda: 0,
    "_integ_domestic_h2_shipping_consumption",
)


@component.add(
    name="Domestic HFO competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "h2_propulsion_cost": 1,
        "hfo_propulsion_cost": 3,
        "electrical_propulsion_cost": 1,
        "meoh_propulsion_cost": 1,
    },
)
def domestic_hfo_competitiveness():
    return np.minimum(
        h2_propulsion_cost() / hfo_propulsion_cost(),
        np.minimum(
            electrical_propulsion_cost() / hfo_propulsion_cost(),
            meoh_propulsion_cost() / hfo_propulsion_cost(),
        ),
    )


@component.add(
    name="Domestic HFO decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"domestic_hfo_shipping_consumption": 1, "ship_lifetime": 1},
)
def domestic_hfo_decay():
    return domestic_hfo_shipping_consumption() / ship_lifetime()


@component.add(
    name="Domestic HFO investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_hfo_investment_level": 1,
        "domestic_shipping_reinvestment": 1,
    },
)
def domestic_hfo_investment():
    return domestic_hfo_investment_level() * domestic_shipping_reinvestment()


@component.add(
    name="Domestic HFO investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"domestic_shipping_equalizer": 1, "domestic_hfo_level": 1},
)
def domestic_hfo_investment_level():
    return domestic_shipping_equalizer() * domestic_hfo_level()


@component.add(
    name="Domestic HFO level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "cross_conventional": 1,
        "domestic_hfo_competitiveness": 1,
        "domestic_hfo_shipping_consumption": 1,
        "sum_dom_shipping": 1,
    },
)
def domestic_hfo_level():
    return (
        1
        / (
            1
            + np.exp(slope() * (cross_conventional() - domestic_hfo_competitiveness()))
        )
        * domestic_hfo_shipping_consumption()
        / sum_dom_shipping()
    )


@component.add(
    name="Domestic HFO shipping consumption",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_domestic_hfo_shipping_consumption": 1},
    other_deps={
        "_integ_domestic_hfo_shipping_consumption": {
            "initial": {"domestic_shipping_consumption": 1},
            "step": {"domestic_hfo_investment": 1, "domestic_hfo_decay": 1},
        }
    },
)
def domestic_hfo_shipping_consumption():
    return _integ_domestic_hfo_shipping_consumption()


_integ_domestic_hfo_shipping_consumption = Integ(
    lambda: domestic_hfo_investment() - domestic_hfo_decay(),
    lambda: domestic_shipping_consumption(),
    "_integ_domestic_hfo_shipping_consumption",
)


@component.add(
    name="Domestic MeOH competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "h2_propulsion_cost": 1,
        "meoh_propulsion_cost": 3,
        "electrical_propulsion_cost": 1,
        "hfo_propulsion_cost": 1,
    },
)
def domestic_meoh_competitiveness():
    return np.minimum(
        h2_propulsion_cost() / meoh_propulsion_cost(),
        np.minimum(
            hfo_propulsion_cost() / meoh_propulsion_cost(),
            electrical_propulsion_cost() / meoh_propulsion_cost(),
        ),
    )


@component.add(
    name="Domestic MeOH decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"domestic_meoh_shipping_consumption": 1, "ship_lifetime": 1},
)
def domestic_meoh_decay():
    return domestic_meoh_shipping_consumption() / ship_lifetime()


@component.add(
    name="Domestic MeOH imitators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_shipping_reinvestment": 1,
        "domestic_meoh_investment_level": 1,
    },
)
def domestic_meoh_imitators():
    return domestic_shipping_reinvestment() * domestic_meoh_investment_level()


@component.add(
    name="Domestic MeOH inno switch",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"domestic_meoh_competitiveness": 1},
)
def domestic_meoh_inno_switch():
    return if_then_else(domestic_meoh_competitiveness() > 0.5, lambda: 1, lambda: 0)


@component.add(
    name="Domestic MeOH innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_shipping_reinvestment": 1,
        "innovators": 1,
        "domestic_meoh_inno_switch": 1,
        "domestic_meoh_shipping_consumption": 1,
        "sum_dom_shipping": 2,
    },
)
def domestic_meoh_innovators():
    return (
        domestic_shipping_reinvestment()
        * innovators()
        * domestic_meoh_inno_switch()
        * (sum_dom_shipping() - domestic_meoh_shipping_consumption())
        / sum_dom_shipping()
    )


@component.add(
    name="Domestic MeOH investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"domestic_meoh_imitators": 1, "domestic_meoh_innovators": 1},
)
def domestic_meoh_investment():
    return domestic_meoh_imitators() + domestic_meoh_innovators()


@component.add(
    name="Domestic MeOH investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"domestic_shipping_equalizer": 1, "domestic_meoh_level": 1},
)
def domestic_meoh_investment_level():
    return domestic_shipping_equalizer() * domestic_meoh_level()


@component.add(
    name="Domestic MeOH level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "domestic_meoh_competitiveness": 1,
        "cross_innovation": 1,
        "domestic_meoh_shipping_consumption": 1,
        "sum_dom_shipping": 1,
    },
)
def domestic_meoh_level():
    return (
        1
        / (1 + np.exp(slope() * (cross_innovation() - domestic_meoh_competitiveness())))
        * domestic_meoh_shipping_consumption()
        / sum_dom_shipping()
    )


@component.add(
    name="Domestic MeOH shipping consumption",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_domestic_meoh_shipping_consumption": 1},
    other_deps={
        "_integ_domestic_meoh_shipping_consumption": {
            "initial": {},
            "step": {"domestic_meoh_investment": 1, "domestic_meoh_decay": 1},
        }
    },
)
def domestic_meoh_shipping_consumption():
    return _integ_domestic_meoh_shipping_consumption()


_integ_domestic_meoh_shipping_consumption = Integ(
    lambda: domestic_meoh_investment() - domestic_meoh_decay(),
    lambda: 0,
    "_integ_domestic_meoh_shipping_consumption",
)


@component.add(
    name="domestic shipping biomass demand",
    units="tBiomass",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_meoh_shipping_consumption": 1,
        "meoh_lhv": 1,
        "meoh_biomass_usage": 1,
    },
)
def domestic_shipping_biomass_demand():
    """
    Convert to GJ MeOH, then to t MeOH, then to t Biomass.
    """
    return (
        domestic_meoh_shipping_consumption() * 3600 / meoh_lhv() * meoh_biomass_usage()
    )


@component.add(
    name="domestic shipping consumption",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def domestic_shipping_consumption():
    """
    Considering an annual growth of 1,79%/year linearly compared to year 2019.
    """
    return np.interp(time(), [2019, 2050], [49177, 97795])


@component.add(
    name="Domestic shipping equalizer",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_hfo_level": 1,
        "domestic_meoh_level": 1,
        "domestic_battery_level": 1,
        "domestic_h2_level": 1,
    },
)
def domestic_shipping_equalizer():
    return 1 / (
        domestic_hfo_level()
        + domestic_meoh_level()
        + domestic_battery_level()
        + domestic_h2_level()
    )


@component.add(
    name="domestic shipping hydrogen demand",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_meoh_shipping_consumption": 1,
        "meoh_lhv": 1,
        "meoh_h2_usage": 1,
        "domestic_h2_shipping_consumption": 1,
        "lhv_h2": 1,
    },
)
def domestic_shipping_hydrogen_demand():
    """
    Convert from GWh to GJ, then from GJ to tons fuel, then from tons fuel to tons H2. Example 1: MeOH cons. [GWh] * 3600 [GJ/GWh] / 19.9 [GJ/t] / 15.7 [t MeOH/t H2] Example 2: NH3 cons. [GWh] * 3600 [GJ/GWh] / 18.6 [GJ/t] / 5.56 [t NH3/t H2]
    """
    return (
        domestic_meoh_shipping_consumption() * 3600 / meoh_lhv() / meoh_h2_usage()
        + domestic_h2_shipping_consumption() * 3600 / lhv_h2()
    )


@component.add(
    name="Domestic shipping reinvestment",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_domestic_shipping_reinvestment": 1},
    other_deps={
        "_integ_domestic_shipping_reinvestment": {
            "initial": {"domestic_shipping_consumption": 1, "ship_lifetime": 1},
            "step": {
                "demand_change_dom_shipping": 1,
                "domestic_battery_decay": 1,
                "domestic_h2_decay": 1,
                "domestic_hfo_decay": 1,
                "domestic_meoh_decay": 1,
                "domestic_battery_investment": 1,
                "domestic_h2_investment": 1,
                "domestic_hfo_investment": 1,
                "domestic_meoh_investment": 1,
            },
        }
    },
)
def domestic_shipping_reinvestment():
    return _integ_domestic_shipping_reinvestment()


_integ_domestic_shipping_reinvestment = Integ(
    lambda: demand_change_dom_shipping()
    + domestic_battery_decay()
    + domestic_h2_decay()
    + domestic_hfo_decay()
    + domestic_meoh_decay()
    - domestic_battery_investment()
    - domestic_h2_investment()
    - domestic_hfo_investment()
    - domestic_meoh_investment(),
    lambda: domestic_shipping_consumption() * (0.0179 + 1 / ship_lifetime()),
    "_integ_domestic_shipping_reinvestment",
)


@component.add(
    name="error dom shipping",
    units="e",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"domestic_shipping_consumption": 1, "sum_dom_shipping": 1},
)
def error_dom_shipping():
    return domestic_shipping_consumption() - sum_dom_shipping()


@component.add(
    name="error int dom shipping",
    units="e",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_error_int_dom_shipping": 1},
    other_deps={
        "_integ_error_int_dom_shipping": {
            "initial": {"domestic_shipping_consumption": 1},
            "step": {"k_i": 1, "error_dom_shipping": 1},
        }
    },
)
def error_int_dom_shipping():
    return _integ_error_int_dom_shipping()


_integ_error_int_dom_shipping = Integ(
    lambda: k_i() * error_dom_shipping(),
    lambda: domestic_shipping_consumption() * 0.0179,
    "_integ_error_int_dom_shipping",
)


@component.add(
    name="sum dom shipping",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_hfo_shipping_consumption": 1,
        "domestic_meoh_shipping_consumption": 1,
        "domestic_battery_shipping_consumption": 1,
        "domestic_h2_shipping_consumption": 1,
    },
)
def sum_dom_shipping():
    return (
        domestic_hfo_shipping_consumption()
        + domestic_meoh_shipping_consumption()
        + domestic_battery_shipping_consumption()
        + domestic_h2_shipping_consumption()
    )
