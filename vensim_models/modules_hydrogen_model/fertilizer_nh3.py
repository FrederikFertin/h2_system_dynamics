"""
Module fertilizer_nh3
Translated using PySD version 3.14.0
"""

@component.add(
    name="Blue NH3",
    units="MT NH3",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_blue_nh3": 1},
    other_deps={
        "_integ_blue_nh3": {
            "initial": {},
            "step": {"blue_nh3_investment": 1, "blue_nh3_decay": 1},
        }
    },
)
def blue_nh3():
    return _integ_blue_nh3()


_integ_blue_nh3 = Integ(
    lambda: blue_nh3_investment() - blue_nh3_decay(), lambda: 0, "_integ_blue_nh3"
)


@component.add(
    name="Blue NH3 competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"grey_nh3_cost": 1, "blue_nh3_cost": 2, "fertilizer_nh3_cost": 1},
)
def blue_nh3_competitiveness():
    return np.minimum(
        grey_nh3_cost() / blue_nh3_cost(), fertilizer_nh3_cost() / blue_nh3_cost()
    )


@component.add(
    name="Blue NH3 decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"blue_nh3": 1, "smr_lifetime": 1},
)
def blue_nh3_decay():
    return blue_nh3() / smr_lifetime()


@component.add(
    name="Blue NH3 imitators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nh3_reinvestment": 1, "blue_nh3_investment_level": 1},
)
def blue_nh3_imitators():
    return nh3_reinvestment() * blue_nh3_investment_level()


@component.add(
    name="Blue NH3 inno switch",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_blue_nh3_inno_switch": 1},
    other_deps={
        "_smooth_blue_nh3_inno_switch": {
            "initial": {
                "blue_nh3_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
            "step": {
                "blue_nh3_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
        }
    },
)
def blue_nh3_inno_switch():
    return _smooth_blue_nh3_inno_switch()


_smooth_blue_nh3_inno_switch = Smooth(
    lambda: if_then_else(
        blue_nh3_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            blue_nh3_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 2,
    lambda: if_then_else(
        blue_nh3_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            blue_nh3_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 3,
    "_smooth_blue_nh3_inno_switch",
)


@component.add(
    name="Blue NH3 innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nh3_reinvestment": 1,
        "innovators": 1,
        "blue_nh3_inno_switch": 1,
        "sum_fertilizer": 2,
        "blue_nh3": 1,
    },
)
def blue_nh3_innovators():
    return (
        nh3_reinvestment()
        * innovators()
        * blue_nh3_inno_switch()
        * (sum_fertilizer() - blue_nh3())
        / sum_fertilizer()
    )


@component.add(
    name="Blue NH3 investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"blue_nh3_innovators": 1, "blue_nh3_imitators": 1},
)
def blue_nh3_investment():
    return blue_nh3_innovators() + blue_nh3_imitators()


@component.add(
    name="Blue NH3 investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nh3_equalizer": 1, "blue_nh3_level": 1},
)
def blue_nh3_investment_level():
    return nh3_equalizer() * blue_nh3_level()


@component.add(
    name="Blue NH3 level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "blue_nh3_competitiveness": 1,
        "cross_innovation": 1,
        "blue_nh3": 1,
        "sum_fertilizer": 1,
    },
)
def blue_nh3_level():
    return (
        1
        / (1 + np.exp(slope() * (cross_innovation() - blue_nh3_competitiveness())))
        * blue_nh3()
        / sum_fertilizer()
    )


@component.add(
    name="ctrl fertilizer",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"k_p": 1, "error_fertilizer": 1, "errorint_fertilizer": 1},
)
def ctrl_fertilizer():
    return k_p() * error_fertilizer() + errorint_fertilizer()


@component.add(
    name="demand change fertilizer",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ctrl_fertilizer": 1},
)
def demand_change_fertilizer():
    return ctrl_fertilizer()


@component.add(
    name="error fertilizer",
    units="e",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nh3_fertilizer_consumption": 1, "sum_fertilizer": 1},
)
def error_fertilizer():
    return nh3_fertilizer_consumption() - sum_fertilizer()


@component.add(
    name="errorint fertilizer",
    units="e",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_errorint_fertilizer": 1},
    other_deps={
        "_integ_errorint_fertilizer": {
            "initial": {},
            "step": {"k_i": 1, "error_fertilizer": 1},
        }
    },
)
def errorint_fertilizer():
    return _integ_errorint_fertilizer()


_integ_errorint_fertilizer = Integ(
    lambda: k_i() * error_fertilizer(), lambda: 0, "_integ_errorint_fertilizer"
)


@component.add(
    name="fertilizer average cost",
    units="€/kgH2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "blue_nh3": 1,
        "blue_nh3_cost": 1,
        "fertilizer_nh3_cost": 1,
        "green_nh3": 1,
        "grey_nh3_cost": 1,
        "grey_nh3": 1,
        "sum_fertilizer": 1,
    },
)
def fertilizer_average_cost():
    return (
        blue_nh3() * blue_nh3_cost()
        + green_nh3() * fertilizer_nh3_cost()
        + grey_nh3() * grey_nh3_cost()
    ) / sum_fertilizer()


@component.add(
    name="fertilizer emissions",
    units="tCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "grey_nh3": 2,
        "cc_capture_rate": 1,
        "blue_nh3": 2,
        "nh3_h2_usage": 1,
        "smr_emission_factor": 1,
        "nh3_el_usage": 1,
        "electricity_emission_factor": 1,
    },
)
def fertilizer_emissions():
    return (
        grey_nh3() + blue_nh3() * (1 - cc_capture_rate())
    ) / nh3_h2_usage() * smr_emission_factor() * 10**6 + (
        grey_nh3() + blue_nh3()
    ) * electricity_emission_factor() * 10**9 * nh3_el_usage()


@component.add(
    name="fertilizer H2 price break",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "blue_nh3_cost": 1,
        "grey_nh3_cost": 1,
        "green_nh3_cost_without_h2": 1,
        "nh3_lhv": 1,
        "nh3_h2_usage": 1,
    },
)
def fertilizer_h2_price_break():
    return (
        np.minimum(blue_nh3_cost(), grey_nh3_cost()) - green_nh3_cost_without_h2()
    ) * (nh3_lhv() * nh3_h2_usage())


@component.add(
    name="fertilizer hydrogen demand",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_nh3": 1, "nh3_h2_usage": 1},
)
def fertilizer_hydrogen_demand():
    """
    Convert from MT to T NH3, then from T NH3 to T H2.
    """
    return green_nh3() * 10**6 / nh3_h2_usage()


@component.add(
    name="Green NH3",
    units="MT NH3",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_green_nh3": 1},
    other_deps={
        "_integ_green_nh3": {
            "initial": {},
            "step": {"green_nh3_investment": 1, "green_nh3_decay": 1},
        }
    },
)
def green_nh3():
    return _integ_green_nh3()


_integ_green_nh3 = Integ(
    lambda: green_nh3_investment() - green_nh3_decay(), lambda: 0, "_integ_green_nh3"
)


@component.add(
    name="Green NH3 competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"blue_nh3_cost": 1, "fertilizer_nh3_cost": 2, "grey_nh3_cost": 1},
)
def green_nh3_competitiveness():
    return np.minimum(
        blue_nh3_cost() / fertilizer_nh3_cost(), grey_nh3_cost() / fertilizer_nh3_cost()
    )


@component.add(
    name="Green NH3 decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_nh3": 1, "aec_lifetime": 1},
)
def green_nh3_decay():
    return green_nh3() / aec_lifetime()


@component.add(
    name="Green NH3 imitators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nh3_reinvestment": 1, "green_nh3_investment_level": 1},
)
def green_nh3_imitators():
    return nh3_reinvestment() * green_nh3_investment_level()


@component.add(
    name="Green NH3 inno switch",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_green_nh3_inno_switch": 1},
    other_deps={
        "_smooth_green_nh3_inno_switch": {
            "initial": {
                "green_nh3_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
            "step": {
                "green_nh3_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
        }
    },
)
def green_nh3_inno_switch():
    return _smooth_green_nh3_inno_switch()


_smooth_green_nh3_inno_switch = Smooth(
    lambda: if_then_else(
        green_nh3_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            green_nh3_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 2,
    lambda: if_then_else(
        green_nh3_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            green_nh3_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 3,
    "_smooth_green_nh3_inno_switch",
)


@component.add(
    name="Green NH3 innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nh3_reinvestment": 1,
        "innovators": 1,
        "green_nh3_inno_switch": 1,
        "sum_fertilizer": 2,
        "green_nh3": 1,
    },
)
def green_nh3_innovators():
    return (
        nh3_reinvestment()
        * innovators()
        * green_nh3_inno_switch()
        * (sum_fertilizer() - green_nh3())
        / sum_fertilizer()
    )


@component.add(
    name="Green NH3 investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_nh3_imitators": 1, "green_nh3_innovators": 1},
)
def green_nh3_investment():
    return green_nh3_imitators() + green_nh3_innovators()


@component.add(
    name="Green NH3 investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nh3_equalizer": 1, "green_nh3_level": 1},
)
def green_nh3_investment_level():
    return nh3_equalizer() * green_nh3_level()


@component.add(
    name="Green NH3 level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "green_nh3_competitiveness": 1,
        "cross_innovation": 1,
        "green_nh3": 1,
        "sum_fertilizer": 1,
    },
)
def green_nh3_level():
    return (
        1
        / (1 + np.exp(slope() * (cross_innovation() - green_nh3_competitiveness())))
        * green_nh3()
        / sum_fertilizer()
    )


@component.add(
    name="Grey NH3",
    units="MT NH3",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_grey_nh3": 1},
    other_deps={
        "_integ_grey_nh3": {
            "initial": {"nh3_fertilizer_consumption": 1},
            "step": {"grey_nh3_investment": 1, "grey_nh3_decay": 1},
        }
    },
)
def grey_nh3():
    return _integ_grey_nh3()


_integ_grey_nh3 = Integ(
    lambda: grey_nh3_investment() - grey_nh3_decay(),
    lambda: nh3_fertilizer_consumption(),
    "_integ_grey_nh3",
)


@component.add(
    name="Grey NH3 competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"blue_nh3_cost": 1, "grey_nh3_cost": 2, "fertilizer_nh3_cost": 1},
)
def grey_nh3_competitiveness():
    return np.minimum(
        blue_nh3_cost() / grey_nh3_cost(), fertilizer_nh3_cost() / grey_nh3_cost()
    )


@component.add(
    name="Grey NH3 decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "grey_nh3": 1,
        "smr_lifetime": 1,
        "grey_nh3_early_decommission_rate": 1,
    },
)
def grey_nh3_decay():
    return grey_nh3() * (grey_nh3_early_decommission_rate() + 1 / smr_lifetime())


@component.add(
    name="Grey NH3 early decommission rate",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"grey_nh3_competitiveness": 1},
)
def grey_nh3_early_decommission_rate():
    return 1 / (1 + np.exp(-5 * -grey_nh3_competitiveness())) * 0


@component.add(
    name="Grey NH3 investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"grey_nh3_investment_level": 1, "nh3_reinvestment": 1},
)
def grey_nh3_investment():
    return grey_nh3_investment_level() * nh3_reinvestment()


@component.add(
    name="Grey NH3 investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nh3_equalizer": 1, "grey_nh3_level": 1},
)
def grey_nh3_investment_level():
    return nh3_equalizer() * grey_nh3_level()


@component.add(
    name="Grey NH3 level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "grey_nh3_competitiveness": 1,
        "cross_conventional": 1,
        "grey_nh3": 1,
        "sum_fertilizer": 1,
    },
)
def grey_nh3_level():
    return (
        1
        / (1 + np.exp(slope() * (cross_conventional() - grey_nh3_competitiveness())))
        * grey_nh3()
        / sum_fertilizer()
    )


@component.add(
    name="NH3 equalizer",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"grey_nh3_level": 1, "green_nh3_level": 1, "blue_nh3_level": 1},
)
def nh3_equalizer():
    return 1 / (grey_nh3_level() + green_nh3_level() + blue_nh3_level())


@component.add(
    name="NH3 fertilizer consumption",
    units="MT NH3",
    comp_type="Constant",
    comp_subtype="Normal",
)
def nh3_fertilizer_consumption():
    """
    19.1 MT/year - assumed constant moving forward. EHB European Backbone Report: 19.1 Mt/year CEPS Report: 21 Mt/year (capacity)
    """
    return 19.1


@component.add(
    name="NH3 reinvestment",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_nh3_reinvestment": 1},
    other_deps={
        "_integ_nh3_reinvestment": {
            "initial": {"nh3_fertilizer_consumption": 1, "smr_lifetime": 1},
            "step": {
                "blue_nh3_decay": 1,
                "demand_change_fertilizer": 1,
                "green_nh3_decay": 1,
                "grey_nh3_decay": 1,
                "blue_nh3_investment": 1,
                "green_nh3_investment": 1,
                "grey_nh3_investment": 1,
            },
        }
    },
)
def nh3_reinvestment():
    return _integ_nh3_reinvestment()


_integ_nh3_reinvestment = Integ(
    lambda: blue_nh3_decay()
    + demand_change_fertilizer()
    + green_nh3_decay()
    + grey_nh3_decay()
    - blue_nh3_investment()
    - green_nh3_investment()
    - grey_nh3_investment(),
    lambda: nh3_fertilizer_consumption() / smr_lifetime(),
    "_integ_nh3_reinvestment",
)


@component.add(
    name="sum fertilizer",
    units="MT NH3",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"grey_nh3": 1, "green_nh3": 1, "blue_nh3": 1},
)
def sum_fertilizer():
    return grey_nh3() + green_nh3() + blue_nh3()
