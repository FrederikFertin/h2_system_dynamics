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
        "fc_ship_cost": 1,
        "be_ship_cost": 3,
        "meoh_ship_cost": 1,
        "hfo_ship_cost": 1,
    },
)
def domestic_battery_competitiveness():
    return np.minimum(
        fc_ship_cost() / be_ship_cost(),
        np.minimum(hfo_ship_cost() / be_ship_cost(), meoh_ship_cost() / be_ship_cost()),
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
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_domestic_battery_inno_switch": 1},
    other_deps={
        "_smooth_domestic_battery_inno_switch": {
            "initial": {
                "domestic_battery_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
            "step": {
                "domestic_battery_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
        }
    },
)
def domestic_battery_inno_switch():
    return _smooth_domestic_battery_inno_switch()


_smooth_domestic_battery_inno_switch = Smooth(
    lambda: if_then_else(
        domestic_battery_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            domestic_battery_competitiveness() > early_switch_level(),
            lambda: 3,
            lambda: 1,
        ),
        lambda: 0,
    ),
    lambda: 2,
    lambda: if_then_else(
        domestic_battery_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            domestic_battery_competitiveness() > early_switch_level(),
            lambda: 3,
            lambda: 1,
        ),
        lambda: 0,
    ),
    lambda: 3,
    "_smooth_domestic_battery_inno_switch",
)


@component.add(
    name="Domestic battery innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_shipping_reinvestment": 1,
        "innovators": 1,
        "domestic_battery_inno_switch": 1,
        "domestic_battery_shipping_consumption": 1,
        "sum_dom_shipping": 2,
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
        "cross_innovation": 1,
        "domestic_battery_competitiveness": 1,
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
        "meoh_ship_cost": 1,
        "fc_ship_cost": 3,
        "be_ship_cost": 1,
        "hfo_ship_cost": 1,
    },
)
def domestic_h2_competitiveness():
    return np.minimum(
        meoh_ship_cost() / fc_ship_cost(),
        np.minimum(hfo_ship_cost() / fc_ship_cost(), be_ship_cost() / fc_ship_cost()),
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
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_domestic_h2_inno_switch": 1},
    other_deps={
        "_smooth_domestic_h2_inno_switch": {
            "initial": {
                "domestic_h2_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
            "step": {
                "domestic_h2_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
        }
    },
)
def domestic_h2_inno_switch():
    return _smooth_domestic_h2_inno_switch()


_smooth_domestic_h2_inno_switch = Smooth(
    lambda: if_then_else(
        domestic_h2_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            domestic_h2_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 2,
    lambda: if_then_else(
        domestic_h2_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            domestic_h2_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 3,
    "_smooth_domestic_h2_inno_switch",
)


@component.add(
    name="Domestic H2 innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "innovators": 1,
        "domestic_h2_inno_switch": 1,
        "domestic_shipping_reinvestment": 1,
        "sum_dom_shipping": 2,
        "domestic_h2_shipping_consumption": 1,
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
        "cross_innovation": 1,
        "domestic_h2_competitiveness": 1,
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
    units="GWh",
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
        "fc_ship_cost": 1,
        "hfo_ship_cost": 3,
        "be_ship_cost": 1,
        "meoh_ship_cost": 1,
    },
)
def domestic_hfo_competitiveness():
    return np.minimum(
        fc_ship_cost() / hfo_ship_cost(),
        np.minimum(
            be_ship_cost() / hfo_ship_cost(), meoh_ship_cost() / hfo_ship_cost()
        ),
    )


@component.add(
    name="Domestic HFO decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_hfo_shipping_consumption": 1,
        "domestic_hfo_early_decommission_rate": 1,
        "ship_lifetime": 1,
    },
)
def domestic_hfo_decay():
    return domestic_hfo_shipping_consumption() * (
        domestic_hfo_early_decommission_rate() + 1 / ship_lifetime()
    )


@component.add(
    name="Domestic HFO early decommission rate",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"domestic_hfo_competitiveness": 1},
)
def domestic_hfo_early_decommission_rate():
    return 1 / (1 + np.exp(-5 * -domestic_hfo_competitiveness())) * 0


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
        "domestic_hfo_competitiveness": 1,
        "cross_conventional": 1,
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
        "fc_ship_cost": 1,
        "meoh_ship_cost": 3,
        "be_ship_cost": 1,
        "hfo_ship_cost": 1,
    },
)
def domestic_meoh_competitiveness():
    return np.minimum(
        fc_ship_cost() / meoh_ship_cost(),
        np.minimum(
            hfo_ship_cost() / meoh_ship_cost(), be_ship_cost() / meoh_ship_cost()
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
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_domestic_meoh_inno_switch": 1},
    other_deps={
        "_smooth_domestic_meoh_inno_switch": {
            "initial": {
                "domestic_meoh_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
            "step": {
                "domestic_meoh_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
        }
    },
)
def domestic_meoh_inno_switch():
    return _smooth_domestic_meoh_inno_switch()


_smooth_domestic_meoh_inno_switch = Smooth(
    lambda: if_then_else(
        domestic_meoh_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            domestic_meoh_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 2,
    lambda: if_then_else(
        domestic_meoh_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            domestic_meoh_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 3,
    "_smooth_domestic_meoh_inno_switch",
)


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
        "cross_innovation": 1,
        "domestic_meoh_competitiveness": 1,
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
    name="domestic shipping average cost",
    units="€/GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_hfo_shipping_consumption": 1,
        "hfo_ship_cost": 1,
        "meoh_ship_cost": 1,
        "domestic_meoh_shipping_consumption": 1,
        "domestic_battery_shipping_consumption": 1,
        "be_ship_cost": 1,
        "fc_ship_cost": 1,
        "domestic_h2_shipping_consumption": 1,
        "yearly_hfo_consumption": 1,
        "sum_dom_shipping": 1,
    },
)
def domestic_shipping_average_cost():
    """
    €/GWh of HFO input energy equivalent. (Total operational costs, some CAPEX included (not ship hull)).
    """
    return (
        (
            domestic_hfo_shipping_consumption() * hfo_ship_cost()
            + domestic_meoh_shipping_consumption() * meoh_ship_cost()
            + domestic_battery_shipping_consumption() * be_ship_cost()
            + domestic_h2_shipping_consumption() * fc_ship_cost()
        )
        / (yearly_hfo_consumption() / 1000)
        / sum_dom_shipping()
    )


@component.add(
    name="domestic shipping biomass demand",
    units="GWh Biomass",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"domestic_meoh_shipping_consumption": 1, "meoh_biomass_usage": 1},
)
def domestic_shipping_biomass_demand():
    """
    Convert from GWh MeOH to GWh biomass
    """
    return domestic_meoh_shipping_consumption() * meoh_biomass_usage()


@component.add(
    name="domestic shipping consumption",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"domestic_shipping_consumption_forecast": 1, "fuel_use_index": 1},
)
def domestic_shipping_consumption():
    """
    Considering an annual growth of 1,79%/year linearly compared to year 2019. Consumption is amount of fuel bunkered. Pre efficiency losses.
    """
    return domestic_shipping_consumption_forecast() * fuel_use_index()


@component.add(
    name="domestic shipping consumption forecast",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def domestic_shipping_consumption_forecast():
    """
    Considering an annual growth of 1,79%/year linearly compared to year 2019. Consumption is amount of fuel bunkered. Pre efficiency losses.
    """
    return np.interp(
        time(),
        [
            1990.0,
            1991.0,
            1992.0,
            1993.0,
            1994.0,
            1995.0,
            1996.0,
            1997.0,
            1998.0,
            1999.0,
            2000.0,
            2001.0,
            2002.0,
            2003.0,
            2004.0,
            2005.0,
            2006.0,
            2007.0,
            2008.0,
            2009.0,
            2010.0,
            2011.0,
            2012.0,
            2013.0,
            2014.0,
            2015.0,
            2016.0,
            2017.0,
            2018.0,
            2019.0,
            2020.0,
            2021.0,
            2022.0,
            2023.0,
            2024.0,
            2025.0,
            2026.0,
            2027.0,
            2028.0,
            2029.0,
            2030.0,
            2031.0,
            2032.0,
            2033.0,
            2034.0,
            2035.0,
            2036.0,
            2037.0,
            2038.0,
            2039.0,
            2040.0,
            2041.0,
            2042.0,
            2043.0,
            2044.0,
            2045.0,
            2046.0,
            2047.0,
            2048.0,
            2049.0,
            2050.0,
        ],
        [
            83165.6,
            84798.6,
            84955.6,
            82767.0,
            82592.5,
            80043.4,
            86680.5,
            84451.0,
            84946.0,
            90256.1,
            80252.8,
            78781.5,
            78382.3,
            88114.3,
            88870.9,
            90189.4,
            97089.0,
            93154.9,
            85130.5,
            81783.4,
            83212.7,
            76752.4,
            74662.0,
            68486.8,
            64589.7,
            70277.9,
            72092.9,
            74424.0,
            72910.5,
            74002.5,
            75482.6,
            76962.6,
            78442.7,
            79922.7,
            81402.8,
            82882.8,
            84362.9,
            85842.9,
            87323.0,
            88803.0,
            90283.1,
            91763.1,
            93243.2,
            94723.2,
            96203.3,
            97683.4,
            99163.4,
            100643.0,
            102124.0,
            103604.0,
            105084.0,
            106564.0,
            108044.0,
            109524.0,
            111004.0,
            112484.0,
            113964.0,
            115444.0,
            116924.0,
            118404.0,
            119884.0,
        ],
    )


@component.add(
    name="domestic shipping emissions",
    units="tCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hfo_emission_factor": 1, "domestic_hfo_shipping_consumption": 1},
)
def domestic_shipping_emissions():
    return hfo_emission_factor() * domestic_hfo_shipping_consumption() * 3600


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
    name="domestic shipping FC hydrogen demand",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_h2_shipping_consumption": 1,
        "ice_efficiency": 1,
        "fc_efficiency": 1,
        "h2_lhv": 1,
    },
)
def domestic_shipping_fc_hydrogen_demand():
    return (
        (domestic_h2_shipping_consumption() * ice_efficiency() / fc_efficiency())
        * 3600
        / h2_lhv()
    )


@component.add(
    name="domestic shipping hydrogen demand",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_shipping_fc_hydrogen_demand": 1,
        "domestic_shipping_meoh_hydrogen_demand": 1,
    },
)
def domestic_shipping_hydrogen_demand():
    """
    Convert from GWh to GJ, then from GJ to tons fuel, then from tons fuel to tons H2. Example 1: MeOH cons. [GWh] * 3600 [GJ/GWh] / 19.9 [GJ/t] / 15.7 [t MeOH/t H2] Example 2: NH3 cons. [GWh] * 3600 [GJ/GWh] / 18.6 [GJ/t] / 5.56 [t NH3/t H2]
    """
    return (
        domestic_shipping_fc_hydrogen_demand()
        + domestic_shipping_meoh_hydrogen_demand()
    )


@component.add(
    name="domestic shipping MeOH hydrogen demand",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_meoh_shipping_consumption": 1,
        "meoh_lhv": 1,
        "meoh_h2_usage": 1,
    },
)
def domestic_shipping_meoh_hydrogen_demand():
    return domestic_meoh_shipping_consumption() * 3600 / meoh_lhv() / meoh_h2_usage()


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
    lambda: domestic_shipping_consumption() / ship_lifetime(),
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
    lambda: domestic_shipping_consumption() / 40,
    "_integ_error_int_dom_shipping",
)


@component.add(
    name="FC ship H2 price break",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "be_ship_cost": 1,
        "hfo_ship_cost": 1,
        "fc_ship_cost_without_h2": 1,
        "h2_lhv": 1,
        "yearly_h2_consumption": 1,
    },
)
def fc_ship_h2_price_break():
    return (
        (np.minimum(be_ship_cost(), hfo_ship_cost()) - fc_ship_cost_without_h2())
        * h2_lhv()
        / yearly_h2_consumption()
        / 1000
    )


@component.add(
    name="MeOH ship H2 price break",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "be_ship_cost": 1,
        "hfo_ship_cost": 1,
        "meoh_ship_cost_without_meoh": 1,
        "yearly_hfo_consumption": 1,
        "biomeoh_cost_without_h2": 1,
        "meoh_h2_usage": 1,
        "meoh_lhv": 1,
    },
)
def meoh_ship_h2_price_break():
    return (
        (
            (
                np.minimum(be_ship_cost(), hfo_ship_cost())
                - meoh_ship_cost_without_meoh()
            )
            / 3600
            / yearly_hfo_consumption()
            - biomeoh_cost_without_h2()
        )
        * meoh_h2_usage()
        * meoh_lhv()
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
