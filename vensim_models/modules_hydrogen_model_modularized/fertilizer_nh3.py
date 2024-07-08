"""
Module fertilizer_nh3
Translated using PySD version 3.14.0
"""

@component.add(
    name="Blue competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"grey_h2_price": 1, "blue_h2_price": 2, "green_h2_price": 1},
)
def blue_competitiveness():
    return np.minimum(
        grey_h2_price() / blue_h2_price(), green_h2_price() / blue_h2_price()
    )


@component.add(
    name="Blue decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"blue_nh3": 1, "smr_lifetime": 1},
)
def blue_decay():
    return blue_nh3() / smr_lifetime()


@component.add(
    name="Blue imitators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nh3_reinvestment": 1, "blue_investment_level": 1},
)
def blue_imitators():
    return nh3_reinvestment() * blue_investment_level()


@component.add(
    name="Blue inno switch",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"blue_competitiveness": 1},
)
def blue_inno_switch():
    return if_then_else(blue_competitiveness() < 0.5, lambda: 1, lambda: 0)


@component.add(
    name="Blue innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nh3_reinvestment": 1,
        "innovators": 1,
        "blue_inno_switch": 1,
        "sum_fertilizer": 2,
        "blue_nh3": 1,
    },
)
def blue_innovators():
    return (
        nh3_reinvestment()
        * innovators()
        * blue_inno_switch()
        * (sum_fertilizer() - blue_nh3())
        / sum_fertilizer()
    )


@component.add(
    name="Blue investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"blue_innovators": 1, "blue_imitators": 1},
)
def blue_investment():
    return blue_innovators() + blue_imitators()


@component.add(
    name="Blue investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nh3_equalizer": 1, "blue_level": 1},
)
def blue_investment_level():
    return nh3_equalizer() * blue_level()


@component.add(
    name="Blue level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "blue_competitiveness": 1,
        "cross_innovation": 1,
        "blue_nh3": 1,
        "sum_fertilizer": 1,
    },
)
def blue_level():
    return (
        1
        / (1 + np.exp(slope() * (cross_innovation() - blue_competitiveness())))
        * blue_nh3()
        / sum_fertilizer()
    )


@component.add(
    name="Blue NH3",
    units="MT NH3",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_blue_nh3": 1},
    other_deps={
        "_integ_blue_nh3": {
            "initial": {},
            "step": {"blue_investment": 1, "blue_decay": 1},
        }
    },
)
def blue_nh3():
    return _integ_blue_nh3()


_integ_blue_nh3 = Integ(
    lambda: blue_investment() - blue_decay(), lambda: 0, "_integ_blue_nh3"
)


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
    name="Green competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"blue_h2_price": 1, "green_h2_price": 2, "grey_h2_price": 1},
)
def green_competitiveness():
    return np.minimum(
        blue_h2_price() / green_h2_price(), grey_h2_price() / green_h2_price()
    )


@component.add(
    name="Green decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_nh3": 1, "aec_lifetime": 1},
)
def green_decay():
    return green_nh3() / aec_lifetime()


@component.add(
    name="Green imitators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nh3_reinvestment": 1, "green_investment_level": 1},
)
def green_imitators():
    return nh3_reinvestment() * green_investment_level()


@component.add(
    name="Green inno switch",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_competitiveness": 1},
)
def green_inno_switch():
    return if_then_else(green_competitiveness() > 0.5, lambda: 1, lambda: 0)


@component.add(
    name="Green innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nh3_reinvestment": 1,
        "innovators": 1,
        "green_inno_switch": 1,
        "green_nh3": 1,
        "sum_fertilizer": 2,
    },
)
def green_innovators():
    return (
        nh3_reinvestment()
        * innovators()
        * green_inno_switch()
        * (sum_fertilizer() - green_nh3())
        / sum_fertilizer()
    )


@component.add(
    name="Green investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_imitators": 1, "green_innovators": 1},
)
def green_investment():
    return green_imitators() + green_innovators()


@component.add(
    name="Green investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nh3_equalizer": 1, "green_level": 1},
)
def green_investment_level():
    return nh3_equalizer() * green_level()


@component.add(
    name="Green level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "green_competitiveness": 1,
        "cross_innovation": 1,
        "green_nh3": 1,
        "sum_fertilizer": 1,
    },
)
def green_level():
    return (
        1
        / (1 + np.exp(slope() * (cross_innovation() - green_competitiveness())))
        * green_nh3()
        / sum_fertilizer()
    )


@component.add(
    name="Green NH3",
    units="MT NH3",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_green_nh3": 1},
    other_deps={
        "_integ_green_nh3": {
            "initial": {},
            "step": {"green_investment": 1, "green_decay": 1},
        }
    },
)
def green_nh3():
    return _integ_green_nh3()


_integ_green_nh3 = Integ(
    lambda: green_investment() - green_decay(), lambda: 0, "_integ_green_nh3"
)


@component.add(
    name="Grey competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"blue_h2_price": 1, "grey_h2_price": 2, "green_h2_price": 1},
)
def grey_competitiveness():
    return np.minimum(
        blue_h2_price() / grey_h2_price(), green_h2_price() / grey_h2_price()
    )


@component.add(
    name="Grey decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"grey_nh3": 1, "smr_lifetime": 1},
)
def grey_decay():
    return grey_nh3() / smr_lifetime()


@component.add(
    name="Grey investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"grey_investment_level": 1, "nh3_reinvestment": 1},
)
def grey_investment():
    return grey_investment_level() * nh3_reinvestment()


@component.add(
    name="Grey investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nh3_equalizer": 1, "grey_level": 1},
)
def grey_investment_level():
    return nh3_equalizer() * grey_level()


@component.add(
    name="Grey level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "cross_conventional": 1,
        "grey_competitiveness": 1,
        "grey_nh3": 1,
        "sum_fertilizer": 1,
    },
)
def grey_level():
    return (
        1
        / (1 + np.exp(slope() * (cross_conventional() - grey_competitiveness())))
        * grey_nh3()
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
            "step": {"grey_investment": 1, "grey_decay": 1},
        }
    },
)
def grey_nh3():
    return _integ_grey_nh3()


_integ_grey_nh3 = Integ(
    lambda: grey_investment() - grey_decay(),
    lambda: nh3_fertilizer_consumption(),
    "_integ_grey_nh3",
)


@component.add(
    name="NH3 equalizer",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"grey_level": 1, "green_level": 1, "blue_level": 1},
)
def nh3_equalizer():
    return 1 / (grey_level() + green_level() + blue_level())


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
                "blue_decay": 1,
                "green_decay": 1,
                "grey_decay": 1,
                "blue_investment": 1,
                "green_investment": 1,
                "grey_investment": 1,
            },
        }
    },
)
def nh3_reinvestment():
    return _integ_nh3_reinvestment()


_integ_nh3_reinvestment = Integ(
    lambda: blue_decay()
    + green_decay()
    + grey_decay()
    - blue_investment()
    - green_investment()
    - grey_investment(),
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
