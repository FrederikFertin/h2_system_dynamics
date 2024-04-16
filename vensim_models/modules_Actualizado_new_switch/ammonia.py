"""
Module ammonia
Translated using PySD version 3.13.4
"""


@component.add(
    name="Blue competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"blue_h2_cost": 2, "green_h2_cost": 1, "grey_h2_cost": 1},
)
def blue_competitiveness():
    return np.maximum(blue_h2_cost() / green_h2_cost(), blue_h2_cost() / grey_h2_cost())


@component.add(
    name="Blue decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"blue_nh3": 1, "smr_lifetime": 1},
)
def blue_decay():
    return blue_nh3() / smr_lifetime()


@component.add(
    name="Blue H2 cost",
    units="€/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "smr_ccs_capex": 1,
        "smr_af": 1,
        "smr_ccs_opex": 1,
        "smr_operating_hours": 1,
        "smr_ccs_efficiency": 1,
        "gas_price": 1,
        "smr_ccs_emission_factor": 1,
        "carbon_tax": 1,
    },
)
def blue_h2_cost():
    """
    €/MJ NH3 [ [ [€/kgH2] / [kgNH3/kgH2] ] + [kWh/kgNH3 * €/kWh] ] / [MJ/kgNH3]
    """
    return (
        (
            smr_ccs_capex() * (smr_af() + smr_ccs_opex()) / smr_operating_hours()
            + (gas_price() / 1000 * 3.6) / smr_ccs_efficiency()
            + (carbon_tax() / 1000) * (smr_ccs_emission_factor() / 33.33)
        )
        * 33.33
        * 1000
    )


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
    return if_then_else(blue_competitiveness() < 2, lambda: 1, lambda: 0)


@component.add(
    name="Blue innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nh3_reinvestment": 1, "innovators": 1, "blue_inno_switch": 1},
)
def blue_innovators():
    return nh3_reinvestment() * innovators() * blue_inno_switch()


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
        "blue_competitiveness": 1,
        "blue_nh3": 2,
        "grey_nh3": 1,
        "green_nh3": 1,
    },
)
def blue_level():
    return (
        1
        / (1 + np.exp(10 * (blue_competitiveness() - 1.1)))
        * blue_nh3()
        / (grey_nh3() + green_nh3() + blue_nh3())
    )


@component.add(
    name="Blue NH3",
    units="GWh",
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
    name="check0",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"grey_nh3": 1, "green_nh3": 1, "blue_nh3": 1},
)
def check0():
    return grey_nh3() + green_nh3() + blue_nh3()


@component.add(
    name="fertilizer hydrogen demand",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_nh3": 1, "nh3h2": 1},
)
def fertilizer_hydrogen_demand():
    """
    Convert from GWh to GJ, then from GJ to tons fuel, then from tons fuel to tons H2. Example 1: MeOH cons. [GWh] * 3600 [GJ/GWh] / 19.9 [GJ/t] / 15.7 [t MeOH/t H2] Example 2: NH3 cons. [GWh] * 3600 [GJ/GWh] / 18.6 [GJ/t] / 5.56 [t NH3/t H2]
    """
    return green_nh3() * 3600 / 18.6 / nh3h2()


@component.add(
    name="Green competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_h2_cost": 2, "blue_h2_cost": 1, "grey_h2_cost": 1},
)
def green_competitiveness():
    return np.maximum(
        green_h2_cost() / blue_h2_cost(), green_h2_cost() / grey_h2_cost()
    )


@component.add(
    name="Green decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "green_nh3": 1,
        "electrolyser_lifetime": 1,
        "electroliser_average_working_hours": 1,
    },
)
def green_decay():
    return green_nh3() / (
        electrolyser_lifetime() / electroliser_average_working_hours()
    )


@component.add(
    name="Green H2 cost",
    units="€/t",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hydrogen_price": 1},
)
def green_h2_cost():
    """
    €/MJ MeOH [ [kgBM/kgMeOH] * [€/GJ] * [MJ/kgBM ] / [MJ/GJ] + [€/kgH2] / [kgMeOH/kgH2] + [€/kWh * kWh/kgMeOH] ] / [MJ/kgMeOH]
    """
    return hydrogen_price() * 1000


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
    return if_then_else(green_competitiveness() < 2, lambda: 1, lambda: 0)


@component.add(
    name="Green innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nh3_reinvestment": 1, "innovators": 1, "green_inno_switch": 1},
)
def green_innovators():
    return nh3_reinvestment() * innovators() * green_inno_switch()


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
        "green_competitiveness": 1,
        "green_nh3": 2,
        "grey_nh3": 1,
        "blue_nh3": 1,
    },
)
def green_level():
    return (
        1
        / (1 + np.exp(10 * (green_competitiveness() - 1.1)))
        * green_nh3()
        / (grey_nh3() + green_nh3() + blue_nh3())
    )


@component.add(
    name="Green NH3",
    units="GWh",
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
    depends_on={"grey_h2_cost": 2, "blue_h2_cost": 1, "green_h2_cost": 1},
)
def grey_competitiveness():
    return np.maximum(grey_h2_cost() / blue_h2_cost(), grey_h2_cost() / green_h2_cost())


@component.add(
    name="Grey decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"grey_nh3": 1, "smr_lifetime": 1},
)
def grey_decay():
    return grey_nh3() / smr_lifetime()


@component.add(
    name="Grey H2 cost",
    units="€/t",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "smr_capex": 1,
        "smr_opex": 1,
        "smr_af": 1,
        "smr_operating_hours": 1,
        "smr_efficiency": 1,
        "gas_price": 1,
        "smr_emission_factor": 1,
        "carbon_tax": 1,
    },
)
def grey_h2_cost():
    """
    €/t grey H2
    """
    return (
        (
            smr_capex() * (smr_af() + smr_opex()) / smr_operating_hours()
            + (gas_price() / 1000 * 3.6) / smr_efficiency()
            + (carbon_tax() / 1000) * (smr_emission_factor() / 33.33)
        )
        * 33.33
        * 1000
    )


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
        "grey_competitiveness": 1,
        "grey_nh3": 2,
        "blue_nh3": 1,
        "green_nh3": 1,
    },
)
def grey_level():
    return (
        1
        / (1 + np.exp(10 * (grey_competitiveness() - 0.9)))
        * grey_nh3()
        / (grey_nh3() + green_nh3() + blue_nh3())
    )


@component.add(
    name="Grey NH3",
    units="GWh",
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
    name="SMR AF",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"discount_rate": 2, "smr_lifetime": 1},
)
def smr_af():
    return 1 / ((1 - (1 + discount_rate()) ** -smr_lifetime()) / discount_rate())


@component.add(name="SMR CAPEX", comp_type="Constant", comp_subtype="Normal")
def smr_capex():
    """
    €/kWH2
    """
    return 800


@component.add(
    name="SMR CCS CAPEX",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def smr_ccs_capex():
    """
    €/kWH2
    """
    return np.interp(time(), [2019, 2030, 2050], [1680, 1360, 1280])


@component.add(name="SMR CCS efficiency", comp_type="Constant", comp_subtype="Normal")
def smr_ccs_efficiency():
    return 0.69


@component.add(
    name="SMR CCS emission factor", comp_type="Constant", comp_subtype="Normal"
)
def smr_ccs_emission_factor():
    """
    1 kgCO2 / kgH2
    """
    return 1


@component.add(name="SMR CCS OPEX", comp_type="Constant", comp_subtype="Normal")
def smr_ccs_opex():
    """
    %/yr of CAPEX
    """
    return 0.047


@component.add(name="SMR efficiency", comp_type="Constant", comp_subtype="Normal")
def smr_efficiency():
    return 0.76


@component.add(name="SMR emission factor", comp_type="Constant", comp_subtype="Normal")
def smr_emission_factor():
    """
    8.9 kgCO2 / kgH2
    """
    return 8.9


@component.add(name="SMR lifetime", comp_type="Constant", comp_subtype="Normal")
def smr_lifetime():
    return 25


@component.add(name="SMR operating hours", comp_type="Constant", comp_subtype="Normal")
def smr_operating_hours():
    return 8500


@component.add(name="SMR OPEX", comp_type="Constant", comp_subtype="Normal")
def smr_opex():
    """
    %/yr of CAPEX
    """
    return 0.047
