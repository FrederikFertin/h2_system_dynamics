"""
Module oil_refining
Translated using PySD version 3.14.0
"""

@component.add(
    name="Blue refinery",
    units="MT H2",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_blue_refinery": 1},
    other_deps={
        "_integ_blue_refinery": {
            "initial": {},
            "step": {"blue_refinery_investment": 1, "blue_refinery_decay": 1},
        }
    },
)
def blue_refinery():
    return _integ_blue_refinery()


_integ_blue_refinery = Integ(
    lambda: blue_refinery_investment() - blue_refinery_decay(),
    lambda: 0,
    "_integ_blue_refinery",
)


@component.add(
    name="Blue refinery competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"grey_h2_price": 1, "blue_h2_price": 2, "green_h2_price": 1},
)
def blue_refinery_competitiveness():
    return np.minimum(
        grey_h2_price() / blue_h2_price(), green_h2_price() / blue_h2_price()
    )


@component.add(
    name="Blue refinery decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"blue_refinery": 1, "smr_lifetime": 1},
)
def blue_refinery_decay():
    return blue_refinery() / smr_lifetime()


@component.add(
    name="Blue refinery imitators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"refinery_reinvestment": 1, "blue_refinery_investment_level": 1},
)
def blue_refinery_imitators():
    return refinery_reinvestment() * blue_refinery_investment_level()


@component.add(
    name="Blue refinery inno switch",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"blue_refinery_competitiveness": 1},
)
def blue_refinery_inno_switch():
    return if_then_else(blue_refinery_competitiveness() > 0.5, lambda: 1, lambda: 0)


@component.add(
    name="Blue refinery innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "refinery_reinvestment": 1,
        "innovators": 1,
        "blue_refinery_inno_switch": 1,
        "sum_refining": 2,
        "blue_refinery": 1,
    },
)
def blue_refinery_innovators():
    return (
        refinery_reinvestment()
        * innovators()
        * blue_refinery_inno_switch()
        * (sum_refining() - blue_refinery())
        / sum_refining()
    )


@component.add(
    name="Blue refinery investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"blue_refinery_innovators": 1, "blue_refinery_imitators": 1},
)
def blue_refinery_investment():
    return blue_refinery_innovators() + blue_refinery_imitators()


@component.add(
    name="Blue refinery investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"refinery_equalizer": 1, "blue_refinery_level": 1},
)
def blue_refinery_investment_level():
    return refinery_equalizer() * blue_refinery_level()


@component.add(
    name="Blue refinery level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "blue_refinery_competitiveness": 1,
        "cross_innovation": 1,
        "blue_refinery": 1,
        "sum_refining": 1,
    },
)
def blue_refinery_level():
    return (
        1
        / (1 + np.exp(slope() * (cross_innovation() - blue_refinery_competitiveness())))
        * blue_refinery()
        / sum_refining()
    )


@component.add(
    name="Green refinery",
    units="MT H2",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_green_refinery": 1},
    other_deps={
        "_integ_green_refinery": {
            "initial": {},
            "step": {"green_refinery_investment": 1, "green_refinery_decay": 1},
        }
    },
)
def green_refinery():
    return _integ_green_refinery()


_integ_green_refinery = Integ(
    lambda: green_refinery_investment() - green_refinery_decay(),
    lambda: 0,
    "_integ_green_refinery",
)


@component.add(
    name="Green refinery competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"blue_h2_price": 1, "green_h2_price": 2, "grey_h2_price": 1},
)
def green_refinery_competitiveness():
    return np.minimum(
        blue_h2_price() / green_h2_price(), grey_h2_price() / green_h2_price()
    )


@component.add(
    name="Green refinery decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_refinery": 1, "aec_lifetime": 1},
)
def green_refinery_decay():
    return green_refinery() / aec_lifetime()


@component.add(
    name="Green refinery imitators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"refinery_reinvestment": 1, "green_refinery_investment_level": 1},
)
def green_refinery_imitators():
    return refinery_reinvestment() * green_refinery_investment_level()


@component.add(
    name="Green refinery inno switch",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_refinery_competitiveness": 1},
)
def green_refinery_inno_switch():
    return if_then_else(green_refinery_competitiveness() > 0.5, lambda: 1, lambda: 0)


@component.add(
    name="Green refinery innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "refinery_reinvestment": 1,
        "innovators": 1,
        "green_refinery_inno_switch": 1,
        "sum_refining": 2,
        "green_refinery": 1,
    },
)
def green_refinery_innovators():
    return (
        refinery_reinvestment()
        * innovators()
        * green_refinery_inno_switch()
        * (sum_refining() - green_refinery())
        / sum_refining()
    )


@component.add(
    name="Green refinery investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_refinery_imitators": 1, "green_refinery_innovators": 1},
)
def green_refinery_investment():
    return green_refinery_imitators() + green_refinery_innovators()


@component.add(
    name="Green refinery investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"refinery_equalizer": 1, "green_refinery_level": 1},
)
def green_refinery_investment_level():
    return refinery_equalizer() * green_refinery_level()


@component.add(
    name="Green refinery level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "green_refinery_competitiveness": 1,
        "cross_innovation": 1,
        "green_refinery": 1,
        "sum_refining": 1,
    },
)
def green_refinery_level():
    return (
        1
        / (
            1
            + np.exp(slope() * (cross_innovation() - green_refinery_competitiveness()))
        )
        * green_refinery()
        / sum_refining()
    )


@component.add(
    name="Grey refinery",
    units="MT NH3",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_grey_refinery": 1},
    other_deps={
        "_integ_grey_refinery": {
            "initial": {"refinery_consumption": 1},
            "step": {"grey_refinery_investment": 1, "grey_refinery_decay": 1},
        }
    },
)
def grey_refinery():
    return _integ_grey_refinery()


_integ_grey_refinery = Integ(
    lambda: grey_refinery_investment() - grey_refinery_decay(),
    lambda: refinery_consumption(),
    "_integ_grey_refinery",
)


@component.add(
    name="Grey refinery competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"blue_h2_price": 1, "grey_h2_price": 2, "green_h2_price": 1},
)
def grey_refinery_competitiveness():
    return np.minimum(
        blue_h2_price() / grey_h2_price(), green_h2_price() / grey_h2_price()
    )


@component.add(
    name="Grey refinery decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"grey_refinery": 1, "smr_lifetime": 1},
)
def grey_refinery_decay():
    return grey_refinery() / smr_lifetime()


@component.add(
    name="Grey refinery investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"grey_refinery_investment_level": 1, "refinery_reinvestment": 1},
)
def grey_refinery_investment():
    return grey_refinery_investment_level() * refinery_reinvestment()


@component.add(
    name="Grey refinery investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"refinery_equalizer": 1, "grey_refinery_level": 1},
)
def grey_refinery_investment_level():
    return refinery_equalizer() * grey_refinery_level()


@component.add(
    name="Grey refinery level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "cross_conventional": 1,
        "grey_refinery_competitiveness": 1,
        "grey_refinery": 1,
        "sum_refining": 1,
    },
)
def grey_refinery_level():
    return (
        1
        / (
            1
            + np.exp(slope() * (cross_conventional() - grey_refinery_competitiveness()))
        )
        * grey_refinery()
        / sum_refining()
    )


@component.add(
    name="Refinery consumption",
    units="MT H2",
    comp_type="Constant",
    comp_subtype="Normal",
)
def refinery_consumption():
    """
    2.4 MT/year - assumed constant moving forward. https://www.petrochemistry.eu/wp-content/uploads/2021/03/Petrochemicals_Pap er_hydrogen-1.pdf
    """
    return 2.4


@component.add(
    name="Refinery equalizer",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "grey_refinery_level": 1,
        "green_refinery_level": 1,
        "blue_refinery_level": 1,
    },
)
def refinery_equalizer():
    return 1 / (grey_refinery_level() + green_refinery_level() + blue_refinery_level())


@component.add(
    name="refinery hydrogen demand",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_refinery": 1},
)
def refinery_hydrogen_demand():
    """
    Convert from MT to T NH3, then from T NH3 to T H2.
    """
    return green_refinery() * 10**6


@component.add(
    name="Refinery reinvestment",
    units="MT H2",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_refinery_reinvestment": 1},
    other_deps={
        "_integ_refinery_reinvestment": {
            "initial": {"refinery_consumption": 1, "smr_lifetime": 1},
            "step": {
                "blue_refinery_decay": 1,
                "green_refinery_decay": 1,
                "grey_refinery_decay": 1,
                "blue_refinery_investment": 1,
                "green_refinery_investment": 1,
                "grey_refinery_investment": 1,
            },
        }
    },
)
def refinery_reinvestment():
    return _integ_refinery_reinvestment()


_integ_refinery_reinvestment = Integ(
    lambda: blue_refinery_decay()
    + green_refinery_decay()
    + grey_refinery_decay()
    - blue_refinery_investment()
    - green_refinery_investment()
    - grey_refinery_investment(),
    lambda: refinery_consumption() / smr_lifetime(),
    "_integ_refinery_reinvestment",
)


@component.add(
    name="sum refining",
    units="MT H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"grey_refinery": 1, "green_refinery": 1, "blue_refinery": 1},
)
def sum_refining():
    return grey_refinery() + green_refinery() + blue_refinery()
