"""
Python model 'hydrogen_model_modularized.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np
from scipy import stats

from pysd.py_backend.functions import pulse, if_then_else
from pysd.py_backend.statefuls import Initial, Integ
from pysd.py_backend.utils import load_modules, load_model_data
from pysd import Component

__pysd_version__ = "3.14.0"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent

_subscript_dict, _modules = load_model_data(_root, "hydrogen_model_modularized")

component = Component()

#######################################################################
#                          CONTROL VARIABLES                          #
#######################################################################

_control_vars = {
    "initial_time": lambda: 2019,
    "final_time": lambda: 2050,
    "time_step": lambda: 0.0625,
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

# load modules from modules_hydrogen_model_modularized directory
exec(load_modules("modules_hydrogen_model_modularized", _modules, _root, []))