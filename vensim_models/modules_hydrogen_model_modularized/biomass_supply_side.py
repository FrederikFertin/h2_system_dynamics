"""
Module biomass_supply_side
Translated using PySD version 3.14.0
"""

@component.add(
    name="biomass availability",
    units="tBiomass",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"crude_oil_lhv": 1, "biomass_lhv": 1},
)
def biomass_availability():
    """
    71342 ktoe @2021. JRC IDEES data for 2021. Primary solid biofuels.
    """
    return 71342 * 1000 * crude_oil_lhv() / biomass_lhv()


@component.add(
    name="BIOMASS DEMAND SATURATION",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"biomass_used": 1, "biomass_availability": 1},
)
def biomass_demand_saturation():
    return np.interp(
        biomass_used() / biomass_availability(),
        [0.0, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1],
        [1.0, 1.0, 1.1, 1.3, 1.6, 2.2, 3.0, 10.0, 20.0],
    )


@component.add(
    name="biomass used",
    units="tBiomass",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_shipping_biomass_demand": 1,
        "international_shipping_biomass_demand": 1,
        "domestic_aviation_biomass_demand": 1,
        "international_aviation_biomass_demand": 1,
        "meoh_biomass_demand": 1,
    },
)
def biomass_used():
    return (
        domestic_shipping_biomass_demand()
        + international_shipping_biomass_demand()
        + domestic_aviation_biomass_demand()
        + international_aviation_biomass_demand()
        + meoh_biomass_demand()
    )
