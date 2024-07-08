"""
Module power_and_electricity__nondynamic
Translated using PySD version 3.14.0
"""

@component.add(
    name="power H2 lookup",
    units="TWh",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def power_h2_lookup():
    return np.interp(time(), [2019, 2030, 2040, 2050], [0, 12, 301, 626])


@component.add(
    name="power hydrogen demand",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"power_h2_lookup": 1, "lhv_h2": 1},
)
def power_hydrogen_demand():
    """
    TWh / (MWh/t) * (MWh/TWh)
    """
    return power_h2_lookup() / lhv_h2() * 10**6 * 0
