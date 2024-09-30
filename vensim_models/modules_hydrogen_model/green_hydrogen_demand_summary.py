"""
Module green_hydrogen_demand_summary
Translated using PySD version 3.14.0
"""

@component.add(
    name="BioKero hydrogen demand",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_aviation_biokero_hydrogen_demand": 1,
        "international_aviation_biokero_hydrogen_demand": 1,
    },
)
def biokero_hydrogen_demand():
    return (
        domestic_aviation_biokero_hydrogen_demand()
        + international_aviation_biokero_hydrogen_demand()
    )


@component.add(
    name="industry hydrogen demand",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fertilizer_hydrogen_demand": 1,
        "naphtha_hydrogen_demand": 1,
        "high_temperature_hydrogen_demand": 1,
        "refinery_hydrogen_demand": 1,
        "steel_hydrogen_demand": 1,
    },
)
def industry_hydrogen_demand():
    return (
        fertilizer_hydrogen_demand()
        + naphtha_hydrogen_demand()
        + high_temperature_hydrogen_demand()
        + refinery_hydrogen_demand()
        + steel_hydrogen_demand()
    )


@component.add(
    name="INDUSTRY TWH",
    units="TWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"h2_lhv": 1, "industry_hydrogen_demand": 1},
)
def industry_twh():
    return h2_lhv() * industry_hydrogen_demand() / 10**6


@component.add(
    name="POWER TWH",
    units="TWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"h2_lhv": 1, "power_hydrogen_demand": 1},
)
def power_twh():
    return h2_lhv() * power_hydrogen_demand() / 10**6


@component.add(
    name="shipping MeOH hydrogen demand",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_shipping_meoh_hydrogen_demand": 1,
        "international_shipping_meoh_hydrogen_demand": 1,
    },
)
def shipping_meoh_hydrogen_demand():
    return (
        domestic_shipping_meoh_hydrogen_demand()
        + international_shipping_meoh_hydrogen_demand()
    )


@component.add(
    name="SynKero hydrogen demand",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_aviation_synkero_hydrogen_demand": 1,
        "international_aviation_synkero_hydrogen_demand": 1,
    },
)
def synkero_hydrogen_demand():
    return (
        domestic_aviation_synkero_hydrogen_demand()
        + international_aviation_synkero_hydrogen_demand()
    )


@component.add(
    name="TOTAL GREEN HYDROGEN DEMAND",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "industry_hydrogen_demand": 1,
        "power_hydrogen_demand": 1,
        "transportation_hydrogen_demand": 1,
    },
)
def total_green_hydrogen_demand():
    return (
        industry_hydrogen_demand()
        + power_hydrogen_demand()
        + transportation_hydrogen_demand()
    )


@component.add(
    name="TOTAL TWH",
    units="TWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"h2_lhv": 1, "total_green_hydrogen_demand": 1},
)
def total_twh():
    return h2_lhv() * total_green_hydrogen_demand() / 10**6


@component.add(
    name="transportation hydrogen demand",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_aviation_hydrogen_demand": 1,
        "domestic_shipping_hydrogen_demand": 1,
        "heavy_duty_hydrogen_demand": 1,
        "international_aviation_hydrogen_demand": 1,
        "international_shipping_hydrogen_demand": 1,
        "light_duty_hydrogen_demand": 1,
    },
)
def transportation_hydrogen_demand():
    return (
        domestic_aviation_hydrogen_demand()
        + domestic_shipping_hydrogen_demand()
        + heavy_duty_hydrogen_demand()
        + international_aviation_hydrogen_demand()
        + international_shipping_hydrogen_demand()
        + light_duty_hydrogen_demand()
    )


@component.add(
    name="TRANSPORTATION TWH",
    units="TWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"h2_lhv": 1, "transportation_hydrogen_demand": 1},
)
def transportation_twh():
    return h2_lhv() * transportation_hydrogen_demand() / 10**6
