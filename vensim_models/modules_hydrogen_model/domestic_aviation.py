"""
Module domestic_aviation
Translated using PySD version 3.14.0
"""

@component.add(
    name="Bio kerosene competitiveness dom",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "synkero_propulsion_cost": 1,
        "biokero_propulsion_cost": 3,
        "jetfuel_propulsion_cost": 1,
        "h2_propulsion_cost_aviation": 1,
    },
)
def bio_kerosene_competitiveness_dom():
    return np.minimum(
        np.minimum(
            synkero_propulsion_cost() / biokero_propulsion_cost(),
            jetfuel_propulsion_cost() / biokero_propulsion_cost(),
        ),
        h2_propulsion_cost_aviation() / biokero_propulsion_cost(),
    )


@component.add(
    name="Bio kerosene consumption dom",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_bio_kerosene_consumption_dom": 1},
    other_deps={
        "_integ_bio_kerosene_consumption_dom": {
            "initial": {},
            "step": {"bio_kerosene_investment_dom": 1, "bio_kerosene_decay_dom": 1},
        }
    },
)
def bio_kerosene_consumption_dom():
    return _integ_bio_kerosene_consumption_dom()


_integ_bio_kerosene_consumption_dom = Integ(
    lambda: bio_kerosene_investment_dom() - bio_kerosene_decay_dom(),
    lambda: 0,
    "_integ_bio_kerosene_consumption_dom",
)


@component.add(
    name="Bio kerosene decay dom",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"bio_kerosene_consumption_dom": 1, "jetfuel_lockin_period": 1},
)
def bio_kerosene_decay_dom():
    return bio_kerosene_consumption_dom() / jetfuel_lockin_period()


@component.add(
    name="Bio kerosene imitators dom",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_aviation_reinvestment": 1,
        "bio_kerosene_investment_level_dom": 1,
    },
)
def bio_kerosene_imitators_dom():
    return domestic_aviation_reinvestment() * bio_kerosene_investment_level_dom()


@component.add(
    name="Bio kerosene inno switch dom",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_bio_kerosene_inno_switch_dom": 1},
    other_deps={
        "_smooth_bio_kerosene_inno_switch_dom": {
            "initial": {
                "bio_kerosene_competitiveness_dom": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
            "step": {
                "bio_kerosene_competitiveness_dom": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
        }
    },
)
def bio_kerosene_inno_switch_dom():
    return _smooth_bio_kerosene_inno_switch_dom()


_smooth_bio_kerosene_inno_switch_dom = Smooth(
    lambda: if_then_else(
        bio_kerosene_competitiveness_dom() > inno_switch_level(),
        lambda: if_then_else(
            bio_kerosene_competitiveness_dom() > early_switch_level(),
            lambda: 3,
            lambda: 1,
        ),
        lambda: 0,
    ),
    lambda: 2,
    lambda: if_then_else(
        bio_kerosene_competitiveness_dom() > inno_switch_level(),
        lambda: if_then_else(
            bio_kerosene_competitiveness_dom() > early_switch_level(),
            lambda: 3,
            lambda: 1,
        ),
        lambda: 0,
    ),
    lambda: 3,
    "_smooth_bio_kerosene_inno_switch_dom",
)


@component.add(
    name="Bio kerosene innovators dom",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_aviation_reinvestment": 1,
        "innovators": 1,
        "bio_kerosene_inno_switch_dom": 1,
        "bio_kerosene_consumption_dom": 1,
        "sum_domestic_aviation": 2,
    },
)
def bio_kerosene_innovators_dom():
    return (
        domestic_aviation_reinvestment()
        * innovators()
        * bio_kerosene_inno_switch_dom()
        * (sum_domestic_aviation() - bio_kerosene_consumption_dom())
        / sum_domestic_aviation()
    )


@component.add(
    name="Bio kerosene investment dom",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"bio_kerosene_imitators_dom": 1, "bio_kerosene_innovators_dom": 1},
)
def bio_kerosene_investment_dom():
    return bio_kerosene_imitators_dom() + bio_kerosene_innovators_dom()


@component.add(
    name="Bio kerosene investment level dom",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dom_aviation_equalizer_dom": 1, "bio_kerosene_level_dom": 1},
)
def bio_kerosene_investment_level_dom():
    return dom_aviation_equalizer_dom() * bio_kerosene_level_dom()


@component.add(
    name="Bio kerosene level dom",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "cross": 1,
        "bio_kerosene_competitiveness_dom": 1,
        "bio_kerosene_consumption_dom": 1,
        "sum_domestic_aviation": 1,
    },
)
def bio_kerosene_level_dom():
    return (
        1
        / (1 + np.exp(slope() * (cross() - bio_kerosene_competitiveness_dom())))
        * bio_kerosene_consumption_dom()
        / sum_domestic_aviation()
    )


@component.add(
    name="ctrl domestic aviation",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "k_p": 1,
        "error_domestic_aviation": 1,
        "errorint_domestic_aviation": 1,
    },
)
def ctrl_domestic_aviation():
    return k_p() * error_domestic_aviation() + errorint_domestic_aviation()


@component.add(
    name="demand change domestic aviation",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ctrl_domestic_aviation": 1},
)
def demand_change_domestic_aviation():
    return ctrl_domestic_aviation()


@component.add(
    name="dom aviation equalizer dom",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "jetfuel_level_dom": 1,
        "bio_kerosene_level_dom": 1,
        "syn_kerosene_level_dom": 1,
        "hydrogen_level_dom": 1,
    },
)
def dom_aviation_equalizer_dom():
    return 1 / (
        jetfuel_level_dom()
        + bio_kerosene_level_dom()
        + syn_kerosene_level_dom()
        + hydrogen_level_dom()
    )


@component.add(
    name="domestic aviation average cost",
    units="€/GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hydrogen_consumption_dom": 1,
        "h2_propulsion_cost_aviation": 1,
        "bio_kerosene_consumption_dom": 1,
        "biokero_propulsion_cost": 1,
        "jetfuel_propulsion_cost": 1,
        "jetfuel_consumption_dom": 1,
        "synkero_propulsion_cost": 1,
        "syn_kerosene_consumption_dom": 1,
        "jet_engine_efficiency": 1,
        "sum_domestic_aviation": 1,
    },
)
def domestic_aviation_average_cost():
    """
    €/GWh of jetfuel input equivalent. (Fuel cost + O&M).
    """
    return (
        (
            hydrogen_consumption_dom() * h2_propulsion_cost_aviation()
            + bio_kerosene_consumption_dom() * biokero_propulsion_cost()
            + jetfuel_consumption_dom() * jetfuel_propulsion_cost()
            + syn_kerosene_consumption_dom() * synkero_propulsion_cost()
        )
        * jet_engine_efficiency()
        * 3.6
        * 10**6
        / sum_domestic_aviation()
    )


@component.add(
    name="domestic aviation BioKero hydrogen demand",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"bio_kerosene_consumption_dom": 1, "biokero_h2_usage": 1, "h2_lhv": 1},
)
def domestic_aviation_biokero_hydrogen_demand():
    """
    Convert from GWh to GJ, then from GJ to tons fuel, then from tons fuel to tons H2. Example 1: MeOH cons. [GWh] * 3600 [GJ/GWh] / 19.9 [GJ/t] / 15.7 [t MeOH/t H2] Example 2: NH3 cons. [GWh] * 3600 [GJ/GWh] / 18.6 [GJ/t] / 5.56 [t NH3/t H2]
    """
    return bio_kerosene_consumption_dom() * biokero_h2_usage() * 1000 / h2_lhv()


@component.add(
    name="domestic aviation biomass demand",
    units="GWh Biomass",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "bio_kerosene_consumption_dom": 1,
        "biokero_fraction": 1,
        "biokero_biomass_usage": 1,
    },
)
def domestic_aviation_biomass_demand():
    """
    Convert from GWh bio-Kerosene to GWh biomass
    """
    return bio_kerosene_consumption_dom() / biokero_fraction() * biokero_biomass_usage()


@component.add(
    name="domestic aviation consumption",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def domestic_aviation_consumption():
    """
    Considering an annual growth of 1,2% from year 2019. Consumption is amount of jetfuel used. Pre efficiency losses.
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
            64403.4,
            60410.3,
            60537.9,
            58822.8,
            55965.2,
            58015.1,
            62231.0,
            66230.6,
            70683.2,
            74366.6,
            78672.6,
            76667.4,
            72057.9,
            73415.2,
            76228.9,
            80822.1,
            82565.6,
            86139.5,
            83828.4,
            76672.3,
            78203.7,
            82852.8,
            77511.0,
            74449.5,
            74976.4,
            77159.7,
            80670.2,
            84531.2,
            86628.5,
            90415.1,
            91500.1,
            92598.1,
            93709.2,
            94833.7,
            95971.8,
            97123.4,
            98288.9,
            99468.4,
            100662.0,
            101870.0,
            103092.0,
            104329.0,
            105581.0,
            106848.0,
            108131.0,
            109428.0,
            110741.0,
            112070.0,
            113415.0,
            114776.0,
            116153.0,
            117547.0,
            118958.0,
            120385.0,
            121830.0,
            123292.0,
            124771.0,
            126269.0,
            127784.0,
            129317.0,
            130869.0,
        ],
    )


@component.add(
    name="domestic aviation emissions",
    units="tCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"jetfuel_emission_factor": 1, "jetfuel_consumption_dom": 1},
)
def domestic_aviation_emissions():
    return jetfuel_emission_factor() * jetfuel_consumption_dom() * 3600


@component.add(
    name="domestic aviation FC hydrogen demand",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hydrogen_consumption_dom": 1,
        "jet_engine_efficiency": 1,
        "hydrogen_fuel_cell_efficiency": 1,
        "h2_lhv": 1,
    },
)
def domestic_aviation_fc_hydrogen_demand():
    """
    Convert from GWh to GJ, then from GJ to tons fuel, then from tons fuel to tons H2. Example 1: MeOH cons. [GWh] * 3600 [GJ/GWh] / 19.9 [GJ/t] / 15.7 [t MeOH/t H2] Example 2: NH3 cons. [GWh] * 3600 [GJ/GWh] / 18.6 [GJ/t] / 5.56 [t NH3/t H2]
    """
    return (
        hydrogen_consumption_dom()
        * jet_engine_efficiency()
        / hydrogen_fuel_cell_efficiency()
        * 1000
        / h2_lhv()
    )


@component.add(
    name="domestic aviation hydrogen demand",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_aviation_biokero_hydrogen_demand": 1,
        "domestic_aviation_fc_hydrogen_demand": 1,
        "domestic_aviation_synkero_hydrogen_demand": 1,
    },
)
def domestic_aviation_hydrogen_demand():
    """
    Convert from GWh to GJ, then from GJ to tons fuel, then from tons fuel to tons H2. Example 1: MeOH cons. [GWh] * 3600 [GJ/GWh] / 19.9 [GJ/t] / 15.7 [t MeOH/t H2] Example 2: NH3 cons. [GWh] * 3600 [GJ/GWh] / 18.6 [GJ/t] / 5.56 [t NH3/t H2]
    """
    return (
        domestic_aviation_biokero_hydrogen_demand()
        + domestic_aviation_fc_hydrogen_demand()
        + domestic_aviation_synkero_hydrogen_demand()
    )


@component.add(
    name="domestic aviation reinvestment",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_domestic_aviation_reinvestment": 1},
    other_deps={
        "_integ_domestic_aviation_reinvestment": {
            "initial": {"domestic_aviation_consumption": 1, "jetfuel_lockin_period": 1},
            "step": {
                "bio_kerosene_decay_dom": 1,
                "demand_change_domestic_aviation": 1,
                "hydrogen_decay_dom": 1,
                "jetfuel_decay_dom": 1,
                "syn_kerosene_decay_dom": 1,
                "bio_kerosene_investment_dom": 1,
                "hydrogen_investment_dom": 1,
                "jetfuel_investment_dom": 1,
                "syn_kerosene_investment_dom": 1,
            },
        }
    },
)
def domestic_aviation_reinvestment():
    return _integ_domestic_aviation_reinvestment()


_integ_domestic_aviation_reinvestment = Integ(
    lambda: bio_kerosene_decay_dom()
    + demand_change_domestic_aviation()
    + hydrogen_decay_dom()
    + jetfuel_decay_dom()
    + syn_kerosene_decay_dom()
    - bio_kerosene_investment_dom()
    - hydrogen_investment_dom()
    - jetfuel_investment_dom()
    - syn_kerosene_investment_dom(),
    lambda: domestic_aviation_consumption() / jetfuel_lockin_period(),
    "_integ_domestic_aviation_reinvestment",
)


@component.add(
    name="domestic aviation SynKero hydrogen demand",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"syn_kerosene_consumption_dom": 1, "synkero_h2_usage": 1, "h2_lhv": 1},
)
def domestic_aviation_synkero_hydrogen_demand():
    """
    Convert from GWh to GJ, then from GJ to tons fuel, then from tons fuel to tons H2. Example 1: MeOH cons. [GWh] * 3600 [GJ/GWh] / 19.9 [GJ/t] / 15.7 [t MeOH/t H2] Example 2: NH3 cons. [GWh] * 3600 [GJ/GWh] / 18.6 [GJ/t] / 5.56 [t NH3/t H2]
    """
    return syn_kerosene_consumption_dom() * synkero_h2_usage() * 1000 / h2_lhv()


@component.add(
    name="error domestic aviation",
    units="e",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"domestic_aviation_consumption": 1, "sum_domestic_aviation": 1},
)
def error_domestic_aviation():
    return domestic_aviation_consumption() - sum_domestic_aviation()


@component.add(
    name="errorint domestic aviation",
    units="e",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_errorint_domestic_aviation": 1},
    other_deps={
        "_integ_errorint_domestic_aviation": {
            "initial": {"domestic_aviation_consumption": 1},
            "step": {"k_i": 1, "error_domestic_aviation": 1},
        }
    },
)
def errorint_domestic_aviation():
    return _integ_errorint_domestic_aviation()


_integ_errorint_domestic_aviation = Integ(
    lambda: k_i() * error_domestic_aviation(),
    lambda: domestic_aviation_consumption() * 0.0179,
    "_integ_errorint_domestic_aviation",
)


@component.add(
    name="Hydrogen competitiveness dom",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "synkero_propulsion_cost": 1,
        "h2_propulsion_cost_aviation": 3,
        "jetfuel_propulsion_cost": 1,
        "biokero_propulsion_cost": 1,
    },
)
def hydrogen_competitiveness_dom():
    return np.minimum(
        np.minimum(
            synkero_propulsion_cost() / h2_propulsion_cost_aviation(),
            jetfuel_propulsion_cost() / h2_propulsion_cost_aviation(),
        ),
        biokero_propulsion_cost() / h2_propulsion_cost_aviation(),
    )


@component.add(
    name="Hydrogen consumption dom",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_hydrogen_consumption_dom": 1},
    other_deps={
        "_integ_hydrogen_consumption_dom": {
            "initial": {},
            "step": {"hydrogen_investment_dom": 1, "hydrogen_decay_dom": 1},
        }
    },
)
def hydrogen_consumption_dom():
    return _integ_hydrogen_consumption_dom()


_integ_hydrogen_consumption_dom = Integ(
    lambda: hydrogen_investment_dom() - hydrogen_decay_dom(),
    lambda: 0,
    "_integ_hydrogen_consumption_dom",
)


@component.add(
    name="Hydrogen decay dom",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hydrogen_consumption_dom": 1, "jetfuel_lockin_period": 1},
)
def hydrogen_decay_dom():
    return hydrogen_consumption_dom() / jetfuel_lockin_period()


@component.add(
    name="Hydrogen imitators dom",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_aviation_reinvestment": 1,
        "hydrogen_investment_level_dom": 1,
    },
)
def hydrogen_imitators_dom():
    return domestic_aviation_reinvestment() * hydrogen_investment_level_dom()


@component.add(
    name="Hydrogen inno switch dom",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_hydrogen_inno_switch_dom": 1},
    other_deps={
        "_smooth_hydrogen_inno_switch_dom": {
            "initial": {
                "hydrogen_competitiveness_dom": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
            "step": {
                "hydrogen_competitiveness_dom": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
        }
    },
)
def hydrogen_inno_switch_dom():
    return _smooth_hydrogen_inno_switch_dom()


_smooth_hydrogen_inno_switch_dom = Smooth(
    lambda: if_then_else(
        hydrogen_competitiveness_dom() > inno_switch_level(),
        lambda: if_then_else(
            hydrogen_competitiveness_dom() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 2,
    lambda: if_then_else(
        hydrogen_competitiveness_dom() > inno_switch_level(),
        lambda: if_then_else(
            hydrogen_competitiveness_dom() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 3,
    "_smooth_hydrogen_inno_switch_dom",
)


@component.add(
    name="Hydrogen innovators dom",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_aviation_reinvestment": 1,
        "innovators": 1,
        "hydrogen_inno_switch_dom": 1,
        "sum_domestic_aviation": 2,
        "hydrogen_consumption_dom": 1,
    },
)
def hydrogen_innovators_dom():
    return (
        domestic_aviation_reinvestment()
        * innovators()
        * hydrogen_inno_switch_dom()
        * (sum_domestic_aviation() - hydrogen_consumption_dom())
        / sum_domestic_aviation()
    )


@component.add(
    name="Hydrogen investment dom",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hydrogen_imitators_dom": 1, "hydrogen_innovators_dom": 1},
)
def hydrogen_investment_dom():
    return hydrogen_imitators_dom() + hydrogen_innovators_dom()


@component.add(
    name="Hydrogen investment level dom",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dom_aviation_equalizer_dom": 1, "hydrogen_level_dom": 1},
)
def hydrogen_investment_level_dom():
    return dom_aviation_equalizer_dom() * hydrogen_level_dom()


@component.add(
    name="Hydrogen level dom",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "hydrogen_competitiveness_dom": 1,
        "cross": 1,
        "hydrogen_consumption_dom": 1,
        "sum_domestic_aviation": 1,
    },
)
def hydrogen_level_dom():
    return (
        1
        / (1 + np.exp(slope() * (cross() - hydrogen_competitiveness_dom())))
        * hydrogen_consumption_dom()
        / sum_domestic_aviation()
    )


@component.add(
    name="Jetfuel competitiveness dom",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "synkero_propulsion_cost": 1,
        "jetfuel_propulsion_cost": 3,
        "biokero_propulsion_cost": 1,
        "h2_propulsion_cost_aviation": 1,
    },
)
def jetfuel_competitiveness_dom():
    return np.minimum(
        np.minimum(
            synkero_propulsion_cost() / jetfuel_propulsion_cost(),
            biokero_propulsion_cost() / jetfuel_propulsion_cost(),
        ),
        h2_propulsion_cost_aviation() / jetfuel_propulsion_cost(),
    )


@component.add(
    name="Jetfuel consumption dom",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_jetfuel_consumption_dom": 1},
    other_deps={
        "_integ_jetfuel_consumption_dom": {
            "initial": {"domestic_aviation_consumption": 1},
            "step": {"jetfuel_investment_dom": 1, "jetfuel_decay_dom": 1},
        }
    },
)
def jetfuel_consumption_dom():
    return _integ_jetfuel_consumption_dom()


_integ_jetfuel_consumption_dom = Integ(
    lambda: jetfuel_investment_dom() - jetfuel_decay_dom(),
    lambda: domestic_aviation_consumption(),
    "_integ_jetfuel_consumption_dom",
)


@component.add(
    name="Jetfuel decay dom",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "jetfuel_consumption_dom": 1,
        "jetfuel_lockin_period": 1,
        "jetfuel_early_decommission_rate_dom": 1,
    },
)
def jetfuel_decay_dom():
    return jetfuel_consumption_dom() * (
        jetfuel_early_decommission_rate_dom() + 1 / jetfuel_lockin_period()
    )


@component.add(
    name="Jetfuel early decommission rate dom",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"jetfuel_competitiveness_dom": 1},
)
def jetfuel_early_decommission_rate_dom():
    return 1 / (1 + np.exp(-5 * -jetfuel_competitiveness_dom())) * 0


@component.add(
    name="Jetfuel investment dom",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"jetfuel_investment_level_dom": 1, "domestic_aviation_reinvestment": 1},
)
def jetfuel_investment_dom():
    return jetfuel_investment_level_dom() * domestic_aviation_reinvestment()


@component.add(
    name="Jetfuel investment level dom",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dom_aviation_equalizer_dom": 1, "jetfuel_level_dom": 1},
)
def jetfuel_investment_level_dom():
    return dom_aviation_equalizer_dom() * jetfuel_level_dom()


@component.add(
    name="Jetfuel level dom",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "jetfuel_competitiveness_dom": 1,
        "cross": 1,
        "jetfuel_consumption_dom": 1,
        "sum_domestic_aviation": 1,
    },
)
def jetfuel_level_dom():
    return (
        1
        / (1 + np.exp(slope() * (cross() - jetfuel_competitiveness_dom())))
        * jetfuel_consumption_dom()
        / sum_domestic_aviation()
    )


@component.add(
    name="sum domestic aviation",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "jetfuel_consumption_dom": 1,
        "bio_kerosene_consumption_dom": 1,
        "syn_kerosene_consumption_dom": 1,
        "hydrogen_consumption_dom": 1,
    },
)
def sum_domestic_aviation():
    return (
        jetfuel_consumption_dom()
        + bio_kerosene_consumption_dom()
        + syn_kerosene_consumption_dom()
        + hydrogen_consumption_dom()
    )


@component.add(
    name="Syn kerosene competitiveness dom",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biokero_propulsion_cost": 1,
        "synkero_propulsion_cost": 3,
        "jetfuel_propulsion_cost": 1,
        "h2_propulsion_cost_aviation": 1,
    },
)
def syn_kerosene_competitiveness_dom():
    return np.minimum(
        np.minimum(
            biokero_propulsion_cost() / synkero_propulsion_cost(),
            jetfuel_propulsion_cost() / synkero_propulsion_cost(),
        ),
        h2_propulsion_cost_aviation() / synkero_propulsion_cost(),
    )


@component.add(
    name="Syn kerosene consumption dom",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_syn_kerosene_consumption_dom": 1},
    other_deps={
        "_integ_syn_kerosene_consumption_dom": {
            "initial": {},
            "step": {"syn_kerosene_investment_dom": 1, "syn_kerosene_decay_dom": 1},
        }
    },
)
def syn_kerosene_consumption_dom():
    return _integ_syn_kerosene_consumption_dom()


_integ_syn_kerosene_consumption_dom = Integ(
    lambda: syn_kerosene_investment_dom() - syn_kerosene_decay_dom(),
    lambda: 0,
    "_integ_syn_kerosene_consumption_dom",
)


@component.add(
    name="Syn kerosene decay dom",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"syn_kerosene_consumption_dom": 1, "jetfuel_lockin_period": 1},
)
def syn_kerosene_decay_dom():
    return syn_kerosene_consumption_dom() / jetfuel_lockin_period()


@component.add(
    name="Syn kerosene imitators dom",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_aviation_reinvestment": 1,
        "syn_kerosene_investment_level_dom": 1,
    },
)
def syn_kerosene_imitators_dom():
    return domestic_aviation_reinvestment() * syn_kerosene_investment_level_dom()


@component.add(
    name="Syn kerosene inno switch dom",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_syn_kerosene_inno_switch_dom": 1},
    other_deps={
        "_smooth_syn_kerosene_inno_switch_dom": {
            "initial": {
                "syn_kerosene_competitiveness_dom": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
            "step": {
                "syn_kerosene_competitiveness_dom": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
        }
    },
)
def syn_kerosene_inno_switch_dom():
    return _smooth_syn_kerosene_inno_switch_dom()


_smooth_syn_kerosene_inno_switch_dom = Smooth(
    lambda: if_then_else(
        syn_kerosene_competitiveness_dom() > inno_switch_level(),
        lambda: if_then_else(
            syn_kerosene_competitiveness_dom() > early_switch_level(),
            lambda: 3,
            lambda: 1,
        ),
        lambda: 0,
    ),
    lambda: 2,
    lambda: if_then_else(
        syn_kerosene_competitiveness_dom() > inno_switch_level(),
        lambda: if_then_else(
            syn_kerosene_competitiveness_dom() > early_switch_level(),
            lambda: 3,
            lambda: 1,
        ),
        lambda: 0,
    ),
    lambda: 3,
    "_smooth_syn_kerosene_inno_switch_dom",
)


@component.add(
    name="Syn kerosene innovators dom",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_aviation_reinvestment": 1,
        "innovators": 1,
        "syn_kerosene_inno_switch_dom": 1,
        "sum_domestic_aviation": 2,
        "syn_kerosene_consumption_dom": 1,
    },
)
def syn_kerosene_innovators_dom():
    return (
        domestic_aviation_reinvestment()
        * innovators()
        * syn_kerosene_inno_switch_dom()
        * (sum_domestic_aviation() - syn_kerosene_consumption_dom())
        / sum_domestic_aviation()
    )


@component.add(
    name="Syn kerosene investment dom",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"syn_kerosene_innovators_dom": 1, "syn_kerosene_imitators_dom": 1},
)
def syn_kerosene_investment_dom():
    return syn_kerosene_innovators_dom() + syn_kerosene_imitators_dom()


@component.add(
    name="Syn kerosene investment level dom",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dom_aviation_equalizer_dom": 1, "syn_kerosene_level_dom": 1},
)
def syn_kerosene_investment_level_dom():
    return dom_aviation_equalizer_dom() * syn_kerosene_level_dom()


@component.add(
    name="Syn kerosene level dom",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "syn_kerosene_competitiveness_dom": 1,
        "cross": 1,
        "syn_kerosene_consumption_dom": 1,
        "sum_domestic_aviation": 1,
    },
)
def syn_kerosene_level_dom():
    return (
        1
        / (1 + np.exp(slope() * (cross() - syn_kerosene_competitiveness_dom())))
        * syn_kerosene_consumption_dom()
        / sum_domestic_aviation()
    )
