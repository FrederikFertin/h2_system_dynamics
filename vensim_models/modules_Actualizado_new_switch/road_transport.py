"""
Module road_transport
Translated using PySD version 3.13.4
"""


@component.add(name="diesel price", comp_type="Constant", comp_subtype="Normal")
def diesel_price():
    return 1.5


@component.add(name="electricity taxes", comp_type="Constant", comp_subtype="Normal")
def electricity_taxes():
    return 2


@component.add(
    name="heavy duty efficiency",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ownership_cost_fcev_long_haul": 2,
        "ownership_cost_diesel_long_haul": 1,
    },
)
def heavy_duty_efficiency():
    return if_then_else(
        np.minimum(ownership_cost_fcev_long_haul(), ownership_cost_diesel_long_haul())
        == ownership_cost_fcev_long_haul(),
        lambda: 0.65,
        lambda: 0.35,
    )


@component.add(
    name="heavy duty energy demand",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_energy_demand": 1},
)
def heavy_duty_energy_demand():
    """
    0.2677 comes from average emissions from heavy duty trucks and buses (Check excel files)
    """
    return total_energy_demand() * 0.2677


@component.add(
    name="heavy duty FCEV energy demand",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_heavy_duty_fcev_energy_demand": 1},
    other_deps={
        "_integ_heavy_duty_fcev_energy_demand": {
            "initial": {},
            "step": {
                "heavy_duty_efficiency": 1,
                "potential_heavy_duty_energy_switch": 2,
            },
        }
    },
)
def heavy_duty_fcev_energy_demand():
    return _integ_heavy_duty_fcev_energy_demand()


_integ_heavy_duty_fcev_energy_demand = Integ(
    lambda: if_then_else(
        heavy_duty_efficiency() == 0.65,
        lambda: potential_heavy_duty_energy_switch(),
        lambda: -potential_heavy_duty_energy_switch(),
    ),
    lambda: 0,
    "_integ_heavy_duty_fcev_energy_demand",
)


@component.add(
    name="heavy duty FCEV enery consumption",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"heavy_duty_fcev_energy_demand": 1, "heavy_duty_energy_demand": 1},
)
def heavy_duty_fcev_enery_consumption():
    return (
        np.minimum(heavy_duty_fcev_energy_demand(), heavy_duty_energy_demand()) / 0.65
    )


@component.add(
    name="heavy duty fossil energy consumption",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"heavy_duty_fossil_energy_demand": 1},
)
def heavy_duty_fossil_energy_consumption():
    return np.maximum(heavy_duty_fossil_energy_demand(), 0) / 0.35


@component.add(
    name="heavy duty fossil energy demand",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_heavy_duty_fossil_energy_demand": 1},
    other_deps={
        "_integ_heavy_duty_fossil_energy_demand": {
            "initial": {"heavy_duty_energy_demand": 1},
            "step": {
                "heavy_duty_efficiency": 1,
                "potential_heavy_duty_energy_switch": 2,
            },
        }
    },
)
def heavy_duty_fossil_energy_demand():
    return _integ_heavy_duty_fossil_energy_demand()


_integ_heavy_duty_fossil_energy_demand = Integ(
    lambda: if_then_else(
        heavy_duty_efficiency() == 0.35,
        lambda: potential_heavy_duty_energy_switch(),
        lambda: -potential_heavy_duty_energy_switch(),
    ),
    lambda: heavy_duty_energy_demand(),
    "_integ_heavy_duty_fossil_energy_demand",
)


@component.add(
    name="heavy duty vehicle renovation rate",
    comp_type="Constant",
    comp_subtype="Normal",
)
def heavy_duty_vehicle_renovation_rate():
    """
    Check excel files
    """
    return 0.0574


@component.add(
    name='"HYDROGEN F. HEAVY DUTY ROAD TRANSPORT"',
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"heavy_duty_fcev_enery_consumption": 1},
)
def hydrogen_f_heavy_duty_road_transport():
    return heavy_duty_fcev_enery_consumption() / 33.33 * 10**3


@component.add(
    name="light duty BEV energy consumption",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"light_duty_bev_energy_demand": 1, "light_duty_energy_demand": 1},
)
def light_duty_bev_energy_consumption():
    return np.minimum(light_duty_bev_energy_demand(), light_duty_energy_demand()) / 0.65


@component.add(
    name="light duty BEV energy demand",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_light_duty_bev_energy_demand": 1},
    other_deps={
        "_integ_light_duty_bev_energy_demand": {
            "initial": {},
            "step": {
                "light_duty_efficiency": 1,
                "potential_light_duty_energy_switch": 2,
            },
        }
    },
)
def light_duty_bev_energy_demand():
    return _integ_light_duty_bev_energy_demand()


_integ_light_duty_bev_energy_demand = Integ(
    lambda: if_then_else(
        light_duty_efficiency() == 0.65,
        lambda: potential_light_duty_energy_switch(),
        lambda: -potential_light_duty_energy_switch(),
    ),
    lambda: 0,
    "_integ_light_duty_bev_energy_demand",
)


@component.add(
    name="light duty efficiency",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ownership_cost_bev_urban": 2, "ownership_cost_diesel_urban": 1},
)
def light_duty_efficiency():
    return if_then_else(
        np.minimum(ownership_cost_bev_urban(), ownership_cost_diesel_urban())
        == ownership_cost_bev_urban(),
        lambda: 0.65,
        lambda: 0.35,
    )


@component.add(
    name="light duty energy demand",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_energy_demand": 1},
)
def light_duty_energy_demand():
    return total_energy_demand() * (1 - 0.2677)


@component.add(
    name="light duty fossil energy consumption",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"light_duty_fossil_energy_demand": 1},
)
def light_duty_fossil_energy_consumption():
    return np.maximum(light_duty_fossil_energy_demand(), 0) / 0.35


@component.add(
    name="light duty fossil energy demand",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_light_duty_fossil_energy_demand": 1},
    other_deps={
        "_integ_light_duty_fossil_energy_demand": {
            "initial": {"light_duty_energy_demand": 1},
            "step": {
                "light_duty_efficiency": 1,
                "potential_light_duty_energy_switch": 2,
            },
        }
    },
)
def light_duty_fossil_energy_demand():
    return _integ_light_duty_fossil_energy_demand()


_integ_light_duty_fossil_energy_demand = Integ(
    lambda: if_then_else(
        light_duty_efficiency() == 0.35,
        lambda: potential_light_duty_energy_switch(),
        lambda: -potential_light_duty_energy_switch(),
    ),
    lambda: light_duty_energy_demand(),
    "_integ_light_duty_fossil_energy_demand",
)


@component.add(
    name="light duty vehicle renovation rate",
    comp_type="Constant",
    comp_subtype="Normal",
)
def light_duty_vehicle_renovation_rate():
    """
    Check excel files
    """
    return 0.0498


@component.add(
    name="ownerhip cost BEV long haul",
    units="€",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"electricity_price": 1, "electricity_taxes": 1},
)
def ownerhip_cost_bev_long_haul():
    return 390000 + electricity_price() * electricity_taxes() * 2.26 * 1200000.0


@component.add(
    name="ownership cost BEV urban",
    units="€",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"electricity_price": 1, "electricity_taxes": 1},
)
def ownership_cost_bev_urban():
    return 35000 + electricity_price() * electricity_taxes() * 0.45 * 240000


@component.add(
    name="ownership cost diesel long haul",
    units="€",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"diesel_price": 1},
)
def ownership_cost_diesel_long_haul():
    return 1500000.0 + diesel_price() / 10.7 * 4.33 * 1200000.0


@component.add(
    name="ownership cost diesel urban",
    units="€",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"diesel_price": 1},
)
def ownership_cost_diesel_urban():
    """
    10.7 kWh/l of diesel
    """
    return 28000 + diesel_price() / 10.7 * 0.87 * 240000


@component.add(
    name="ownership cost FCEV long haul",
    units="€",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hydrogen_price": 1},
)
def ownership_cost_fcev_long_haul():
    """
    33.33 (kWh/kg H2)
    """
    return 325000 + hydrogen_price() / 33.33 * 3.53 * 1200000.0


@component.add(
    name="ownership cost FCEV urban",
    units="€",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hydrogen_price": 1},
)
def ownership_cost_fcev_urban():
    return 57000 + hydrogen_price() / 33.33 * 0.71 * 240000


@component.add(
    name="potential heavy duty energy switch",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"heavy_duty_energy_demand": 1, "heavy_duty_vehicle_renovation_rate": 1},
)
def potential_heavy_duty_energy_switch():
    return heavy_duty_energy_demand() * heavy_duty_vehicle_renovation_rate()


@component.add(
    name="potential light duty energy switch",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"light_duty_energy_demand": 1, "light_duty_vehicle_renovation_rate": 1},
)
def potential_light_duty_energy_switch():
    return light_duty_energy_demand() * light_duty_vehicle_renovation_rate()


@component.add(
    name="total energy demand",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def total_energy_demand():
    """

    !Year
    """
    return np.interp(time(), [2019.0, 2050.0], [867029.0, 1401000.0])
