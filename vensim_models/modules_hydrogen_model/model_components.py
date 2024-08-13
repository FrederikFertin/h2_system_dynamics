"""
Module model_components
Translated using PySD version 3.14.0
"""

@component.add(
    name="biomass demand",
    units="GWh Biomass",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"technology_activity": 1},
)
def biomass_demand():
    """
    Convert from GWh MeOH to GWh biomass
    """
    return technology_activity()


@component.add(
    name="Fuel 1 cost",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"input_parameters": 1, "other_assumptions": 1},
)
def fuel_1_cost():
    return 0 + input_parameters() + other_assumptions()


@component.add(
    name="Fuel 2 cost",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"input_parameters": 1, "other_assumptions": 1},
)
def fuel_2_cost():
    return 0 + input_parameters() + other_assumptions()


@component.add(
    name="hydrogen demand",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"technology_activity": 1},
)
def hydrogen_demand():
    """
    Get this from Balmorel or have a range of possible scenarios?
    """
    return technology_activity()


@component.add(
    name="INPUT PARAMETERS",
    units="percent",
    comp_type="Constant",
    comp_subtype="Normal",
)
def input_parameters():
    return 0


@component.add(name="Investment Flow", comp_type="Constant", comp_subtype="Normal")
def investment_flow():
    return 0


@component.add(name="Other assumptions", comp_type="Constant", comp_subtype="Normal")
def other_assumptions():
    return 0


@component.add(
    name="sector emissions",
    units="tCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"technology_activity": 1},
)
def sector_emissions():
    return technology_activity()


@component.add(
    name="technology activity",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_technology_activity": 1},
    other_deps={
        "_integ_technology_activity": {
            "initial": {},
            "step": {"investment_flow": 1, "fuel_2_cost": 1, "fuel_1_cost": 1},
        }
    },
)
def technology_activity():
    return _integ_technology_activity()


_integ_technology_activity = Integ(
    lambda: investment_flow() * (fuel_1_cost() - fuel_2_cost()),
    lambda: 0,
    "_integ_technology_activity",
)
