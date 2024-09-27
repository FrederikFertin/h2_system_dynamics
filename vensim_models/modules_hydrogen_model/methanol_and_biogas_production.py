"""
Module methanol_and_biogas_production
Translated using PySD version 3.14.0
"""

@component.add(
    name="biogas AF",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"discount_rate": 2, "biogas_lifetime": 1},
)
def biogas_af():
    return 1 / ((1 - (1 + discount_rate()) ** -biogas_lifetime()) / discount_rate())


@component.add(
    name="biogas biomass usage",
    units="GJ Biomass / GJ biogas",
    comp_type="Constant",
    comp_subtype="Normal",
)
def biogas_biomass_usage():
    """
    1.67 GJ biogas is produced per ton of biomass. Each ton of biomass contains 2.81 GJ of energy.
    """
    return 2.81 / 1.67


@component.add(
    name="biogas CAPEX",
    units="€/MW",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def biogas_capex():
    return np.interp(
        time(), [2015.0, 2025.0, 2030.0, 2040.0, 2050.0], [1.04, 1.04, 0.9, 0.87, 0.82]
    )


@component.add(
    name="biogas cost",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biogas_af": 1,
        "biogas_capex": 1,
        "biogas_opex": 1,
        "biogas_operating_hours": 1,
        "biogas_electricity_usage": 1,
        "renewable_electricity_price": 1,
        "biogas_heat_usage": 1,
        "heat_cost": 1,
        "biogas_biomass_usage": 1,
        "biomass_price": 1,
    },
)
def biogas_cost():
    """
    Assumes 8500 full load hours - no mention of downtime in the tech. catalogue. OPEX multiplied by 2.28/3.42 to not double-count electricity and heat costs.
    """
    return (
        (biogas_af() * biogas_capex() * 1000 + biogas_opex() * 2.28 / 3.42)
        * 1000
        / biogas_operating_hours()
        / 3.6
        + biogas_electricity_usage() * renewable_electricity_price() * 1000 / 3.6
        + biogas_heat_usage() * heat_cost() / 3.6
        + biogas_biomass_usage() * biomass_price()
    )


@component.add(
    name="biogas electricity usage",
    units="GJ el / GJ biogas",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def biogas_electricity_usage():
    return np.interp(
        time(),
        [2015.0, 2025.0, 2030.0, 2040.0, 2050.0],
        [0.0216, 0.0216, 0.0188, 0.0182, 0.0171],
    )


@component.add(
    name="biogas heat usage",
    units="GJ heat / GJ biogas",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def biogas_heat_usage():
    return np.interp(
        time(),
        [2015.0, 2025.0, 2030.0, 2040.0, 2050.0],
        [0.0505, 0.0505, 0.044, 0.0425, 0.0425],
    )


@component.add(
    name="biogas lifetime", units="years", comp_type="Constant", comp_subtype="Normal"
)
def biogas_lifetime():
    return 20


@component.add(
    name="biogas operating hours",
    units="hours",
    comp_type="Constant",
    comp_subtype="Normal",
)
def biogas_operating_hours():
    return 8000


@component.add(
    name="biogas OPEX",
    units="k€/MW/yr",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def biogas_opex():
    return np.interp(
        time(),
        [2015.0, 2025.0, 2030.0, 2040.0, 2050.0],
        [63.98, 63.98, 55.66, 53.74, 50.54],
    )


@component.add(
    name="bioMeOH cost without H2",
    units="€/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "meoh_learning": 1,
        "meoh_capex": 1,
        "meoh_opex": 1,
        "meoh_af": 1,
        "meoh_operating_hours": 1,
        "meoh_lhv": 2,
        "heat_cost": 1,
        "renewable_electricity_price": 1,
        "meoh_electricity_usage": 1,
        "meoh_excess_heat": 1,
        "biomass_price": 1,
        "meoh_biomass_usage": 1,
    },
)
def biomeoh_cost_without_h2():
    """
    €/MJ MeOH [ [kgBM/kgMeOH] * [€/GJ] * [MJ/kgBM ] / [MJ/GJ] + [€/kgH2] / [kgMeOH/kgH2] + [€/kWh * kWh/kgMeOH] ] / [MJ/kgMeOH]
    """
    return (
        meoh_learning()
        * meoh_capex()
        * (meoh_af() + meoh_opex())
        / (meoh_operating_hours() * meoh_lhv())
        + (
            renewable_electricity_price() * meoh_electricity_usage()
            - heat_cost() / 1000 * meoh_excess_heat()
        )
        / meoh_lhv()
        + meoh_biomass_usage() * biomass_price() / 1000
    )


@component.add(
    name="Blue bioMeOH cost",
    units="€/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biomeoh_cost_without_h2": 1,
        "blue_h2_cost": 1,
        "meoh_h2_usage": 1,
        "meoh_lhv": 1,
    },
)
def blue_biomeoh_cost():
    return biomeoh_cost_without_h2() + blue_h2_cost() / meoh_h2_usage() / meoh_lhv()


@component.add(
    name="Blue eMeOH cost",
    units="€/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "emeoh_cost_without_hydrogen": 1,
        "blue_h2_cost": 1,
        "emeoh_h2_usage": 1,
        "meoh_lhv": 1,
    },
)
def blue_emeoh_cost():
    return (
        emeoh_cost_without_hydrogen() + blue_h2_cost() / emeoh_h2_usage() / meoh_lhv()
    )


@component.add(
    name="convMeOH AF",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"discount_rate": 2, "convmeoh_lifetime": 1},
)
def convmeoh_af():
    return 1 / ((1 - (1 + discount_rate()) ** -convmeoh_lifetime()) / discount_rate())


@component.add(
    name="convMeOH CAPEX", units="€/(t/yr)", comp_type="Constant", comp_subtype="Normal"
)
def convmeoh_capex():
    return 846.73


@component.add(
    name="convMeOH cost",
    units="€/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "convmeoh_electricity_usage": 1,
        "grid_electricity_price": 1,
        "convmeoh_emission_factor": 1,
        "carbon_tax": 1,
        "convmeoh_gas_usage": 1,
        "gas_price": 1,
        "convmeoh_opex": 1,
        "convmeoh_capex": 1,
        "convmeoh_af": 1,
        "meoh_lhv": 1,
    },
)
def convmeoh_cost():
    return (
        (
            convmeoh_electricity_usage() * grid_electricity_price() * 1000
            + convmeoh_emission_factor() * carbon_tax()
            + convmeoh_gas_usage() * gas_price()
            + convmeoh_opex()
            + convmeoh_capex() * convmeoh_af()
        )
        / 1000
        / meoh_lhv()
    )


@component.add(
    name="convMeOH electricity usage",
    units="MWh/t MeOH",
    comp_type="Constant",
    comp_subtype="Normal",
)
def convmeoh_electricity_usage():
    return 0.147


@component.add(
    name="convMeOH emission factor",
    units="tCO2/tMeOH",
    comp_type="Constant",
    comp_subtype="Normal",
)
def convmeoh_emission_factor():
    """
    Direct + indirect CO2 emissions + combustion emissions
    """
    return 0.695 + 0.073 + 0.069 * 19.9


@component.add(
    name="convMeOH gas usage", units="GJ/t", comp_type="Constant", comp_subtype="Normal"
)
def convmeoh_gas_usage():
    """
    https://petrowiki.spe.org/Gas_to_methanol
    """
    return 45.26


@component.add(
    name="convMeOH lifetime", units="years", comp_type="Constant", comp_subtype="Normal"
)
def convmeoh_lifetime():
    return 25


@component.add(
    name="convMeOH OPEX", units="€/t", comp_type="Constant", comp_subtype="Normal"
)
def convmeoh_opex():
    """
    Variable costs + fixed costs
    """
    return 42.84


@component.add(
    name="eMeOH AF",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"discount_rate": 2, "emeoh_lifetime": 1},
)
def emeoh_af():
    return 1 / ((1 - (1 + discount_rate()) ** -emeoh_lifetime()) / discount_rate())


@component.add(
    name="eMeOH CAPEX", units="€/kgMeOH/h", comp_type="Constant", comp_subtype="Normal"
)
def emeoh_capex():
    return 10000


@component.add(
    name="eMeOH CO2 usage",
    units="kgCO2/kgMeOH",
    comp_type="Constant",
    comp_subtype="Normal",
)
def emeoh_co2_usage():
    """
    kg CO2 per kg MeOH
    """
    return 1.374


@component.add(
    name="eMeOH cost without hydrogen",
    units="€/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "emeoh_capex": 1,
        "emeoh_af": 1,
        "emeoh_opex": 1,
        "emeoh_operating_hours": 1,
        "meoh_lhv": 2,
        "emeoh_electricity_usage": 1,
        "ps_cc_cost": 1,
        "renewable_electricity_price": 1,
        "emeoh_co2_usage": 1,
        "heat_cost": 1,
        "cc_capture_rate": 1,
        "emeoh_excess_heat": 1,
    },
)
def emeoh_cost_without_hydrogen():
    """
    €/MJ MeOH [ [kgBM/kgMeOH] * [€/GJ] * [MJ/kgBM ] / [MJ/GJ] + [€/kgH2] / [kgMeOH/kgH2] + [€/kWh * kWh/kgMeOH] ] / [MJ/kgMeOH]
    """
    return (
        emeoh_capex()
        * (emeoh_af() + emeoh_opex())
        / (emeoh_operating_hours() * meoh_lhv())
        + (
            emeoh_co2_usage() * (ps_cc_cost() / cc_capture_rate() / 1000)
            + renewable_electricity_price() * emeoh_electricity_usage()
            - heat_cost() / 1000 * emeoh_excess_heat()
        )
        / meoh_lhv()
    )


@component.add(
    name="eMeOH electricity usage",
    units="kWh/kgMeOH",
    comp_type="Constant",
    comp_subtype="Normal",
)
def emeoh_electricity_usage():
    """
    kWhe/kgMeOH
    """
    return 0.316


@component.add(
    name="eMeOH excess heat",
    units="kWh/kg MeOH",
    comp_type="Constant",
    comp_subtype="Normal",
)
def emeoh_excess_heat():
    return 0.68


@component.add(
    name="eMeOH H2 usage",
    units="kgMeOH/kgH2",
    comp_type="Constant",
    comp_subtype="Normal",
)
def emeoh_h2_usage():
    """
    kg MeOH per kg H2
    """
    return 5.26


@component.add(
    name="eMeOH lifetime", units="years", comp_type="Constant", comp_subtype="Normal"
)
def emeoh_lifetime():
    return 20


@component.add(
    name="eMeOH operating hours", units="h", comp_type="Constant", comp_subtype="Normal"
)
def emeoh_operating_hours():
    return 8000


@component.add(
    name="eMeOH OPEX", units="percent", comp_type="Constant", comp_subtype="Normal"
)
def emeoh_opex():
    """
    Percentage of CAPEX
    """
    return 0.04


@component.add(
    name="Green bioMeOH cost",
    units="€/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biomeoh_cost_without_h2": 1,
        "green_h2_cost": 1,
        "meoh_h2_usage": 1,
        "meoh_lhv": 1,
    },
)
def green_biomeoh_cost():
    return biomeoh_cost_without_h2() + green_h2_cost() / meoh_h2_usage() / meoh_lhv()


@component.add(
    name="Green eMeOH cost",
    units="€/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "emeoh_cost_without_hydrogen": 1,
        "green_h2_cost": 1,
        "emeoh_h2_usage": 1,
        "meoh_lhv": 1,
    },
)
def green_emeoh_cost():
    return (
        emeoh_cost_without_hydrogen() + green_h2_cost() / emeoh_h2_usage() / meoh_lhv()
    )


@component.add(
    name="Grey bioMeOH cost",
    units="€/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biomeoh_cost_without_h2": 1,
        "grey_h2_cost": 1,
        "meoh_h2_usage": 1,
        "meoh_lhv": 1,
    },
)
def grey_biomeoh_cost():
    return biomeoh_cost_without_h2() + grey_h2_cost() / meoh_h2_usage() / meoh_lhv()


@component.add(
    name="Grey eMeOH cost",
    units="€/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "emeoh_cost_without_hydrogen": 1,
        "grey_h2_cost": 1,
        "emeoh_h2_usage": 1,
        "meoh_lhv": 1,
    },
)
def grey_emeoh_cost():
    return (
        emeoh_cost_without_hydrogen() + grey_h2_cost() / emeoh_h2_usage() / meoh_lhv()
    )


@component.add(
    name="MeOH AF",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"discount_rate": 2, "meoh_lifetime": 1},
)
def meoh_af():
    return 1 / ((1 - (1 + discount_rate()) ** -meoh_lifetime()) / discount_rate())


@component.add(
    name="MeOH biomass usage",
    units="kWh biomass/kWh MeOH",
    comp_type="Constant",
    comp_subtype="Normal",
)
def meoh_biomass_usage():
    """
    kWh biomass/kWh MeOH Source:https://doi.org/10.1016/j.energy.2020.118432
    """
    return 0.73


@component.add(
    name="MeOH CAPEX", units="€/kgMeOH/h", comp_type="Constant", comp_subtype="Normal"
)
def meoh_capex():
    return 20000


@component.add(
    name="MeOH electricity usage",
    units="kWh/kgMeOH",
    comp_type="Constant",
    comp_subtype="Normal",
)
def meoh_electricity_usage():
    """
    kWhe/kgMeOH
    """
    return 0.64


@component.add(
    name="MeOH excess heat",
    units="kWh/kgMeOH",
    comp_type="Constant",
    comp_subtype="Normal",
)
def meoh_excess_heat():
    return 0.428


@component.add(
    name="MeOH H2 usage",
    units="kgMeOH/kgH2",
    comp_type="Constant",
    comp_subtype="Normal",
)
def meoh_h2_usage():
    """
    kg MeOH per kg H2
    """
    return 15.7


@component.add(
    name="MeOH learning",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "meoh_plant_size": 2,
        "domestic_meoh_shipping_consumption": 1,
        "meoh_shipping_consumption": 1,
        "meoh_learning_rate": 1,
    },
)
def meoh_learning():
    return (
        np.maximum(
            meoh_plant_size(),
            domestic_meoh_shipping_consumption() + meoh_shipping_consumption(),
        )
        / meoh_plant_size()
    ) ** (np.log(1 - meoh_learning_rate()) / np.log(2))


@component.add(name="MeOH learning rate", comp_type="Constant", comp_subtype="Normal")
def meoh_learning_rate():
    return 0.08


@component.add(
    name="MeOH LHV", units="MJ/kg", comp_type="Constant", comp_subtype="Normal"
)
def meoh_lhv():
    return 19.9


@component.add(
    name="MeOH lifetime", units="years", comp_type="Constant", comp_subtype="Normal"
)
def meoh_lifetime():
    return 20


@component.add(
    name="MeOH operating hours", units="h", comp_type="Constant", comp_subtype="Normal"
)
def meoh_operating_hours():
    return 8000


@component.add(
    name="MeOH OPEX", units="percent", comp_type="Constant", comp_subtype="Normal"
)
def meoh_opex():
    """
    Percentage of CAPEX
    """
    return 0.04


@component.add(
    name="MeOH plant size",
    units="GWh/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def meoh_plant_size():
    return 400 * 1000 * 19.9 / 3600
