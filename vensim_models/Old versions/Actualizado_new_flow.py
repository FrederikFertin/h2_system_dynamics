"""
Python model 'Actualizado_new_flow.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np

from pysd.py_backend.functions import if_then_else
from pysd.py_backend.statefuls import Integ, Delay
from pysd.py_backend.utils import load_modules, load_model_data
from pysd import Component

__pysd_version__ = "3.13.4"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent

_subscript_dict, _modules = load_model_data(_root, "Actualizado_new_flow")

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

# load modules from modules_Actualizado_new_flow directory
exec(load_modules("modules_Actualizado_new_flow", _modules, _root, []))


@component.add(
    name="synfuel curve",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def synfuel_curve():
    return np.interp(
        time(),
        [2019.0, 2025.0, 2028.48, 2033.4, 2036.83, 2039.81, 2043.59, 2047.54, 2050.0],
        [0.0, 0.0, 0.0212121, 0.129545, 0.231818, 0.354545, 0.438636, 0.484091, 0.5],
    )


@component.add(
    name="fossil substitution aviation",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "electric_aircraft": 1,
        "hydrogen_aircraft": 1,
        "biofuel": 1,
        "synfuel": 1,
    },
)
def fossil_substitution_aviation():
    return electric_aircraft() + hydrogen_aircraft() + biofuel() + synfuel()


@component.add(
    name="biofuel",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"biofuel_curve": 1, "medium_long_range": 1},
)
def biofuel():
    return biofuel_curve() * medium_long_range()


@component.add(
    name="biofuel curve",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def biofuel_curve():
    return np.interp(
        time(),
        [2019.0, 2025.32, 2028.22, 2031.21, 2033.31, 2035.6, 2038.85, 2043.85, 2050.0],
        [
            0.0,
            0.00151515,
            0.0287879,
            0.0909091,
            0.143939,
            0.215152,
            0.290909,
            0.356061,
            0.4,
        ],
    )


@component.add(
    name="synfuel",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"synfuel_curve": 1, "medium_long_range": 1},
)
def synfuel():
    return synfuel_curve() * medium_long_range()


@component.add(
    name="kerosene",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"aviation": 1, "fossil_substitution_aviation": 1},
)
def kerosene():
    return aviation() - fossil_substitution_aviation()


@component.add(
    name="short hydrogen aircraft curve",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def short_hydrogen_aircraft_curve():
    return np.interp(
        time(),
        [2019.0, 2029.98, 2033.58, 2037.97, 2040.78, 2044.91, 2050.0],
        [0.0, 0.0568182, 0.166667, 0.583333, 0.80303, 0.912879, 1.0],
    )


@component.add(
    name='"commuter/regional"',
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"aviation": 1},
)
def commuterregional():
    return 0.03 * aviation()


@component.add(
    name="medium long range",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"aviation": 1},
)
def medium_long_range():
    return 0.73 * aviation()


@component.add(
    name="electric aircraft",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"commuterregional": 1, "electric_aircraft_curve": 1},
)
def electric_aircraft():
    return commuterregional() * electric_aircraft_curve()


@component.add(
    name="electric aircraft curve",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def electric_aircraft_curve():
    """

    !Year
    !share (%)
    """
    return np.interp(
        time(),
        [
            2019.0,
            2025.15,
            2029.98,
            2032.52,
            2034.02,
            2035.16,
            2037.18,
            2039.29,
            2041.13,
            2043.85,
            2046.66,
            2050.0,
        ],
        [
            0.0,
            0.00378788,
            0.0530303,
            0.155303,
            0.265152,
            0.344697,
            0.518939,
            0.715909,
            0.840909,
            0.931818,
            0.977273,
            1.0,
        ],
    )


@component.add(
    name="hydrogen aircraft",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"short_hydrogen_aircraft_curve": 1, "short_range": 1},
)
def hydrogen_aircraft():
    return short_hydrogen_aircraft_curve() * short_range()


@component.add(
    name="short range",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"aviation": 1},
)
def short_range():
    return 0.24 * aviation()


@component.add(
    name="aviation",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def aviation():
    """
    That is 1.9% average annual growth per year over the 2017-2040 period. The traffic growth will be faster in the early years (2018-2030) than in the late years (2030-2040). Estimated 2.1% (2019-2030), 1.7% (2030-2040), 1.5% (2040-2050).
    !year
    !GWh
    """
    return np.interp(
        time(), [2019.0, 2030.0, 2040.0, 2050.0], [75721.7, 95170.8, 112645.0, 130729.0]
    )
