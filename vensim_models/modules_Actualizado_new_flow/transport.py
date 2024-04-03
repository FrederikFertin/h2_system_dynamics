"""
Module transport
Translated using PySD version 3.13.4
"""


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


@component.add(
    name='"bio kerosene - hydrogen rate"',
    units="MWh H2 / MWh kero",
    comp_type="Constant",
    comp_subtype="Normal",
)
def bio_kerosene_hydrogen_rate():
    return 0.15


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
    name='"biomethanol - hydrogen rate"', comp_type="Constant", comp_subtype="Normal"
)
def biomethanol_hydrogen_rate():
    return 2


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
    name="diesel locomotive efficiency", comp_type="Constant", comp_subtype="Normal"
)
def diesel_locomotive_efficiency():
    return 0.3


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
    name='"dom. navigation energy demand"',
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dom_navigation_energy_consumption": 1, "ice_efficiency": 1},
)
def dom_navigation_energy_demand():
    return dom_navigation_energy_consumption() * ice_efficiency()


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
    name='"dom. navigation fossil fuel demand"',
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dom_navigation_energy_demand": 1, "bev_implementation_curve": 1},
)
def dom_navigation_fossil_fuel_demand():
    return dom_navigation_energy_demand() * (1 - bev_implementation_curve())


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
    name='"HYDROGEN F. SHIPPING"',
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hydrogen_ammonia_shipping": 1, "hydrogen_methanol_shipping": 1},
)
def hydrogen_f_shipping():
    return hydrogen_ammonia_shipping() + hydrogen_methanol_shipping()


@component.add(
    name="HYDROGEN METHANOL SHIPPING",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "methanol_ice_energy_consumption": 1,
        "synthetic_methanol_hydrogen_rate": 1,
        "biomethanol_hydrogen_rate": 1,
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


@component.add(name="ICE efficiency", comp_type="Constant", comp_subtype="Normal")
def ice_efficiency():
    """
    Considering the same efficiency for all the fossil fuel engines
    """
    return 0.45


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
    name='"syn kerosene - hydrogen rate"',
    units="MWh H2 / MWh kero",
    comp_type="Constant",
    comp_subtype="Normal",
)
def syn_kerosene_hydrogen_rate():
    return 1.2


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
    name='"synthetic methanol - hydrogen rate"',
    units="MWh H2 / t synmethanol",
    comp_type="Constant",
    comp_subtype="Normal",
)
def synthetic_methanol_hydrogen_rate():
    return 6.3
