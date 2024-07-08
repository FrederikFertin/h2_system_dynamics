"""
Python model 'test with two sectors.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np

from pysd.py_backend.functions import if_then_else
from pysd.py_backend.statefuls import Integ
from pysd import Component

__pysd_version__ = "3.13.4"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent


component = Component()

#######################################################################
#                          CONTROL VARIABLES                          #
#######################################################################

_control_vars = {
    "initial_time": lambda: 2019,
    "final_time": lambda: 2050,
    "time_step": lambda: 1,
    "saveper": lambda: time_step(),
}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


@component.add(name="Time")
def time():
    """
    Current time of the model.
    """
    return __data["time"]()


@component.add(
    name="FINAL TIME", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="INITIAL TIME", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(
    name="SAVEPER",
    units="Year",
    limits=(0.0, np.nan),
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time_step": 1},
)
def saveper():
    """
    The frequency with which output is stored.
    """
    return __data["time"].saveper()


@component.add(
    name="TIME STEP",
    units="Year",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_step():
    """
    The time step for the simulation.
    """
    return __data["time"].time_step()


#######################################################################
#                           MODEL VARIABLES                           #
#######################################################################


@component.add(
    name="Alternative fuel demand S1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_alternative_fuel_demand_s1": 1},
    other_deps={
        "_integ_alternative_fuel_demand_s1": {
            "initial": {},
            "step": {
                "demand_distribution_s1": 1,
                "renorate_s1": 1,
                "demand_annual_increase_s1": 1,
                "demand_total_s1": 1,
            },
        }
    },
)
def alternative_fuel_demand_s1():
    return _integ_alternative_fuel_demand_s1()


_integ_alternative_fuel_demand_s1 = Integ(
    lambda: if_then_else(
        demand_distribution_s1() == 1,
        lambda: renorate_s1() * demand_total_s1() + demand_annual_increase_s1(),
        lambda: 0,
    ),
    lambda: 0,
    "_integ_alternative_fuel_demand_s1",
)


@component.add(
    name="Alternative fuel demand S2",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_alternative_fuel_demand_s2": 1},
    other_deps={
        "_integ_alternative_fuel_demand_s2": {
            "initial": {},
            "step": {
                "demand_distribution_s2": 1,
                "demand_total_s2": 1,
                "renorate_s2": 1,
                "demand_annual_increase_s2": 1,
            },
        }
    },
)
def alternative_fuel_demand_s2():
    return _integ_alternative_fuel_demand_s2()


_integ_alternative_fuel_demand_s2 = Integ(
    lambda: if_then_else(
        demand_distribution_s2() == 1,
        lambda: renorate_s2() * demand_total_s2() + demand_annual_increase_s2(),
        lambda: 0,
    ),
    lambda: 0,
    "_integ_alternative_fuel_demand_s2",
)


@component.add(
    name="Average working hours", units="h", comp_type="Constant", comp_subtype="Normal"
)
def average_working_hours():
    return 4000


@component.add(
    name="Capacity of electrolyser",
    units="GW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_h2_demand": 1,
        "efficiency_of_electrolyser": 1,
        "average_working_hours": 1,
    },
)
def capacity_of_electrolyser():
    """
    Hydrogen demand (tH2) * 1000 (kgH2/tH2) * 33.33 (kWhH2/kgH2) / efficiency / working hours (h) *10^-6 (GW/kW)= GW of electroliser capacity
    """
    return (
        total_h2_demand()
        * 33.33
        / efficiency_of_electrolyser()
        / average_working_hours()
        / 1000
    )


@component.add(
    name="CAPEX",
    units="€/kWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"cost_of_electrolyser": 1, "electrolyser_lifespan": 1},
)
def capex():
    return cost_of_electrolyser() / electrolyser_lifespan()


@component.add(
    name="Cost of electrolyser",
    units="€/kW",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"capacity_of_electrolyser": 1},
)
def cost_of_electrolyser():
    """
    IRENA learning curve
    """
    return np.interp(
        capacity_of_electrolyser(),
        [
            0.00e00,
            1.00e00,
            5.00e00,
            1.00e01,
            1.50e01,
            2.00e01,
            2.50e01,
            3.00e01,
            3.50e01,
            4.00e01,
            4.50e01,
            5.00e01,
            5.50e01,
            6.00e01,
            6.50e01,
            7.00e01,
            7.50e01,
            8.00e01,
            8.50e01,
            9.00e01,
            9.50e01,
            1.00e02,
            1.05e02,
            1.10e02,
            1.15e02,
            1.20e02,
            2.50e02,
            5.00e02,
            7.50e02,
            1.00e03,
            1.25e03,
            1.50e03,
            1.75e03,
            2.00e03,
            2.25e03,
            2.50e03,
            2.75e03,
            3.00e03,
            3.25e03,
            3.50e03,
            3.75e03,
            4.00e03,
            4.25e03,
            4.50e03,
            4.75e03,
            5.00e03,
            5.25e03,
            5.50e03,
            5.75e03,
            6.00e03,
        ],
        [
            650.0,
            612.12,
            526.24,
            489.25,
            467.62,
            452.27,
            440.36,
            430.63,
            422.41,
            415.28,
            409.0,
            403.37,
            398.29,
            393.65,
            389.37,
            385.42,
            381.74,
            378.3,
            375.06,
            372.01,
            369.13,
            366.39,
            363.78,
            361.3,
            358.93,
            356.66,
            317.49,
            280.51,
            258.87,
            243.52,
            231.62,
            221.89,
            213.66,
            206.54,
            200.25,
            194.63,
            189.54,
            184.9,
            180.63,
            176.67,
            172.99,
            169.55,
            166.31,
            163.26,
            160.38,
            157.64,
            155.04,
            152.56,
            150.18,
            147.91,
        ],
    )


@component.add(
    name="Demand annual increase S1", comp_type="Constant", comp_subtype="Normal"
)
def demand_annual_increase_s1():
    return (871296 - 501403) / (2050 - 2019)


@component.add(
    name="Demand annual increase S2", comp_type="Constant", comp_subtype="Normal"
)
def demand_annual_increase_s2():
    return (1401000.0 - 867029) / (2050 - 2019)


@component.add(
    name="Demand distribution S1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"min_cost_s1": 2, "lcoe_alternative_fuel_s1": 1, "lcoe_fossil_s1": 1},
)
def demand_distribution_s1():
    return if_then_else(
        min_cost_s1() == lcoe_alternative_fuel_s1(),
        lambda: 1,
        lambda: if_then_else(min_cost_s1() == lcoe_fossil_s1(), lambda: 2, lambda: 0),
    )


@component.add(
    name="Demand distribution S2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"min_cost_s2": 2, "lcoe_alternative_fuel_s2": 1, "lcoe_fossil_s2": 1},
)
def demand_distribution_s2():
    return if_then_else(
        min_cost_s2() == lcoe_alternative_fuel_s2(),
        lambda: 1,
        lambda: if_then_else(min_cost_s2() == lcoe_fossil_s2(), lambda: 2, lambda: 0),
    )


@component.add(name="Demand other sectors", comp_type="Constant", comp_subtype="Normal")
def demand_other_sectors():
    return 200000


@component.add(
    name="Demand total S1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_demand_total_s1": 1},
    other_deps={
        "_integ_demand_total_s1": {
            "initial": {},
            "step": {"demand_annual_increase_s1": 1},
        }
    },
)
def demand_total_s1():
    return _integ_demand_total_s1()


_integ_demand_total_s1 = Integ(
    lambda: demand_annual_increase_s1(), lambda: 501403, "_integ_demand_total_s1"
)


@component.add(
    name="Demand total S2",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_demand_total_s2": 1},
    other_deps={
        "_integ_demand_total_s2": {
            "initial": {},
            "step": {"demand_annual_increase_s2": 1},
        }
    },
)
def demand_total_s2():
    return _integ_demand_total_s2()


_integ_demand_total_s2 = Integ(
    lambda: demand_annual_increase_s2(), lambda: 867029, "_integ_demand_total_s2"
)


@component.add(
    name="Efficiency of electrolyser", comp_type="Constant", comp_subtype="Normal"
)
def efficiency_of_electrolyser():
    return 0.63


@component.add(
    name="electrolyser lifespan", units="h", comp_type="Constant", comp_subtype="Normal"
)
def electrolyser_lifespan():
    return 60000


@component.add(
    name="elprice",
    units="€/kWh",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def elprice():
    """
    Ioannis e-mail
    """
    return np.interp(time(), [2019.0, 2030.0, 2050.0], [0.038, 0.05, 0.045])


@component.add(
    name="Fossil demand S1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_fossil_demand_s1": 1},
    other_deps={
        "_integ_fossil_demand_s1": {
            "initial": {"demand_total_s1": 1},
            "step": {
                "demand_distribution_s1": 1,
                "demand_annual_increase_s1": 1,
                "renorate_s1": 1,
                "demand_total_s1": 1,
            },
        }
    },
)
def fossil_demand_s1():
    return _integ_fossil_demand_s1()


_integ_fossil_demand_s1 = Integ(
    lambda: if_then_else(
        demand_distribution_s1() == 2,
        lambda: demand_annual_increase_s1(),
        lambda: -renorate_s1() * demand_total_s1(),
    ),
    lambda: demand_total_s1(),
    "_integ_fossil_demand_s1",
)


@component.add(
    name="Fossil demand S2",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_fossil_demand_s2": 1},
    other_deps={
        "_integ_fossil_demand_s2": {
            "initial": {"demand_total_s2": 1},
            "step": {
                "demand_distribution_s2": 1,
                "demand_annual_increase_s2": 1,
                "demand_total_s2": 1,
                "renorate_s2": 1,
            },
        }
    },
)
def fossil_demand_s2():
    return _integ_fossil_demand_s2()


_integ_fossil_demand_s2 = Integ(
    lambda: if_then_else(
        demand_distribution_s2() == 2,
        lambda: demand_annual_increase_s2(),
        lambda: -renorate_s2() * demand_total_s2(),
    ),
    lambda: demand_total_s2(),
    "_integ_fossil_demand_s2",
)


@component.add(
    name="fossilprice", units="€/l", comp_type="Constant", comp_subtype="Normal"
)
def fossilprice():
    return 1.5


@component.add(
    name="Hydrogen demand S1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"alternative_fuel_demand_s1": 1},
)
def hydrogen_demand_s1():
    return alternative_fuel_demand_s1() * 177 / 1000


@component.add(
    name="Hydrogen demand S2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"alternative_fuel_demand_s2": 1},
)
def hydrogen_demand_s2():
    return alternative_fuel_demand_s2() * 200 / 1000


@component.add(
    name="hydrogenprice",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"capex": 1, "opex": 1, "efficiency_of_electrolyser": 1},
)
def hydrogenprice():
    """
    33.33 kWh/kg as HVHh2
    """
    return (capex() + opex()) * (33.33 / efficiency_of_electrolyser())


@component.add(
    name="LCOE alternative fuel S1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hydrogenprice": 1},
)
def lcoe_alternative_fuel_s1():
    return 1 + hydrogenprice() * 2


@component.add(
    name="LCOE alternative fuel S2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hydrogenprice": 1},
)
def lcoe_alternative_fuel_s2():
    return 1 + hydrogenprice() * 2.5


@component.add(
    name="LCOE fossil S1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fossilprice": 1},
)
def lcoe_fossil_s1():
    return 3 + fossilprice() * 2.7


@component.add(
    name="LCOE fossil S2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fossilprice": 1},
)
def lcoe_fossil_s2():
    return 2 + fossilprice() * 4.5


@component.add(
    name="Min cost S1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"lcoe_alternative_fuel_s1": 1, "lcoe_fossil_s1": 1},
)
def min_cost_s1():
    return np.minimum(lcoe_alternative_fuel_s1(), lcoe_fossil_s1())


@component.add(
    name="Min cost S2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"lcoe_alternative_fuel_s2": 1, "lcoe_fossil_s2": 1},
)
def min_cost_s2():
    return np.minimum(lcoe_alternative_fuel_s2(), lcoe_fossil_s2())


@component.add(
    name="OPEX",
    units="€/kWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"elprice": 1},
)
def opex():
    return elprice()


@component.add(name="Renorate S1", comp_type="Constant", comp_subtype="Normal")
def renorate_s1():
    return 0.03


@component.add(name="Renorate S2", comp_type="Constant", comp_subtype="Normal")
def renorate_s2():
    return 0.05


@component.add(
    name="TOTAL H2 DEMAND",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "demand_other_sectors": 1,
        "hydrogen_demand_s1": 1,
        "hydrogen_demand_s2": 1,
    },
)
def total_h2_demand():
    return demand_other_sectors() + hydrogen_demand_s1() + hydrogen_demand_s2()


@component.add(
    name="TotDemandCheck S1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"alternative_fuel_demand_s1": 1, "fossil_demand_s1": 1},
)
def totdemandcheck_s1():
    return alternative_fuel_demand_s1() + fossil_demand_s1()


@component.add(
    name="TotDemandCheck S2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"alternative_fuel_demand_s2": 1, "fossil_demand_s2": 1},
)
def totdemandcheck_s2():
    return alternative_fuel_demand_s2() + fossil_demand_s2()
