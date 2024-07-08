"""
Module industrial_ht_heat
Translated using PySD version 3.14.0
"""

@component.add(
    name="Biogas NM",
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
        "biogas_price": 3,
        "green_h2_nm_cost": 1,
        "grey_ng_cost": 1,
    },
)
def biogas_nm_competitiveness():
    return np.minimum(
        np.minimum(
            blue_ng_cost() / biogas_price(), green_h2_nm_cost() / biogas_price()
        ),
        grey_ng_cost() / biogas_price(),
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
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"biogas_nm_competitiveness": 1},
)
def biogas_nm_inno_switch():
    return if_then_else(biogas_nm_competitiveness() > 0.5, lambda: 1, lambda: 0)


@component.add(
    name="Biogas NM innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nm_reinvestment": 1,
        "innovators": 1,
        "biogas_nm_inno_switch": 1,
        "biogas_nm": 1,
        "sum_nm": 2,
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
        "biogas_nm_competitiveness": 1,
        "cross_innovation": 1,
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
    units="MT NH3",
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
        "biogas_price": 1,
    },
)
def blue_ng_nm_competitiveness():
    return np.minimum(
        np.minimum(
            grey_ng_cost() / blue_ng_cost(), green_h2_nm_cost() / blue_ng_cost()
        ),
        biogas_price() / blue_ng_cost(),
    )


@component.add(
    name="Blue NG NM decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"blue_ng_nm": 1, "cc_lifetime": 1},
)
def blue_ng_nm_decay():
    return blue_ng_nm() / cc_lifetime()


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
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"blue_ng_nm_competitiveness": 1},
)
def blue_ng_nm_inno_switch():
    return if_then_else(blue_ng_nm_competitiveness() > 0.5, lambda: 1, lambda: 0)


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
        "blue_ng_nm_competitiveness": 1,
        "cross_innovation": 1,
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
    name="Gas lockin factor", units="years", comp_type="Constant", comp_subtype="Normal"
)
def gas_lockin_factor():
    """
    equivalent lifetime of technology - based on assumptions that the same furnaces can run on NG / blue NG / H2.
    """
    return 12


@component.add(
    name="Green H2 NM cost",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_h2_price": 1},
)
def green_h2_nm_cost():
    """
    Converts the €/kg H2 price to a €/GJ H2 cost.
    """
    return green_h2_price() / 120 * 1000


@component.add(
    name="H2 NM",
    units="MT NH3",
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
        "biogas_price": 1,
    },
)
def h2_nm_competitiveness():
    return np.minimum(
        np.minimum(
            blue_ng_cost() / green_h2_nm_cost(), grey_ng_cost() / green_h2_nm_cost()
        ),
        biogas_price() / green_h2_nm_cost(),
    )


@component.add(
    name="H2 NM decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"h2_nm": 1, "aec_lifetime": 1},
)
def h2_nm_decay():
    return h2_nm() / aec_lifetime()


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
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"h2_nm_competitiveness": 1},
)
def h2_nm_inno_switch():
    return if_then_else(h2_nm_competitiveness() > 0.5, lambda: 1, lambda: 0)


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
    name="NG NM",
    units="MT NH3",
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
        "biogas_price": 1,
    },
)
def ng_nm_competitiveness():
    return np.minimum(
        np.minimum(
            blue_ng_cost() / grey_ng_cost(), green_h2_nm_cost() / grey_ng_cost()
        ),
        biogas_price() / grey_ng_cost(),
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
    136 TWh/year - assumed constant moving forward.
    """
    return 136000


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
    + h2_nm_decay()
    + ng_nm_decay()
    - biogas_nm_investment()
    - blue_ng_nm_investment()
    - h2_nm_investment()
    - ng_nm_investment(),
    lambda: nm_gas_consumption() / gas_lockin_factor(),
    "_integ_nm_reinvestment",
)


@component.add(
    name="nonmetallic industry hydrogen demand",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"h2_nm": 1, "lhv_h2": 1},
)
def nonmetallic_industry_hydrogen_demand():
    """
    Convert from GWh to tons.
    """
    return h2_nm() * 1000 / lhv_h2()


@component.add(
    name="sum NM",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ng_nm": 1, "h2_nm": 1, "blue_ng_nm": 1, "biogas_nm": 1},
)
def sum_nm():
    return ng_nm() + h2_nm() + blue_ng_nm() + biogas_nm()
