"""
Module methanol
Translated using PySD version 3.14.0
"""

@component.add(
    name="BioMeOH",
    units="MT",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_biomeoh": 1},
    other_deps={
        "_integ_biomeoh": {
            "initial": {},
            "step": {"biomeoh_investment": 1, "biomeoh_decay": 1},
        }
    },
)
def biomeoh():
    return _integ_biomeoh()


_integ_biomeoh = Integ(
    lambda: biomeoh_investment() - biomeoh_decay(), lambda: 0, "_integ_biomeoh"
)


@component.add(
    name="BioMeOH competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "blue_meoh_cost": 1,
        "green_biomeoh_cost": 3,
        "convmeoh_cost": 1,
        "green_emeoh_cost": 1,
    },
)
def biomeoh_competitiveness():
    return np.minimum(
        np.minimum(
            blue_meoh_cost() / green_biomeoh_cost(),
            convmeoh_cost() / green_biomeoh_cost(),
        ),
        green_emeoh_cost() / green_biomeoh_cost(),
    )


@component.add(
    name="BioMeOH decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"biomeoh": 1, "meoh_plant_lifetime": 1},
)
def biomeoh_decay():
    return biomeoh() / meoh_plant_lifetime()


@component.add(
    name="BioMeOH imitators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"meoh_reinvestment": 1, "biomeoh_investment_level": 1},
)
def biomeoh_imitators():
    return meoh_reinvestment() * biomeoh_investment_level()


@component.add(
    name="BioMeOH inno switch",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_biomeoh_inno_switch": 1},
    other_deps={
        "_smooth_biomeoh_inno_switch": {
            "initial": {
                "biomeoh_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
            "step": {
                "biomeoh_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
        }
    },
)
def biomeoh_inno_switch():
    return _smooth_biomeoh_inno_switch()


_smooth_biomeoh_inno_switch = Smooth(
    lambda: if_then_else(
        biomeoh_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            biomeoh_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 2,
    lambda: if_then_else(
        biomeoh_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            biomeoh_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 3,
    "_smooth_biomeoh_inno_switch",
)


@component.add(
    name="BioMeOH innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "meoh_reinvestment": 1,
        "innovators": 1,
        "biomeoh_inno_switch": 1,
        "biomeoh": 1,
        "sum_meoh": 2,
    },
)
def biomeoh_innovators():
    return (
        meoh_reinvestment()
        * innovators()
        * biomeoh_inno_switch()
        * (sum_meoh() - biomeoh())
        / sum_meoh()
    )


@component.add(
    name="BioMeOH investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"biomeoh_imitators": 1, "biomeoh_innovators": 1},
)
def biomeoh_investment():
    return biomeoh_imitators() + biomeoh_innovators()


@component.add(
    name="BioMeOH investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"equalizer_meoh": 1, "biomeoh_level": 1},
)
def biomeoh_investment_level():
    return equalizer_meoh() * biomeoh_level()


@component.add(
    name="BioMeOH level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "biomeoh_competitiveness": 1,
        "cross": 1,
        "biomeoh": 1,
        "sum_meoh": 1,
    },
)
def biomeoh_level():
    return (
        1
        / (1 + np.exp(slope() * (cross() - biomeoh_competitiveness())))
        * biomeoh()
        / sum_meoh()
    )


@component.add(
    name="Blue MeOH",
    units="MT",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_blue_meoh": 1},
    other_deps={
        "_integ_blue_meoh": {
            "initial": {},
            "step": {"blue_meoh_investment": 1, "blue_meoh_decay": 1},
        }
    },
)
def blue_meoh():
    return _integ_blue_meoh()


_integ_blue_meoh = Integ(
    lambda: blue_meoh_investment() - blue_meoh_decay(), lambda: 0, "_integ_blue_meoh"
)


@component.add(
    name="Blue MeOH competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "convmeoh_cost": 1,
        "blue_meoh_cost": 3,
        "green_biomeoh_cost": 1,
        "green_emeoh_cost": 1,
    },
)
def blue_meoh_competitiveness():
    return np.minimum(
        np.minimum(
            convmeoh_cost() / blue_meoh_cost(), green_biomeoh_cost() / blue_meoh_cost()
        ),
        green_emeoh_cost() / blue_meoh_cost(),
    )


@component.add(
    name="Blue MeOH decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"blue_meoh": 1, "meoh_plant_lifetime": 1},
)
def blue_meoh_decay():
    return blue_meoh() / meoh_plant_lifetime()


@component.add(
    name="Blue MeOH imitators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"meoh_reinvestment": 1, "blue_meoh_investment_level": 1},
)
def blue_meoh_imitators():
    return meoh_reinvestment() * blue_meoh_investment_level()


@component.add(
    name="Blue MeOH inno switch",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_blue_meoh_inno_switch": 1},
    other_deps={
        "_smooth_blue_meoh_inno_switch": {
            "initial": {
                "blue_meoh_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
            "step": {
                "blue_meoh_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
        }
    },
)
def blue_meoh_inno_switch():
    return _smooth_blue_meoh_inno_switch()


_smooth_blue_meoh_inno_switch = Smooth(
    lambda: if_then_else(
        blue_meoh_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            blue_meoh_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 2,
    lambda: if_then_else(
        blue_meoh_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            blue_meoh_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 3,
    "_smooth_blue_meoh_inno_switch",
)


@component.add(
    name="Blue MeOH innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "meoh_reinvestment": 1,
        "innovators": 1,
        "blue_meoh_inno_switch": 1,
        "blue_meoh": 1,
        "sum_meoh": 2,
    },
)
def blue_meoh_innovators():
    return (
        meoh_reinvestment()
        * innovators()
        * blue_meoh_inno_switch()
        * (sum_meoh() - blue_meoh())
        / sum_meoh()
    )


@component.add(
    name="Blue MeOH investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"blue_meoh_innovators": 1, "blue_meoh_imitators": 1},
)
def blue_meoh_investment():
    return blue_meoh_innovators() + blue_meoh_imitators()


@component.add(
    name="Blue MeOH investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"equalizer_meoh": 1, "blue_meoh_level": 1},
)
def blue_meoh_investment_level():
    return equalizer_meoh() * blue_meoh_level()


@component.add(
    name="Blue MeOH level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "blue_meoh_competitiveness": 1,
        "cross": 1,
        "blue_meoh": 1,
        "sum_meoh": 1,
    },
)
def blue_meoh_level():
    return (
        1
        / (1 + np.exp(slope() * (cross() - blue_meoh_competitiveness())))
        * blue_meoh()
        / sum_meoh()
    )


@component.add(
    name="ctrl MeOH",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"k_p": 1, "error_meoh": 1, "errorint_meoh": 1},
)
def ctrl_meoh():
    return k_p() * error_meoh() + errorint_meoh()


@component.add(
    name="demand change MeOH",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ctrl_meoh": 1},
)
def demand_change_meoh():
    return ctrl_meoh()


@component.add(
    name="eMeOH",
    units="MT",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_emeoh": 1},
    other_deps={
        "_integ_emeoh": {
            "initial": {},
            "step": {"emeoh_investment": 1, "emeoh_decay": 1},
        }
    },
)
def emeoh():
    return _integ_emeoh()


_integ_emeoh = Integ(
    lambda: emeoh_investment() - emeoh_decay(), lambda: 0, "_integ_emeoh"
)


@component.add(
    name="eMeOH competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "blue_meoh_cost": 1,
        "green_emeoh_cost": 3,
        "convmeoh_cost": 1,
        "green_biomeoh_cost": 1,
    },
)
def emeoh_competitiveness():
    return np.minimum(
        np.minimum(
            blue_meoh_cost() / green_emeoh_cost(), convmeoh_cost() / green_emeoh_cost()
        ),
        green_biomeoh_cost() / green_emeoh_cost(),
    )


@component.add(
    name="eMeOH decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"emeoh": 1, "meoh_plant_lifetime": 1},
)
def emeoh_decay():
    return emeoh() / meoh_plant_lifetime()


@component.add(
    name="eMeOH imitators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"meoh_reinvestment": 1, "emeoh_investment_level": 1},
)
def emeoh_imitators():
    return meoh_reinvestment() * emeoh_investment_level()


@component.add(
    name="eMeOH inno switch",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_emeoh_inno_switch": 1},
    other_deps={
        "_smooth_emeoh_inno_switch": {
            "initial": {
                "emeoh_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
            "step": {
                "emeoh_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
        }
    },
)
def emeoh_inno_switch():
    return _smooth_emeoh_inno_switch()


_smooth_emeoh_inno_switch = Smooth(
    lambda: if_then_else(
        emeoh_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            emeoh_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 2,
    lambda: if_then_else(
        emeoh_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            emeoh_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 3,
    "_smooth_emeoh_inno_switch",
)


@component.add(
    name="eMeOH innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "meoh_reinvestment": 1,
        "innovators": 1,
        "emeoh_inno_switch": 1,
        "emeoh": 1,
        "sum_meoh": 2,
    },
)
def emeoh_innovators():
    return (
        meoh_reinvestment()
        * innovators()
        * emeoh_inno_switch()
        * (sum_meoh() - emeoh())
        / sum_meoh()
    )


@component.add(
    name="eMeOH investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"emeoh_imitators": 1, "emeoh_innovators": 1},
)
def emeoh_investment():
    return emeoh_imitators() + emeoh_innovators()


@component.add(
    name="eMeOH investment level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"equalizer_meoh": 1, "emeoh_level": 1},
)
def emeoh_investment_level():
    return equalizer_meoh() * emeoh_level()


@component.add(
    name="eMeOH level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "cross": 1,
        "emeoh_competitiveness": 1,
        "emeoh": 1,
        "sum_meoh": 1,
    },
)
def emeoh_level():
    return (
        1
        / (1 + np.exp(slope() * (cross() - emeoh_competitiveness())))
        * emeoh()
        / sum_meoh()
    )


@component.add(
    name="equalizer MeOH",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "grey_meoh_level": 1,
        "biomeoh_level": 1,
        "blue_meoh_level": 1,
        "emeoh_level": 1,
    },
)
def equalizer_meoh():
    return 1 / (grey_meoh_level() + biomeoh_level() + blue_meoh_level() + emeoh_level())


@component.add(
    name="error MeOH",
    units="e",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"methanol_demand": 1, "sum_meoh": 1},
)
def error_meoh():
    return methanol_demand() - sum_meoh()


@component.add(
    name="errorint MeOH",
    units="e",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_errorint_meoh": 1},
    other_deps={
        "_integ_errorint_meoh": {"initial": {}, "step": {"k_i": 1, "error_meoh": 1}}
    },
)
def errorint_meoh():
    return _integ_errorint_meoh()


_integ_errorint_meoh = Integ(
    lambda: k_i() * error_meoh(), lambda: 0, "_integ_errorint_meoh"
)


@component.add(
    name="Green BioMeOH weight",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"emeoh": 2, "biomeoh": 2},
)
def green_biomeoh_weight():
    return if_then_else(
        emeoh() > 0, lambda: biomeoh() / (biomeoh() + emeoh()), lambda: 1
    )


@component.add(
    name="Green MeOH av cost",
    units="€/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "green_biomeoh_weight": 2,
        "green_biomeoh_cost": 1,
        "green_emeoh_cost": 1,
    },
)
def green_meoh_av_cost():
    return (
        green_biomeoh_weight() * green_biomeoh_cost()
        + (1 - green_biomeoh_weight()) * green_emeoh_cost()
    )


@component.add(
    name="Grey MeOH",
    units="MT",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_grey_meoh": 1},
    other_deps={
        "_integ_grey_meoh": {
            "initial": {"methanol_demand": 1},
            "step": {"grey_meoh_investment": 1, "grey_meoh_decay": 1},
        }
    },
)
def grey_meoh():
    return _integ_grey_meoh()


_integ_grey_meoh = Integ(
    lambda: grey_meoh_investment() - grey_meoh_decay(),
    lambda: methanol_demand(),
    "_integ_grey_meoh",
)


@component.add(
    name="Grey MeOH competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "blue_meoh_cost": 1,
        "convmeoh_cost": 3,
        "green_biomeoh_cost": 1,
        "green_emeoh_cost": 1,
    },
)
def grey_meoh_competitiveness():
    return np.minimum(
        np.minimum(
            blue_meoh_cost() / convmeoh_cost(), green_biomeoh_cost() / convmeoh_cost()
        ),
        green_emeoh_cost() / convmeoh_cost(),
    )


@component.add(
    name="Grey MeOH decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"grey_meoh": 1, "meoh_plant_lifetime": 1},
)
def grey_meoh_decay():
    return grey_meoh() / meoh_plant_lifetime()


@component.add(
    name="Grey MeOH investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"grey_meoh_investment_level": 1, "meoh_reinvestment": 1},
)
def grey_meoh_investment():
    return grey_meoh_investment_level() * meoh_reinvestment()


@component.add(
    name="Grey MeOH investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"equalizer_meoh": 1, "grey_meoh_level": 1},
)
def grey_meoh_investment_level():
    return equalizer_meoh() * grey_meoh_level()


@component.add(
    name="Grey MeOH level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "cross": 1,
        "grey_meoh_competitiveness": 1,
        "grey_meoh": 1,
        "sum_meoh": 1,
    },
)
def grey_meoh_level():
    return (
        1
        / (1 + np.exp(slope() * (cross() - grey_meoh_competitiveness())))
        * grey_meoh()
        / sum_meoh()
    )


@component.add(
    name="MeOH average cost",
    units="€/MJ MeOH",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biomeoh": 1,
        "green_biomeoh_cost": 1,
        "blue_meoh": 1,
        "blue_meoh_cost": 1,
        "convmeoh_cost": 1,
        "grey_meoh": 1,
        "green_emeoh_cost": 1,
        "emeoh": 1,
        "sum_meoh": 1,
    },
)
def meoh_average_cost():
    return (
        biomeoh() * green_biomeoh_cost()
        + blue_meoh() * blue_meoh_cost()
        + grey_meoh() * convmeoh_cost()
        + emeoh() * green_emeoh_cost()
    ) / sum_meoh()


@component.add(
    name="MeOH biomass demand",
    units="GWh Biomass",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"biomeoh": 1, "meoh_lhv": 1, "biomeoh_biomass_usage": 1},
)
def meoh_biomass_demand():
    """
    Convert from MT MeOH to GWh MeOH to GWh biomass
    """
    return biomeoh() * (meoh_lhv() / 3.6 * 1000) * biomeoh_biomass_usage()


@component.add(
    name="MeOH emissions",
    units="tCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "grey_meoh": 2,
        "blue_meoh": 2,
        "electricity_emission_factor": 1,
        "convmeoh_electricity_usage": 1,
        "cc_capture_rate": 1,
        "convmeoh_emission_factor": 1,
    },
)
def meoh_emissions():
    return (
        (grey_meoh() + blue_meoh())
        * electricity_emission_factor()
        * 1000
        * convmeoh_electricity_usage()
        + (grey_meoh() + blue_meoh() * (1 - cc_capture_rate()))
        * convmeoh_emission_factor()
    ) * 10**6


@component.add(
    name="MeOH hydrogen demand",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"biomeoh": 1, "biomeoh_h2_usage": 1, "emeoh": 1, "emeoh_h2_usage": 1},
)
def meoh_hydrogen_demand():
    """
    Convert from GWh to GJ, then from GJ to tons fuel, then from tons fuel to tons H2. Example 1: MeOH cons. [GWh] * 3600 [GJ/GWh] / 19.9 [GJ/t] / 15.7 [t MeOH/t H2] Example 2: NH3 cons. [GWh] * 3600 [GJ/GWh] / 18.6 [GJ/t] / 5.56 [t NH3/t H2]
    """
    return (biomeoh() / biomeoh_h2_usage() + emeoh() / emeoh_h2_usage()) * 10**6


@component.add(
    name="MeOH plant lifetime",
    units="years",
    comp_type="Constant",
    comp_subtype="Normal",
)
def meoh_plant_lifetime():
    return 20


@component.add(
    name="MeOH reinvestment",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_meoh_reinvestment": 1},
    other_deps={
        "_integ_meoh_reinvestment": {
            "initial": {
                "methanol_demand": 1,
                "meoh_plant_lifetime": 1,
                "innovators": 1,
            },
            "step": {
                "biomeoh_decay": 1,
                "blue_meoh_decay": 1,
                "demand_change_meoh": 1,
                "emeoh_decay": 1,
                "grey_meoh_decay": 1,
                "biomeoh_investment": 1,
                "blue_meoh_investment": 1,
                "emeoh_investment": 1,
                "grey_meoh_investment": 1,
            },
        }
    },
)
def meoh_reinvestment():
    return _integ_meoh_reinvestment()


_integ_meoh_reinvestment = Integ(
    lambda: biomeoh_decay()
    + blue_meoh_decay()
    + demand_change_meoh()
    + emeoh_decay()
    + grey_meoh_decay()
    - biomeoh_investment()
    - blue_meoh_investment()
    - emeoh_investment()
    - grey_meoh_investment(),
    lambda: methanol_demand() / meoh_plant_lifetime() * (1 - innovators()),
    "_integ_meoh_reinvestment",
)


@component.add(
    name="methanol demand", units="MT MeOH", comp_type="Constant", comp_subtype="Normal"
)
def methanol_demand():
    """
    European MeOH demand. Primary assumption: To not double count MeOH demand for chemicals, plastics, and fuels the demand is assumed constant moving forward. Source: Deloitte - Clean Hydrogen Europe. (https://www.clean-hydrogen.europa.eu/document/download/9fef29ac-6f95-465b- bb6e-1365526f43c4_en?filename=Study%20on%20hydrogen%20in%20ports%20and%20in dustrial%20coastal%20areas.pdf) Based on 2023 level of 11.3 MT. Forecasted 3.96% CAGR from 2023 to 2034. Assumed 3% CAGR from 2034 to 2050. Extrapolated back to 2019 with same growth as forecast (3.96%). Source: https://www.chemanalyst.com/industry-report/europe-methanol-market-215
    """
    return 2.9


@component.add(
    name="min green MeOH cost",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_biomeoh_cost": 1, "green_emeoh_cost": 1},
)
def min_green_meoh_cost():
    return np.minimum(green_biomeoh_cost(), green_emeoh_cost())


@component.add(
    name="sum MeOH",
    units="MT MeOH",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"grey_meoh": 1, "biomeoh": 1, "blue_meoh": 1, "emeoh": 1},
)
def sum_meoh():
    return grey_meoh() + biomeoh() + blue_meoh() + emeoh()
