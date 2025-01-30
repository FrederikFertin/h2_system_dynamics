"""
Module model_components
Translated using PySD version 3.14.0
"""

@component.add(name="Activity Change", comp_type="Constant", comp_subtype="Normal")
def activity_change():
    return 0


@component.add(
    name="biomass demand",
    units="GWh Biomass",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"technology_activity_distribution": 1},
)
def biomass_demand():
    """
    Convert from GWh MeOH to GWh biomass
    """
    return technology_activity_distribution()


@component.add(name="Decom missions", comp_type="Constant", comp_subtype="Normal")
def decom_missions():
    return 0


@component.add(
    name="Learning Curves",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sectoral_hydrogen_demand": 1},
)
def learning_curves():
    return sectoral_hydrogen_demand() * 0


@component.add(
    name="Reinvestments",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"technology_1_cost": 1, "technology_2_cost": 1},
)
def reinvestments():
    return technology_1_cost() * technology_2_cost() * 0


@component.add(
    name="sector emissions",
    units="tCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"technology_activity_distribution": 1},
)
def sector_emissions():
    return technology_activity_distribution()


@component.add(
    name="Sectoral Hydrogen Demand",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"technology_activity_distribution": 1},
)
def sectoral_hydrogen_demand():
    """
    Get this from Balmorel or have a range of possible scenarios?
    """
    return technology_activity_distribution()


@component.add(
    name='"Techno-economics"',
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"learning_curves": 1},
)
def technoeconomics():
    return 1 * learning_curves()


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
    name="Technology 2 cost",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"technoeconomics": 1},
)
def technology_2_cost():
    return technoeconomics()


@component.add(
    name="Technology Activity Distribution",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_technology_activity_distribution": 1},
    other_deps={
        "_integ_technology_activity_distribution": {
            "initial": {},
            "step": {"reinvestments": 1, "decom_missions": 1},
        }
    },
)
def technology_activity_distribution():
    return _integ_technology_activity_distribution()


_integ_technology_activity_distribution = Integ(
    lambda: reinvestments() + decom_missions(),
    lambda: 0,
    "_integ_technology_activity_distribution",
)


@component.add(
    name="Yearly Investments",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_yearly_investments": 1},
    other_deps={
        "_integ_yearly_investments": {
            "initial": {},
            "step": {"activity_change": 1, "decom_missions": 1, "reinvestments": 1},
        }
    },
)
def yearly_investments():
    return _integ_yearly_investments()


_integ_yearly_investments = Integ(
    lambda: activity_change() + decom_missions() - reinvestments(),
    lambda: 0,
    "_integ_yearly_investments",
)
