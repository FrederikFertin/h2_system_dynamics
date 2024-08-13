"""
Module ghg_emissions_summary
Translated using PySD version 3.14.0
"""

@component.add(
    name="domestic aviation CT revenue",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_domestic_aviation_ct_revenue": 1},
    other_deps={
        "_integ_domestic_aviation_ct_revenue": {
            "initial": {},
            "step": {"carbon_tax": 1, "domestic_aviation_emissions": 1},
        }
    },
)
def domestic_aviation_ct_revenue():
    return _integ_domestic_aviation_ct_revenue()


_integ_domestic_aviation_ct_revenue = Integ(
    lambda: carbon_tax() * domestic_aviation_emissions() * 10**-6,
    lambda: 0,
    "_integ_domestic_aviation_ct_revenue",
)


@component.add(
    name="domestic shipping CT revenue",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_domestic_shipping_ct_revenue": 1},
    other_deps={
        "_integ_domestic_shipping_ct_revenue": {
            "initial": {},
            "step": {"carbon_tax": 1, "domestic_shipping_emissions": 1},
        }
    },
)
def domestic_shipping_ct_revenue():
    return _integ_domestic_shipping_ct_revenue()


_integ_domestic_shipping_ct_revenue = Integ(
    lambda: carbon_tax() * domestic_shipping_emissions() * 10**-6,
    lambda: 0,
    "_integ_domestic_shipping_ct_revenue",
)


@component.add(
    name="fertilizer CT revenue",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_fertilizer_ct_revenue": 1},
    other_deps={
        "_integ_fertilizer_ct_revenue": {
            "initial": {},
            "step": {"carbon_tax": 1, "fertilizer_emissions": 1},
        }
    },
)
def fertilizer_ct_revenue():
    return _integ_fertilizer_ct_revenue()


_integ_fertilizer_ct_revenue = Integ(
    lambda: carbon_tax() * fertilizer_emissions() * 10**-6,
    lambda: 0,
    "_integ_fertilizer_ct_revenue",
)


@component.add(
    name="heavy duty CT revenue",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_heavy_duty_ct_revenue": 1},
    other_deps={
        "_integ_heavy_duty_ct_revenue": {
            "initial": {},
            "step": {"carbon_tax": 1, "heavy_duty_emissions": 1},
        }
    },
)
def heavy_duty_ct_revenue():
    return _integ_heavy_duty_ct_revenue()


_integ_heavy_duty_ct_revenue = Integ(
    lambda: carbon_tax() * heavy_duty_emissions() * 10**-6,
    lambda: 0,
    "_integ_heavy_duty_ct_revenue",
)


@component.add(
    name="high temperature CT revenue",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_high_temperature_ct_revenue": 1},
    other_deps={
        "_integ_high_temperature_ct_revenue": {
            "initial": {},
            "step": {"carbon_tax": 1, "high_temperature_emissions": 1},
        }
    },
)
def high_temperature_ct_revenue():
    return _integ_high_temperature_ct_revenue()


_integ_high_temperature_ct_revenue = Integ(
    lambda: carbon_tax() * high_temperature_emissions() * 10**-6,
    lambda: 0,
    "_integ_high_temperature_ct_revenue",
)


@component.add(
    name="industry CT revenue",
    units="M€",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fertilizer_ct_revenue": 1,
        "meoh_ct_revenue": 1,
        "naphtha_ct_revenue": 1,
        "high_temperature_ct_revenue": 1,
        "refinery_ct_revenue": 1,
        "steel_ct_revenue": 1,
    },
)
def industry_ct_revenue():
    return (
        fertilizer_ct_revenue()
        + meoh_ct_revenue()
        + naphtha_ct_revenue()
        + high_temperature_ct_revenue()
        + refinery_ct_revenue()
        + steel_ct_revenue()
    )


@component.add(
    name="industry emissions",
    units="tCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fertilizer_emissions": 1,
        "meoh_emissions": 1,
        "naphtha_emissions": 1,
        "high_temperature_emissions": 1,
        "refinery_emissions": 1,
        "steel_emissions": 1,
    },
)
def industry_emissions():
    return (
        fertilizer_emissions()
        + meoh_emissions()
        + naphtha_emissions()
        + high_temperature_emissions()
        + refinery_emissions()
        + steel_emissions()
    )


@component.add(
    name="international aviation CT revenue",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_international_aviation_ct_revenue": 1},
    other_deps={
        "_integ_international_aviation_ct_revenue": {
            "initial": {},
            "step": {"carbon_tax": 1, "international_aviation_emissions": 1},
        }
    },
)
def international_aviation_ct_revenue():
    return _integ_international_aviation_ct_revenue()


_integ_international_aviation_ct_revenue = Integ(
    lambda: carbon_tax() * international_aviation_emissions() * 10**-6,
    lambda: 0,
    "_integ_international_aviation_ct_revenue",
)


@component.add(
    name="international shipping CT revenue",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_international_shipping_ct_revenue": 1},
    other_deps={
        "_integ_international_shipping_ct_revenue": {
            "initial": {},
            "step": {"carbon_tax": 1, "international_shipping_emissions": 1},
        }
    },
)
def international_shipping_ct_revenue():
    return _integ_international_shipping_ct_revenue()


_integ_international_shipping_ct_revenue = Integ(
    lambda: carbon_tax() * international_shipping_emissions() * 10**-6,
    lambda: 0,
    "_integ_international_shipping_ct_revenue",
)


@component.add(
    name="light duty CT revenue",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_light_duty_ct_revenue": 1},
    other_deps={
        "_integ_light_duty_ct_revenue": {
            "initial": {},
            "step": {"carbon_tax": 1, "light_duty_emissions": 1},
        }
    },
)
def light_duty_ct_revenue():
    return _integ_light_duty_ct_revenue()


_integ_light_duty_ct_revenue = Integ(
    lambda: carbon_tax() * light_duty_emissions() * 10**-6,
    lambda: 0,
    "_integ_light_duty_ct_revenue",
)


@component.add(
    name="MeOH CT revenue",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_meoh_ct_revenue": 1},
    other_deps={
        "_integ_meoh_ct_revenue": {
            "initial": {},
            "step": {"carbon_tax": 1, "meoh_emissions": 1},
        }
    },
)
def meoh_ct_revenue():
    return _integ_meoh_ct_revenue()


_integ_meoh_ct_revenue = Integ(
    lambda: carbon_tax() * meoh_emissions() * 10**-6,
    lambda: 0,
    "_integ_meoh_ct_revenue",
)


@component.add(
    name="naphtha CT revenue",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_naphtha_ct_revenue": 1},
    other_deps={
        "_integ_naphtha_ct_revenue": {
            "initial": {},
            "step": {"carbon_tax": 1, "naphtha_emissions": 1},
        }
    },
)
def naphtha_ct_revenue():
    return _integ_naphtha_ct_revenue()


_integ_naphtha_ct_revenue = Integ(
    lambda: carbon_tax() * naphtha_emissions() * 10**-6,
    lambda: 0,
    "_integ_naphtha_ct_revenue",
)


@component.add(
    name="refinery CT revenue",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_refinery_ct_revenue": 1},
    other_deps={
        "_integ_refinery_ct_revenue": {
            "initial": {},
            "step": {"carbon_tax": 1, "refinery_emissions": 1},
        }
    },
)
def refinery_ct_revenue():
    return _integ_refinery_ct_revenue()


_integ_refinery_ct_revenue = Integ(
    lambda: carbon_tax() * refinery_emissions() * 10**-6,
    lambda: 0,
    "_integ_refinery_ct_revenue",
)


@component.add(
    name="steel CT revenue",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_steel_ct_revenue": 1},
    other_deps={
        "_integ_steel_ct_revenue": {
            "initial": {},
            "step": {"carbon_tax": 1, "steel_emissions": 1},
        }
    },
)
def steel_ct_revenue():
    return _integ_steel_ct_revenue()


_integ_steel_ct_revenue = Integ(
    lambda: carbon_tax() * steel_emissions() * 10**-6,
    lambda: 0,
    "_integ_steel_ct_revenue",
)


@component.add(
    name="TOTAL CARBON TAX REVENUE",
    units="M€",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"industry_ct_revenue": 1, "transportation_ct_revenue": 1},
)
def total_carbon_tax_revenue():
    return industry_ct_revenue() + transportation_ct_revenue()


@component.add(
    name="TOTAL EMISSIONS",
    units="tCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"industry_emissions": 1, "transportation_emissions": 1},
)
def total_emissions():
    return industry_emissions() + transportation_emissions()


@component.add(
    name="transportation CT revenue",
    units="M€",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_aviation_ct_revenue": 1,
        "domestic_shipping_ct_revenue": 1,
        "heavy_duty_ct_revenue": 1,
        "international_aviation_ct_revenue": 1,
        "international_shipping_ct_revenue": 1,
        "light_duty_ct_revenue": 1,
    },
)
def transportation_ct_revenue():
    return (
        domestic_aviation_ct_revenue()
        + domestic_shipping_ct_revenue()
        + heavy_duty_ct_revenue()
        + international_aviation_ct_revenue()
        + international_shipping_ct_revenue()
        + light_duty_ct_revenue()
    )


@component.add(
    name="transportation emissions",
    units="tCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_aviation_emissions": 1,
        "domestic_shipping_emissions": 1,
        "heavy_duty_emissions": 1,
        "international_aviation_emissions": 1,
        "international_shipping_emissions": 1,
        "light_duty_emissions": 1,
    },
)
def transportation_emissions():
    return (
        domestic_aviation_emissions()
        + domestic_shipping_emissions()
        + heavy_duty_emissions()
        + international_aviation_emissions()
        + international_shipping_emissions()
        + light_duty_emissions()
    )
