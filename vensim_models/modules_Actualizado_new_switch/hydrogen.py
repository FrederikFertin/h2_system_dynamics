"""
Module hydrogen
Translated using PySD version 3.13.4
"""


@component.add(
    name="CAPEX hydrogen",
    units="€/kWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"electrolyser_cost": 1, "electrolyser_lifetime": 1},
)
def capex_hydrogen():
    return electrolyser_cost() / electrolyser_lifetime()


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
    name="electroliser efficiency",
    units="{%}",
    comp_type="Constant",
    comp_subtype="Normal",
)
def electroliser_efficiency():
    return 0.7


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
            1.00e05,
            1.00e06,
            1.00e07,
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
            140.0,
            130.0,
            120.0,
        ],
    )


@component.add(
    name="electrolyser efficiency", comp_type="Constant", comp_subtype="Normal"
)
def electrolyser_efficiency():
    return 0.63


@component.add(
    name="electrolyser lifetime", units="h", comp_type="Constant", comp_subtype="Normal"
)
def electrolyser_lifetime():
    return 60000


@component.add(
    name="hydrogen price",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"capex_hydrogen": 1, "opex_hydrogen": 1, "electrolyser_efficiency": 1},
)
def hydrogen_price():
    """
    33.33 kWh/kg as LHV H2
    """
    return (capex_hydrogen() + opex_hydrogen()) * (33.33 / electrolyser_efficiency())


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
        "shipping_hydrogen_demand": 1,
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
        + shipping_hydrogen_demand()
    )
