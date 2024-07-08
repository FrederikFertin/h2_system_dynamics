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
    depends_on={"bio_kerosene_consumption_dom": 1, "plane_lifetime_dom": 1},
)
def bio_kerosene_decay_dom():
    return bio_kerosene_consumption_dom() / plane_lifetime_dom()


@component.add(
    name="Bio kerosene imitators dom",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dom_aviation_reinvestment": 1, "bio_kerosene_investment_level_dom": 1},
)
def bio_kerosene_imitators_dom():
    return dom_aviation_reinvestment() * bio_kerosene_investment_level_dom()


@component.add(
    name="Bio kerosene inno switch dom",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"bio_kerosene_competitiveness_dom": 1},
)
def bio_kerosene_inno_switch_dom():
    return if_then_else(bio_kerosene_competitiveness_dom() > 0.5, lambda: 1, lambda: 0)


@component.add(
    name="Bio kerosene innovators dom",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "dom_aviation_reinvestment": 1,
        "innovators": 1,
        "bio_kerosene_inno_switch_dom": 1,
        "sum_dom_aviation": 2,
        "bio_kerosene_consumption_dom": 1,
    },
)
def bio_kerosene_innovators_dom():
    return (
        dom_aviation_reinvestment()
        * innovators()
        * bio_kerosene_inno_switch_dom()
        * (sum_dom_aviation() - bio_kerosene_consumption_dom())
        / sum_dom_aviation()
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
        "bio_kerosene_competitiveness_dom": 1,
        "cross_innovation": 1,
        "bio_kerosene_consumption_dom": 1,
        "sum_dom_aviation": 1,
    },
)
def bio_kerosene_level_dom():
    return (
        1
        / (
            1
            + np.exp(
                slope() * (cross_innovation() - bio_kerosene_competitiveness_dom())
            )
        )
        * bio_kerosene_consumption_dom()
        / sum_dom_aviation()
    )


@component.add(
    name="ctrl dom aviation",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"k_p": 1, "error_dom_aviation": 1, "error_dom_dom_aviation": 1},
)
def ctrl_dom_aviation():
    return k_p() * error_dom_aviation() + error_dom_dom_aviation()


@component.add(
    name="demand change dom aviation",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ctrl_dom_aviation": 1},
)
def demand_change_dom_aviation():
    return ctrl_dom_aviation()


@component.add(
    name="dom aviation consumption",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def dom_aviation_consumption():
    """
    Considering an annual growth of 1,79%/year linearly compared to year 2019.
    """
    return np.interp(time(), [2019, 2050], [75722, 109601])


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
    name="dom aviation reinvestment",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_dom_aviation_reinvestment": 1},
    other_deps={
        "_integ_dom_aviation_reinvestment": {
            "initial": {"dom_aviation_consumption": 1, "plane_lifetime_dom": 1},
            "step": {
                "bio_kerosene_decay_dom": 1,
                "demand_change_dom_aviation": 1,
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
def dom_aviation_reinvestment():
    return _integ_dom_aviation_reinvestment()


_integ_dom_aviation_reinvestment = Integ(
    lambda: bio_kerosene_decay_dom()
    + demand_change_dom_aviation()
    + hydrogen_decay_dom()
    + jetfuel_decay_dom()
    + syn_kerosene_decay_dom()
    - bio_kerosene_investment_dom()
    - hydrogen_investment_dom()
    - jetfuel_investment_dom()
    - syn_kerosene_investment_dom(),
    lambda: dom_aviation_consumption() * (0.0179 + 1 / plane_lifetime_dom()),
    "_integ_dom_aviation_reinvestment",
)


@component.add(
    name="domestic aviation biomass demand",
    units="tBiomass",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "bio_kerosene_consumption_dom": 1,
        "biokero_biomass_usage": 1,
        "biomass_lhv": 1,
    },
)
def domestic_aviation_biomass_demand():
    return (
        bio_kerosene_consumption_dom() * biokero_biomass_usage() * 3600 / biomass_lhv()
    )


@component.add(
    name="domestic aviation hydrogen demand",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "bio_kerosene_consumption_dom": 1,
        "biokero_h2_usage": 1,
        "synkero_h2_usage": 1,
        "syn_kerosene_consumption_dom": 1,
        "lhv_h2": 2,
        "hydrogen_consumption_dom": 1,
    },
)
def domestic_aviation_hydrogen_demand():
    """
    Convert from GWh to GJ, then from GJ to tons fuel, then from tons fuel to tons H2. Example 1: MeOH cons. [GWh] * 3600 [GJ/GWh] / 19.9 [GJ/t] / 15.7 [t MeOH/t H2] Example 2: NH3 cons. [GWh] * 3600 [GJ/GWh] / 18.6 [GJ/t] / 5.56 [t NH3/t H2]
    """
    return (
        bio_kerosene_consumption_dom() * biokero_h2_usage()
        + syn_kerosene_consumption_dom() * synkero_h2_usage()
    ) * 1000 / lhv_h2() + hydrogen_consumption_dom() * 1000 / lhv_h2()


@component.add(
    name="error dom aviation",
    units="e",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dom_aviation_consumption": 1, "sum_dom_aviation": 1},
)
def error_dom_aviation():
    return dom_aviation_consumption() - sum_dom_aviation()


@component.add(
    name="error dom dom aviation",
    units="e",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_error_dom_dom_aviation": 1},
    other_deps={
        "_integ_error_dom_dom_aviation": {
            "initial": {"dom_aviation_consumption": 1},
            "step": {"k_i": 1, "error_dom_aviation": 1},
        }
    },
)
def error_dom_dom_aviation():
    return _integ_error_dom_dom_aviation()


_integ_error_dom_dom_aviation = Integ(
    lambda: k_i() * error_dom_aviation(),
    lambda: dom_aviation_consumption() * 0.0179,
    "_integ_error_dom_dom_aviation",
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
    depends_on={"hydrogen_consumption_dom": 1, "plane_lifetime_dom": 1},
)
def hydrogen_decay_dom():
    return hydrogen_consumption_dom() / plane_lifetime_dom()


@component.add(
    name="Hydrogen imitators dom",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dom_aviation_reinvestment": 1, "hydrogen_investment_level_dom": 1},
)
def hydrogen_imitators_dom():
    return dom_aviation_reinvestment() * hydrogen_investment_level_dom()


@component.add(
    name="Hydrogen inno switch dom",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hydrogen_competitiveness_dom": 1},
)
def hydrogen_inno_switch_dom():
    return if_then_else(hydrogen_competitiveness_dom() > 0.5, lambda: 1, lambda: 0)


@component.add(
    name="Hydrogen innovators dom",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "dom_aviation_reinvestment": 1,
        "innovators": 1,
        "hydrogen_inno_switch_dom": 1,
        "sum_dom_aviation": 2,
        "hydrogen_consumption_dom": 1,
    },
)
def hydrogen_innovators_dom():
    return (
        dom_aviation_reinvestment()
        * innovators()
        * hydrogen_inno_switch_dom()
        * (sum_dom_aviation() - hydrogen_consumption_dom())
        / sum_dom_aviation()
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
        "cross_innovation": 1,
        "hydrogen_consumption_dom": 1,
        "sum_dom_aviation": 1,
    },
)
def hydrogen_level_dom():
    return (
        1
        / (1 + np.exp(slope() * (cross_innovation() - hydrogen_competitiveness_dom())))
        * hydrogen_consumption_dom()
        / sum_dom_aviation()
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
            "initial": {"dom_aviation_consumption": 1},
            "step": {"jetfuel_investment_dom": 1, "jetfuel_decay_dom": 1},
        }
    },
)
def jetfuel_consumption_dom():
    return _integ_jetfuel_consumption_dom()


_integ_jetfuel_consumption_dom = Integ(
    lambda: jetfuel_investment_dom() - jetfuel_decay_dom(),
    lambda: dom_aviation_consumption(),
    "_integ_jetfuel_consumption_dom",
)


@component.add(
    name="Jetfuel decay dom",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"jetfuel_consumption_dom": 1, "plane_lifetime_dom": 1},
)
def jetfuel_decay_dom():
    return jetfuel_consumption_dom() / plane_lifetime_dom()


@component.add(
    name="Jetfuel investment dom",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"jetfuel_investment_level_dom": 1, "dom_aviation_reinvestment": 1},
)
def jetfuel_investment_dom():
    return jetfuel_investment_level_dom() * dom_aviation_reinvestment()


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
        "cross_conventional": 1,
        "jetfuel_competitiveness_dom": 1,
        "jetfuel_consumption_dom": 1,
        "sum_dom_aviation": 1,
    },
)
def jetfuel_level_dom():
    return (
        1
        / (1 + np.exp(slope() * (cross_conventional() - jetfuel_competitiveness_dom())))
        * jetfuel_consumption_dom()
        / sum_dom_aviation()
    )


@component.add(name="plane lifetime dom", comp_type="Constant", comp_subtype="Normal")
def plane_lifetime_dom():
    return 25


@component.add(
    name="sum dom aviation",
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
def sum_dom_aviation():
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
    depends_on={"syn_kerosene_consumption_dom": 1, "plane_lifetime_dom": 1},
)
def syn_kerosene_decay_dom():
    return syn_kerosene_consumption_dom() / plane_lifetime_dom()


@component.add(
    name="Syn kerosene imitators dom",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dom_aviation_reinvestment": 1, "syn_kerosene_investment_level_dom": 1},
)
def syn_kerosene_imitators_dom():
    return dom_aviation_reinvestment() * syn_kerosene_investment_level_dom()


@component.add(
    name="Syn kerosene inno switch dom",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"syn_kerosene_competitiveness_dom": 1},
)
def syn_kerosene_inno_switch_dom():
    return if_then_else(syn_kerosene_competitiveness_dom() > 0.5, lambda: 1, lambda: 0)


@component.add(
    name="Syn kerosene innovators dom",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "dom_aviation_reinvestment": 1,
        "innovators": 1,
        "syn_kerosene_inno_switch_dom": 1,
        "sum_dom_aviation": 2,
        "syn_kerosene_consumption_dom": 1,
    },
)
def syn_kerosene_innovators_dom():
    return (
        dom_aviation_reinvestment()
        * innovators()
        * syn_kerosene_inno_switch_dom()
        * (sum_dom_aviation() - syn_kerosene_consumption_dom())
        / sum_dom_aviation()
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
        "cross_innovation": 1,
        "syn_kerosene_consumption_dom": 1,
        "sum_dom_aviation": 1,
    },
)
def syn_kerosene_level_dom():
    return (
        1
        / (
            1
            + np.exp(
                slope() * (cross_innovation() - syn_kerosene_competitiveness_dom())
            )
        )
        * syn_kerosene_consumption_dom()
        / sum_dom_aviation()
    )
