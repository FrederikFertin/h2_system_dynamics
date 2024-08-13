"""
Module industrial_ht_heat
Translated using PySD version 3.14.0
"""

@component.add(
    name="Biogas NM",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_biogas_nm": 1},
    other_deps={
        "_integ_biogas_nm": {
            "initial": {},
            "step": {"biogas_nm_investment": 1, "biogas_nm_decay": 1},
        }
    },
)
def biogas_nm():
    return _integ_biogas_nm()


_integ_biogas_nm = Integ(
    lambda: biogas_nm_investment() - biogas_nm_decay(), lambda: 0, "_integ_biogas_nm"
)


@component.add(
    name="Biogas NM competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "blue_ng_cost": 1,
        "biogas_cost": 3,
        "green_h2_nm_cost": 1,
        "grey_ng_cost": 1,
    },
)
def biogas_nm_competitiveness():
    return np.minimum(
        np.minimum(blue_ng_cost() / biogas_cost(), green_h2_nm_cost() / biogas_cost()),
        grey_ng_cost() / biogas_cost(),
    )


@component.add(
    name="Biogas NM decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"biogas_nm": 1, "gas_lockin_factor": 1},
)
def biogas_nm_decay():
    return biogas_nm() / gas_lockin_factor()


@component.add(
    name="Biogas NM imitators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"biogas_nm_investment_level": 1, "nm_reinvestment": 1},
)
def biogas_nm_imitators():
    return biogas_nm_investment_level() * nm_reinvestment()


@component.add(
    name="Biogas NM inno switch",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_biogas_nm_inno_switch": 1},
    other_deps={
        "_smooth_biogas_nm_inno_switch": {
            "initial": {
                "biogas_nm_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
            "step": {
                "biogas_nm_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
        }
    },
)
def biogas_nm_inno_switch():
    return _smooth_biogas_nm_inno_switch()


_smooth_biogas_nm_inno_switch = Smooth(
    lambda: if_then_else(
        biogas_nm_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            biogas_nm_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 2,
    lambda: if_then_else(
        biogas_nm_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            biogas_nm_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 3,
    "_smooth_biogas_nm_inno_switch",
)


@component.add(
    name="Biogas NM innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nm_reinvestment": 1,
        "innovators": 1,
        "biogas_nm_inno_switch": 1,
        "sum_nm": 2,
        "biogas_nm": 1,
    },
)
def biogas_nm_innovators():
    return (
        nm_reinvestment()
        * innovators()
        * biogas_nm_inno_switch()
        * (sum_nm() - biogas_nm())
        / sum_nm()
    )


@component.add(
    name="Biogas NM investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"biogas_nm_imitators": 1, "biogas_nm_innovators": 1},
)
def biogas_nm_investment():
    return biogas_nm_imitators() + biogas_nm_innovators()


@component.add(
    name="Biogas NM investment level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"biogas_nm_level": 1, "nm_equalizer": 1},
)
def biogas_nm_investment_level():
    return biogas_nm_level() * nm_equalizer()


@component.add(
    name="Biogas NM level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "cross_innovation": 1,
        "biogas_nm_competitiveness": 1,
        "biogas_nm": 1,
        "sum_nm": 1,
    },
)
def biogas_nm_level():
    return (
        1
        / (1 + np.exp(slope() * (cross_innovation() - biogas_nm_competitiveness())))
        * biogas_nm()
        / sum_nm()
    )


@component.add(
    name="Blue NG NM",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_blue_ng_nm": 1},
    other_deps={
        "_integ_blue_ng_nm": {
            "initial": {},
            "step": {"blue_ng_nm_investment": 1, "blue_ng_nm_decay": 1},
        }
    },
)
def blue_ng_nm():
    return _integ_blue_ng_nm()


_integ_blue_ng_nm = Integ(
    lambda: blue_ng_nm_investment() - blue_ng_nm_decay(), lambda: 0, "_integ_blue_ng_nm"
)


@component.add(
    name="Blue NG NM competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "grey_ng_cost": 1,
        "blue_ng_cost": 3,
        "green_h2_nm_cost": 1,
        "biogas_cost": 1,
    },
)
def blue_ng_nm_competitiveness():
    return np.minimum(
        np.minimum(
            grey_ng_cost() / blue_ng_cost(), green_h2_nm_cost() / blue_ng_cost()
        ),
        biogas_cost() / blue_ng_cost(),
    )


@component.add(
    name="Blue NG NM decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"blue_ng_nm": 1, "cc_lifetime": 1},
)
def blue_ng_nm_decay():
    return blue_ng_nm() / (cc_lifetime() / 2)


@component.add(
    name="Blue NG NM imitators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nm_reinvestment": 1, "blue_ng_nm_investment_level": 1},
)
def blue_ng_nm_imitators():
    return nm_reinvestment() * blue_ng_nm_investment_level()


@component.add(
    name="Blue NG NM inno switch",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_blue_ng_nm_inno_switch": 1},
    other_deps={
        "_smooth_blue_ng_nm_inno_switch": {
            "initial": {
                "blue_ng_nm_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
            "step": {
                "blue_ng_nm_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
        }
    },
)
def blue_ng_nm_inno_switch():
    return _smooth_blue_ng_nm_inno_switch()


_smooth_blue_ng_nm_inno_switch = Smooth(
    lambda: if_then_else(
        blue_ng_nm_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            blue_ng_nm_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 2,
    lambda: if_then_else(
        blue_ng_nm_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            blue_ng_nm_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 3,
    "_smooth_blue_ng_nm_inno_switch",
)


@component.add(
    name="Blue NG NM innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nm_reinvestment": 1,
        "innovators": 1,
        "blue_ng_nm_inno_switch": 1,
        "blue_ng_nm": 1,
        "sum_nm": 2,
    },
)
def blue_ng_nm_innovators():
    return (
        nm_reinvestment()
        * innovators()
        * blue_ng_nm_inno_switch()
        * (sum_nm() - blue_ng_nm())
        / sum_nm()
    )


@component.add(
    name="Blue NG NM investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"blue_ng_nm_innovators": 1, "blue_ng_nm_imitators": 1},
)
def blue_ng_nm_investment():
    return blue_ng_nm_innovators() + blue_ng_nm_imitators()


@component.add(
    name="Blue NG NM investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nm_equalizer": 1, "blue_ng_nm_level": 1},
)
def blue_ng_nm_investment_level():
    return nm_equalizer() * blue_ng_nm_level()


@component.add(
    name="Blue NG NM level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "cross_innovation": 1,
        "blue_ng_nm_competitiveness": 1,
        "blue_ng_nm": 1,
        "sum_nm": 1,
    },
)
def blue_ng_nm_level():
    return (
        1
        / (1 + np.exp(slope() * (cross_innovation() - blue_ng_nm_competitiveness())))
        * blue_ng_nm()
        / sum_nm()
    )


@component.add(
    name="ctrl NM",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"k_p": 1, "error_nm": 1, "errorint_nm": 1},
)
def ctrl_nm():
    return k_p() * error_nm() + errorint_nm()


@component.add(
    name="demand change NM",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ctrl_nm": 1},
)
def demand_change_nm():
    return ctrl_nm()


@component.add(
    name="error NM",
    units="e",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nm_gas_consumption": 1, "sum_nm": 1},
)
def error_nm():
    return nm_gas_consumption() - sum_nm()


@component.add(
    name="errorint NM",
    units="e",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_errorint_nm": 1},
    other_deps={
        "_integ_errorint_nm": {"initial": {}, "step": {"k_i": 1, "error_nm": 1}}
    },
)
def errorint_nm():
    return _integ_errorint_nm()


_integ_errorint_nm = Integ(lambda: k_i() * error_nm(), lambda: 0, "_integ_errorint_nm")


@component.add(
    name="Gas lockin factor", units="years", comp_type="Constant", comp_subtype="Normal"
)
def gas_lockin_factor():
    """
    equivalent lifetime of technology - based on assumptions that the same furnaces can run on NG / blue NG / H2.
    """
    return 5


@component.add(
    name="Green H2 NM cost",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_h2_cost": 1},
)
def green_h2_nm_cost():
    """
    Converts the €/kg H2 price to a €/GJ H2 cost.
    """
    return green_h2_cost() / 120 * 1000


@component.add(
    name="H2 NM",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_h2_nm": 1},
    other_deps={
        "_integ_h2_nm": {
            "initial": {},
            "step": {"h2_nm_investment": 1, "h2_nm_decay": 1},
        }
    },
)
def h2_nm():
    return _integ_h2_nm()


_integ_h2_nm = Integ(
    lambda: h2_nm_investment() - h2_nm_decay(), lambda: 0, "_integ_h2_nm"
)


@component.add(
    name="H2 NM competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "blue_ng_cost": 1,
        "green_h2_nm_cost": 3,
        "grey_ng_cost": 1,
        "biogas_cost": 1,
    },
)
def h2_nm_competitiveness():
    return np.minimum(
        np.minimum(
            blue_ng_cost() / green_h2_nm_cost(), grey_ng_cost() / green_h2_nm_cost()
        ),
        biogas_cost() / green_h2_nm_cost(),
    )


@component.add(
    name="H2 NM decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"h2_nm": 1, "gas_lockin_factor": 1},
)
def h2_nm_decay():
    return h2_nm() / gas_lockin_factor()


@component.add(
    name="H2 NM imitators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nm_reinvestment": 1, "h2_nm_investment_level": 1},
)
def h2_nm_imitators():
    return nm_reinvestment() * h2_nm_investment_level()


@component.add(
    name="H2 NM inno switch",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_h2_nm_inno_switch": 1},
    other_deps={
        "_smooth_h2_nm_inno_switch": {
            "initial": {
                "h2_nm_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
            "step": {
                "h2_nm_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
        }
    },
)
def h2_nm_inno_switch():
    return _smooth_h2_nm_inno_switch()


_smooth_h2_nm_inno_switch = Smooth(
    lambda: if_then_else(
        h2_nm_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            h2_nm_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 2,
    lambda: if_then_else(
        h2_nm_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            h2_nm_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 3,
    "_smooth_h2_nm_inno_switch",
)


@component.add(
    name="H2 NM innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nm_reinvestment": 1,
        "innovators": 1,
        "h2_nm_inno_switch": 1,
        "sum_nm": 2,
        "h2_nm": 1,
    },
)
def h2_nm_innovators():
    return (
        nm_reinvestment()
        * innovators()
        * h2_nm_inno_switch()
        * (sum_nm() - h2_nm())
        / sum_nm()
    )


@component.add(
    name="H2 NM investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"h2_nm_imitators": 1, "h2_nm_innovators": 1},
)
def h2_nm_investment():
    return h2_nm_imitators() + h2_nm_innovators()


@component.add(
    name="H2 NM investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nm_equalizer": 1, "h2_nm_level": 1},
)
def h2_nm_investment_level():
    return nm_equalizer() * h2_nm_level()


@component.add(
    name="H2 NM level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "h2_nm_competitiveness": 1,
        "cross_innovation": 1,
        "h2_nm": 1,
        "sum_nm": 1,
    },
)
def h2_nm_level():
    return (
        1
        / (1 + np.exp(slope() * (cross_innovation() - h2_nm_competitiveness())))
        * h2_nm()
        / sum_nm()
    )


@component.add(
    name="high temperature average cost",
    units="€/kgH2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biogas_nm": 1,
        "biogas_cost": 1,
        "blue_ng_cost": 1,
        "blue_ng_nm": 1,
        "grey_ng_cost": 1,
        "ng_nm": 1,
        "green_h2_nm_cost": 1,
        "h2_nm": 1,
        "sum_nm": 1,
    },
)
def high_temperature_average_cost():
    """
    €/kgH2 equivalent heat.
    """
    return (
        (
            biogas_nm() * biogas_cost()
            + blue_ng_nm() * blue_ng_cost()
            + ng_nm() * grey_ng_cost()
            + h2_nm() * green_h2_nm_cost()
        )
        / 1000
        * 120
        / sum_nm()
    )


@component.add(
    name="high temperature biomass demand",
    units="GWh Biomass",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"biogas_nm": 1, "biogas_biomass_usage": 1},
)
def high_temperature_biomass_demand():
    return biogas_nm() * biogas_biomass_usage()


@component.add(
    name="high temperature emissions",
    units="tCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ng_nm": 1,
        "cc_capture_rate": 1,
        "blue_ng_nm": 1,
        "gas_emission_factor": 1,
    },
)
def high_temperature_emissions():
    return (
        (ng_nm() + blue_ng_nm() * (1 - cc_capture_rate()))
        * gas_emission_factor()
        * 3600
    )


@component.add(
    name="high temperature hydrogen demand",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"h2_nm": 1, "h2_lhv": 1},
)
def high_temperature_hydrogen_demand():
    """
    Convert from GWh to tons.
    """
    return h2_nm() * 1000 / h2_lhv()


@component.add(
    name="NG NM",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_ng_nm": 1},
    other_deps={
        "_integ_ng_nm": {
            "initial": {"nm_gas_consumption": 1},
            "step": {"ng_nm_investment": 1, "ng_nm_decay": 1},
        }
    },
)
def ng_nm():
    return _integ_ng_nm()


_integ_ng_nm = Integ(
    lambda: ng_nm_investment() - ng_nm_decay(),
    lambda: nm_gas_consumption(),
    "_integ_ng_nm",
)


@component.add(
    name="NG NM competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "blue_ng_cost": 1,
        "grey_ng_cost": 3,
        "green_h2_nm_cost": 1,
        "biogas_cost": 1,
    },
)
def ng_nm_competitiveness():
    return np.minimum(
        np.minimum(
            blue_ng_cost() / grey_ng_cost(), green_h2_nm_cost() / grey_ng_cost()
        ),
        biogas_cost() / grey_ng_cost(),
    )


@component.add(
    name="NG NM decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ng_nm": 1, "gas_lockin_factor": 1},
)
def ng_nm_decay():
    return ng_nm() / gas_lockin_factor()


@component.add(
    name="NG NM investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ng_nm_investment_level": 1, "nm_reinvestment": 1},
)
def ng_nm_investment():
    return ng_nm_investment_level() * nm_reinvestment()


@component.add(
    name="NG NM investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nm_equalizer": 1, "ng_nm_level": 1},
)
def ng_nm_investment_level():
    return nm_equalizer() * ng_nm_level()


@component.add(
    name="NG NM level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "cross_conventional": 1,
        "ng_nm_competitiveness": 1,
        "ng_nm": 1,
        "sum_nm": 1,
    },
)
def ng_nm_level():
    return (
        1
        / (1 + np.exp(slope() * (cross_conventional() - ng_nm_competitiveness())))
        * ng_nm()
        / sum_nm()
    )


@component.add(
    name="NM equalizer",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ng_nm_level": 1,
        "h2_nm_level": 1,
        "blue_ng_nm_level": 1,
        "biogas_nm_level": 1,
    },
)
def nm_equalizer():
    return 1 / (ng_nm_level() + h2_nm_level() + blue_ng_nm_level() + biogas_nm_level())


@component.add(
    name="NM gas consumption", units="GWh", comp_type="Constant", comp_subtype="Normal"
)
def nm_gas_consumption():
    """
    207 TWh/year - assumed constant moving forward.
    """
    return 207000


@component.add(
    name="NM reinvestment",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_nm_reinvestment": 1},
    other_deps={
        "_integ_nm_reinvestment": {
            "initial": {"nm_gas_consumption": 1, "gas_lockin_factor": 1},
            "step": {
                "biogas_nm_decay": 1,
                "blue_ng_nm_decay": 1,
                "demand_change_nm": 1,
                "h2_nm_decay": 1,
                "ng_nm_decay": 1,
                "biogas_nm_investment": 1,
                "blue_ng_nm_investment": 1,
                "h2_nm_investment": 1,
                "ng_nm_investment": 1,
            },
        }
    },
)
def nm_reinvestment():
    return _integ_nm_reinvestment()


_integ_nm_reinvestment = Integ(
    lambda: biogas_nm_decay()
    + blue_ng_nm_decay()
    + demand_change_nm()
    + h2_nm_decay()
    + ng_nm_decay()
    - biogas_nm_investment()
    - blue_ng_nm_investment()
    - h2_nm_investment()
    - ng_nm_investment(),
    lambda: nm_gas_consumption() / gas_lockin_factor() * 0.8,
    "_integ_nm_reinvestment",
)


@component.add(
    name="sum NM",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ng_nm": 1, "h2_nm": 1, "blue_ng_nm": 1, "biogas_nm": 1},
)
def sum_nm():
    return ng_nm() + h2_nm() + blue_ng_nm() + biogas_nm()
