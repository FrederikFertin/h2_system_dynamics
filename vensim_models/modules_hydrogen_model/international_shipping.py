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
    lambda: int_shipping_consumption() / 40,
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
    depends_on={
        "meoh_containership_cost": 1,
        "hfo_containership_cost": 2,
        "nh3_containership_cost": 1,
    },
)
def hfo_competitiveness():
    return np.minimum(
        meoh_containership_cost() / hfo_containership_cost(),
        nh3_containership_cost() / hfo_containership_cost(),
    )


@component.add(
    name="HFO decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hfo_shipping_consumption": 1,
        "ship_lifetime": 1,
        "hfo_early_decommission_rate": 1,
    },
)
def hfo_decay():
    return hfo_shipping_consumption() * (
        hfo_early_decommission_rate() + 1 / ship_lifetime()
    )


@component.add(
    name="HFO early decommission rate",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hfo_competitiveness": 1},
)
def hfo_early_decommission_rate():
    return 1 / (1 + np.exp(-5 * -hfo_competitiveness()))


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
        "hfo_competitiveness": 1,
        "cross_conventional": 1,
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
    comp_subtype="Normal",
    depends_on={"fuel_use_index": 1, "int_shipping_consumption_forecast": 1},
)
def int_shipping_consumption():
    """
    Considering an annual growth of 1,79%/year linearly compared to year 2019. Consumption is amount of fuel bunkered. Pre efficiency losses.
    """
    return fuel_use_index() * int_shipping_consumption_forecast()


@component.add(
    name="int shipping consumption forecast",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def int_shipping_consumption_forecast():
    """
    Considering an annual growth of 1,79%/year linearly compared to year 2019. Consumption is amount of fuel bunkered. Pre efficiency losses.
    """
    return np.interp(
        time(),
        [
            1990,
            1991,
            1992,
            1993,
            1994,
            1995,
            1996,
            1997,
            1998,
            1999,
            2000,
            2001,
            2002,
            2003,
            2004,
            2005,
            2006,
            2007,
            2008,
            2009,
            2010,
            2011,
            2012,
            2013,
            2014,
            2015,
            2016,
            2017,
            2018,
            2019,
            2020,
            2021,
            2022,
            2023,
            2024,
            2025,
            2026,
            2027,
            2028,
            2029,
            2030,
            2031,
            2032,
            2033,
            2034,
            2035,
            2036,
            2037,
            2038,
            2039,
            2040,
            2041,
            2042,
            2043,
            2044,
            2045,
            2046,
            2047,
            2048,
            2049,
            2050,
        ],
        [
            420443,
            416041,
            421378,
            419745,
            412997,
            418664,
            441341,
            476294,
            497165,
            471125,
            504202,
            519926,
            528817,
            540227,
            569438,
            581506,
            618546,
            645924,
            649579,
            583112,
            581223,
            583251,
            542692,
            514524,
            499874,
            494726,
            519189,
            522157,
            539450,
            534033,
            543592,
            553151,
            562710,
            572270,
            581829,
            591388,
            600947,
            610506,
            620066,
            629625,
            639184,
            648743,
            658302,
            667862,
            677421,
            686980,
            696539,
            706098,
            715657,
            725217,
            734776,
            744335,
            753894,
            763453,
            773013,
            782572,
            792131,
            801690,
            811249,
            820809,
            830368,
        ],
    )


@component.add(
    name="international shipping average cost",
    units="€/GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hfo_shipping_consumption": 1,
        "hfo_containership_cost": 1,
        "meoh_containership_cost": 1,
        "meoh_shipping_consumption": 1,
        "nh3_shipping_consumption": 1,
        "nh3_containership_cost": 1,
        "yearly_containership_consumption": 1,
        "sum_int_shipping": 1,
    },
)
def international_shipping_average_cost():
    """
    €/GWh of HFO input equivalent. (Total ship ownership costs).
    """
    return (
        (
            hfo_shipping_consumption() * hfo_containership_cost()
            + meoh_shipping_consumption() * meoh_containership_cost()
            + nh3_shipping_consumption() * nh3_containership_cost()
        )
        / yearly_containership_consumption()
        * 10**6
        / sum_int_shipping()
    )


@component.add(
    name="international shipping biomass demand",
    units="GWh Biomass",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"meoh_shipping_consumption": 1, "meoh_biomass_usage": 1},
)
def international_shipping_biomass_demand():
    """
    Convert from GWh MeOH to GWh biomass
    """
    return meoh_shipping_consumption() * meoh_biomass_usage()


@component.add(
    name="international shipping emissions",
    units="tCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hfo_emission_factor": 1, "hfo_shipping_consumption": 1},
)
def international_shipping_emissions():
    return hfo_emission_factor() * hfo_shipping_consumption() * 3600


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


@component.add(
    name="MeOH competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nh3_containership_cost": 1,
        "meoh_containership_cost": 2,
        "hfo_containership_cost": 1,
    },
)
def meoh_competitiveness():
    return np.minimum(
        nh3_containership_cost() / meoh_containership_cost(),
        hfo_containership_cost() / meoh_containership_cost(),
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
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_meoh_inno_switch": 1},
    other_deps={
        "_smooth_meoh_inno_switch": {
            "initial": {
                "meoh_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
            "step": {
                "meoh_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
        }
    },
)
def meoh_inno_switch():
    return _smooth_meoh_inno_switch()


_smooth_meoh_inno_switch = Smooth(
    lambda: if_then_else(
        meoh_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            meoh_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 2,
    lambda: if_then_else(
        meoh_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            meoh_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 3,
    "_smooth_meoh_inno_switch",
)


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
        "cross_innovation": 1,
        "meoh_competitiveness": 1,
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
    depends_on={
        "meoh_containership_cost": 1,
        "nh3_containership_cost": 2,
        "hfo_containership_cost": 1,
    },
)
def nh3_competitiveness():
    return np.minimum(
        meoh_containership_cost() / nh3_containership_cost(),
        hfo_containership_cost() / nh3_containership_cost(),
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
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_nh3_inno_switch": 1},
    other_deps={
        "_smooth_nh3_inno_switch": {
            "initial": {
                "nh3_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
            "step": {
                "nh3_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
        }
    },
)
def nh3_inno_switch():
    return _smooth_nh3_inno_switch()


_smooth_nh3_inno_switch = Smooth(
    lambda: if_then_else(
        nh3_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            nh3_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 2,
    lambda: if_then_else(
        nh3_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            nh3_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 3,
    "_smooth_nh3_inno_switch",
)


@component.add(
    name="NH3 innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "shipping_reinvestment": 1,
        "innovators": 1,
        "nh3_inno_switch": 1,
        "nh3_shipping_consumption": 1,
        "sum_int_shipping": 2,
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
        "cross_innovation": 1,
        "nh3_competitiveness": 1,
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


@component.add(
    name="ship lifetime", units="years", comp_type="Constant", comp_subtype="Normal"
)
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
    lambda: int_shipping_consumption() / ship_lifetime(),
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
