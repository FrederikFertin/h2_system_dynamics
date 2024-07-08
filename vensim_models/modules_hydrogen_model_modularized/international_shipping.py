"""
Module international_shipping
Translated using PySD version 3.14.0
"""

@component.add(
    name="ctrl shipping",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"k_p": 1, "error_shipping": 1, "error_int_shipping": 1},
)
def ctrl_shipping():
    return k_p() * error_shipping() + error_int_shipping()


@component.add(
    name="demand change shipping",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ctrl_shipping": 1},
)
def demand_change_shipping():
    return ctrl_shipping()


@component.add(
    name="error int shipping",
    units="e",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_error_int_shipping": 1},
    other_deps={
        "_integ_error_int_shipping": {
            "initial": {"int_shipping_consumption": 1},
            "step": {"k_i": 1, "error_shipping": 1},
        }
    },
)
def error_int_shipping():
    return _integ_error_int_shipping()


_integ_error_int_shipping = Integ(
    lambda: k_i() * error_shipping(),
    lambda: int_shipping_consumption() * 0.0179,
    "_integ_error_int_shipping",
)


@component.add(
    name="error shipping",
    units="e",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"int_shipping_consumption": 1, "sum_int_shipping": 1},
)
def error_shipping():
    return int_shipping_consumption() - sum_int_shipping()


@component.add(
    name="HFO competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_nh3_price": 1, "hfo_cost": 2, "green_biomeoh_price": 1},
)
def hfo_competitiveness():
    return np.minimum(
        green_nh3_price() / hfo_cost(), green_biomeoh_price() / hfo_cost()
    )


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
    depends_on={"hfo_investment_level": 1, "shipping_reinvestment": 1},
)
def hfo_investment():
    return hfo_investment_level() * shipping_reinvestment()


@component.add(
    name="HFO investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"shipping_equalizer": 1, "hfo_level": 1},
)
def hfo_investment_level():
    return shipping_equalizer() * hfo_level()


@component.add(
    name="HFO level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "cross_conventional": 1,
        "hfo_competitiveness": 1,
        "hfo_shipping_consumption": 1,
        "sum_int_shipping": 1,
    },
)
def hfo_level():
    return (
        1
        / (1 + np.exp(slope() * (cross_conventional() - hfo_competitiveness())))
        * hfo_shipping_consumption()
        / sum_int_shipping()
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
    Considering an annual growth of 1,79%/year linearly compared to year 2019.
    """
    return np.interp(time(), [2019, 2050], [501403, 871296])


@component.add(
    name="international shipping biomass demand",
    units="tBiomass",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"meoh_shipping_consumption": 1, "meoh_lhv": 1, "meoh_biomass_usage": 1},
)
def international_shipping_biomass_demand():
    """
    Convert to GJ MeOH, then to t MeOH, then to t Biomass.
    """
    return meoh_shipping_consumption() * 3600 / meoh_lhv() * meoh_biomass_usage()


@component.add(
    name="international shipping hydrogen demand",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "meoh_shipping_consumption": 1,
        "meoh_lhv": 1,
        "meoh_h2_usage": 1,
        "nh3_shipping_consumption": 1,
        "nh3_lhv": 1,
        "nh3_h2_usage": 1,
    },
)
def international_shipping_hydrogen_demand():
    """
    Convert from GWh to GJ, then from GJ to tons fuel, then from tons fuel to tons H2. Example 1: MeOH cons. [GWh] * 3600 [GJ/GWh] / 19.9 [GJ/t] / 15.7 [t MeOH/t H2] Example 2: NH3 cons. [GWh] * 3600 [GJ/GWh] / 18.6 [GJ/t] / 5.56 [t NH3/t H2]
    """
    return (
        meoh_shipping_consumption() * 3600 / meoh_lhv() / meoh_h2_usage()
        + nh3_shipping_consumption() * 3600 / nh3_lhv() / nh3_h2_usage()
    )


@component.add(name="k i", comp_type="Constant", comp_subtype="Normal")
def k_i():
    return 0.54 / 4


@component.add(name="k p", comp_type="Constant", comp_subtype="Normal")
def k_p():
    return 3


@component.add(
    name="MeOH competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_nh3_price": 1, "green_biomeoh_price": 2, "hfo_cost": 1},
)
def meoh_competitiveness():
    return np.minimum(
        green_nh3_price() / green_biomeoh_price(), hfo_cost() / green_biomeoh_price()
    )


@component.add(
    name="MeOH decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"meoh_shipping_consumption": 1, "ship_lifetime": 1},
)
def meoh_decay():
    return meoh_shipping_consumption() / ship_lifetime()


@component.add(
    name="MeOH imitators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"shipping_reinvestment": 1, "meoh_investment_level": 1},
)
def meoh_imitators():
    return shipping_reinvestment() * meoh_investment_level()


@component.add(
    name="MeOH inno switch",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"meoh_competitiveness": 1},
)
def meoh_inno_switch():
    return if_then_else(meoh_competitiveness() > 0.5, lambda: 1, lambda: 0)


@component.add(
    name="MeOH innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "shipping_reinvestment": 1,
        "meoh_inno_switch": 1,
        "innovators": 1,
        "sum_int_shipping": 2,
        "meoh_shipping_consumption": 1,
    },
)
def meoh_innovators():
    return (
        shipping_reinvestment()
        * meoh_inno_switch()
        * innovators()
        * (sum_int_shipping() - meoh_shipping_consumption())
        / sum_int_shipping()
    )


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
    depends_on={"shipping_equalizer": 1, "meoh_level": 1},
)
def meoh_investment_level():
    return shipping_equalizer() * meoh_level()


@component.add(
    name="MeOH level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "meoh_competitiveness": 1,
        "cross_innovation": 1,
        "meoh_shipping_consumption": 1,
        "sum_int_shipping": 1,
    },
)
def meoh_level():
    return (
        1
        / (1 + np.exp(slope() * (cross_innovation() - meoh_competitiveness())))
        * meoh_shipping_consumption()
        / sum_int_shipping()
    )


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
    name="NH3 competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_biomeoh_price": 1, "green_nh3_price": 2, "hfo_cost": 1},
)
def nh3_competitiveness():
    return np.minimum(
        green_biomeoh_price() / green_nh3_price(), hfo_cost() / green_nh3_price()
    )


@component.add(
    name="NH3 decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nh3_shipping_consumption": 1, "ship_lifetime": 1},
)
def nh3_decay():
    return nh3_shipping_consumption() / ship_lifetime()


@component.add(
    name="NH3 imitators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"shipping_reinvestment": 1, "nh3_investment_level": 1},
)
def nh3_imitators():
    return shipping_reinvestment() * nh3_investment_level()


@component.add(
    name="NH3 inno switch",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nh3_competitiveness": 1},
)
def nh3_inno_switch():
    return if_then_else(nh3_competitiveness() > 0.5, lambda: 1, lambda: 0)


@component.add(
    name="NH3 innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "shipping_reinvestment": 1,
        "innovators": 1,
        "nh3_inno_switch": 1,
        "sum_int_shipping": 2,
        "nh3_shipping_consumption": 1,
    },
)
def nh3_innovators():
    return (
        shipping_reinvestment()
        * innovators()
        * nh3_inno_switch()
        * (sum_int_shipping() - nh3_shipping_consumption())
        / sum_int_shipping()
    )


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
    depends_on={"shipping_equalizer": 1, "nh3_level": 1},
)
def nh3_investment_level():
    return shipping_equalizer() * nh3_level()


@component.add(
    name="NH3 level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "nh3_competitiveness": 1,
        "cross_innovation": 1,
        "nh3_shipping_consumption": 1,
        "sum_int_shipping": 1,
    },
)
def nh3_level():
    return (
        1
        / (1 + np.exp(slope() * (cross_innovation() - nh3_competitiveness())))
        * nh3_shipping_consumption()
        / sum_int_shipping()
    )


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


@component.add(name="ship lifetime", comp_type="Constant", comp_subtype="Normal")
def ship_lifetime():
    return 15


@component.add(
    name="shipping equalizer",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hfo_level": 1, "meoh_level": 1, "nh3_level": 1},
)
def shipping_equalizer():
    return 1 / (hfo_level() + meoh_level() + nh3_level())


@component.add(
    name="shipping reinvestment",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_shipping_reinvestment": 1},
    other_deps={
        "_integ_shipping_reinvestment": {
            "initial": {"int_shipping_consumption": 1, "ship_lifetime": 1},
            "step": {
                "demand_change_shipping": 1,
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
def shipping_reinvestment():
    return _integ_shipping_reinvestment()


_integ_shipping_reinvestment = Integ(
    lambda: demand_change_shipping()
    + hfo_decay()
    + meoh_decay()
    + nh3_decay()
    - hfo_investment()
    - meoh_investment()
    - nh3_investment(),
    lambda: int_shipping_consumption() * (0.0179 + 1 / ship_lifetime()),
    "_integ_shipping_reinvestment",
)


@component.add(
    name="sum int shipping",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hfo_shipping_consumption": 1,
        "meoh_shipping_consumption": 1,
        "nh3_shipping_consumption": 1,
    },
)
def sum_int_shipping():
    return (
        hfo_shipping_consumption()
        + meoh_shipping_consumption()
        + nh3_shipping_consumption()
    )
