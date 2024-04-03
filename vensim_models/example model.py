"""
Python model 'example model.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np

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
    "initial_time": lambda: 2022,
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
    name="Acceptability",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_movement": 4, "sigmoid": 2, "smr_users": 1, "ec_users": 2},
)
def acceptability():
    return (
        green_movement()
        + (1 - green_movement()) * sigmoid()
        + (1 - green_movement() - (1 - green_movement()) * sigmoid())
        * ec_users()
        / (ec_users() + smr_users())
    )


@component.add(
    name="Adopters",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"users_renovating": 1, "acceptability": 1},
)
def adopters():
    return users_renovating() * acceptability()


@component.add(
    name="EC price",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_hydrogen_demand": 2},
)
def ec_price():
    return 15 * (green_hydrogen_demand() / 20) ** 0.8 * 20 / green_hydrogen_demand()


@component.add(
    name="EC Users",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_ec_users": 1},
    other_deps={"_integ_ec_users": {"initial": {}, "step": {"adopters": 1}}},
)
def ec_users():
    return _integ_ec_users()


_integ_ec_users = Integ(lambda: adopters(), lambda: 0.1, "_integ_ec_users")


@component.add(
    name="Green Hydrogen Demand", comp_type="Constant", comp_subtype="Normal"
)
def green_hydrogen_demand():
    return 20


@component.add(name="Green Movement", comp_type="Constant", comp_subtype="Normal")
def green_movement():
    return 0.1


@component.add(name="Renovation Rate", comp_type="Constant", comp_subtype="Normal")
def renovation_rate():
    """
    Inverse of the Lifetime of SMR
    """
    return 1 / 25


@component.add(
    name="Sigmoid",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ec_price": 1, "smr_price": 1},
)
def sigmoid():
    return 1 / (1 + np.exp(ec_price() - smr_price()))


@component.add(name="SMR price", comp_type="Constant", comp_subtype="Normal")
def smr_price():
    return 20


@component.add(
    name="SMR Users",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_smr_users": 1},
    other_deps={"_integ_smr_users": {"initial": {}, "step": {"adopters": 1}}},
)
def smr_users():
    return _integ_smr_users()


_integ_smr_users = Integ(lambda: -adopters(), lambda: 400 - 0.1, "_integ_smr_users")


@component.add(
    name="Users renovating",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"renovation_rate": 1, "smr_users": 1},
)
def users_renovating():
    return renovation_rate() * smr_users()
