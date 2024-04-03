"""
Module view_9
Translated using PySD version 3.13.4
"""


@component.add(
    name="ammonia cost",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hydrogen_price": 1, "nh3h2": 1, "electricity_price": 1},
)
def ammonia_cost():
    """
    €/MJ NH3
    """
    return (hydrogen_price() / nh3h2() + 0.6 * electricity_price() * 0) / 18.6


@component.add(
    name="ammonia shipping consumption",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_ammonia_shipping_consumption": 1},
    other_deps={
        "_integ_ammonia_shipping_consumption": {
            "initial": {},
            "step": {"nh3_investment": 1, "nh3_decay": 1},
        }
    },
)
def ammonia_shipping_consumption():
    return _integ_ammonia_shipping_consumption()


_integ_ammonia_shipping_consumption = Integ(
    lambda: nh3_investment() - nh3_decay(),
    lambda: 0,
    "_integ_ammonia_shipping_consumption",
)


@component.add(
    name='"bio-methanol cost"',
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biomass_price": 1,
        "meohh2": 1,
        "hydrogen_price": 1,
        "electricity_price": 1,
    },
)
def biomethanol_cost():
    """
    €/MJ MeOH
    """
    return (
        1.17 * biomass_price() * (12.5 / 1000)
        + hydrogen_price() / meohh2()
        + electricity_price() * 0.64
    ) / 19.9


@component.add(
    name="calc shipping switch",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ammonia_cost": 2,
        "fossil_shipping_fuel_costs": 2,
        "biomethanol_cost": 2,
    },
)
def calc_shipping_switch():
    """
    outputs 0 if fossil fuels are cheapest, 1 if bio-methanol, and 2 if ammonia.
    """
    return if_then_else(
        np.logical_or(
            ammonia_cost() <= fossil_shipping_fuel_costs(),
            biomethanol_cost() <= fossil_shipping_fuel_costs(),
        ),
        lambda: if_then_else(
            ammonia_cost() <= biomethanol_cost(), lambda: 2, lambda: 1
        ),
        lambda: 0,
    )


@component.add(
    name="energy increase",
    comp_type="Stateful",
    comp_subtype="Delay",
    depends_on={"time": 1, "int_shipping_consumption": 1, "_delay_energy_increase": 1},
    other_deps={
        "_delay_energy_increase": {
            "initial": {"int_shipping_consumption": 1},
            "step": {"int_shipping_consumption": 1},
        }
    },
)
def energy_increase():
    return if_then_else(
        time() > 2019,
        lambda: int_shipping_consumption() - _delay_energy_increase(),
        lambda: 10000,
    )


_delay_energy_increase = Delay(
    lambda: int_shipping_consumption(),
    lambda: 1,
    lambda: int_shipping_consumption(),
    lambda: 1,
    time_step,
    "_delay_energy_increase",
)


@component.add(
    name="fleet reinvested",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_fleet_reinvested": 1},
    other_deps={
        "_integ_fleet_reinvested": {
            "initial": {
                "int_shipping_fossil_energy_consumption": 1,
                "ship_lifetime": 1,
            },
            "step": {
                "investments": 1,
                "fossil_investment": 1,
                "meoh_investment": 1,
                "nh3_investment": 1,
            },
        }
    },
)
def fleet_reinvested():
    return _integ_fleet_reinvested()


_integ_fleet_reinvested = Integ(
    lambda: investments() - fossil_investment() - meoh_investment() - nh3_investment(),
    lambda: int_shipping_fossil_energy_consumption() / ship_lifetime(),
    "_integ_fleet_reinvested",
)


@component.add(
    name="fleet reinvestment",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_fleet_reinvestment": 1},
    other_deps={
        "_integ_fleet_reinvestment": {
            "initial": {"int_shipping_consumption": 1, "ship_lifetime": 1},
            "step": {
                "energy_increase": 1,
                "fossil_decay": 1,
                "meoh_decay": 1,
                "nh3_decay": 1,
                "investments": 1,
            },
        }
    },
)
def fleet_reinvestment():
    return _integ_fleet_reinvestment()


_integ_fleet_reinvestment = Integ(
    lambda: energy_increase()
    + fossil_decay()
    + meoh_decay()
    + nh3_decay()
    - investments(),
    lambda: int_shipping_consumption() / ship_lifetime(),
    "_integ_fleet_reinvestment",
)


@component.add(
    name="Fossil decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"int_shipping_fossil_energy_consumption": 1, "ship_lifetime": 1},
)
def fossil_decay():
    return int_shipping_fossil_energy_consumption() / ship_lifetime()


@component.add(
    name="fossil investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"calc_shipping_switch": 1, "fleet_reinvested": 1},
)
def fossil_investment():
    return if_then_else(
        calc_shipping_switch() == 0, lambda: fleet_reinvested(), lambda: 0
    )


@component.add(
    name="fossil shipping fuel costs",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"oil_price": 1, "carbon_tax": 1},
)
def fossil_shipping_fuel_costs():
    """
    €/MJ Oil Emission factor: 0.075 t per GJ
    """
    return oil_price() / 1000 + carbon_tax() * (0.075 / 1000)


@component.add(
    name="int shipping consumption",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def int_shipping_consumption():
    """
    Considering an annual growth of 1,79%
    !Year
    """
    return np.interp(time(), [2018, 2050], [501403, 871296])


@component.add(
    name="int shipping fossil energy consumption",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_int_shipping_fossil_energy_consumption": 1},
    other_deps={
        "_integ_int_shipping_fossil_energy_consumption": {
            "initial": {"int_shipping_consumption": 1},
            "step": {"fossil_investment": 1, "fossil_decay": 1},
        }
    },
)
def int_shipping_fossil_energy_consumption():
    return _integ_int_shipping_fossil_energy_consumption()


_integ_int_shipping_fossil_energy_consumption = Integ(
    lambda: fossil_investment() - fossil_decay(),
    lambda: int_shipping_consumption(),
    "_integ_int_shipping_fossil_energy_consumption",
)


@component.add(
    name="investments",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fleet_reinvestment": 1},
)
def investments():
    return fleet_reinvestment()


@component.add(
    name="MeOH decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"methanol_shipping_consumption": 1, "ship_lifetime": 1},
)
def meoh_decay():
    return methanol_shipping_consumption() / ship_lifetime()


@component.add(
    name="MeOH investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"calc_shipping_switch": 1, "fleet_reinvested": 1},
)
def meoh_investment():
    return if_then_else(
        calc_shipping_switch() == 1, lambda: fleet_reinvested(), lambda: 0
    )


@component.add(name='"MeOH/H2"', comp_type="Constant", comp_subtype="Normal")
def meohh2():
    """
    kg MeOH/kg H2
    """
    return 15.7


@component.add(
    name="methanol shipping consumption",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_methanol_shipping_consumption": 1},
    other_deps={
        "_integ_methanol_shipping_consumption": {
            "initial": {},
            "step": {"meoh_investment": 1, "meoh_decay": 1},
        }
    },
)
def methanol_shipping_consumption():
    return _integ_methanol_shipping_consumption()


_integ_methanol_shipping_consumption = Integ(
    lambda: meoh_investment() - meoh_decay(),
    lambda: 0,
    "_integ_methanol_shipping_consumption",
)


@component.add(
    name="NH3 decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ammonia_shipping_consumption": 1, "ship_lifetime": 1},
)
def nh3_decay():
    return ammonia_shipping_consumption() / ship_lifetime()


@component.add(
    name="NH3 investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"calc_shipping_switch": 1, "fleet_reinvested": 1},
)
def nh3_investment():
    return if_then_else(
        calc_shipping_switch() == 2, lambda: fleet_reinvested(), lambda: 0
    )


@component.add(name='"NH3/H2"', comp_type="Constant", comp_subtype="Normal")
def nh3h2():
    """
    kg NH3/kg H2
    """
    return 5.56


@component.add(name="ship lifetime", comp_type="Constant", comp_subtype="Normal")
def ship_lifetime():
    return 15


@component.add(
    name="shipping hydrogen demand",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "methanol_shipping_consumption": 1,
        "meohh2": 1,
        "nh3h2": 1,
        "ammonia_shipping_consumption": 1,
    },
)
def shipping_hydrogen_demand():
    """
    Convert from GWh to GJ, then from GJ to tons fuel, then from tons fuel to tons H2. Example 1: MeOH cons. [GWh] * 3600 [GJ/GWh] / 19.9 [GJ/t] / 15.7 [t MeOH/t H2] Example 2: NH3 cons. [GWh] * 3600 [GJ/GWh] / 18.6 [GJ/t] / 5.56 [t NH3/t H2]
    """
    return (
        methanol_shipping_consumption() * 3600 / 19.9 / meohh2()
        + ammonia_shipping_consumption() * 3600 / 18.6 / nh3h2()
    )
