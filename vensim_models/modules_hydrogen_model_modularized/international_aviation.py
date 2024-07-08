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
    depends_on={"bio_kerosene_consumption": 1, "jetfuel_fuel_lockin_period": 1},
)
def bio_kerosene_decay():
    return bio_kerosene_consumption() / jetfuel_fuel_lockin_period()


@component.add(
    name="Bio kerosene imitators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"int_aviation_reinvestment": 1, "bio_kerosene_investment_level": 1},
)
def bio_kerosene_imitators():
    return int_aviation_reinvestment() * bio_kerosene_investment_level()


@component.add(
    name="Bio kerosene inno switch",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"bio_kerosene_competitiveness": 1},
)
def bio_kerosene_inno_switch():
    return if_then_else(bio_kerosene_competitiveness() > 0.5, lambda: 1, lambda: 0)


@component.add(
    name="Bio kerosene innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "int_aviation_reinvestment": 1,
        "innovators": 1,
        "bio_kerosene_inno_switch": 1,
        "bio_kerosene_consumption": 1,
        "sum_int_aviation": 2,
    },
)
def bio_kerosene_innovators():
    return (
        int_aviation_reinvestment()
        * innovators()
        * bio_kerosene_inno_switch()
        * (sum_int_aviation() - bio_kerosene_consumption())
        / sum_int_aviation()
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
    depends_on={"int_aviation_equalizer": 1, "bio_kerosene_level": 1},
)
def bio_kerosene_investment_level():
    return int_aviation_equalizer() * bio_kerosene_level()


@component.add(
    name="Bio kerosene level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "bio_kerosene_competitiveness": 1,
        "cross_innovation": 1,
        "bio_kerosene_consumption": 1,
        "sum_int_aviation": 1,
    },
)
def bio_kerosene_level():
    return (
        1
        / (1 + np.exp(slope() * (cross_innovation() - bio_kerosene_competitiveness())))
        * bio_kerosene_consumption()
        / sum_int_aviation()
    )


@component.add(
    name="ctrl int aviation",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"k_p": 1, "error_int_aviation": 1, "error_int_int_aviation": 1},
)
def ctrl_int_aviation():
    return k_p() * error_int_aviation() + error_int_int_aviation()


@component.add(
    name="demand change int aviation",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ctrl_int_aviation": 1},
)
def demand_change_int_aviation():
    return ctrl_int_aviation()


@component.add(
    name="error int aviation",
    units="e",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"int_aviation_consumption": 1, "sum_int_aviation": 1},
)
def error_int_aviation():
    return int_aviation_consumption() - sum_int_aviation()


@component.add(
    name="error int int aviation",
    units="e",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_error_int_int_aviation": 1},
    other_deps={
        "_integ_error_int_int_aviation": {
            "initial": {"int_aviation_consumption": 1},
            "step": {"k_i": 1, "error_int_aviation": 1},
        }
    },
)
def error_int_int_aviation():
    return _integ_error_int_int_aviation()


_integ_error_int_int_aviation = Integ(
    lambda: k_i() * error_int_aviation(),
    lambda: int_aviation_consumption() * 0.0179,
    "_integ_error_int_int_aviation",
)


@component.add(
    name="int aviation consumption",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def int_aviation_consumption():
    """
    Considering an annual growth of 1,79%/year linearly compared to year 2019.
    """
    return np.interp(time(), [2019, 2050], [486033, 703496])


@component.add(
    name="int aviation equalizer",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"jetfuel_level": 1, "bio_kerosene_level": 1, "syn_kerosene_level": 1},
)
def int_aviation_equalizer():
    return 1 / (jetfuel_level() + bio_kerosene_level() + syn_kerosene_level())


@component.add(
    name="int aviation reinvestment",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_int_aviation_reinvestment": 1},
    other_deps={
        "_integ_int_aviation_reinvestment": {
            "initial": {"int_aviation_consumption": 1, "jetfuel_fuel_lockin_period": 1},
            "step": {
                "demand_change_int_aviation": 1,
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
def int_aviation_reinvestment():
    return _integ_int_aviation_reinvestment()


_integ_int_aviation_reinvestment = Integ(
    lambda: demand_change_int_aviation()
    + jetfuel_decay()
    + bio_kerosene_decay()
    + syn_kerosene_decay()
    - jetfuel_investment()
    - bio_kerosene_investment()
    - syn_kerosene_investment(),
    lambda: int_aviation_consumption() * (0.0179 + 1 / jetfuel_fuel_lockin_period()),
    "_integ_int_aviation_reinvestment",
)


@component.add(
    name="international aviation biomass demand",
    units="tBiomass",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "bio_kerosene_consumption": 1,
        "biokero_biomass_usage": 1,
        "biomass_lhv": 1,
    },
)
def international_aviation_biomass_demand():
    """
    Convert to GWh biomass, then to GJ biomass, then to t biomass.
    """
    return bio_kerosene_consumption() * biokero_biomass_usage() * 3600 / biomass_lhv()


@component.add(
    name="international aviation hydrogen demand",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "bio_kerosene_consumption": 1,
        "biokero_h2_usage": 1,
        "syn_kerosene_consumption": 1,
        "synkero_h2_usage": 1,
        "lhv_h2": 1,
    },
)
def international_aviation_hydrogen_demand():
    """
    Convert from GWh jetfuel to GWh G2 - then to MWh H2 - then to tons H2
    """
    return (
        (
            bio_kerosene_consumption() * biokero_h2_usage()
            + syn_kerosene_consumption() * synkero_h2_usage()
        )
        * 1000
        / lhv_h2()
    )


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
            "initial": {"int_aviation_consumption": 1},
            "step": {"jetfuel_investment": 1, "jetfuel_decay": 1},
        }
    },
)
def jetfuel_consumption():
    return _integ_jetfuel_consumption()


_integ_jetfuel_consumption = Integ(
    lambda: jetfuel_investment() - jetfuel_decay(),
    lambda: int_aviation_consumption(),
    "_integ_jetfuel_consumption",
)


@component.add(
    name="Jetfuel decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"jetfuel_consumption": 1, "jetfuel_fuel_lockin_period": 1},
)
def jetfuel_decay():
    return jetfuel_consumption() / jetfuel_fuel_lockin_period()


@component.add(
    name="jetfuel fuel lockin period", comp_type="Constant", comp_subtype="Normal"
)
def jetfuel_fuel_lockin_period():
    return 10


@component.add(
    name="Jetfuel investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"jetfuel_investment_level": 1, "int_aviation_reinvestment": 1},
)
def jetfuel_investment():
    return jetfuel_investment_level() * int_aviation_reinvestment()


@component.add(
    name="Jetfuel investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"int_aviation_equalizer": 1, "jetfuel_level": 1},
)
def jetfuel_investment_level():
    return int_aviation_equalizer() * jetfuel_level()


@component.add(
    name="Jetfuel level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "cross_conventional": 1,
        "jetfuel_competitiveness": 1,
        "jetfuel_consumption": 1,
        "sum_int_aviation": 1,
    },
)
def jetfuel_level():
    return (
        1
        / (1 + np.exp(slope() * (cross_conventional() - jetfuel_competitiveness())))
        * jetfuel_consumption()
        / sum_int_aviation()
    )


@component.add(
    name="sum int aviation",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "jetfuel_consumption": 1,
        "bio_kerosene_consumption": 1,
        "syn_kerosene_consumption": 1,
    },
)
def sum_int_aviation():
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
    depends_on={"syn_kerosene_consumption": 1, "jetfuel_fuel_lockin_period": 1},
)
def syn_kerosene_decay():
    return syn_kerosene_consumption() / jetfuel_fuel_lockin_period()


@component.add(
    name="Syn kerosene imitators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"int_aviation_reinvestment": 1, "syn_kerosene_investment_level": 1},
)
def syn_kerosene_imitators():
    return int_aviation_reinvestment() * syn_kerosene_investment_level()


@component.add(
    name="Syn kerosene inno switch",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"syn_kerosene_competitiveness": 1},
)
def syn_kerosene_inno_switch():
    return if_then_else(syn_kerosene_competitiveness() > 0.5, lambda: 1, lambda: 0)


@component.add(
    name="Syn kerosene innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "int_aviation_reinvestment": 1,
        "innovators": 1,
        "syn_kerosene_inno_switch": 1,
        "syn_kerosene_consumption": 1,
        "sum_int_aviation": 2,
    },
)
def syn_kerosene_innovators():
    return (
        int_aviation_reinvestment()
        * innovators()
        * syn_kerosene_inno_switch()
        * (sum_int_aviation() - syn_kerosene_consumption())
        / sum_int_aviation()
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
    depends_on={"int_aviation_equalizer": 1, "syn_kerosene_level": 1},
)
def syn_kerosene_investment_level():
    return int_aviation_equalizer() * syn_kerosene_level()


@component.add(
    name="Syn kerosene level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "syn_kerosene_competitiveness": 1,
        "cross_innovation": 1,
        "syn_kerosene_consumption": 1,
        "sum_int_aviation": 1,
    },
)
def syn_kerosene_level():
    return (
        1
        / (1 + np.exp(slope() * (cross_innovation() - syn_kerosene_competitiveness())))
        * syn_kerosene_consumption()
        / sum_int_aviation()
    )
