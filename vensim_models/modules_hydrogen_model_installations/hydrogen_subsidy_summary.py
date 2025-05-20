"""
Module hydrogen_subsidy_summary
Translated using PySD version 3.14.0
"""

@component.add(
    name="buildings subsidy",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_buildings_subsidy": 1},
    other_deps={
        "_integ_buildings_subsidy": {
            "initial": {},
            "step": {"green_h2_actual_subsidy": 1, "buildings_hydrogen_demand": 1},
        }
    },
)
def buildings_subsidy():
    return _integ_buildings_subsidy()


_integ_buildings_subsidy = Integ(
    lambda: green_h2_actual_subsidy() * buildings_hydrogen_demand() / 1000,
    lambda: 0,
    "_integ_buildings_subsidy",
)


@component.add(
    name="buildings subsidy YTD",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_buildings_subsidy_ytd": 1},
    other_deps={
        "_integ_buildings_subsidy_ytd": {
            "initial": {},
            "step": {
                "time": 1,
                "time_step": 2,
                "buildings_hydrogen_demand": 1,
                "green_h2_actual_subsidy": 1,
                "buildings_subsidy_ytd": 1,
            },
        }
    },
)
def buildings_subsidy_ytd():
    return _integ_buildings_subsidy_ytd()


_integ_buildings_subsidy_ytd = Integ(
    lambda: if_then_else(
        modulo(time(), 1) >= time_step(),
        lambda: green_h2_actual_subsidy() * buildings_hydrogen_demand() / 1000,
        lambda: -buildings_subsidy_ytd() / time_step(),
    ),
    lambda: 0,
    "_integ_buildings_subsidy_ytd",
)


@component.add(
    name="domestic aviation subsidy",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_domestic_aviation_subsidy": 1},
    other_deps={
        "_integ_domestic_aviation_subsidy": {
            "initial": {},
            "step": {
                "domestic_aviation_hydrogen_demand": 1,
                "ft_h2_actual_subsidy": 1,
                "green_h2_actual_subsidy": 1,
            },
        }
    },
)
def domestic_aviation_subsidy():
    return _integ_domestic_aviation_subsidy()


_integ_domestic_aviation_subsidy = Integ(
    lambda: domestic_aviation_hydrogen_demand()
    * (green_h2_actual_subsidy() + ft_h2_actual_subsidy())
    / 1000,
    lambda: 0,
    "_integ_domestic_aviation_subsidy",
)


@component.add(
    name="domestic aviation subsidy YTD",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_domestic_aviation_subsidy_ytd": 1},
    other_deps={
        "_integ_domestic_aviation_subsidy_ytd": {
            "initial": {},
            "step": {
                "time": 1,
                "time_step": 2,
                "domestic_aviation_hydrogen_demand": 1,
                "ft_h2_actual_subsidy": 1,
                "green_h2_actual_subsidy": 1,
                "domestic_aviation_subsidy_ytd": 1,
            },
        }
    },
)
def domestic_aviation_subsidy_ytd():
    return _integ_domestic_aviation_subsidy_ytd()


_integ_domestic_aviation_subsidy_ytd = Integ(
    lambda: if_then_else(
        modulo(time(), 1) >= time_step(),
        lambda: (green_h2_actual_subsidy() + ft_h2_actual_subsidy())
        * domestic_aviation_hydrogen_demand()
        / 1000,
        lambda: -domestic_aviation_subsidy_ytd() / time_step(),
    ),
    lambda: 0,
    "_integ_domestic_aviation_subsidy_ytd",
)


@component.add(
    name="domestic shipping subsidy",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_domestic_shipping_subsidy": 1},
    other_deps={
        "_integ_domestic_shipping_subsidy": {
            "initial": {},
            "step": {
                "domestic_shipping_hydrogen_demand": 1,
                "green_h2_actual_subsidy": 1,
            },
        }
    },
)
def domestic_shipping_subsidy():
    return _integ_domestic_shipping_subsidy()


_integ_domestic_shipping_subsidy = Integ(
    lambda: domestic_shipping_hydrogen_demand() * green_h2_actual_subsidy() / 1000,
    lambda: 0,
    "_integ_domestic_shipping_subsidy",
)


@component.add(
    name="domestic shipping subsidy YTD",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_domestic_shipping_subsidy_ytd": 1},
    other_deps={
        "_integ_domestic_shipping_subsidy_ytd": {
            "initial": {},
            "step": {
                "time": 1,
                "time_step": 2,
                "domestic_shipping_hydrogen_demand": 1,
                "green_h2_actual_subsidy": 1,
                "domestic_shipping_subsidy_ytd": 1,
            },
        }
    },
)
def domestic_shipping_subsidy_ytd():
    return _integ_domestic_shipping_subsidy_ytd()


_integ_domestic_shipping_subsidy_ytd = Integ(
    lambda: if_then_else(
        modulo(time(), 1) >= time_step(),
        lambda: green_h2_actual_subsidy() * domestic_shipping_hydrogen_demand() / 1000,
        lambda: -domestic_shipping_subsidy_ytd() / time_step(),
    ),
    lambda: 0,
    "_integ_domestic_shipping_subsidy_ytd",
)


@component.add(
    name="fertilizer subsidy",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_fertilizer_subsidy": 1},
    other_deps={
        "_integ_fertilizer_subsidy": {
            "initial": {},
            "step": {
                "fertilizer_hydrogen_demand": 1,
                "fertilizer_h2_actual_subsidy": 1,
                "green_h2_actual_subsidy": 1,
            },
        }
    },
)
def fertilizer_subsidy():
    return _integ_fertilizer_subsidy()


_integ_fertilizer_subsidy = Integ(
    lambda: fertilizer_hydrogen_demand()
    * (green_h2_actual_subsidy() + fertilizer_h2_actual_subsidy())
    / 1000,
    lambda: 0,
    "_integ_fertilizer_subsidy",
)


@component.add(
    name="fertilizer subsidy YTD",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_fertilizer_subsidy_ytd": 1},
    other_deps={
        "_integ_fertilizer_subsidy_ytd": {
            "initial": {},
            "step": {
                "time": 1,
                "time_step": 2,
                "fertilizer_h2_actual_subsidy": 1,
                "fertilizer_hydrogen_demand": 1,
                "green_h2_actual_subsidy": 1,
                "fertilizer_subsidy_ytd": 1,
            },
        }
    },
)
def fertilizer_subsidy_ytd():
    return _integ_fertilizer_subsidy_ytd()


_integ_fertilizer_subsidy_ytd = Integ(
    lambda: if_then_else(
        modulo(time(), 1) >= time_step(),
        lambda: (green_h2_actual_subsidy() + fertilizer_h2_actual_subsidy())
        * fertilizer_hydrogen_demand()
        / 1000,
        lambda: -fertilizer_subsidy_ytd() / time_step(),
    ),
    lambda: 0,
    "_integ_fertilizer_subsidy_ytd",
)


@component.add(
    name="heavy duty subsidy",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_heavy_duty_subsidy": 1},
    other_deps={
        "_integ_heavy_duty_subsidy": {
            "initial": {},
            "step": {
                "green_h2_actual_subsidy": 1,
                "hd_h2_actual_subsidy": 1,
                "heavy_duty_hydrogen_demand": 1,
            },
        }
    },
)
def heavy_duty_subsidy():
    return _integ_heavy_duty_subsidy()


_integ_heavy_duty_subsidy = Integ(
    lambda: (green_h2_actual_subsidy() + hd_h2_actual_subsidy())
    * heavy_duty_hydrogen_demand()
    / 1000,
    lambda: 0,
    "_integ_heavy_duty_subsidy",
)


@component.add(
    name="heavy duty subsidy YTD",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_heavy_duty_subsidy_ytd": 1},
    other_deps={
        "_integ_heavy_duty_subsidy_ytd": {
            "initial": {},
            "step": {
                "time": 1,
                "time_step": 2,
                "hd_h2_actual_subsidy": 1,
                "heavy_duty_hydrogen_demand": 1,
                "green_h2_actual_subsidy": 1,
                "heavy_duty_subsidy_ytd": 1,
            },
        }
    },
)
def heavy_duty_subsidy_ytd():
    return _integ_heavy_duty_subsidy_ytd()


_integ_heavy_duty_subsidy_ytd = Integ(
    lambda: if_then_else(
        modulo(time(), 1) >= time_step(),
        lambda: (green_h2_actual_subsidy() + hd_h2_actual_subsidy())
        * heavy_duty_hydrogen_demand()
        / 1000,
        lambda: -heavy_duty_subsidy_ytd() / time_step(),
    ),
    lambda: 0,
    "_integ_heavy_duty_subsidy_ytd",
)


@component.add(
    name="high temperature subsidy",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_high_temperature_subsidy": 1},
    other_deps={
        "_integ_high_temperature_subsidy": {
            "initial": {},
            "step": {
                "green_h2_actual_subsidy": 1,
                "nm_h2_actual_subsidy": 1,
                "high_temperature_hydrogen_demand": 1,
            },
        }
    },
)
def high_temperature_subsidy():
    return _integ_high_temperature_subsidy()


_integ_high_temperature_subsidy = Integ(
    lambda: (green_h2_actual_subsidy() + nm_h2_actual_subsidy())
    * high_temperature_hydrogen_demand()
    / 1000,
    lambda: 0,
    "_integ_high_temperature_subsidy",
)


@component.add(
    name="high temperature subsidy YTD",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_high_temperature_subsidy_ytd": 1},
    other_deps={
        "_integ_high_temperature_subsidy_ytd": {
            "initial": {},
            "step": {
                "time": 1,
                "time_step": 2,
                "high_temperature_hydrogen_demand": 1,
                "nm_h2_actual_subsidy": 1,
                "green_h2_actual_subsidy": 1,
                "high_temperature_subsidy_ytd": 1,
            },
        }
    },
)
def high_temperature_subsidy_ytd():
    return _integ_high_temperature_subsidy_ytd()


_integ_high_temperature_subsidy_ytd = Integ(
    lambda: if_then_else(
        modulo(time(), 1) >= time_step(),
        lambda: (green_h2_actual_subsidy() + nm_h2_actual_subsidy())
        * high_temperature_hydrogen_demand()
        / 1000,
        lambda: -high_temperature_subsidy_ytd() / time_step(),
    ),
    lambda: 0,
    "_integ_high_temperature_subsidy_ytd",
)


@component.add(
    name="international aviation subsidy",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_international_aviation_subsidy": 1},
    other_deps={
        "_integ_international_aviation_subsidy": {
            "initial": {},
            "step": {
                "green_h2_actual_subsidy": 1,
                "ft_h2_actual_subsidy": 1,
                "international_aviation_hydrogen_demand": 1,
            },
        }
    },
)
def international_aviation_subsidy():
    return _integ_international_aviation_subsidy()


_integ_international_aviation_subsidy = Integ(
    lambda: (green_h2_actual_subsidy() + ft_h2_actual_subsidy())
    * international_aviation_hydrogen_demand()
    / 1000,
    lambda: 0,
    "_integ_international_aviation_subsidy",
)


@component.add(
    name="international aviation subsidy YTD",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_international_aviation_subsidy_ytd": 1},
    other_deps={
        "_integ_international_aviation_subsidy_ytd": {
            "initial": {},
            "step": {
                "time": 1,
                "time_step": 2,
                "international_aviation_hydrogen_demand": 1,
                "ft_h2_actual_subsidy": 1,
                "green_h2_actual_subsidy": 1,
                "international_aviation_subsidy_ytd": 1,
            },
        }
    },
)
def international_aviation_subsidy_ytd():
    return _integ_international_aviation_subsidy_ytd()


_integ_international_aviation_subsidy_ytd = Integ(
    lambda: if_then_else(
        modulo(time(), 1) >= time_step(),
        lambda: (green_h2_actual_subsidy() + ft_h2_actual_subsidy())
        * international_aviation_hydrogen_demand()
        / 1000,
        lambda: -international_aviation_subsidy_ytd() / time_step(),
    ),
    lambda: 0,
    "_integ_international_aviation_subsidy_ytd",
)


@component.add(
    name="international shipping subsidy",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_international_shipping_subsidy": 1},
    other_deps={
        "_integ_international_shipping_subsidy": {
            "initial": {},
            "step": {
                "green_h2_actual_subsidy": 1,
                "international_shipping_hydrogen_demand": 1,
            },
        }
    },
)
def international_shipping_subsidy():
    return _integ_international_shipping_subsidy()


_integ_international_shipping_subsidy = Integ(
    lambda: green_h2_actual_subsidy() * international_shipping_hydrogen_demand() / 1000,
    lambda: 0,
    "_integ_international_shipping_subsidy",
)


@component.add(
    name="international shipping subsidy YTD",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_international_shipping_subsidy_ytd": 1},
    other_deps={
        "_integ_international_shipping_subsidy_ytd": {
            "initial": {},
            "step": {
                "time": 1,
                "time_step": 2,
                "international_shipping_hydrogen_demand": 1,
                "green_h2_actual_subsidy": 1,
                "international_shipping_subsidy_ytd": 1,
            },
        }
    },
)
def international_shipping_subsidy_ytd():
    return _integ_international_shipping_subsidy_ytd()


_integ_international_shipping_subsidy_ytd = Integ(
    lambda: if_then_else(
        modulo(time(), 1) >= time_step(),
        lambda: green_h2_actual_subsidy()
        * international_shipping_hydrogen_demand()
        / 1000,
        lambda: -international_shipping_subsidy_ytd() / time_step(),
    ),
    lambda: 0,
    "_integ_international_shipping_subsidy_ytd",
)


@component.add(
    name="light duty subsidy",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_light_duty_subsidy": 1},
    other_deps={
        "_integ_light_duty_subsidy": {
            "initial": {},
            "step": {
                "green_h2_actual_subsidy": 1,
                "ld_h2_actual_subsidy": 1,
                "light_duty_hydrogen_demand": 1,
            },
        }
    },
)
def light_duty_subsidy():
    return _integ_light_duty_subsidy()


_integ_light_duty_subsidy = Integ(
    lambda: (green_h2_actual_subsidy() + ld_h2_actual_subsidy())
    * light_duty_hydrogen_demand()
    / 1000,
    lambda: 0,
    "_integ_light_duty_subsidy",
)


@component.add(
    name="light duty subsidy YTD",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_light_duty_subsidy_ytd": 1},
    other_deps={
        "_integ_light_duty_subsidy_ytd": {
            "initial": {},
            "step": {
                "time": 1,
                "time_step": 2,
                "light_duty_hydrogen_demand": 1,
                "ld_h2_actual_subsidy": 1,
                "green_h2_actual_subsidy": 1,
                "light_duty_subsidy_ytd": 1,
            },
        }
    },
)
def light_duty_subsidy_ytd():
    return _integ_light_duty_subsidy_ytd()


_integ_light_duty_subsidy_ytd = Integ(
    lambda: if_then_else(
        modulo(time(), 1) >= time_step(),
        lambda: (green_h2_actual_subsidy() + ld_h2_actual_subsidy())
        * light_duty_hydrogen_demand()
        / 1000,
        lambda: -light_duty_subsidy_ytd() / time_step(),
    ),
    lambda: 0,
    "_integ_light_duty_subsidy_ytd",
)


@component.add(
    name="MeOH subsidy",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_meoh_subsidy": 1},
    other_deps={
        "_integ_meoh_subsidy": {
            "initial": {},
            "step": {"meoh_hydrogen_demand": 1, "green_h2_actual_subsidy": 1},
        }
    },
)
def meoh_subsidy():
    return _integ_meoh_subsidy()


_integ_meoh_subsidy = Integ(
    lambda: meoh_hydrogen_demand() * green_h2_actual_subsidy() / 1000,
    lambda: 0,
    "_integ_meoh_subsidy",
)


@component.add(
    name="MeOH subsidy YTD",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_meoh_subsidy_ytd": 1},
    other_deps={
        "_integ_meoh_subsidy_ytd": {
            "initial": {},
            "step": {
                "time": 1,
                "time_step": 2,
                "meoh_hydrogen_demand": 1,
                "green_h2_actual_subsidy": 1,
                "meoh_subsidy_ytd": 1,
            },
        }
    },
)
def meoh_subsidy_ytd():
    return _integ_meoh_subsidy_ytd()


_integ_meoh_subsidy_ytd = Integ(
    lambda: if_then_else(
        modulo(time(), 1) >= time_step(),
        lambda: green_h2_actual_subsidy() * meoh_hydrogen_demand() / 1000,
        lambda: -meoh_subsidy_ytd() / time_step(),
    ),
    lambda: 0,
    "_integ_meoh_subsidy_ytd",
)


@component.add(
    name="naphtha subsidy",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_naphtha_subsidy": 1},
    other_deps={
        "_integ_naphtha_subsidy": {
            "initial": {},
            "step": {
                "naphtha_hydrogen_demand": 1,
                "ft_h2_actual_subsidy": 1,
                "green_h2_actual_subsidy": 1,
            },
        }
    },
)
def naphtha_subsidy():
    return _integ_naphtha_subsidy()


_integ_naphtha_subsidy = Integ(
    lambda: naphtha_hydrogen_demand()
    * (green_h2_actual_subsidy() + ft_h2_actual_subsidy())
    / 1000,
    lambda: 0,
    "_integ_naphtha_subsidy",
)


@component.add(
    name="naphtha subsidy YTD",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_naphtha_subsidy_ytd": 1},
    other_deps={
        "_integ_naphtha_subsidy_ytd": {
            "initial": {},
            "step": {
                "time": 1,
                "time_step": 2,
                "naphtha_hydrogen_demand": 1,
                "green_h2_actual_subsidy": 1,
                "ft_h2_actual_subsidy": 1,
                "naphtha_subsidy_ytd": 1,
            },
        }
    },
)
def naphtha_subsidy_ytd():
    return _integ_naphtha_subsidy_ytd()


_integ_naphtha_subsidy_ytd = Integ(
    lambda: if_then_else(
        modulo(time(), 1) >= time_step(),
        lambda: (green_h2_actual_subsidy() + ft_h2_actual_subsidy())
        * naphtha_hydrogen_demand()
        / 1000,
        lambda: -naphtha_subsidy_ytd() / time_step(),
    ),
    lambda: 0,
    "_integ_naphtha_subsidy_ytd",
)


@component.add(
    name="power subsidy",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_power_subsidy": 1},
    other_deps={
        "_integ_power_subsidy": {
            "initial": {},
            "step": {"green_h2_actual_subsidy": 1, "power_hydrogen_demand": 1},
        }
    },
)
def power_subsidy():
    return _integ_power_subsidy()


_integ_power_subsidy = Integ(
    lambda: green_h2_actual_subsidy() * power_hydrogen_demand() / 1000,
    lambda: 0,
    "_integ_power_subsidy",
)


@component.add(
    name="power subsidy YTD",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_power_subsidy_ytd": 1},
    other_deps={
        "_integ_power_subsidy_ytd": {
            "initial": {},
            "step": {
                "time": 1,
                "time_step": 2,
                "power_hydrogen_demand": 1,
                "green_h2_actual_subsidy": 1,
                "power_subsidy_ytd": 1,
            },
        }
    },
)
def power_subsidy_ytd():
    return _integ_power_subsidy_ytd()


_integ_power_subsidy_ytd = Integ(
    lambda: if_then_else(
        modulo(time(), 1) >= time_step(),
        lambda: green_h2_actual_subsidy() * power_hydrogen_demand() / 1000,
        lambda: -power_subsidy_ytd() / time_step(),
    ),
    lambda: 0,
    "_integ_power_subsidy_ytd",
)


@component.add(
    name="refinery subsidy",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_refinery_subsidy": 1},
    other_deps={
        "_integ_refinery_subsidy": {
            "initial": {},
            "step": {
                "refinery_hydrogen_demand": 1,
                "refinery_h2_actual_subsidy": 1,
                "green_h2_actual_subsidy": 1,
            },
        }
    },
)
def refinery_subsidy():
    return _integ_refinery_subsidy()


_integ_refinery_subsidy = Integ(
    lambda: refinery_hydrogen_demand()
    * (green_h2_actual_subsidy() + refinery_h2_actual_subsidy())
    / 1000,
    lambda: 0,
    "_integ_refinery_subsidy",
)


@component.add(
    name="refinery subsidy YTD",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_refinery_subsidy_ytd": 1},
    other_deps={
        "_integ_refinery_subsidy_ytd": {
            "initial": {},
            "step": {
                "time": 1,
                "time_step": 2,
                "refinery_h2_actual_subsidy": 1,
                "refinery_hydrogen_demand": 1,
                "green_h2_actual_subsidy": 1,
                "refinery_subsidy_ytd": 1,
            },
        }
    },
)
def refinery_subsidy_ytd():
    return _integ_refinery_subsidy_ytd()


_integ_refinery_subsidy_ytd = Integ(
    lambda: if_then_else(
        modulo(time(), 1) >= time_step(),
        lambda: (green_h2_actual_subsidy() + refinery_h2_actual_subsidy())
        * refinery_hydrogen_demand()
        / 1000,
        lambda: -refinery_subsidy_ytd() / time_step(),
    ),
    lambda: 0,
    "_integ_refinery_subsidy_ytd",
)


@component.add(
    name="shipping MeOH subsidy",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_shipping_meoh_subsidy": 1},
    other_deps={
        "_integ_shipping_meoh_subsidy": {
            "initial": {},
            "step": {
                "shipping_meoh_hydrogen_demand": 1,
                "shipping_meoh_h2_actual_subsidy": 1,
                "green_h2_actual_subsidy": 1,
            },
        }
    },
)
def shipping_meoh_subsidy():
    return _integ_shipping_meoh_subsidy()


_integ_shipping_meoh_subsidy = Integ(
    lambda: shipping_meoh_hydrogen_demand()
    * (green_h2_actual_subsidy() + shipping_meoh_h2_actual_subsidy())
    / 1000,
    lambda: 0,
    "_integ_shipping_meoh_subsidy",
)


@component.add(
    name="shipping MeOH subsidy YTD",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_shipping_meoh_subsidy_ytd": 1},
    other_deps={
        "_integ_shipping_meoh_subsidy_ytd": {
            "initial": {},
            "step": {
                "time": 1,
                "time_step": 2,
                "shipping_meoh_h2_actual_subsidy": 1,
                "shipping_meoh_hydrogen_demand": 1,
                "green_h2_actual_subsidy": 1,
                "shipping_meoh_subsidy_ytd": 1,
            },
        }
    },
)
def shipping_meoh_subsidy_ytd():
    return _integ_shipping_meoh_subsidy_ytd()


_integ_shipping_meoh_subsidy_ytd = Integ(
    lambda: if_then_else(
        modulo(time(), 1) >= time_step(),
        lambda: (green_h2_actual_subsidy() + shipping_meoh_h2_actual_subsidy())
        * shipping_meoh_hydrogen_demand()
        / 1000,
        lambda: -shipping_meoh_subsidy_ytd() / time_step(),
    ),
    lambda: 0,
    "_integ_shipping_meoh_subsidy_ytd",
)


@component.add(
    name="shipping NH3 subsidy",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_shipping_nh3_subsidy": 1},
    other_deps={
        "_integ_shipping_nh3_subsidy": {
            "initial": {},
            "step": {
                "international_shipping_nh3_hydrogen_demand": 1,
                "shipping_nh3_h2_actual_subsidy": 1,
                "green_h2_actual_subsidy": 1,
            },
        }
    },
)
def shipping_nh3_subsidy():
    return _integ_shipping_nh3_subsidy()


_integ_shipping_nh3_subsidy = Integ(
    lambda: international_shipping_nh3_hydrogen_demand()
    * (green_h2_actual_subsidy() + shipping_nh3_h2_actual_subsidy())
    / 1000,
    lambda: 0,
    "_integ_shipping_nh3_subsidy",
)


@component.add(
    name="shipping NH3 subsidy YTD",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_shipping_nh3_subsidy_ytd": 1},
    other_deps={
        "_integ_shipping_nh3_subsidy_ytd": {
            "initial": {},
            "step": {
                "time": 1,
                "time_step": 2,
                "shipping_nh3_h2_actual_subsidy": 1,
                "international_shipping_nh3_hydrogen_demand": 1,
                "green_h2_actual_subsidy": 1,
                "shipping_nh3_subsidy_ytd": 1,
            },
        }
    },
)
def shipping_nh3_subsidy_ytd():
    return _integ_shipping_nh3_subsidy_ytd()


_integ_shipping_nh3_subsidy_ytd = Integ(
    lambda: if_then_else(
        modulo(time(), 1) >= time_step(),
        lambda: (green_h2_actual_subsidy() + shipping_nh3_h2_actual_subsidy())
        * international_shipping_nh3_hydrogen_demand()
        / 1000,
        lambda: -shipping_nh3_subsidy_ytd() / time_step(),
    ),
    lambda: 0,
    "_integ_shipping_nh3_subsidy_ytd",
)


@component.add(
    name="steel subsidy",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_steel_subsidy": 1},
    other_deps={
        "_integ_steel_subsidy": {
            "initial": {},
            "step": {
                "green_h2_actual_subsidy": 1,
                "steel_h2_actual_subsidy": 1,
                "steel_hydrogen_demand": 1,
            },
        }
    },
)
def steel_subsidy():
    return _integ_steel_subsidy()


_integ_steel_subsidy = Integ(
    lambda: (green_h2_actual_subsidy() + steel_h2_actual_subsidy())
    * steel_hydrogen_demand()
    / 1000,
    lambda: 0,
    "_integ_steel_subsidy",
)


@component.add(
    name="steel subsidy YTD",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_steel_subsidy_ytd": 1},
    other_deps={
        "_integ_steel_subsidy_ytd": {
            "initial": {},
            "step": {
                "time": 1,
                "time_step": 2,
                "steel_hydrogen_demand": 1,
                "steel_h2_actual_subsidy": 1,
                "green_h2_actual_subsidy": 1,
                "steel_subsidy_ytd": 1,
            },
        }
    },
)
def steel_subsidy_ytd():
    return _integ_steel_subsidy_ytd()


_integ_steel_subsidy_ytd = Integ(
    lambda: if_then_else(
        modulo(time(), 1) >= time_step(),
        lambda: (green_h2_actual_subsidy() + steel_h2_actual_subsidy())
        * steel_hydrogen_demand()
        / 1000,
        lambda: -steel_subsidy_ytd() / time_step(),
    ),
    lambda: 0,
    "_integ_steel_subsidy_ytd",
)


@component.add(
    name="total annual subsidies",
    units="M€",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "green_h2_actual_subsidy": 1,
        "industry_hydrogen_demand": 1,
        "transportation_hydrogen_demand": 1,
    },
)
def total_annual_subsidies():
    return (
        green_h2_actual_subsidy()
        * (industry_hydrogen_demand() + transportation_hydrogen_demand())
        / 1000
    )


@component.add(
    name="TOTAL SUBSIDIES",
    units="M€",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_aviation_subsidy": 1,
        "fertilizer_subsidy": 1,
        "heavy_duty_subsidy": 1,
        "international_aviation_subsidy": 1,
        "light_duty_subsidy": 1,
        "naphtha_subsidy": 1,
        "high_temperature_subsidy": 1,
        "refinery_subsidy": 1,
        "steel_subsidy": 1,
        "power_subsidy": 1,
        "shipping_meoh_subsidy": 1,
        "shipping_nh3_subsidy": 1,
        "meoh_subsidy": 1,
        "buildings_subsidy": 1,
    },
)
def total_subsidies():
    return (
        domestic_aviation_subsidy()
        + fertilizer_subsidy()
        + heavy_duty_subsidy()
        + international_aviation_subsidy()
        + light_duty_subsidy()
        + naphtha_subsidy()
        + high_temperature_subsidy()
        + refinery_subsidy()
        + steel_subsidy()
        + power_subsidy()
        + shipping_meoh_subsidy()
        + shipping_nh3_subsidy()
        + meoh_subsidy()
        + buildings_subsidy()
    )


@component.add(
    name="TOTAL SUBSIDIES YTD",
    units="M€",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_aviation_subsidy_ytd": 1,
        "fertilizer_subsidy_ytd": 1,
        "heavy_duty_subsidy_ytd": 1,
        "international_aviation_subsidy_ytd": 1,
        "light_duty_subsidy_ytd": 1,
        "naphtha_subsidy_ytd": 1,
        "high_temperature_subsidy_ytd": 1,
        "power_subsidy_ytd": 1,
        "refinery_subsidy_ytd": 1,
        "steel_subsidy_ytd": 1,
        "shipping_meoh_subsidy_ytd": 1,
        "shipping_nh3_subsidy_ytd": 1,
        "meoh_subsidy_ytd": 1,
        "buildings_subsidy_ytd": 1,
    },
)
def total_subsidies_ytd():
    return (
        domestic_aviation_subsidy_ytd()
        + fertilizer_subsidy_ytd()
        + heavy_duty_subsidy_ytd()
        + international_aviation_subsidy_ytd()
        + light_duty_subsidy_ytd()
        + naphtha_subsidy_ytd()
        + high_temperature_subsidy_ytd()
        + power_subsidy_ytd()
        + refinery_subsidy_ytd()
        + steel_subsidy_ytd()
        + shipping_meoh_subsidy_ytd()
        + shipping_nh3_subsidy_ytd()
        + meoh_subsidy_ytd()
        + buildings_subsidy_ytd()
    )
