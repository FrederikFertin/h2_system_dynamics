"""
Module iron_and_steel
Translated using PySD version 3.14.0
"""

@component.add(
    name="BF CCS competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ngdri_cost": 1, "bf_ccs_cost": 3, "h2dri_cost": 1, "bf_coal_cost": 1},
)
def bf_ccs_competitiveness():
    return np.minimum(
        ngdri_cost() / bf_ccs_cost(),
        np.minimum(bf_coal_cost() / bf_ccs_cost(), h2dri_cost() / bf_ccs_cost()),
    )


@component.add(
    name="BF CCS decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"coal_bf_bof_ccs": 1, "foundry_lifetime": 1},
)
def bf_ccs_decay():
    return coal_bf_bof_ccs() / foundry_lifetime()


@component.add(
    name="BF CCS imitators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"foundry_reinvestment": 1, "bf_ccs_investment_level": 1},
)
def bf_ccs_imitators():
    return foundry_reinvestment() * bf_ccs_investment_level()


@component.add(
    name="BF CCS inno switch",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_bf_ccs_inno_switch": 1},
    other_deps={
        "_smooth_bf_ccs_inno_switch": {
            "initial": {
                "bf_ccs_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
            "step": {
                "bf_ccs_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
        }
    },
)
def bf_ccs_inno_switch():
    return _smooth_bf_ccs_inno_switch()


_smooth_bf_ccs_inno_switch = Smooth(
    lambda: if_then_else(
        bf_ccs_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            bf_ccs_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 2,
    lambda: if_then_else(
        bf_ccs_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            bf_ccs_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 3,
    "_smooth_bf_ccs_inno_switch",
)


@component.add(
    name="BF CCS innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "foundry_reinvestment": 1,
        "innovators": 1,
        "bf_ccs_inno_switch": 1,
        "sum_steel": 2,
        "coal_bf_bof_ccs": 1,
    },
)
def bf_ccs_innovators():
    return (
        foundry_reinvestment()
        * innovators()
        * bf_ccs_inno_switch()
        * (sum_steel() - coal_bf_bof_ccs())
        / sum_steel()
    )


@component.add(
    name="BF CCS investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"bf_ccs_innovators": 1, "bf_ccs_imitators": 1},
)
def bf_ccs_investment():
    return bf_ccs_innovators() + bf_ccs_imitators()


@component.add(
    name="BF CCS investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"steel_equalizer": 1, "bf_ccs_level": 1},
)
def bf_ccs_investment_level():
    return steel_equalizer() * bf_ccs_level()


@component.add(
    name="BF CCS level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "bf_ccs_competitiveness": 1,
        "cross": 1,
        "coal_bf_bof_ccs": 1,
        "sum_steel": 1,
    },
)
def bf_ccs_level():
    return (
        1
        / (1 + np.exp(slope() * (cross() - bf_ccs_competitiveness())))
        * coal_bf_bof_ccs()
        / sum_steel()
    )


@component.add(
    name="BF Coal competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ngdri_cost": 1, "bf_coal_cost": 3, "h2dri_cost": 1, "bf_ccs_cost": 1},
)
def bf_coal_competitiveness():
    return np.minimum(
        ngdri_cost() / bf_coal_cost(),
        np.minimum(bf_ccs_cost() / bf_coal_cost(), h2dri_cost() / bf_coal_cost()),
    )


@component.add(
    name="BF Coal decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "coal_bf_bof": 1,
        "bf_coal_early_decommission_rate": 1,
        "foundry_lifetime": 1,
    },
)
def bf_coal_decay():
    return coal_bf_bof() * (bf_coal_early_decommission_rate() + 1 / foundry_lifetime())


@component.add(
    name="BF Coal early decommission rate",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"bf_coal_competitiveness": 1},
)
def bf_coal_early_decommission_rate():
    return 1 / (1 + np.exp(-5 * -bf_coal_competitiveness())) * 0


@component.add(
    name="BF Coal investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"bf_coal_investment_level": 1, "foundry_reinvestment": 1},
)
def bf_coal_investment():
    return bf_coal_investment_level() * foundry_reinvestment()


@component.add(
    name="BF Coal investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"steel_equalizer": 1, "bf_coal_level": 1},
)
def bf_coal_investment_level():
    return steel_equalizer() * bf_coal_level()


@component.add(
    name="BF Coal level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "bf_coal_competitiveness": 1,
        "cross": 1,
        "coal_bf_bof": 1,
        "sum_steel": 1,
    },
)
def bf_coal_level():
    return (
        1
        / (1 + np.exp(slope() * (cross() - bf_coal_competitiveness())))
        * coal_bf_bof()
        / sum_steel()
    )


@component.add(
    name="Coal BF BOF",
    units="Mtsteel",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_coal_bf_bof": 1},
    other_deps={
        "_integ_coal_bf_bof": {
            "initial": {"primary_sector": 1},
            "step": {"bf_coal_investment": 1, "bf_coal_decay": 1},
        }
    },
)
def coal_bf_bof():
    return _integ_coal_bf_bof()


_integ_coal_bf_bof = Integ(
    lambda: bf_coal_investment() - bf_coal_decay(),
    lambda: primary_sector(),
    "_integ_coal_bf_bof",
)


@component.add(
    name="Coal BF BOF CCS",
    units="Mtsteel",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_coal_bf_bof_ccs": 1},
    other_deps={
        "_integ_coal_bf_bof_ccs": {
            "initial": {},
            "step": {"bf_ccs_investment": 1, "bf_ccs_decay": 1},
        }
    },
)
def coal_bf_bof_ccs():
    return _integ_coal_bf_bof_ccs()


_integ_coal_bf_bof_ccs = Integ(
    lambda: bf_ccs_investment() - bf_ccs_decay(), lambda: 0, "_integ_coal_bf_bof_ccs"
)


@component.add(
    name="Coal BF BOF CCS emissions",
    units="tCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "coal_bf_bof_ccs": 1,
        "cc_capture_rate": 1,
        "el_to_steel_bf_coal": 1,
        "electricity_emission_factor": 1,
        "bf_coal_emission_factor": 1,
    },
)
def coal_bf_bof_ccs_emissions():
    return (
        coal_bf_bof_ccs()
        * 10**6
        * (
            (1 - cc_capture_rate()) * bf_coal_emission_factor()
            + el_to_steel_bf_coal() * electricity_emission_factor()
        )
    )


@component.add(
    name="Coal BF BOF emissions",
    units="tCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "coal_bf_bof": 1,
        "el_to_steel_bf_coal": 1,
        "electricity_emission_factor": 1,
        "bf_coal_emission_factor": 1,
    },
)
def coal_bf_bof_emissions():
    return (
        coal_bf_bof()
        * 10**6
        * (
            bf_coal_emission_factor()
            + el_to_steel_bf_coal() * electricity_emission_factor()
        )
    )


@component.add(
    name="ctrl steel",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"k_p": 1, "error_steel": 1, "errorint_steel": 1},
)
def ctrl_steel():
    return k_p() * error_steel() + errorint_steel()


@component.add(
    name="demand change steel",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ctrl_steel": 1},
)
def demand_change_steel():
    return ctrl_steel()


@component.add(
    name="error steel",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"primary_sector": 1, "sum_steel": 1},
)
def error_steel():
    return primary_sector() - sum_steel()


@component.add(
    name="errorint steel",
    units="e",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_errorint_steel": 1},
    other_deps={
        "_integ_errorint_steel": {"initial": {}, "step": {"k_i": 1, "error_steel": 1}}
    },
)
def errorint_steel():
    return _integ_errorint_steel()


_integ_errorint_steel = Integ(
    lambda: k_i() * error_steel(), lambda: 0, "_integ_errorint_steel"
)


@component.add(
    name="foundry lifetime", units="years", comp_type="Constant", comp_subtype="Normal"
)
def foundry_lifetime():
    return 25


@component.add(
    name="foundry reinvestment",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_foundry_reinvestment": 1},
    other_deps={
        "_integ_foundry_reinvestment": {
            "initial": {"primary_sector": 1, "foundry_lifetime": 1},
            "step": {
                "bf_ccs_decay": 1,
                "bf_coal_decay": 1,
                "demand_change_steel": 1,
                "h2dri_eaf_decay": 1,
                "ngdri_eaf_decay": 1,
                "bf_ccs_investment": 1,
                "bf_coal_investment": 1,
                "h2dri_eaf_investment": 1,
                "ngdri_eaf_investment": 1,
            },
        }
    },
)
def foundry_reinvestment():
    return _integ_foundry_reinvestment()


_integ_foundry_reinvestment = Integ(
    lambda: bf_ccs_decay()
    + bf_coal_decay()
    + demand_change_steel()
    + h2dri_eaf_decay()
    + ngdri_eaf_decay()
    - bf_ccs_investment()
    - bf_coal_investment()
    - h2dri_eaf_investment()
    - ngdri_eaf_investment(),
    lambda: primary_sector() / foundry_lifetime(),
    "_integ_foundry_reinvestment",
)


@component.add(
    name="H2 to steel", units="tH2/tsteel", comp_type="Constant", comp_subtype="Normal"
)
def h2_to_steel():
    return 0.0563


@component.add(
    name="H2DRI EAF",
    units="Mtsteel",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_h2dri_eaf": 1},
    other_deps={
        "_integ_h2dri_eaf": {
            "initial": {},
            "step": {"h2dri_eaf_investment": 1, "h2dri_eaf_decay": 1},
        }
    },
)
def h2dri_eaf():
    return _integ_h2dri_eaf()


_integ_h2dri_eaf = Integ(
    lambda: h2dri_eaf_investment() - h2dri_eaf_decay(), lambda: 0, "_integ_h2dri_eaf"
)


@component.add(
    name="H2DRI EAF competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ngdri_cost": 1, "h2dri_cost": 3, "bf_coal_cost": 1, "bf_ccs_cost": 1},
)
def h2dri_eaf_competitiveness():
    return np.minimum(
        ngdri_cost() / h2dri_cost(),
        np.minimum(bf_coal_cost() / h2dri_cost(), bf_ccs_cost() / h2dri_cost()),
    )


@component.add(
    name="H2DRI EAF decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"h2dri_eaf": 1, "foundry_lifetime": 1},
)
def h2dri_eaf_decay():
    return h2dri_eaf() / foundry_lifetime()


@component.add(
    name="H2DRI EAF emissions",
    units="tCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "h2dri_eaf": 1,
        "el_to_steel_h2dri": 1,
        "electricity_emission_factor": 1,
    },
)
def h2dri_eaf_emissions():
    return (
        h2dri_eaf()
        * 10**6
        * (el_to_steel_h2dri() / 3.6 * electricity_emission_factor())
    )


@component.add(
    name="H2DRI EAF imitators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"foundry_reinvestment": 1, "h2dri_eaf_investment_level": 1},
)
def h2dri_eaf_imitators():
    return foundry_reinvestment() * h2dri_eaf_investment_level()


@component.add(
    name="H2DRI EAF inno switch",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "h2dri_eaf_competitiveness": 2,
        "inno_switch_level": 1,
        "early_switch_level": 1,
    },
)
def h2dri_eaf_inno_switch():
    return if_then_else(
        h2dri_eaf_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            h2dri_eaf_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    )


@component.add(
    name="H2DRI EAF innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "foundry_reinvestment": 1,
        "innovators": 1,
        "h2dri_eaf_inno_switch": 1,
        "sum_steel": 2,
        "h2dri_eaf": 1,
    },
)
def h2dri_eaf_innovators():
    return (
        foundry_reinvestment()
        * innovators()
        * h2dri_eaf_inno_switch()
        * (sum_steel() - h2dri_eaf())
        / sum_steel()
    )


@component.add(
    name="H2DRI EAF investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"h2dri_eaf_imitators": 1, "h2dri_eaf_innovators": 1},
)
def h2dri_eaf_investment():
    return h2dri_eaf_imitators() + h2dri_eaf_innovators()


@component.add(
    name="H2DRI EAF investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"steel_equalizer": 1, "h2dri_eaf_level": 1},
)
def h2dri_eaf_investment_level():
    return steel_equalizer() * h2dri_eaf_level()


@component.add(
    name="H2DRI EAF level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "h2dri_eaf_competitiveness": 1,
        "cross": 1,
        "h2dri_eaf": 1,
        "sum_steel": 1,
    },
)
def h2dri_eaf_level():
    return (
        1
        / (1 + np.exp(slope() * (cross() - h2dri_eaf_competitiveness())))
        * h2dri_eaf()
        / sum_steel()
    )


@component.add(
    name="NGDRI EAF",
    units="Mtsteel",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_ngdri_eaf": 1},
    other_deps={
        "_integ_ngdri_eaf": {
            "initial": {},
            "step": {"ngdri_eaf_investment": 1, "ngdri_eaf_decay": 1},
        }
    },
)
def ngdri_eaf():
    return _integ_ngdri_eaf()


_integ_ngdri_eaf = Integ(
    lambda: ngdri_eaf_investment() - ngdri_eaf_decay(), lambda: 0, "_integ_ngdri_eaf"
)


@component.add(
    name="NGDRI EAF competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"h2dri_cost": 1, "ngdri_cost": 3, "bf_coal_cost": 1, "bf_ccs_cost": 1},
)
def ngdri_eaf_competitiveness():
    return np.minimum(
        h2dri_cost() / ngdri_cost(),
        np.minimum(bf_coal_cost() / ngdri_cost(), bf_ccs_cost() / ngdri_cost()),
    )


@component.add(
    name="NGDRI EAF decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ngdri_eaf": 1, "foundry_lifetime": 1},
)
def ngdri_eaf_decay():
    return ngdri_eaf() / foundry_lifetime()


@component.add(
    name="NGDRI EAF emissions",
    units="tCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ngdri_eaf": 1,
        "ngdri_emission_factor": 1,
        "el_to_steel_ngdri": 1,
        "electricity_emission_factor": 1,
    },
)
def ngdri_eaf_emissions():
    return (
        ngdri_eaf()
        * 10**6
        * (
            ngdri_emission_factor()
            + el_to_steel_ngdri() * electricity_emission_factor()
        )
    )


@component.add(
    name="NGDRI EAF imitators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"foundry_reinvestment": 1, "ngdri_eaf_investment_level": 1},
)
def ngdri_eaf_imitators():
    return foundry_reinvestment() * ngdri_eaf_investment_level()


@component.add(
    name="NGDRI EAF inno switch",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ngdri_eaf_competitiveness": 2,
        "inno_switch_level": 1,
        "early_switch_level": 1,
    },
)
def ngdri_eaf_inno_switch():
    return if_then_else(
        ngdri_eaf_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            ngdri_eaf_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    )


@component.add(
    name="NGDRI EAF innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "foundry_reinvestment": 1,
        "innovators": 1,
        "ngdri_eaf_inno_switch": 1,
        "sum_steel": 2,
        "ngdri_eaf": 1,
    },
)
def ngdri_eaf_innovators():
    return (
        foundry_reinvestment()
        * innovators()
        * ngdri_eaf_inno_switch()
        * (sum_steel() - ngdri_eaf())
        / sum_steel()
    )


@component.add(
    name="NGDRI EAF investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ngdri_eaf_imitators": 1, "ngdri_eaf_innovators": 1},
)
def ngdri_eaf_investment():
    return ngdri_eaf_imitators() + ngdri_eaf_innovators()


@component.add(
    name="NGDRI EAF investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"steel_equalizer": 1, "ngdri_eaf_level": 1},
)
def ngdri_eaf_investment_level():
    return steel_equalizer() * ngdri_eaf_level()


@component.add(
    name="NGDRI EAF level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "ngdri_eaf_competitiveness": 1,
        "cross": 1,
        "ngdri_eaf": 1,
        "sum_steel": 1,
    },
)
def ngdri_eaf_level():
    return (
        1
        / (1 + np.exp(slope() * (cross() - ngdri_eaf_competitiveness())))
        * ngdri_eaf()
        / sum_steel()
    )


@component.add(
    name="primary sector",
    units="Mtsteel",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"steel_production_forecast": 1, "secondary_sector_growth": 1},
)
def primary_sector():
    return steel_production_forecast() * (1 - secondary_sector_growth())


@component.add(
    name="secondary sector",
    units="Mtsteel",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"steel_production_forecast": 1, "secondary_sector_growth": 1},
)
def secondary_sector():
    return steel_production_forecast() * secondary_sector_growth()


@component.add(
    name="secondary sector growth",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def secondary_sector_growth():
    """
    At the same time, the share of secondary steel production is expected to increase to 50%, as less scrap will be exported out of Europe to now serve decarbonisation of steel production in the European market
    !year
    !share of steel production
    """
    return np.interp(time(), [2019.0, 2050.0], [0.4, 0.5])


@component.add(
    name="steel average cost",
    units="€/tsteel",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "coal_bf_bof": 1,
        "bf_coal_cost": 1,
        "coal_bf_bof_ccs": 1,
        "bf_ccs_cost": 1,
        "h2dri_cost": 1,
        "h2dri_eaf": 1,
        "ngdri_eaf": 1,
        "ngdri_cost": 1,
        "sum_steel": 1,
    },
)
def steel_average_cost():
    """
    €/kgH2 equivalent necessary in the HDRI production pathway of steel.
    """
    return (
        coal_bf_bof() * bf_coal_cost()
        + coal_bf_bof_ccs() * bf_ccs_cost()
        + h2dri_eaf() * h2dri_cost()
        + ngdri_eaf() * ngdri_cost()
    ) / sum_steel()


@component.add(
    name="steel emissions",
    units="tCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "coal_bf_bof_ccs_emissions": 1,
        "coal_bf_bof_emissions": 1,
        "h2dri_eaf_emissions": 1,
        "ngdri_eaf_emissions": 1,
    },
)
def steel_emissions():
    return (
        coal_bf_bof_ccs_emissions()
        + coal_bf_bof_emissions()
        + h2dri_eaf_emissions()
        + ngdri_eaf_emissions()
    )


@component.add(
    name="steel equalizer",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "bf_coal_level": 1,
        "h2dri_eaf_level": 1,
        "bf_ccs_level": 1,
        "ngdri_eaf_level": 1,
    },
)
def steel_equalizer():
    return 1 / (
        bf_coal_level() + h2dri_eaf_level() + bf_ccs_level() + ngdri_eaf_level()
    )


@component.add(
    name="steel hydrogen demand",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"h2dri_eaf": 1, "h2_to_steel": 1},
)
def steel_hydrogen_demand():
    return h2dri_eaf() * 10**6 * h2_to_steel()


@component.add(
    name="Steel Production Forecast",
    units="Mtsteel",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def steel_production_forecast():
    """
    The change in European steel production is taken from Material Economics’ modelling based on EUROFER, which yields a 0.6% yearly increase in the steel stock/capacity up to the 2040s, when it stabilises at 193 million tonnes per year, up from 170 million tonnes per year today.
    !year
    !Mt steel
    """
    return np.interp(time(), [2019, 2040, 2050], [170, 193, 193])


@component.add(
    name="sum steel",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"coal_bf_bof": 1, "h2dri_eaf": 1, "coal_bf_bof_ccs": 1, "ngdri_eaf": 1},
)
def sum_steel():
    return coal_bf_bof() + h2dri_eaf() + coal_bf_bof_ccs() + ngdri_eaf()
