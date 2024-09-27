"""
Module light_duty_road_transport
Translated using PySD version 3.14.0
"""

@component.add(
    name="ctrl LD RT",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"k_p": 1, "error_ld_rt": 1, "error_int_ld_rt": 1},
)
def ctrl_ld_rt():
    return k_p() * error_ld_rt() + error_int_ld_rt()


@component.add(
    name="demand change LD RT",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ctrl_ld_rt": 1},
)
def demand_change_ld_rt():
    return ctrl_ld_rt()


@component.add(
    name="error int LD RT",
    units="e",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_error_int_ld_rt": 1},
    other_deps={
        "_integ_error_int_ld_rt": {
            "initial": {"ld_rt_consumption": 1},
            "step": {"k_i": 1, "error_ld_rt": 1},
        }
    },
)
def error_int_ld_rt():
    return _integ_error_int_ld_rt()


_integ_error_int_ld_rt = Integ(
    lambda: k_i() * error_ld_rt(),
    lambda: ld_rt_consumption() * 0.0179,
    "_integ_error_int_ld_rt",
)


@component.add(
    name="error LD RT",
    units="e",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ld_rt_consumption": 1, "sum_ld_rt": 1},
)
def error_ld_rt():
    return ld_rt_consumption() - sum_ld_rt()


@component.add(
    name="ICE car ban",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1},
)
def ice_car_ban():
    return step(__data["time"], 1, 2035)


@component.add(
    name="LD average cost",
    units="€/GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ld_bev_consumption": 1,
        "ld_be_lco": 1,
        "ld_fc_lco": 1,
        "ld_fcev_consumption": 1,
        "ld_ice_lco": 1,
        "ld_fossil_consumption": 1,
        "diesel_lhv": 1,
        "ld_ice_energy_usage": 1,
        "sum_ld_rt": 1,
    },
)
def ld_average_cost():
    """
    €/GWh of diesel equivalent. (Total car ownership costs). Unit check: GWh * €/km * km/kWh * 10^6 kWh/GWh = € -> €/GWh
    """
    return (
        (
            ld_bev_consumption() * ld_be_lco()
            + ld_fcev_consumption() * ld_fc_lco()
            + ld_fossil_consumption() * ld_ice_lco()
        )
        / (ld_ice_energy_usage() * diesel_lhv())
        * 10**6
        / sum_ld_rt()
    )


@component.add(
    name="LD BEV competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ld_ice_lco": 1, "ld_be_lco": 2, "ld_fc_lco": 1},
)
def ld_bev_competitiveness():
    return np.minimum(ld_ice_lco() / ld_be_lco(), ld_fc_lco() / ld_be_lco())


@component.add(
    name="LD BEV consumption",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_ld_bev_consumption": 1},
    other_deps={
        "_integ_ld_bev_consumption": {
            "initial": {"ld_rt_consumption": 1},
            "step": {"ld_bev_investment": 1, "ld_bev_decay": 1},
        }
    },
)
def ld_bev_consumption():
    """
    1.4% of the passenger cars in Europe in 2022 are electrical. The rest are fossil.
    """
    return _integ_ld_bev_consumption()


_integ_ld_bev_consumption = Integ(
    lambda: ld_bev_investment() - ld_bev_decay(),
    lambda: ld_rt_consumption() * 0.014,
    "_integ_ld_bev_consumption",
)


@component.add(
    name="LD BEV decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ld_bev_consumption": 1, "ld_lifetime": 1},
)
def ld_bev_decay():
    return ld_bev_consumption() / ld_lifetime()


@component.add(
    name="LD BEV imitators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ld_bev_investment_level": 1, "ld_rt_reinvestment": 1},
)
def ld_bev_imitators():
    return ld_bev_investment_level() * ld_rt_reinvestment()


@component.add(
    name="LD BEV inno switch",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_ld_bev_inno_switch": 1},
    other_deps={
        "_smooth_ld_bev_inno_switch": {
            "initial": {
                "ld_bev_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
            "step": {
                "ld_bev_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
        }
    },
)
def ld_bev_inno_switch():
    return _smooth_ld_bev_inno_switch()


_smooth_ld_bev_inno_switch = Smooth(
    lambda: if_then_else(
        ld_bev_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            ld_bev_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 2,
    lambda: if_then_else(
        ld_bev_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            ld_bev_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 3,
    "_smooth_ld_bev_inno_switch",
)


@component.add(
    name="LD BEV innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ld_rt_reinvestment": 1,
        "innovators": 1,
        "ld_bev_inno_switch": 1,
        "sum_ld_rt": 2,
        "ld_bev_consumption": 1,
    },
)
def ld_bev_innovators():
    return (
        ld_rt_reinvestment()
        * innovators()
        * ld_bev_inno_switch()
        * (sum_ld_rt() - ld_bev_consumption())
        / sum_ld_rt()
    )


@component.add(
    name="LD BEV investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ld_bev_imitators": 1, "ld_bev_innovators": 1},
)
def ld_bev_investment():
    return ld_bev_imitators() + ld_bev_innovators()


@component.add(
    name="LD BEV investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ld_rt_equalizer": 1, "ld_bev_level": 1},
)
def ld_bev_investment_level():
    return ld_rt_equalizer() * ld_bev_level()


@component.add(
    name="LD BEV level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "cross_innovation": 1,
        "ld_bev_competitiveness": 1,
        "ld_bev_consumption": 1,
        "sum_ld_rt": 1,
    },
)
def ld_bev_level():
    return (
        1
        / (1 + np.exp(slope() * (cross_innovation() - ld_bev_competitiveness())))
        * ld_bev_consumption()
        / sum_ld_rt()
    )


@component.add(
    name="LD FCEV competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ld_be_lco": 1, "ld_fc_lco": 2, "ld_ice_lco": 1},
)
def ld_fcev_competitiveness():
    return np.minimum(ld_be_lco() / ld_fc_lco(), ld_ice_lco() / ld_fc_lco())


@component.add(
    name="LD FCEV consumption",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_ld_fcev_consumption": 1},
    other_deps={
        "_integ_ld_fcev_consumption": {
            "initial": {},
            "step": {"ld_fcev_investment": 1, "ld_fcev_decay": 1},
        }
    },
)
def ld_fcev_consumption():
    return _integ_ld_fcev_consumption()


_integ_ld_fcev_consumption = Integ(
    lambda: ld_fcev_investment() - ld_fcev_decay(),
    lambda: 0,
    "_integ_ld_fcev_consumption",
)


@component.add(
    name="LD FCEV decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ld_fcev_consumption": 1, "ld_lifetime": 1},
)
def ld_fcev_decay():
    return ld_fcev_consumption() / ld_lifetime()


@component.add(
    name="LD FCEV imitators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ld_rt_reinvestment": 1, "ld_fcev_investment_level": 1},
)
def ld_fcev_imitators():
    return ld_rt_reinvestment() * ld_fcev_investment_level()


@component.add(
    name="LD FCEV inno switch",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_ld_fcev_inno_switch": 1},
    other_deps={
        "_smooth_ld_fcev_inno_switch": {
            "initial": {
                "ld_fcev_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
            "step": {
                "ld_fcev_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
        }
    },
)
def ld_fcev_inno_switch():
    return _smooth_ld_fcev_inno_switch()


_smooth_ld_fcev_inno_switch = Smooth(
    lambda: if_then_else(
        ld_fcev_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            ld_fcev_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 2,
    lambda: if_then_else(
        ld_fcev_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            ld_fcev_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 3,
    "_smooth_ld_fcev_inno_switch",
)


@component.add(
    name="LD FCEV innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ld_rt_reinvestment": 1,
        "innovators": 1,
        "ld_fcev_inno_switch": 1,
        "sum_ld_rt": 2,
        "ld_fcev_consumption": 1,
    },
)
def ld_fcev_innovators():
    return (
        ld_rt_reinvestment()
        * innovators()
        * ld_fcev_inno_switch()
        * (sum_ld_rt() - ld_fcev_consumption())
        / sum_ld_rt()
    )


@component.add(
    name="LD FCEV investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ld_fcev_imitators": 1, "ld_fcev_innovators": 1},
)
def ld_fcev_investment():
    return ld_fcev_imitators() + ld_fcev_innovators()


@component.add(
    name="LD FCEV investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ld_rt_equalizer": 1, "ld_fcev_level": 1},
)
def ld_fcev_investment_level():
    return ld_rt_equalizer() * ld_fcev_level()


@component.add(
    name="LD FCEV level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "ld_fcev_competitiveness": 1,
        "cross_innovation": 1,
        "ld_fcev_consumption": 1,
        "sum_ld_rt": 1,
    },
)
def ld_fcev_level():
    return (
        1
        / (1 + np.exp(slope() * (cross_innovation() - ld_fcev_competitiveness())))
        * ld_fcev_consumption()
        / sum_ld_rt()
    )


@component.add(
    name="LD Fossil competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ld_be_lco": 1, "ld_ice_lco": 2, "ld_fc_lco": 1},
)
def ld_fossil_competitiveness():
    return np.minimum(ld_be_lco() / ld_ice_lco(), ld_fc_lco() / ld_ice_lco())


@component.add(
    name="LD Fossil consumption",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_ld_fossil_consumption": 1},
    other_deps={
        "_integ_ld_fossil_consumption": {
            "initial": {"ld_rt_consumption": 1},
            "step": {"ld_fossil_investment": 1, "ld_fossil_decay": 1},
        }
    },
)
def ld_fossil_consumption():
    """
    1.4% of the passenger cars in Europe in 2022 are electrical. The rest are fossil.
    """
    return _integ_ld_fossil_consumption()


_integ_ld_fossil_consumption = Integ(
    lambda: ld_fossil_investment() - ld_fossil_decay(),
    lambda: ld_rt_consumption() * 0.986,
    "_integ_ld_fossil_consumption",
)


@component.add(
    name="LD Fossil decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ld_fossil_consumption": 1,
        "ld_lifetime": 1,
        "ld_fossil_early_decommission_rate": 1,
    },
)
def ld_fossil_decay():
    return ld_fossil_consumption() * (
        ld_fossil_early_decommission_rate() + 1 / ld_lifetime()
    )


@component.add(
    name="LD Fossil early decommission rate",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ld_fossil_competitiveness": 1},
)
def ld_fossil_early_decommission_rate():
    return 1 / (1 + np.exp(-5 * -ld_fossil_competitiveness())) * 0


@component.add(
    name="LD Fossil investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ld_fossil_investment_level": 1, "ld_rt_reinvestment": 1},
)
def ld_fossil_investment():
    return ld_fossil_investment_level() * ld_rt_reinvestment()


@component.add(
    name="LD Fossil investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ld_rt_equalizer": 1, "ld_fossil_level": 1},
)
def ld_fossil_investment_level():
    return ld_rt_equalizer() * ld_fossil_level()


@component.add(
    name="LD Fossil level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ice_car_ban": 1,
        "sum_ld_rt": 1,
        "ld_fossil_consumption": 1,
        "slope": 1,
        "ld_fossil_competitiveness": 1,
        "cross_conventional": 1,
    },
)
def ld_fossil_level():
    return if_then_else(
        ice_car_ban(),
        lambda: 0,
        lambda: 1
        / (1 + np.exp(slope() * (cross_conventional() - ld_fossil_competitiveness())))
        * ld_fossil_consumption()
        / sum_ld_rt(),
    )


@component.add(
    name="LD H2 price break",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ld_be_lco": 1,
        "ld_ice_lco": 1,
        "ld_fc_lco_without_h2": 1,
        "ld_fc_energy_usage": 1,
    },
)
def ld_h2_price_break():
    return (
        np.minimum(ld_be_lco(), ld_ice_lco()) - ld_fc_lco_without_h2()
    ) / ld_fc_energy_usage()


@component.add(
    name="LD ICE efficiency",
    units="percent",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ld_ice_efficiency():
    """
    Builds on assumption that the ICE car can drive 20 km/l, while the EV car can drive 5 km/kWh and has an assumed efficiency of 85%
    """
    return 0.32


@component.add(
    name="LD RT consumption",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"rt_energy_demand": 1, "light_duty_fraction": 1},
)
def ld_rt_consumption():
    return rt_energy_demand() * light_duty_fraction()


@component.add(
    name="LD RT equalizer",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ld_fossil_level": 1, "ld_fcev_level": 1, "ld_bev_level": 1},
)
def ld_rt_equalizer():
    return 1 / (ld_fossil_level() + ld_fcev_level() + ld_bev_level())


@component.add(
    name="LD RT reinvestment",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_ld_rt_reinvestment": 1},
    other_deps={
        "_integ_ld_rt_reinvestment": {
            "initial": {"ld_rt_consumption": 1, "ld_lifetime": 1},
            "step": {
                "demand_change_ld_rt": 1,
                "ld_bev_decay": 1,
                "ld_fcev_decay": 1,
                "ld_fossil_decay": 1,
                "ld_bev_investment": 1,
                "ld_fcev_investment": 1,
                "ld_fossil_investment": 1,
            },
        }
    },
)
def ld_rt_reinvestment():
    return _integ_ld_rt_reinvestment()


_integ_ld_rt_reinvestment = Integ(
    lambda: demand_change_ld_rt()
    + ld_bev_decay()
    + ld_fcev_decay()
    + ld_fossil_decay()
    - ld_bev_investment()
    - ld_fcev_investment()
    - ld_fossil_investment(),
    lambda: ld_rt_consumption() / ld_lifetime(),
    "_integ_ld_rt_reinvestment",
)


@component.add(
    name="light duty emissions",
    units="tCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ld_fossil_consumption": 1,
        "diesel_emission_factor": 1,
        "ld_bev_consumption": 1,
        "ld_ev_efficiency": 1,
        "charging_efficiency": 1,
        "electricity_emission_factor": 1,
        "ld_ice_efficiency": 1,
    },
)
def light_duty_emissions():
    return (
        ld_fossil_consumption() * diesel_emission_factor()
        + ld_bev_consumption()
        * ld_ice_efficiency()
        / (charging_efficiency() * ld_ev_efficiency())
        * electricity_emission_factor()
    ) * 10**6


@component.add(name="Light duty fraction", comp_type="Constant", comp_subtype="Normal")
def light_duty_fraction():
    """
    Fraction of road transport energy consumption which is light duty.
    """
    return 0.73


@component.add(
    name="light duty hydrogen demand",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ld_fcev_consumption": 1,
        "ld_ice_efficiency": 1,
        "ld_fcev_efficiency": 1,
        "h2_lhv": 1,
    },
)
def light_duty_hydrogen_demand():
    """
    GWh * MWh/GWh / MWh/t
    """
    return (
        ld_fcev_consumption()
        * ld_ice_efficiency()
        / ld_fcev_efficiency()
        * 1000
        / h2_lhv()
    )


@component.add(
    name="RT energy demand",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def rt_energy_demand():
    """
    1.56% increase per year compared to the base year (2019). Energy is denoted as total energy supplied to the wheels after ICE efficiency losses.
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
            2826790.0,
            2855560.0,
            2925860.0,
            2963340.0,
            2986900.0,
            3019350.0,
            3126610.0,
            3178780.0,
            3276960.0,
            3346050.0,
            3340730.0,
            3398480.0,
            3446660.0,
            3479300.0,
            3566350.0,
            3575440.0,
            3649610.0,
            3704130.0,
            3653790.0,
            3573480.0,
            3566740.0,
            3543890.0,
            3425970.0,
            3413450.0,
            3484900.0,
            3534240.0,
            3616960.0,
            3678130.0,
            3689730.0,
            3718680.0,
            3776690.0,
            3835610.0,
            3895440.0,
            3956210.0,
            4017930.0,
            4080610.0,
            4144270.0,
            4208920.0,
            4274580.0,
            4341260.0,
            4408980.0,
            4477760.0,
            4547620.0,
            4618560.0,
            4690610.0,
            4763780.0,
            4838100.0,
            4913570.0,
            4990220.0,
            5068070.0,
            5147130.0,
            5227430.0,
            5308980.0,
            5391800.0,
            5475910.0,
            5561330.0,
            5648090.0,
            5736200.0,
            5825680.0,
            5916560.0,
            6008860.0,
        ],
    )


@component.add(
    name="sum LD RT",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ld_fossil_consumption": 1,
        "ld_fcev_consumption": 1,
        "ld_bev_consumption": 1,
    },
)
def sum_ld_rt():
    return ld_fossil_consumption() + ld_fcev_consumption() + ld_bev_consumption()
