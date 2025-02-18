"""
Module ets_approximation__not_developed
Translated using PySD version 3.14.0
"""

@component.add(
    name="CARBON COST",
    units="€/tCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ps_cc_cost": 1,
        "cc_capture_rate": 1,
        "carbon_tax": 1,
        "carbon_storage_cost": 1,
    },
)
def carbon_cost():
    return ps_cc_cost() / cc_capture_rate() + (carbon_tax() - carbon_storage_cost())


@component.add(
    name="EMISSIONS CAP LOOKUP",
    units="tCO2/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def emissions_cap_lookup():
    return 0
