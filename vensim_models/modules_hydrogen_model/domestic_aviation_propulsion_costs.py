"""
Module domestic_aviation_propulsion_costs
Translated using PySD version 3.14.0
"""

@component.add(
    name="Biokero propulsion cost",
    units="€/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"biokero_cost": 1, "opex_jet_engine": 1, "jet_engine_efficiency": 1},
)
def biokero_propulsion_cost():
    return (biokero_cost() + opex_jet_engine()) / jet_engine_efficiency()


@component.add(
    name="H2 propulsion cost aviation",
    units="€/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "green_h2_cost": 1,
        "h2_lhv": 1,
        "hydrogen_fuel_cell_efficiency": 1,
        "synkero_propulsion_cost": 1,
    },
)
def h2_propulsion_cost_aviation():
    return (
        green_h2_cost() / (h2_lhv() * 3.6)
    ) / hydrogen_fuel_cell_efficiency() * 0 + synkero_propulsion_cost() * 2


@component.add(
    name="hydrogen fuel cell efficiency",
    units="percent",
    comp_type="Constant",
    comp_subtype="Normal",
)
def hydrogen_fuel_cell_efficiency():
    return 0.5


@component.add(
    name="Jet engine efficiency",
    units="percent",
    comp_type="Constant",
    comp_subtype="Normal",
)
def jet_engine_efficiency():
    return 0.4


@component.add(
    name="Jetfuel propulsion cost",
    units="€/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"jetfuel_cost": 1, "opex_jet_engine": 1, "jet_engine_efficiency": 1},
)
def jetfuel_propulsion_cost():
    return (jetfuel_cost() + opex_jet_engine()) / jet_engine_efficiency()


@component.add(
    name="OPEX jet engine", units="€/MJ", comp_type="Constant", comp_subtype="Normal"
)
def opex_jet_engine():
    return 0.005


@component.add(
    name="Synkero propulsion cost",
    units="€/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"synkero_cost": 1, "opex_jet_engine": 1, "jet_engine_efficiency": 1},
)
def synkero_propulsion_cost():
    return (synkero_cost() + opex_jet_engine()) / jet_engine_efficiency()
