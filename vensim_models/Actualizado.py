"""
Python model 'Actualizado.py'
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
    name='"electricity (sensitivity)"', comp_type="Constant", comp_subtype="Normal"
)
def electricity_sensitivity():
    return 1


@component.add(
    name="electricity price",
    units="€/kWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"electricity_sensitivity": 1, "electricity_price_forecast": 1},
)
def electricity_price():
    return electricity_sensitivity() * electricity_price_forecast()


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
    name="ownerhip cost BEV long haul",
    units="€",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"electricity_price": 1, "electricity_taxes": 1},
)
def ownerhip_cost_bev_long_haul():
    return 390000 + electricity_price() * electricity_taxes() * 2.26 * 1200000.0


@component.add(
    name="OPEX hydrogen",
    units="€/kWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"electricity_price": 1},
)
def opex_hydrogen():
    return electricity_price()


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
    name="TOTAL HYDROGEN",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hydrogen_f_ammonia": 1,
        "hydrogen_f_olefin": 1,
        "hydrogen_f_refinery": 1,
        "hydrogen_f_steel": 1,
        "hydrogen_f_industrial_heat": 1,
        "hydrogen_f_aviaton": 1,
        "hydrogen_f_heavy_duty_road_transport": 1,
        "hydrogen_f_shipping": 1,
    },
)
def total_hydrogen():
    return (
        hydrogen_f_ammonia()
        + hydrogen_f_olefin()
        + hydrogen_f_refinery()
        + hydrogen_f_steel()
        + hydrogen_f_industrial_heat()
        + hydrogen_f_aviaton()
        + hydrogen_f_heavy_duty_road_transport()
        + hydrogen_f_shipping()
    )


@component.add(
    name="decarbonization curve refinery",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def decarbonization_curve_refinery():
    return np.interp(
        time(),
        [
            2019.0,
            2020.0,
            2021.0,
            2022.0,
            2023.0,
            2024.0,
            2025.0,
            2026.0,
            2027.0,
            2028.0,
            2029.0,
            2030.0,
            2031.0,
            2032.0,
            2033.0,
            2034.0,
            2035.0,
            2036.0,
            2037.0,
            2038.0,
            2039.0,
            2040.0,
            2041.0,
            2042.0,
            2043.0,
            2044.0,
            2045.0,
            2046.0,
            2047.0,
            2048.0,
            2049.0,
            2050.0,
        ],
        [
            0.0,
            0.0,
            0.01,
            0.01,
            0.02,
            0.03,
            0.04,
            0.05,
            0.07,
            0.09,
            0.12,
            0.16,
            0.2,
            0.27,
            0.33,
            0.41,
            0.49,
            0.57,
            0.65,
            0.72,
            0.79,
            0.84,
            0.89,
            0.91,
            0.94,
            0.96,
            0.97,
            0.98,
            0.99,
            0.99,
            0.996294,
            0.998147,
        ],
    )


@component.add(
    name='"HYDROGEN F. REFINERY"',
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"decarbonization_curve_refinery": 1},
)
def hydrogen_f_refinery():
    return 4.8 * 10**6 * decarbonization_curve_refinery()


@component.add(
    name='"HYDROGEN F. SHIPPING"',
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hydrogen_ammonia_shipping": 1, "hydrogen_methanol_shipping": 1},
)
def hydrogen_f_shipping():
    return hydrogen_ammonia_shipping() + hydrogen_methanol_shipping()


@component.add(
    name='"hydrogen energy consumption dom. aviation"',
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "dom_aviation_energy_consumption": 1,
        "hydrogen_penetration_in_dom_aviation": 1,
    },
)
def hydrogen_energy_consumption_dom_aviation():
    return dom_aviation_energy_consumption() * hydrogen_penetration_in_dom_aviation()


@component.add(
    name='"bio-kerosene energy consumption int. aviation"',
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "decarbonization_curve_int_aviation": 1,
        "int_aviation_energy_consumption": 1,
    },
)
def biokerosene_energy_consumption_int_aviation():
    return decarbonization_curve_int_aviation() * int_aviation_energy_consumption() * 1


@component.add(
    name='"int. aviation energy consumption"',
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def int_aviation_energy_consumption():
    return np.interp(time(), [2019, 2050], [486033, 703496])


@component.add(
    name='"decarbonization curve dom. aviation"',
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def decarbonization_curve_dom_aviation():
    return np.interp(
        time(),
        [
            2019.0,
            2020.0,
            2021.0,
            2022.0,
            2023.0,
            2024.0,
            2025.0,
            2026.0,
            2027.0,
            2028.0,
            2029.0,
            2030.0,
            2031.0,
            2032.0,
            2033.0,
            2034.0,
            2035.0,
            2036.0,
            2037.0,
            2038.0,
            2039.0,
            2040.0,
            2041.0,
            2042.0,
            2043.0,
            2044.0,
            2045.0,
            2046.0,
            2047.0,
            2048.0,
            2049.0,
            2050.0,
        ],
        [
            0.0,
            0.0,
            0.01,
            0.01,
            0.02,
            0.03,
            0.04,
            0.05,
            0.07,
            0.09,
            0.12,
            0.16,
            0.2,
            0.27,
            0.33,
            0.41,
            0.49,
            0.57,
            0.65,
            0.72,
            0.79,
            0.84,
            0.89,
            0.91,
            0.94,
            0.96,
            0.97,
            0.98,
            0.99,
            0.99,
            0.996294,
            0.998147,
        ],
    )


@component.add(
    name='"hydrogen penetration in dom. aviation"',
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def hydrogen_penetration_in_dom_aviation():
    return np.interp(
        time(),
        [
            2019.0,
            2020.0,
            2021.0,
            2022.0,
            2023.0,
            2024.0,
            2025.0,
            2026.0,
            2027.0,
            2028.0,
            2029.0,
            2030.0,
            2031.0,
            2032.0,
            2033.0,
            2034.0,
            2035.0,
            2036.0,
            2037.0,
            2038.0,
            2039.0,
            2040.0,
            2041.0,
            2042.0,
            2043.0,
            2044.0,
            2045.0,
            2046.0,
            2047.0,
            2048.0,
            2049.0,
            2050.0,
        ],
        [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.01,
            0.01,
            0.02,
            0.03,
            0.04,
            0.05,
            0.07,
            0.09,
            0.12,
            0.16,
            0.2,
            0.27,
            0.33,
            0.41,
            0.49,
            0.57,
            0.65,
            0.72,
            0.79,
        ],
    )


@component.add(
    name='"decarbonization curve int. aviation"',
    units="{%}",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def decarbonization_curve_int_aviation():
    return np.interp(
        time(),
        [
            2019.0,
            2020.0,
            2021.0,
            2022.0,
            2023.0,
            2024.0,
            2025.0,
            2026.0,
            2027.0,
            2028.0,
            2029.0,
            2030.0,
            2031.0,
            2032.0,
            2033.0,
            2034.0,
            2035.0,
            2036.0,
            2037.0,
            2038.0,
            2039.0,
            2040.0,
            2041.0,
            2042.0,
            2043.0,
            2044.0,
            2045.0,
            2046.0,
            2047.0,
            2048.0,
            2049.0,
            2050.0,
        ],
        [
            0.0,
            0.0,
            0.01,
            0.01,
            0.02,
            0.03,
            0.04,
            0.05,
            0.07,
            0.09,
            0.12,
            0.16,
            0.2,
            0.27,
            0.33,
            0.41,
            0.49,
            0.57,
            0.65,
            0.72,
            0.79,
            0.84,
            0.89,
            0.91,
            0.94,
            0.96,
            0.97,
            0.98,
            0.99,
            0.99,
            0.996294,
            0.998147,
        ],
    )


@component.add(
    name='"bio-kerosene energy consumption dom. aviation"',
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "decarbonization_curve_dom_aviation": 1,
        "dom_aviation_energy_consumption": 1,
        "hydrogen_energy_consumption_dom_aviation": 1,
    },
)
def biokerosene_energy_consumption_dom_aviation():
    return (
        decarbonization_curve_dom_aviation() * dom_aviation_energy_consumption()
        - hydrogen_energy_consumption_dom_aviation()
    ) * 1


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
    name='"HYDROGEN F. AVIATON"',
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biokerosene_energy_consumption_dom_aviation": 1,
        "biokerosene_energy_consumption_int_aviation": 1,
        "bio_kerosene_hydrogen_rate": 1,
        "syn_kerosene_hydrogen_rate": 1,
        "synthetic_kerosene_energy_consumption_int_aviation": 1,
        "synthetic_kerosene_energy_consumption_dom_aviation": 1,
        "hydrogen_energy_consumption_dom_aviation": 1,
    },
)
def hydrogen_f_aviaton():
    """
    33.33 MWh/t = calorific power H2
    """
    return (
        (
            (
                biokerosene_energy_consumption_dom_aviation()
                + biokerosene_energy_consumption_int_aviation()
            )
            * bio_kerosene_hydrogen_rate()
            + (
                synthetic_kerosene_energy_consumption_dom_aviation()
                + synthetic_kerosene_energy_consumption_int_aviation()
            )
            * syn_kerosene_hydrogen_rate()
            + hydrogen_energy_consumption_dom_aviation()
        )
        * 10**3
        / 33.33
    )


@component.add(
    name='"dom. aviation energy consumption"',
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def dom_aviation_energy_consumption():
    return np.interp(time(), [2019, 2050], [75722, 109601])


@component.add(
    name='"synthetic kerosene energy consumption int. aviation"',
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "decarbonization_curve_int_aviation": 1,
        "int_aviation_energy_consumption": 1,
    },
)
def synthetic_kerosene_energy_consumption_int_aviation():
    return decarbonization_curve_int_aviation() * int_aviation_energy_consumption() * 0


@component.add(
    name='"synthetic kerosene energy consumption dom. aviation"',
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "dom_aviation_energy_consumption": 1,
        "decarbonization_curve_dom_aviation": 1,
        "hydrogen_energy_consumption_dom_aviation": 1,
    },
)
def synthetic_kerosene_energy_consumption_dom_aviation():
    return (
        dom_aviation_energy_consumption() * decarbonization_curve_dom_aviation()
        - hydrogen_energy_consumption_dom_aviation()
    ) * 0


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
    name="diesel price", units="€/l", comp_type="Constant", comp_subtype="Normal"
)
def diesel_price():
    return 1.5


@component.add(
    name="HYDROGEN AMMONIA SHIPPING",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ammonia_ice_energy_consumption": 1, "h2_ammonia_ratio": 1},
)
def hydrogen_ammonia_shipping():
    """
    1 t NH3 = 160000 * GWh NH3
    """
    return ammonia_ice_energy_consumption() * 3600 * h2_ammonia_ratio() / 22.5 / 1000


@component.add(
    name="ammonia ICE energy consumption",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "int_navigation_energy_consumption": 1,
        "decarbonization_curve_shipping": 1,
    },
)
def ammonia_ice_energy_consumption():
    """
    CONSIDERING 50% OF AMMONIA
    """
    return int_navigation_energy_consumption() * decarbonization_curve_shipping() * 0.35


@component.add(
    name='"dom. navigation fossil energy consumption"',
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dom_navigation_fossil_fuel_demand": 1, "ice_efficiency": 1},
)
def dom_navigation_fossil_energy_consumption():
    return dom_navigation_fossil_fuel_demand() / ice_efficiency()


@component.add(
    name="methanol ICE energy consumption",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "decarbonization_curve_shipping": 1,
        "int_navigation_energy_consumption": 1,
    },
)
def methanol_ice_energy_consumption():
    """
    CONSIDERING 50% OF METHANOL; considering a sub-division of e-methanol and bio-methanol
    """
    return decarbonization_curve_shipping() * int_navigation_energy_consumption() * 0.35


@component.add(
    name='"int. aviation fossil energy consumption"',
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "int_navigation_energy_consumption": 1,
        "ammonia_ice_energy_consumption": 1,
        "methanol_ice_energy_consumption": 1,
    },
)
def int_aviation_fossil_energy_consumption():
    return (
        int_navigation_energy_consumption()
        - ammonia_ice_energy_consumption()
        - methanol_ice_energy_consumption()
    )


@component.add(
    name='"ammonia consumption f. agriculture"',
    units="Mt/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ammonia_consumption_f_agriculture():
    """
    EHB European Backbone Report: 19.1 Mt/year CEPS Report: 21 Mt/year (capacity)
    """
    return 19.1


@component.add(
    name="electrolyser cost",
    units="€/kW",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"electroliser_capacity": 1},
)
def electrolyser_cost():
    """
    IRENA learning curve
    """
    return np.interp(
        electroliser_capacity(),
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
    name='"hydrogen-syntheticnaphfta rate"',
    units="MWh H2/t Naphfta",
    comp_type="Constant",
    comp_subtype="Normal",
)
def hydrogensyntheticnaphfta_rate():
    return 5.85


@component.add(
    name='"HYDROGEN F. AMMONIA"',
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ammonia_consumption_f_agriculture": 1,
        "green_hydrogen_pentration": 1,
        "h2_ammonia_ratio": 1,
    },
)
def hydrogen_f_ammonia():
    """
    (tH2) = (MtNH3/year)*10^6*(kgH2/tNH3)/1000*%
    """
    return (
        ammonia_consumption_f_agriculture()
        * green_hydrogen_pentration()
        * h2_ammonia_ratio()
        * 1000
    )


@component.add(
    name="Olefin production",
    units="t",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def olefin_production():
    """
    20% decrease in connection to plastic production forecasts
    """
    return np.interp(time(), [2019.0, 2050.0], [41495000.0, 33196000.0])


@component.add(
    name="green hydrogen pentration",
    units="{%}",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def green_hydrogen_pentration():
    return np.interp(
        time(),
        [
            2019.0,
            2020.0,
            2021.0,
            2022.0,
            2023.0,
            2024.0,
            2025.0,
            2026.0,
            2027.0,
            2028.0,
            2029.0,
            2030.0,
            2031.0,
            2032.0,
            2033.0,
            2034.0,
            2035.0,
            2036.0,
            2037.0,
            2038.0,
            2039.0,
            2040.0,
            2041.0,
            2042.0,
            2043.0,
            2044.0,
            2045.0,
            2046.0,
            2047.0,
            2048.0,
            2049.0,
            2050.0,
        ],
        [
            0.0,
            0.0,
            0.01,
            0.01,
            0.02,
            0.03,
            0.04,
            0.05,
            0.07,
            0.09,
            0.12,
            0.16,
            0.2,
            0.27,
            0.33,
            0.41,
            0.49,
            0.57,
            0.65,
            0.72,
            0.79,
            0.84,
            0.89,
            0.91,
            0.94,
            0.96,
            0.97,
            0.98,
            0.99,
            0.99,
            0.996294,
            0.998147,
        ],
    )


@component.add(
    name='"HYDROGEN F. OLEFIN"',
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "synthetic_naphfta_demand_for_olefin_production": 1,
        "hydrogensyntheticnaphfta_rate": 1,
        "bionaphfta_demand_for_olefin_production": 1,
        "hydrogenbionaphfta_rate": 1,
    },
)
def hydrogen_f_olefin():
    """
    33.33 kg/kWh = t/MWh
    """
    return (
        synthetic_naphfta_demand_for_olefin_production()
        * hydrogensyntheticnaphfta_rate()
        + bionaphfta_demand_for_olefin_production() * hydrogenbionaphfta_rate()
    ) / 33.33


@component.add(
    name='"hydrogen-bionaphfta rate"',
    units="MWh H2/t naphtfa",
    comp_type="Constant",
    comp_subtype="Normal",
)
def hydrogenbionaphfta_rate():
    return 0.78


@component.add(
    name="synthetic naphfta demand for olefin production",
    units="t methanol",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "olefin_production": 1,
        "decarbonization_curve_for_olefin_production": 1,
        "naphtaolefin_rate": 1,
    },
)
def synthetic_naphfta_demand_for_olefin_production():
    return (
        olefin_production()
        * decarbonization_curve_for_olefin_production()
        / 2
        * naphtaolefin_rate()
    )


@component.add(
    name='"naphta-olefin rate"',
    units="t Naphfta / t HVC",
    comp_type="Constant",
    comp_subtype="Normal",
)
def naphtaolefin_rate():
    return 1.66


@component.add(
    name='"bio-naphfta demand for olefin production"',
    units="t Naphfta",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "olefin_production": 1,
        "decarbonization_curve_for_olefin_production": 1,
        "naphtaolefin_rate": 1,
    },
)
def bionaphfta_demand_for_olefin_production():
    return (
        olefin_production()
        * decarbonization_curve_for_olefin_production()
        / 2
        * naphtaolefin_rate()
    )


@component.add(name="electricity taxes", comp_type="Constant", comp_subtype="Normal")
def electricity_taxes():
    return 2


@component.add(
    name="HYDROGEN METHANOL SHIPPING",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "methanol_ice_energy_consumption": 1,
        "biomethanol_hydrogen_rate": 1,
        "synthetic_methanol_hydrogen_rate": 1,
    },
)
def hydrogen_methanol_shipping():
    """
    22.7 MJ/kg is the calorific power of methanol; 33.33 kWh/kg is the calorific power of h2 = 33.33 MWh/t
    """
    return (
        methanol_ice_energy_consumption()
        * 3600
        / 22.7
        * (biomethanol_hydrogen_rate() * 1 + synthetic_methanol_hydrogen_rate() * 0)
    ) / 33.33


@component.add(
    name='"bio kerosene - hydrogen rate"',
    units="MWh H2 / MWh kero",
    comp_type="Constant",
    comp_subtype="Normal",
)
def bio_kerosene_hydrogen_rate():
    return 0.15


@component.add(
    name='"synthetic methanol - hydrogen rate"',
    units="MWh H2 / t synmethanol",
    comp_type="Constant",
    comp_subtype="Normal",
)
def synthetic_methanol_hydrogen_rate():
    return 6.3


@component.add(
    name='"syn kerosene - hydrogen rate"',
    units="MWh H2 / MWh kero",
    comp_type="Constant",
    comp_subtype="Normal",
)
def syn_kerosene_hydrogen_rate():
    return 1.2


@component.add(
    name="decarbonization curve for olefin production",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def decarbonization_curve_for_olefin_production():
    return np.interp(
        time(),
        [
            2019.0,
            2020.0,
            2021.0,
            2022.0,
            2023.0,
            2024.0,
            2025.0,
            2026.0,
            2027.0,
            2028.0,
            2029.0,
            2030.0,
            2031.0,
            2032.0,
            2033.0,
            2034.0,
            2035.0,
            2036.0,
            2037.0,
            2038.0,
            2039.0,
            2040.0,
            2041.0,
            2042.0,
            2043.0,
            2044.0,
            2045.0,
            2046.0,
            2047.0,
            2048.0,
            2049.0,
            2050.0,
        ],
        [
            0.0,
            0.0,
            0.01,
            0.01,
            0.02,
            0.03,
            0.04,
            0.05,
            0.07,
            0.09,
            0.12,
            0.16,
            0.2,
            0.27,
            0.33,
            0.41,
            0.49,
            0.57,
            0.65,
            0.72,
            0.79,
            0.84,
            0.89,
            0.91,
            0.94,
            0.96,
            0.97,
            0.98,
            0.99,
            0.99,
            0.996294,
            0.998147,
        ],
    )


@component.add(
    name='"biomethanol - hydrogen rate"',
    units="MWh H2/ t biomethanol",
    comp_type="Constant",
    comp_subtype="Normal",
)
def biomethanol_hydrogen_rate():
    return 2


@component.add(
    name='"Natural gas consumption f. industrial heat"',
    units="TWh",
    comp_type="Constant",
    comp_subtype="Normal",
)
def natural_gas_consumption_f_industrial_heat():
    """
    Natural gas consumption (TWh)
    """
    return 175 / 2


@component.add(
    name='"Hydrogen implementation curve f. industrial heat"',
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def hydrogen_implementation_curve_f_industrial_heat():
    return np.interp(
        time(),
        [
            2019.0,
            2020.0,
            2021.0,
            2022.0,
            2023.0,
            2024.0,
            2025.0,
            2026.0,
            2027.0,
            2028.0,
            2029.0,
            2030.0,
            2031.0,
            2032.0,
            2033.0,
            2034.0,
            2035.0,
            2036.0,
            2037.0,
            2038.0,
            2039.0,
            2040.0,
            2041.0,
            2042.0,
            2043.0,
            2044.0,
            2045.0,
            2046.0,
            2047.0,
            2048.0,
            2049.0,
            2050.0,
        ],
        [
            0.0,
            0.0,
            0.01,
            0.01,
            0.02,
            0.03,
            0.04,
            0.05,
            0.07,
            0.09,
            0.12,
            0.16,
            0.2,
            0.27,
            0.33,
            0.41,
            0.49,
            0.57,
            0.65,
            0.72,
            0.79,
            0.84,
            0.89,
            0.91,
            0.94,
            0.96,
            0.97,
            0.98,
            0.99,
            0.99,
            0.996294,
            0.998147,
        ],
    )


@component.add(
    name='"HYDROGEN F. INDUSTRIAL HEAT"',
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hydrogen_implementation_curve_f_industrial_heat": 1,
        "natural_gas_consumption_f_industrial_heat": 1,
    },
)
def hydrogen_f_industrial_heat():
    """
    1 (TWh) * 10^6 (MWh/TWh) / 33.33 (MWh/tH2) = tH2
    """
    return (
        hydrogen_implementation_curve_f_industrial_heat()
        * natural_gas_consumption_f_industrial_heat()
        * 10**6
        / 33.33
    )


@component.add(
    name="biofuels share",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"rail_electricity_share": 1, "time": 1},
)
def biofuels_share():
    return if_then_else(
        rail_electricity_share() < 1,
        lambda: (0.1857 * (time() - 2019) + 0.012) / 100,
        lambda: 0,
    )


@component.add(
    name="fossil energy consumption from rail",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fossil_energy_demand": 1, "diesel_locomotive_efficiency": 1},
)
def fossil_energy_consumption_from_rail():
    return fossil_energy_demand() / diesel_locomotive_efficiency()


@component.add(
    name="fossil energy demand",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "rail_energy_demand": 1,
        "rail_electricity_share": 1,
        "biofuels_share": 1,
    },
)
def fossil_energy_demand():
    return (
        rail_energy_demand() * (1 - rail_electricity_share()) * (1 - biofuels_share())
    )


@component.add(
    name="rail electricity share",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def rail_electricity_share():
    return np.interp(time(), [2019.0, 2038.0, 2050.0], [0.7615, 1.0, 1.0])


@component.add(
    name="rail energy demand",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def rail_energy_demand():
    return np.interp(time(), [2019, 2050], [47212, 39177])


@component.add(
    name="diesel locomotive efficiency", comp_type="Constant", comp_subtype="Normal"
)
def diesel_locomotive_efficiency():
    return 0.3


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
    name='"HYDROGEN F. HEAVY DUTY ROAD TRANSPORT"',
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"heavy_duty_fcev_enery_consumption": 1},
)
def hydrogen_f_heavy_duty_road_transport():
    return heavy_duty_fcev_enery_consumption() / 33.33 * 10**3


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
    name="light duty fossil energy consumption",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"light_duty_fossil_energy_demand": 1},
)
def light_duty_fossil_energy_consumption():
    return np.maximum(light_duty_fossil_energy_demand(), 0) / 0.35


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
    name="potential heavy duty energy switch",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"heavy_duty_energy_demand": 1, "heavy_duty_vehicle_renovation_rate": 1},
)
def potential_heavy_duty_energy_switch():
    return heavy_duty_energy_demand() * heavy_duty_vehicle_renovation_rate()


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
    name="electricity price forecast",
    units="€/kWh",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def electricity_price_forecast():
    """
    Ioannis e-mail
    """
    return np.interp(time(), [2019.0, 2030.0, 2050.0], [0.038, 0.05, 0.045])


@component.add(
    name="hydrogen price",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"capex_hydrogen": 1, "opex_hydrogen": 1, "electrolyser_efficiency": 1},
)
def hydrogen_price():
    """
    33.33 kWh/kg as HVHh2
    """
    return (capex_hydrogen() + opex_hydrogen()) * (33.33 / electrolyser_efficiency())


@component.add(
    name="electrolyser efficiency", comp_type="Constant", comp_subtype="Normal"
)
def electrolyser_efficiency():
    return 0.63


@component.add(
    name="CAPEX hydrogen",
    units="€/kWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"electrolyser_cost": 1, "electrolyser_life_spand": 1},
)
def capex_hydrogen():
    return electrolyser_cost() / electrolyser_life_spand()


@component.add(
    name="electrolyser life spand",
    units="h",
    comp_type="Constant",
    comp_subtype="Normal",
)
def electrolyser_life_spand():
    return 60000


@component.add(
    name="electroliser efficiency",
    units="{%}",
    comp_type="Constant",
    comp_subtype="Normal",
)
def electroliser_efficiency():
    return 0.7


@component.add(
    name="electroliser average working hours",
    units="h",
    comp_type="Constant",
    comp_subtype="Normal",
)
def electroliser_average_working_hours():
    return 4000


@component.add(
    name="electroliser capacity",
    units="GW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_hydrogen": 1,
        "electroliser_efficiency": 1,
        "electroliser_average_working_hours": 1,
    },
)
def electroliser_capacity():
    """
    Hydrogen demand (tH2) * 1000 (kgH2/tH2) * 33.33 (kWhH2/kgH2) / efficiency / working hours (h) *10^-6 (GW/kW)= GW of electroliser capacity
    """
    return (
        total_hydrogen()
        * 33.33
        / electroliser_efficiency()
        / electroliser_average_working_hours()
        / 1000
    )


@component.add(
    name='"H2 - ammonia ratio"',
    units="kg H2/t NH3",
    comp_type="Constant",
    comp_subtype="Normal",
)
def h2_ammonia_ratio():
    return 177


@component.add(
    name='"dom. navigation energy demand"',
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dom_navigation_energy_consumption": 1, "ice_efficiency": 1},
)
def dom_navigation_energy_demand():
    return dom_navigation_energy_consumption() * ice_efficiency()


@component.add(
    name='"dom. navigation energy consumption"',
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def dom_navigation_energy_consumption():
    """
    Considering an annual growth rate of 2.64%
    """
    return np.interp(time(), [2019, 2050], [49177, 97795])


@component.add(
    name="BEV implementation curve",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def bev_implementation_curve():
    return np.interp(
        time(),
        [
            2019.0,
            2020.0,
            2021.0,
            2022.0,
            2023.0,
            2024.0,
            2025.0,
            2026.0,
            2027.0,
            2028.0,
            2029.0,
            2030.0,
            2031.0,
            2032.0,
            2033.0,
            2034.0,
            2035.0,
            2036.0,
            2037.0,
            2038.0,
            2039.0,
            2040.0,
            2041.0,
            2042.0,
            2043.0,
            2044.0,
            2045.0,
            2046.0,
            2047.0,
            2048.0,
            2049.0,
            2050.0,
        ],
        [
            0.0,
            0.0,
            0.01,
            0.01,
            0.02,
            0.03,
            0.04,
            0.05,
            0.07,
            0.09,
            0.12,
            0.16,
            0.2,
            0.27,
            0.33,
            0.41,
            0.49,
            0.57,
            0.65,
            0.72,
            0.79,
            0.84,
            0.89,
            0.91,
            0.94,
            0.96,
            0.97,
            0.98,
            0.99,
            0.99,
            0.996294,
            0.998147,
        ],
    )


@component.add(name="ICE efficiency", comp_type="Constant", comp_subtype="Normal")
def ice_efficiency():
    """
    Considering the same efficiency for all the fossil fuel engines
    """
    return 0.45


@component.add(
    name='"int. navigation energy consumption"',
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def int_navigation_energy_consumption():
    """
    Considering an annual growth of 1,79%
    !Year
    """
    return np.interp(time(), [2019, 2050], [501403, 871296])


@component.add(
    name='"dom. navigation fossil fuel demand"',
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dom_navigation_energy_demand": 1, "bev_implementation_curve": 1},
)
def dom_navigation_fossil_fuel_demand():
    return dom_navigation_energy_demand() * (1 - bev_implementation_curve())


@component.add(
    name="decarbonization curve shipping",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def decarbonization_curve_shipping():
    """
    COMPLETE WITH BIOFUELS IMPLEMENTATION CURVE
    """
    return np.interp(
        time(),
        [
            2019.0,
            2020.0,
            2021.0,
            2022.0,
            2023.0,
            2024.0,
            2025.0,
            2026.0,
            2027.0,
            2028.0,
            2029.0,
            2030.0,
            2031.0,
            2032.0,
            2033.0,
            2034.0,
            2035.0,
            2036.0,
            2037.0,
            2038.0,
            2039.0,
            2040.0,
            2041.0,
            2042.0,
            2043.0,
            2044.0,
            2045.0,
            2046.0,
            2047.0,
            2048.0,
            2049.0,
            2050.0,
        ],
        [
            0.0,
            0.0,
            0.01,
            0.01,
            0.02,
            0.03,
            0.04,
            0.05,
            0.07,
            0.09,
            0.12,
            0.16,
            0.2,
            0.27,
            0.33,
            0.41,
            0.49,
            0.57,
            0.65,
            0.72,
            0.79,
            0.84,
            0.89,
            0.91,
            0.94,
            0.96,
            0.97,
            0.98,
            0.99,
            0.99,
            0.996294,
            0.998147,
        ],
    )


@component.add(
    name="secondary growth",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def secondary_growth():
    """
    At the same time, the share of secondary steel production is expected to increase to 50%, as less scrap will be exported out of Europe to now serve decarbonisation of steel production in the European market
    !year
    !share of steel production
    """
    return np.interp(time(), [2019.0, 2050.0], [0.4, 0.5])


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
    name='"HYDROGEN F. STEEL"',
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"drieaf": 1, "h2_to_steel": 1},
)
def hydrogen_f_steel():
    return drieaf() * 10**6 * h2_to_steel()


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


@component.add(
    name='"BF-BOF"',
    units="Mtsteel",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"primary": 1, "decarbonization": 1},
)
def bfbof():
    return primary() * (1 - decarbonization())


@component.add(
    name="decarbonization",
    units="{%}",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def decarbonization():
    return np.interp(
        time(),
        [
            2019.0,
            2020.0,
            2021.0,
            2022.0,
            2023.0,
            2024.0,
            2025.0,
            2026.0,
            2027.0,
            2028.0,
            2029.0,
            2030.0,
            2031.0,
            2032.0,
            2033.0,
            2034.0,
            2035.0,
            2036.0,
            2037.0,
            2038.0,
            2039.0,
            2040.0,
            2041.0,
            2042.0,
            2043.0,
            2044.0,
            2045.0,
            2046.0,
            2047.0,
            2048.0,
            2049.0,
            2050.0,
        ],
        [
            0.0,
            0.0,
            0.01,
            0.01,
            0.02,
            0.03,
            0.04,
            0.05,
            0.07,
            0.09,
            0.12,
            0.16,
            0.2,
            0.27,
            0.33,
            0.41,
            0.49,
            0.57,
            0.65,
            0.72,
            0.79,
            0.84,
            0.89,
            0.91,
            0.94,
            0.96,
            0.97,
            0.98,
            0.99,
            0.99,
            0.996294,
            0.998147,
        ],
    )


@component.add(
    name='"DRI-EAF"',
    units="Mtsteel",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"primary": 1, "decarbonization": 1},
)
def drieaf():
    return primary() * decarbonization()


@component.add(
    name="H2 to steel", units="tH2/tsteel", comp_type="Constant", comp_subtype="Normal"
)
def h2_to_steel():
    return 0.0563


@component.add(
    name="primary",
    units="Mtsteel",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"steel": 1, "secondary_growth": 1},
)
def primary():
    return steel() * (1 - secondary_growth())


@component.add(
    name="secondary",
    units="Mtsteel",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"steel": 1, "secondary_growth": 1},
)
def secondary():
    return steel() * secondary_growth()


@component.add(
    name="steel",
    units="Mtsteel",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def steel():
    """
    The change in European steel production is taken from Material Economics’ modelling based on EUROFER, which yields a 0.6% yearly increase in the steel stock/capacity up to the 2040s, when it stabilises at 193 million tonnes per year, up from 170 million tonnes per year today.
    !year
    !Mt steel
    """
    return np.interp(time(), [2019, 2040, 2050], [170, 193, 193])
