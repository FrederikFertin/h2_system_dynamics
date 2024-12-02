"""
Module international_aviation
Translated using PySD version 3.14.0
"""

@component.add(
    name="Bio kerosene competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"synkero_cost": 1, "biokero_cost": 2, "jetfuel_cost": 1},
)
def bio_kerosene_competitiveness():
    return np.minimum(synkero_cost() / biokero_cost(), jetfuel_cost() / biokero_cost())


@component.add(
    name="Bio kerosene consumption",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_bio_kerosene_consumption": 1},
    other_deps={
        "_integ_bio_kerosene_consumption": {
            "initial": {},
            "step": {"bio_kerosene_investment": 1, "bio_kerosene_decay": 1},
        }
    },
)
def bio_kerosene_consumption():
    return _integ_bio_kerosene_consumption()


_integ_bio_kerosene_consumption = Integ(
    lambda: bio_kerosene_investment() - bio_kerosene_decay(),
    lambda: 0,
    "_integ_bio_kerosene_consumption",
)


@component.add(
    name="Bio kerosene decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"bio_kerosene_consumption": 1, "jetfuel_lockin_period": 1},
)
def bio_kerosene_decay():
    return bio_kerosene_consumption() / jetfuel_lockin_period()


@component.add(
    name="Bio kerosene imitators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "international_aviation_reinvestment": 1,
        "bio_kerosene_investment_level": 1,
    },
)
def bio_kerosene_imitators():
    return international_aviation_reinvestment() * bio_kerosene_investment_level()


@component.add(
    name="Bio kerosene inno switch",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_bio_kerosene_inno_switch": 1},
    other_deps={
        "_smooth_bio_kerosene_inno_switch": {
            "initial": {
                "bio_kerosene_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
            "step": {
                "bio_kerosene_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
        }
    },
)
def bio_kerosene_inno_switch():
    return _smooth_bio_kerosene_inno_switch()


_smooth_bio_kerosene_inno_switch = Smooth(
    lambda: if_then_else(
        bio_kerosene_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            bio_kerosene_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 2,
    lambda: if_then_else(
        bio_kerosene_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            bio_kerosene_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 3,
    "_smooth_bio_kerosene_inno_switch",
)


@component.add(
    name="Bio kerosene innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "international_aviation_reinvestment": 1,
        "innovators": 1,
        "bio_kerosene_inno_switch": 1,
        "bio_kerosene_consumption": 1,
        "sum_international_aviation": 2,
    },
)
def bio_kerosene_innovators():
    return (
        international_aviation_reinvestment()
        * innovators()
        * bio_kerosene_inno_switch()
        * (sum_international_aviation() - bio_kerosene_consumption())
        / sum_international_aviation()
    )


@component.add(
    name="Bio kerosene investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"bio_kerosene_imitators": 1, "bio_kerosene_innovators": 1},
)
def bio_kerosene_investment():
    return bio_kerosene_imitators() + bio_kerosene_innovators()


@component.add(
    name="Bio kerosene investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"international_aviation_equalizer": 1, "bio_kerosene_level": 1},
)
def bio_kerosene_investment_level():
    return international_aviation_equalizer() * bio_kerosene_level()


@component.add(
    name="Bio kerosene level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "bio_kerosene_competitiveness": 1,
        "cross": 1,
        "bio_kerosene_consumption": 1,
        "sum_international_aviation": 1,
    },
)
def bio_kerosene_level():
    return (
        1
        / (1 + np.exp(slope() * (cross() - bio_kerosene_competitiveness())))
        * bio_kerosene_consumption()
        / sum_international_aviation()
    )


@component.add(
    name="ctrl international aviation",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "k_p": 1,
        "error_international_aviation": 1,
        "errorint_international_aviation": 1,
    },
)
def ctrl_international_aviation():
    return k_p() * error_international_aviation() + errorint_international_aviation()


@component.add(
    name="demand change international aviation",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ctrl_international_aviation": 1},
)
def demand_change_international_aviation():
    return ctrl_international_aviation()


@component.add(
    name="error international aviation",
    units="e",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "international_aviation_consumption": 1,
        "sum_international_aviation": 1,
    },
)
def error_international_aviation():
    return international_aviation_consumption() - sum_international_aviation()


@component.add(
    name="errorint international aviation",
    units="e",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_errorint_international_aviation": 1},
    other_deps={
        "_integ_errorint_international_aviation": {
            "initial": {"international_aviation_consumption": 1},
            "step": {"k_i": 1, "error_international_aviation": 1},
        }
    },
)
def errorint_international_aviation():
    return _integ_errorint_international_aviation()


_integ_errorint_international_aviation = Integ(
    lambda: k_i() * error_international_aviation(),
    lambda: international_aviation_consumption() * 0.0179,
    "_integ_errorint_international_aviation",
)


@component.add(
    name="international aviation average cost",
    units="€/GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "bio_kerosene_consumption": 1,
        "biokero_cost": 1,
        "jetfuel_consumption": 1,
        "jetfuel_cost": 1,
        "synkero_cost": 1,
        "syn_kerosene_consumption": 1,
        "sum_international_aviation": 1,
    },
)
def international_aviation_average_cost():
    """
    €/GWh of jetfuel input equivalent. (Fuel cost only)
    """
    return (
        (
            bio_kerosene_consumption() * biokero_cost()
            + jetfuel_consumption() * jetfuel_cost()
            + syn_kerosene_consumption() * synkero_cost()
        )
        * 3.6
        * 10**6
        / sum_international_aviation()
    )


@component.add(
    name="international aviation BioKero hydrogen demand",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"bio_kerosene_consumption": 1, "biokero_h2_usage": 1, "h2_lhv": 1},
)
def international_aviation_biokero_hydrogen_demand():
    """
    Convert from GWh jetfuel to GWh G2 - then to MWh H2 - then to tons H2
    """
    return bio_kerosene_consumption() * biokero_h2_usage() * 1000 / h2_lhv()


@component.add(
    name="international aviation biomass demand",
    units="GWh Biomass",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "bio_kerosene_consumption": 1,
        "biokero_fraction": 1,
        "biokero_biomass_usage": 1,
    },
)
def international_aviation_biomass_demand():
    """
    Convert to GWh biomass
    """
    return bio_kerosene_consumption() / biokero_fraction() * biokero_biomass_usage()


@component.add(
    name="international aviation consumption",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def international_aviation_consumption():
    """
    Considering an annual growth of 1,2% from year 2019.
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
            295302,
            286815,
            307477,
            322972,
            340650,
            356308,
            370663,
            387639,
            411181,
            442206,
            463700,
            453780,
            447489,
            454576,
            486965,
            512323,
            533393,
            548726,
            551816,
            509099,
            508465,
            525469,
            516769,
            519055,
            524542,
            541947,
            563051,
            606262,
            632335,
            641196,
            648890,
            656677,
            664557,
            672531,
            680602,
            688769,
            697034,
            705399,
            713863,
            722430,
            731099,
            739872,
            748751,
            757736,
            766828,
            776030,
            785343,
            794767,
            804304,
            813956,
            823723,
            833608,
            843611,
            853734,
            863979,
            874347,
            884839,
            895457,
            906203,
            917077,
            928082,
        ],
    )


@component.add(
    name="international aviation emissions",
    units="tCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"jetfuel_emission_factor": 1, "jetfuel_consumption": 1},
)
def international_aviation_emissions():
    return jetfuel_emission_factor() * jetfuel_consumption() * 3600


@component.add(
    name="international aviation equalizer",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"jetfuel_level": 1, "bio_kerosene_level": 1, "syn_kerosene_level": 1},
)
def international_aviation_equalizer():
    return 1 / (jetfuel_level() + bio_kerosene_level() + syn_kerosene_level())


@component.add(
    name="international aviation hydrogen demand",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "international_aviation_synkero_hydrogen_demand": 1,
        "international_aviation_biokero_hydrogen_demand": 1,
    },
)
def international_aviation_hydrogen_demand():
    """
    Convert from GWh jetfuel to GWh G2 - then to MWh H2 - then to tons H2
    """
    return (
        international_aviation_synkero_hydrogen_demand()
        + international_aviation_biokero_hydrogen_demand()
    )


@component.add(
    name="international aviation reinvestment",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_international_aviation_reinvestment": 1},
    other_deps={
        "_integ_international_aviation_reinvestment": {
            "initial": {
                "international_aviation_consumption": 1,
                "jetfuel_lockin_period": 1,
            },
            "step": {
                "demand_change_international_aviation": 1,
                "jetfuel_decay": 1,
                "bio_kerosene_decay": 1,
                "syn_kerosene_decay": 1,
                "jetfuel_investment": 1,
                "bio_kerosene_investment": 1,
                "syn_kerosene_investment": 1,
            },
        }
    },
)
def international_aviation_reinvestment():
    return _integ_international_aviation_reinvestment()


_integ_international_aviation_reinvestment = Integ(
    lambda: demand_change_international_aviation()
    + jetfuel_decay()
    + bio_kerosene_decay()
    + syn_kerosene_decay()
    - jetfuel_investment()
    - bio_kerosene_investment()
    - syn_kerosene_investment(),
    lambda: international_aviation_consumption() / jetfuel_lockin_period(),
    "_integ_international_aviation_reinvestment",
)


@component.add(
    name="international aviation SynKero hydrogen demand",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"syn_kerosene_consumption": 1, "synkero_h2_usage": 1, "h2_lhv": 1},
)
def international_aviation_synkero_hydrogen_demand():
    """
    Convert from GWh jetfuel to GWh G2 - then to MWh H2 - then to tons H2
    """
    return syn_kerosene_consumption() * synkero_h2_usage() * 1000 / h2_lhv()


@component.add(
    name="Jetfuel competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"synkero_cost": 1, "jetfuel_cost": 2, "biokero_cost": 1},
)
def jetfuel_competitiveness():
    return np.minimum(synkero_cost() / jetfuel_cost(), biokero_cost() / jetfuel_cost())


@component.add(
    name="Jetfuel consumption",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_jetfuel_consumption": 1},
    other_deps={
        "_integ_jetfuel_consumption": {
            "initial": {"international_aviation_consumption": 1},
            "step": {"jetfuel_investment": 1, "jetfuel_decay": 1},
        }
    },
)
def jetfuel_consumption():
    return _integ_jetfuel_consumption()


_integ_jetfuel_consumption = Integ(
    lambda: jetfuel_investment() - jetfuel_decay(),
    lambda: international_aviation_consumption(),
    "_integ_jetfuel_consumption",
)


@component.add(
    name="Jetfuel decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "jetfuel_consumption": 1,
        "jetfuel_early_decommission_rate": 1,
        "jetfuel_lockin_period": 1,
    },
)
def jetfuel_decay():
    return jetfuel_consumption() * (
        jetfuel_early_decommission_rate() + 1 / jetfuel_lockin_period()
    )


@component.add(
    name="Jetfuel early decommission rate",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"jetfuel_competitiveness": 1},
)
def jetfuel_early_decommission_rate():
    return 1 / (1 + np.exp(-5 * -jetfuel_competitiveness())) * 0


@component.add(
    name="Jetfuel investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "jetfuel_investment_level": 1,
        "international_aviation_reinvestment": 1,
    },
)
def jetfuel_investment():
    return jetfuel_investment_level() * international_aviation_reinvestment()


@component.add(
    name="Jetfuel investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"international_aviation_equalizer": 1, "jetfuel_level": 1},
)
def jetfuel_investment_level():
    return international_aviation_equalizer() * jetfuel_level()


@component.add(
    name="Jetfuel level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "cross": 1,
        "jetfuel_competitiveness": 1,
        "jetfuel_consumption": 1,
        "sum_international_aviation": 1,
    },
)
def jetfuel_level():
    return (
        1
        / (1 + np.exp(slope() * (cross() - jetfuel_competitiveness())))
        * jetfuel_consumption()
        / sum_international_aviation()
    )


@component.add(
    name="jetfuel lockin period",
    units="years",
    comp_type="Constant",
    comp_subtype="Normal",
)
def jetfuel_lockin_period():
    return 5


@component.add(
    name="sum international aviation",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "jetfuel_consumption": 1,
        "bio_kerosene_consumption": 1,
        "syn_kerosene_consumption": 1,
    },
)
def sum_international_aviation():
    return (
        jetfuel_consumption() + bio_kerosene_consumption() + syn_kerosene_consumption()
    )


@component.add(
    name="Syn kerosene competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"jetfuel_cost": 1, "synkero_cost": 2, "biokero_cost": 1},
)
def syn_kerosene_competitiveness():
    return np.minimum(jetfuel_cost() / synkero_cost(), biokero_cost() / synkero_cost())


@component.add(
    name="Syn kerosene consumption",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_syn_kerosene_consumption": 1},
    other_deps={
        "_integ_syn_kerosene_consumption": {
            "initial": {},
            "step": {"syn_kerosene_investment": 1, "syn_kerosene_decay": 1},
        }
    },
)
def syn_kerosene_consumption():
    return _integ_syn_kerosene_consumption()


_integ_syn_kerosene_consumption = Integ(
    lambda: syn_kerosene_investment() - syn_kerosene_decay(),
    lambda: 0,
    "_integ_syn_kerosene_consumption",
)


@component.add(
    name="Syn kerosene decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"syn_kerosene_consumption": 1, "jetfuel_lockin_period": 1},
)
def syn_kerosene_decay():
    return syn_kerosene_consumption() / jetfuel_lockin_period()


@component.add(
    name="Syn kerosene imitators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "international_aviation_reinvestment": 1,
        "syn_kerosene_investment_level": 1,
    },
)
def syn_kerosene_imitators():
    return international_aviation_reinvestment() * syn_kerosene_investment_level()


@component.add(
    name="Syn kerosene inno switch",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_syn_kerosene_inno_switch": 1},
    other_deps={
        "_smooth_syn_kerosene_inno_switch": {
            "initial": {
                "syn_kerosene_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
            "step": {
                "syn_kerosene_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
        }
    },
)
def syn_kerosene_inno_switch():
    return _smooth_syn_kerosene_inno_switch()


_smooth_syn_kerosene_inno_switch = Smooth(
    lambda: if_then_else(
        syn_kerosene_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            syn_kerosene_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 2,
    lambda: if_then_else(
        syn_kerosene_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            syn_kerosene_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 3,
    "_smooth_syn_kerosene_inno_switch",
)


@component.add(
    name="Syn kerosene innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "international_aviation_reinvestment": 1,
        "innovators": 1,
        "syn_kerosene_inno_switch": 1,
        "sum_international_aviation": 2,
        "syn_kerosene_consumption": 1,
    },
)
def syn_kerosene_innovators():
    return (
        international_aviation_reinvestment()
        * innovators()
        * syn_kerosene_inno_switch()
        * (sum_international_aviation() - syn_kerosene_consumption())
        / sum_international_aviation()
    )


@component.add(
    name="Syn kerosene investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"syn_kerosene_innovators": 1, "syn_kerosene_imitators": 1},
)
def syn_kerosene_investment():
    return syn_kerosene_innovators() + syn_kerosene_imitators()


@component.add(
    name="Syn kerosene investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"international_aviation_equalizer": 1, "syn_kerosene_level": 1},
)
def syn_kerosene_investment_level():
    return international_aviation_equalizer() * syn_kerosene_level()


@component.add(
    name="Syn kerosene level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "cross": 1,
        "syn_kerosene_competitiveness": 1,
        "syn_kerosene_consumption": 1,
        "sum_international_aviation": 1,
    },
)
def syn_kerosene_level():
    return (
        1
        / (1 + np.exp(slope() * (cross() - syn_kerosene_competitiveness())))
        * syn_kerosene_consumption()
        / sum_international_aviation()
    )
