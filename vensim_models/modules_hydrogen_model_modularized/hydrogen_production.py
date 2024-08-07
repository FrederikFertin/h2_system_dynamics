"""
Module hydrogen_production
Translated using PySD version 3.14.0
"""

@component.add(
    name="AEC AF",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"discount_rate": 2, "aec_lifetime": 1},
)
def aec_af():
    return 1 / ((1 - (1 + discount_rate()) ** -aec_lifetime()) / discount_rate())


@component.add(
    name="AEC CAPEX",
    units="€/kW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "electrolyser_capacity": 3,
        "one_gw_aec_capex": 2,
        "learning_rate": 1,
        "initial_gw_aec_capex": 2,
    },
)
def aec_capex():
    """
    If it is desired to use the Irena learning curve from Carmen's work: - Initial GW AEC CAPEX should be set to 650 €/kW. - One GW AEC CAPEX should be set to 600 €/kW. IF statement used to ensure reasonable costs at very low levels of installed electrolysis.
    """
    return if_then_else(
        electrolyser_capacity() > 0.6,
        lambda: one_gw_aec_capex()
        * electrolyser_capacity() ** (np.log(1 - learning_rate()) / np.log(2)),
        lambda: initial_gw_aec_capex()
        - (initial_gw_aec_capex() - one_gw_aec_capex()) * electrolyser_capacity(),
    )


@component.add(
    name="AEC efficiency",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def aec_efficiency():
    return np.interp(time(), [2019.0, 2050.0], [0.53, 0.53])


@component.add(
    name="AEC lifetime",
    units="years",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"aec_lifetime_hours": 1, "electrolyser_operating_hours": 1},
)
def aec_lifetime():
    """
    electrolyzer lifetime in years
    """
    return aec_lifetime_hours() / electrolyser_operating_hours()


@component.add(
    name="AEC lifetime hours", units="h", comp_type="Constant", comp_subtype="Normal"
)
def aec_lifetime_hours():
    """
    electrolyzer lifetime in hours
    """
    return 70000


@component.add(
    name="AEC OPEX", units="percent", comp_type="Constant", comp_subtype="Normal"
)
def aec_opex():
    """
    Percentage of CAPEX - ren. fuels tech. catalogue
    """
    return 0.04


@component.add(
    name="Alternative Blue price",
    units="€/kgH2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "grey_h2_price": 1,
        "smr_emission_factor": 1,
        "ccs_cost": 1,
        "carbon_tax": 1,
        "cc_capture_rate": 1,
    },
)
def alternative_blue_price():
    return (
        grey_h2_price()
        + smr_emission_factor() * cc_capture_rate() * (ccs_cost() - carbon_tax()) / 1000
    )


@component.add(
    name="Blue H2 price",
    units="€/kgH2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "smr_ccs_capex": 1,
        "smr_af": 1,
        "smr_ccs_opex": 1,
        "smr_operating_hours": 1,
        "smr_ccs_efficiency": 1,
        "gas_price": 1,
        "carbon_tax": 1,
        "smr_ccs_emission_factor": 1,
    },
)
def blue_h2_price():
    """
    €/kg H2
    """
    return (
        smr_ccs_capex() * (smr_af() + smr_ccs_opex()) / smr_operating_hours()
        + (gas_price() / 1000 * 3.6) / smr_ccs_efficiency()
        + (carbon_tax() / 1000) * (smr_ccs_emission_factor() / 33.33)
    ) * 33.33


@component.add(name="CAPEX multiplier", comp_type="Constant", comp_subtype="Normal")
def capex_multiplier():
    return 1


@component.add(name="constant demand", comp_type="Constant", comp_subtype="Normal")
def constant_demand():
    return 20000000.0 * 0


@component.add(
    name="electrolyser capacity",
    units="GW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_green_hydrogen_demand": 1,
        "aec_efficiency": 1,
        "electrolyser_operating_hours": 1,
    },
)
def electrolyser_capacity():
    """
    Hydrogen demand (tH2) * 1000 (kgH2/tH2) * 33.33 (kWhH2/kgH2) / efficiency / working hours (h) *10^-6 (GW/kW)= GW of electroliser capacity
    """
    return (
        total_green_hydrogen_demand()
        * 33.33
        / aec_efficiency()
        / electrolyser_operating_hours()
        / 1000
    )


@component.add(
    name="electrolyser operating hours",
    units="h",
    comp_type="Constant",
    comp_subtype="Normal",
)
def electrolyser_operating_hours():
    return 4000


@component.add(
    name="Green H2 price",
    units="€/kgH2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"raw_green_h2_price": 1, "green_h2_subsidy": 1},
)
def green_h2_price():
    """
    First CAPEX and OPEX is calculated as €/kWh input energy, then as €/kWh output H2. Electricity costs are added on top, also as €/kWh output H2. Multiplied by LHV of H2 to change the value to €/kg
    """
    return np.maximum(raw_green_h2_price() - green_h2_subsidy(), 0.1)


@component.add(
    name="Green H2 subsidy",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_h2_subsidy_size": 1, "pulse_h2_subsidy": 1},
)
def green_h2_subsidy():
    return green_h2_subsidy_size() * pulse_h2_subsidy()


@component.add(
    name="Green H2 subsidy size",
    units="€/kgH2",
    comp_type="Constant",
    comp_subtype="Normal",
)
def green_h2_subsidy_size():
    return 0


@component.add(
    name="Grey H2 price",
    units="€/kgH2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "smr_capex": 1,
        "smr_af": 1,
        "smr_opex": 1,
        "smr_operating_hours": 1,
        "gas_price": 1,
        "smr_efficiency": 1,
        "smr_emission_factor": 1,
        "carbon_tax": 1,
    },
)
def grey_h2_price():
    """
    €/kg grey H2
    """
    return (
        smr_capex() * (smr_af() + smr_opex()) / smr_operating_hours()
        + (gas_price() / 1000 * 3.6) / smr_efficiency()
        + (carbon_tax() / 1000) * (smr_emission_factor() / 33.33)
    ) * 33.33


@component.add(
    name="in TWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"lhv_h2": 1, "total_green_hydrogen_demand": 1},
)
def in_twh():
    return lhv_h2() * total_green_hydrogen_demand() / 10**6


@component.add(
    name="industry hydrogen demand",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fertilizer_hydrogen_demand": 1,
        "naphtha_hydrogen_demand": 1,
        "nonmetallic_industry_hydrogen_demand": 1,
        "refinery_hydrogen_demand": 1,
        "steel_hydrogen_demand": 1,
        "meoh_hydrogen_demand": 1,
    },
)
def industry_hydrogen_demand():
    return (
        fertilizer_hydrogen_demand()
        + naphtha_hydrogen_demand()
        + nonmetallic_industry_hydrogen_demand()
        + refinery_hydrogen_demand()
        + steel_hydrogen_demand()
        + meoh_hydrogen_demand()
    )


@component.add(
    name="Initial GW AEC CAPEX",
    units="€/kW",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_gw_aec_capex():
    return 2500


@component.add(
    name="learning rate", units="percent", comp_type="Constant", comp_subtype="Normal"
)
def learning_rate():
    return 0.18


@component.add(
    name="LHV H2", units="kWh/kg", comp_type="Constant", comp_subtype="Normal"
)
def lhv_h2():
    """
    33.33 kWh/kg as LHV H2
    """
    return 33.33


@component.add(name="One GW AEC CAPEX", comp_type="Constant", comp_subtype="Normal")
def one_gw_aec_capex():
    return 1900


@component.add(
    name="pulse H2 subsidy",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1},
)
def pulse_h2_subsidy():
    return pulse(__data["time"], 2015, width=30)


@component.add(
    name="Raw green H2 price",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "aec_capex": 1,
        "aec_af": 1,
        "aec_opex": 1,
        "electrolyser_operating_hours": 1,
        "aec_efficiency": 2,
        "capex_multiplier": 1,
        "electricity_price": 1,
        "lhv_h2": 1,
    },
)
def raw_green_h2_price():
    return (
        aec_capex()
        * (aec_af() + aec_opex())
        / electrolyser_operating_hours()
        / aec_efficiency()
        * capex_multiplier()
        + electricity_price() / aec_efficiency()
    ) * lhv_h2()


@component.add(
    name="SMR AF",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"discount_rate": 2, "smr_lifetime": 1},
)
def smr_af():
    return 1 / ((1 - (1 + discount_rate()) ** -smr_lifetime()) / discount_rate())


@component.add(
    name="SMR CAPEX", units="€/kWH2", comp_type="Constant", comp_subtype="Normal"
)
def smr_capex():
    """
    €/kWH2
    """
    return 800


@component.add(
    name="SMR CCS CAPEX",
    units="€/kWH2",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def smr_ccs_capex():
    """
    €/kWH2
    """
    return np.interp(time(), [2019, 2030, 2050], [1680, 1360, 1280])


@component.add(
    name="SMR CCS efficiency",
    units="percent",
    comp_type="Constant",
    comp_subtype="Normal",
)
def smr_ccs_efficiency():
    return 0.69


@component.add(
    name="SMR CCS emission factor",
    units="kgCO2/kgH2",
    comp_type="Constant",
    comp_subtype="Normal",
)
def smr_ccs_emission_factor():
    """
    1 kgCO2 / kgH2
    """
    return 1


@component.add(
    name="SMR CCS OPEX", units="percent", comp_type="Constant", comp_subtype="Normal"
)
def smr_ccs_opex():
    """
    %/yr of CAPEX
    """
    return 0.047


@component.add(
    name="SMR efficiency", units="percent", comp_type="Constant", comp_subtype="Normal"
)
def smr_efficiency():
    return 0.76


@component.add(
    name="SMR emission factor",
    units="kgCO2/kgH2",
    comp_type="Constant",
    comp_subtype="Normal",
)
def smr_emission_factor():
    """
    8.9 kgCO2 / kgH2
    """
    return 8.9


@component.add(
    name="SMR lifetime", units="years", comp_type="Constant", comp_subtype="Normal"
)
def smr_lifetime():
    return 25


@component.add(
    name="SMR operating hours", units="h", comp_type="Constant", comp_subtype="Normal"
)
def smr_operating_hours():
    return 8500


@component.add(
    name="SMR OPEX", units="percent", comp_type="Constant", comp_subtype="Normal"
)
def smr_opex():
    """
    %/yr of CAPEX
    """
    return 0.047


@component.add(
    name="TOTAL GREEN HYDROGEN DEMAND",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "industry_hydrogen_demand": 1,
        "power_hydrogen_demand": 1,
        "transportation_hydrogen_demand": 1,
        "constant_demand": 1,
    },
)
def total_green_hydrogen_demand():
    return (
        industry_hydrogen_demand()
        + power_hydrogen_demand()
        + transportation_hydrogen_demand()
        + constant_demand()
    )


@component.add(
    name="total subsidies",
    units="M€",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_total_subsidies": 1},
    other_deps={
        "_integ_total_subsidies": {
            "initial": {},
            "step": {
                "raw_green_h2_price": 1,
                "green_h2_price": 1,
                "total_green_hydrogen_demand": 1,
            },
        }
    },
)
def total_subsidies():
    return _integ_total_subsidies()


_integ_total_subsidies = Integ(
    lambda: (raw_green_h2_price() - green_h2_price())
    * total_green_hydrogen_demand()
    / 1000,
    lambda: 0,
    "_integ_total_subsidies",
)


@component.add(
    name="transportation hydrogen demand",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_aviation_hydrogen_demand": 1,
        "domestic_shipping_hydrogen_demand": 1,
        "heavy_duty_hydrogen_demand": 1,
        "international_aviation_hydrogen_demand": 1,
        "international_shipping_hydrogen_demand": 1,
        "light_duty_hydrogen_demand": 1,
    },
)
def transportation_hydrogen_demand():
    return (
        domestic_aviation_hydrogen_demand()
        + domestic_shipping_hydrogen_demand()
        + heavy_duty_hydrogen_demand()
        + international_aviation_hydrogen_demand()
        + international_shipping_hydrogen_demand()
        + light_duty_hydrogen_demand()
    )
