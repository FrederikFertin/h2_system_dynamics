"""
Module model_components
Translated using PySD version 3.14.0
"""

@component.add(
    name="Activity Change",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"activity_projection": 1},
)
def activity_change():
    return 0 * activity_projection()


@component.add(name="Activity Projection", comp_type="Constant", comp_subtype="Normal")
def activity_projection():
    return 0


@component.add(
    name="biomass demand",
    units="GWh Biomass",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"technology_activity_levels": 1},
)
def biomass_demand():
    """
    Convert from GWh MeOH to GWh biomass
    """
    return technology_activity_levels()


@component.add(name='"Decom- missioning"', comp_type="Constant", comp_subtype="Normal")
def decom_missioning():
    return 0


@component.add(
    name="Green Hydrogen Cost",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_green_hydrogen_cost": 1},
    other_deps={
        "_delay_green_hydrogen_cost": {
            "initial": {"installed_electrolysis": 1},
            "step": {"installed_electrolysis": 1},
        },
        "_integ_green_hydrogen_cost": {
            "initial": {},
            "step": {"_delay_green_hydrogen_cost": 1},
        },
    },
)
def green_hydrogen_cost():
    return _integ_green_hydrogen_cost()


_delay_green_hydrogen_cost = Delay(
    lambda: installed_electrolysis(),
    lambda: 1,
    lambda: installed_electrolysis(),
    lambda: 1,
    time_step,
    "_delay_green_hydrogen_cost",
)

_integ_green_hydrogen_cost = Integ(
    lambda: _delay_green_hydrogen_cost(), lambda: 0, "_integ_green_hydrogen_cost"
)


@component.add(
    name="Installed Electrolysis",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sectoral_green_h2_demands": 1},
)
def installed_electrolysis():
    return sectoral_green_h2_demands()


@component.add(
    name='"Invest- ments"',
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "technology_cost": 1,
        "technology_1_cost": 1,
        "technology_n_cost": 1,
        "technology_activity_levels": 1,
    },
)
def invest_ments():
    return (
        technology_cost()
        * technology_1_cost()
        * 0
        * technology_n_cost()
        * technology_activity_levels()
    )


@component.add(
    name="Investment Pipeline",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_investment_pipeline": 1},
    other_deps={
        "_integ_investment_pipeline": {
            "initial": {},
            "step": {"activity_change": 1, "decom_missioning": 1, "invest_ments": 1},
        }
    },
)
def investment_pipeline():
    return _integ_investment_pipeline()


_integ_investment_pipeline = Integ(
    lambda: activity_change() + decom_missioning() - invest_ments(),
    lambda: 0,
    "_integ_investment_pipeline",
)


@component.add(
    name="Learning Curves",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sectoral_hydrogen_demand": 1},
)
def learning_curves():
    return sectoral_hydrogen_demand() * 0


@component.add(
    name="sector emissions",
    units="tCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"technology_activity_levels": 1},
)
def sector_emissions():
    return technology_activity_levels()


@component.add(
    name="Sectoral Green H2 Demands",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sectoral_h2_investments": 1},
)
def sectoral_green_h2_demands():
    return sectoral_h2_investments()


@component.add(
    name="Sectoral H2 Competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_hydrogen_cost": 1},
)
def sectoral_h2_competitiveness():
    return green_hydrogen_cost()


@component.add(
    name="Sectoral H2 Investments",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sectoral_h2_competitiveness": 1},
)
def sectoral_h2_investments():
    return sectoral_h2_competitiveness()


@component.add(
    name="Sectoral Hydrogen Demand",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"technology_activity_levels": 1},
)
def sectoral_hydrogen_demand():
    """
    Get this from Balmorel or have a range of possible scenarios?
    """
    return technology_activity_levels()


@component.add(name='"Techno-economics"', comp_type="Constant", comp_subtype="Normal")
def technoeconomics():
    return 1


@component.add(
    name="Technology 1 cost",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"technoeconomics": 1},
)
def technology_1_cost():
    return technoeconomics()


@component.add(
    name="Technology Activity Levels",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_technology_activity_levels": 1},
    other_deps={
        "_integ_technology_activity_levels": {
            "initial": {},
            "step": {"invest_ments": 1, "decom_missioning": 1},
        }
    },
)
def technology_activity_levels():
    return _integ_technology_activity_levels()


_integ_technology_activity_levels = Integ(
    lambda: invest_ments() + decom_missioning(),
    lambda: 0,
    "_integ_technology_activity_levels",
)


@component.add(
    name='"Technology .. cost"',
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"technoeconomics": 1},
)
def technology_cost():
    return technoeconomics()


@component.add(
    name="Technology N cost",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"technoeconomics": 1},
)
def technology_n_cost():
    return technoeconomics()
