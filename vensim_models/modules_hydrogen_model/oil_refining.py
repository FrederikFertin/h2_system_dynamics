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
    name="Blue refinery CO2 WTP",
    units="€/tCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"blue_h2_co2_wtp": 1},
)
def blue_refinery_co2_wtp():
    return blue_h2_co2_wtp()


@component.add(
    name="Blue refinery competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"grey_h2_cost": 1, "blue_h2_cost": 2, "refinery_h2_cost": 1},
)
def blue_refinery_competitiveness():
    """
    Old: MIN( Grey H2 cost / Blue H2 cost , refinery H2 cost / Blue H2 cost )
    """
    return np.minimum(
        grey_h2_cost() / blue_h2_cost(), refinery_h2_cost() / blue_h2_cost()
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
    name="blue refinery emissions",
    units="tCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"blue_refinery": 1, "cc_capture_rate": 1, "smr_emission_factor": 1},
)
def blue_refinery_emissions():
    return blue_refinery() * (1 - cc_capture_rate()) * smr_emission_factor() * 10**6


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
    depends_on={
        "blue_refinery_competitiveness": 2,
        "inno_switch_level": 1,
        "early_switch_level": 1,
    },
)
def blue_refinery_inno_switch():
    return if_then_else(
        blue_refinery_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            blue_refinery_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    )


@component.add(
    name="Blue refinery innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "refinery_reinvestment": 1,
        "innovators": 1,
        "blue_refinery_inno_switch": 1,
        "blue_refinery": 1,
        "sum_refining": 2,
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
        "cross": 1,
        "blue_refinery": 1,
        "sum_refining": 1,
    },
)
def blue_refinery_level():
    return (
        1
        / (1 + np.exp(slope() * (cross() - blue_refinery_competitiveness())))
        * (blue_refinery() / sum_refining()) ** 0.8
    )


@component.add(
    name="ctrl refinery",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"k_p": 1, "error_refinery": 1, "errorint_refinery": 1},
)
def ctrl_refinery():
    return k_p() * error_refinery() + errorint_refinery()


@component.add(
    name="demand change refinery",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ctrl_refinery": 1},
)
def demand_change_refinery():
    return ctrl_refinery()


@component.add(
    name="error refinery",
    units="e",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"refinery_consumption": 1, "sum_refining": 1},
)
def error_refinery():
    return refinery_consumption() - sum_refining()


@component.add(
    name="errorint refinery",
    units="e",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_errorint_refinery": 1},
    other_deps={
        "_integ_errorint_refinery": {
            "initial": {"refinery_consumption": 1},
            "step": {"k_i": 1, "error_refinery": 1},
        }
    },
)
def errorint_refinery():
    return _integ_errorint_refinery()


_integ_errorint_refinery = Integ(
    lambda: k_i() * error_refinery(),
    lambda: -refinery_consumption() / 50,
    "_integ_errorint_refinery",
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
    depends_on={"blue_h2_cost": 1, "refinery_h2_cost": 2, "grey_h2_cost": 1},
)
def green_refinery_competitiveness():
    """
    MIN( Blue H2 cost / refinery H2 cost , Grey H2 cost / refinery H2 cost )
    """
    return np.minimum(
        blue_h2_cost() / refinery_h2_cost(), grey_h2_cost() / refinery_h2_cost()
    )


@component.add(
    name="Green refinery decay",
    units="MT H2/Year",
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
    depends_on={
        "green_refinery_competitiveness": 2,
        "inno_switch_level": 1,
        "early_switch_level": 1,
    },
)
def green_refinery_inno_switch():
    return if_then_else(
        green_refinery_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            green_refinery_competitiveness() > early_switch_level(),
            lambda: 3,
            lambda: 1,
        ),
        lambda: 0,
    )


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
        "cross": 1,
        "sum_refining": 1,
        "green_refinery": 1,
    },
)
def green_refinery_level():
    return (
        1
        / (1 + np.exp(slope() * (cross() - green_refinery_competitiveness())))
        * (green_refinery() / sum_refining()) ** 0.8
    )


@component.add(
    name="Grey refinery",
    units="MT H2",
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
    name="Grey refinery CO2 WTP",
    units="€/tCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"grey_h2_co2_wtp": 1},
)
def grey_refinery_co2_wtp():
    return grey_h2_co2_wtp()


@component.add(
    name="Grey refinery competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"blue_h2_cost": 1, "grey_h2_cost": 2, "refinery_h2_cost": 1},
)
def grey_refinery_competitiveness():
    return np.minimum(
        blue_h2_cost() / grey_h2_cost(), refinery_h2_cost() / grey_h2_cost()
    )


@component.add(
    name="Grey refinery decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "grey_refinery": 1,
        "grey_refinery_early_decommission_rate": 1,
        "smr_lifetime": 1,
    },
)
def grey_refinery_decay():
    return grey_refinery() * (
        grey_refinery_early_decommission_rate() + 1 / smr_lifetime()
    )


@component.add(
    name="Grey refinery early decommission rate",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"grey_refinery_competitiveness": 1},
)
def grey_refinery_early_decommission_rate():
    return 1 / (1 + np.exp(-5 * -grey_refinery_competitiveness())) * 0


@component.add(
    name="grey refinery emissions",
    units="tCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"grey_refinery": 1, "smr_emission_factor": 1},
)
def grey_refinery_emissions():
    return grey_refinery() * smr_emission_factor() * 10**6


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
        "grey_refinery_competitiveness": 1,
        "cross": 1,
        "grey_refinery": 1,
        "sum_refining": 1,
    },
)
def grey_refinery_level():
    return (
        1
        / (1 + np.exp(slope() * (cross() - grey_refinery_competitiveness())))
        * (grey_refinery() / sum_refining()) ** 0.8
    )


@component.add(
    name="refinery average cost",
    units="€/kgH2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "blue_refinery": 1,
        "blue_h2_cost": 1,
        "green_refinery": 1,
        "refinery_h2_cost": 1,
        "grey_refinery": 1,
        "grey_h2_cost": 1,
        "sum_refining": 1,
    },
)
def refinery_average_cost():
    return (
        blue_refinery() * blue_h2_cost()
        + green_refinery() * refinery_h2_cost()
        + grey_refinery() * grey_h2_cost()
    ) / sum_refining()


@component.add(
    name="Refinery consumption",
    units="MT H2",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def refinery_consumption():
    """
    2.4 MT/year - assumed constant moving forward. https://www.petrochemistry.eu/wp-content/uploads/2021/03/Petrochemicals_Pap er_hydrogen-1.pdf
    """
    return np.interp(
        time(),
        [
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
            2.4,
            2.352,
            2.30496,
            2.25886,
            2.21368,
            2.16941,
            2.12602,
            2.0835,
            2.04183,
            2.00099,
            1.96097,
            1.92176,
            1.88332,
            1.84565,
            1.80874,
            1.77257,
            1.73711,
            1.70237,
            1.66832,
            1.63496,
            1.60226,
            1.57021,
            1.53881,
            1.50803,
            1.47787,
            1.44832,
            1.41935,
            1.39096,
            1.36314,
        ],
    )


@component.add(
    name="refinery emissions",
    units="tCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"blue_refinery_emissions": 1, "grey_refinery_emissions": 1},
)
def refinery_emissions():
    return blue_refinery_emissions() + grey_refinery_emissions()


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
    name="refinery grey and blue hydrogen demand",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"blue_refinery": 1, "grey_refinery": 1},
)
def refinery_grey_and_blue_hydrogen_demand():
    return (blue_refinery() + grey_refinery()) * 10**6


@component.add(
    name="refinery H2 WTP",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_h2_h2_wtp": 1},
)
def refinery_h2_wtp():
    return green_h2_h2_wtp()


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
                "demand_change_refinery": 1,
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
    + demand_change_refinery()
    + green_refinery_decay()
    + grey_refinery_decay()
    - blue_refinery_investment()
    - green_refinery_investment()
    - grey_refinery_investment(),
    lambda: refinery_consumption() / smr_lifetime() * 0.3,
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
