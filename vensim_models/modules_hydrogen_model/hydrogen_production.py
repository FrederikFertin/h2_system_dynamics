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
    units="€/kWe",
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
        electrolyser_capacity() > 1,
        lambda: one_gw_aec_capex()
        * electrolyser_capacity() ** (np.log(1 - learning_rate()) / np.log(2)),
        lambda: initial_gw_aec_capex()
        - (initial_gw_aec_capex() - one_gw_aec_capex()) * electrolyser_capacity(),
    )


@component.add(
    name="AEC CAPEX BASE", units="€/kW", comp_type="Constant", comp_subtype="Normal"
)
def aec_capex_base():
    return 1400


@component.add(
    name="AEC efficiency",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"aec_efficiency_improvement": 1, "aec_max_efficiency": 1},
)
def aec_efficiency():
    return aec_efficiency_improvement() * aec_max_efficiency()


@component.add(
    name="AEC efficiency improvement",
    units="scalar",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def aec_efficiency_improvement():
    return np.interp(time(), [2022.0, 2050.0], [0.8, 1.0])


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
    name="AEC max efficiency",
    units="percent",
    comp_type="Constant",
    comp_subtype="Normal",
)
def aec_max_efficiency():
    return 0.65


@component.add(
    name="AEC OPEX", units="percent", comp_type="Constant", comp_subtype="Normal"
)
def aec_opex():
    """
    Percentage of CAPEX - ren. fuels tech. catalogue
    """
    return 0.04


@component.add(
    name="Blue H2 CAPEX",
    units="€/kgH2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"grey_h2_capex": 1, "smr_emission_factor": 1, "ccs_capex": 1},
)
def blue_h2_capex():
    return grey_h2_capex() + smr_emission_factor() / 1000 * ccs_capex()


@component.add(
    name="Blue H2 CO2 WTP",
    units="€/tCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "green_h2_cost": 1,
        "grey_h2_cost": 1,
        "grey_h2_cost_wo_co2": 1,
        "ccs_cost": 1,
        "smr_emission_factor": 2,
        "cc_capture_rate": 1,
    },
)
def blue_h2_co2_wtp():
    """
    Blue_cost = Grey H2 cost wo CO2 + SMR emission factor/1000 * (CCS cost + (1-CC Capture Rate) * CARBON TAX) + SMR emission factor/1000 * (CCS OPEX - CC Capture Rate * CARBON TAX) + SMR emission factor/1000 * CCS CAPEX
    """
    return (
        np.minimum(green_h2_cost(), grey_h2_cost())
        - grey_h2_cost_wo_co2()
        - smr_emission_factor() / 1000 * ccs_cost()
    ) / (smr_emission_factor() / 1000 * (1 - cc_capture_rate()))


@component.add(
    name="Blue H2 cost",
    units="€/kgH2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"blue_h2_capex": 1, "blue_h2_opex": 1},
)
def blue_h2_cost():
    return blue_h2_capex() + blue_h2_opex()


@component.add(
    name="Blue H2 OPEX",
    units="€/kgH2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "grey_h2_variable_cost": 1,
        "cc_capture_rate": 1,
        "smr_emission_factor": 1,
        "carbon_tax": 1,
        "ccs_opex": 1,
    },
)
def blue_h2_opex():
    return grey_h2_variable_cost() + smr_emission_factor() / 1000 * (
        ccs_opex() - cc_capture_rate() * carbon_tax()
    )


@component.add(
    name="electrolyser capacity",
    units="GW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_green_hydrogen_demand": 1,
        "aec_efficiency": 1,
        "electrolyser_operating_hours": 1,
        "pilot_plant_capacity": 1,
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
        + pilot_plant_capacity()
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
    name="FC EC induced learning curve",
    units="scalar",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"electrolyser_capacity": 1, "learning_rate": 1},
)
def fc_ec_induced_learning_curve():
    return np.minimum(
        1, electrolyser_capacity() ** (np.log(1 - learning_rate() / 2) / np.log(2))
    )


@component.add(
    name="Green H2 actual subsidy",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"raw_green_h2_cost": 1, "green_h2_cost": 1},
)
def green_h2_actual_subsidy():
    return raw_green_h2_cost() - green_h2_cost()


@component.add(
    name="Green H2 CAPEX",
    units="€/kgH2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "aec_capex": 1,
        "aec_af": 1,
        "electrolyser_operating_hours": 1,
        "aec_efficiency": 1,
        "h2_lhv": 1,
    },
)
def green_h2_capex():
    return (
        aec_capex()
        * aec_af()
        / electrolyser_operating_hours()
        / aec_efficiency()
        * h2_lhv()
    )


@component.add(
    name="Green H2 cost",
    units="€/kgH2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"raw_green_h2_cost": 1, "green_h2_subsidy": 1},
)
def green_h2_cost():
    """
    First CAPEX and OPEX is calculated as €/kWh input energy, then as €/kWh output H2. Electricity costs are added on top, also as €/kWh output H2. Multiplied by LHV of H2 to change the value to €/kg
    """
    return np.maximum(raw_green_h2_cost() - green_h2_subsidy(), 0.1)


@component.add(
    name="Green H2 H2 WTP",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"blue_h2_cost": 1, "grey_h2_cost": 1},
)
def green_h2_h2_wtp():
    return np.minimum(blue_h2_cost(), grey_h2_cost())


@component.add(
    name="Green H2 OPEX",
    units="€/kgH2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "aec_capex": 1,
        "aec_opex": 1,
        "electrolyser_operating_hours": 1,
        "renewable_electricity_price": 1,
        "aec_efficiency": 1,
        "h2_lhv": 1,
    },
)
def green_h2_opex():
    return (
        (
            aec_capex() * aec_opex() / electrolyser_operating_hours()
            + renewable_electricity_price() / 1000
        )
        / aec_efficiency()
        * h2_lhv()
    )


@component.add(
    name="Green H2 subsidy",
    units="€/kgH2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "yearly_total_subsidies_limit": 1,
        "total_subsidies_ytd": 1,
        "green_h2_subsidy_size": 1,
        "pulse_h2_subsidy": 1,
    },
)
def green_h2_subsidy():
    return if_then_else(
        yearly_total_subsidies_limit() >= total_subsidies_ytd(),
        lambda: green_h2_subsidy_size() * pulse_h2_subsidy(),
        lambda: 0,
    )


@component.add(
    name="Green H2 subsidy size",
    units="€/kgH2",
    comp_type="Constant",
    comp_subtype="Normal",
)
def green_h2_subsidy_size():
    return 0


@component.add(
    name="Grey H2 CAPEX",
    units="€/kgH2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"smr_capex": 1, "smr_af": 1, "smr_fixed_opex": 1},
)
def grey_h2_capex():
    return (smr_capex() * smr_af() + smr_fixed_opex()) / 1000


@component.add(
    name="Grey H2 CO2 WTP",
    units="€/tCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "blue_h2_cost": 1,
        "green_h2_cost": 1,
        "grey_h2_cost_wo_co2": 1,
        "smr_emission_factor": 1,
    },
)
def grey_h2_co2_wtp():
    return (
        (np.minimum(blue_h2_cost(), green_h2_cost()) - grey_h2_cost_wo_co2())
        / smr_emission_factor()
        * 1000
    )


@component.add(
    name="Grey H2 cost",
    units="€/kgH2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"grey_h2_capex": 1, "grey_h2_variable_cost": 1},
)
def grey_h2_cost():
    """
    €/kg grey H2
    """
    return grey_h2_capex() + grey_h2_variable_cost()


@component.add(
    name="Grey H2 cost wo CO2",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "smr_capex": 1,
        "smr_af": 1,
        "smr_fixed_opex": 1,
        "gas_price": 1,
        "smr_ng_usage": 1,
        "grid_electricity_price": 1,
        "smr_el_usage": 1,
    },
)
def grey_h2_cost_wo_co2():
    """
    Cost_grey = SMR CAPEX * (SMR AF + SMR OPEX) / SMR operating hours * H2 LHV + (GAS PRICE/1000 * 3.6) / SMR efficiency * H2 LHV + (CARBON TAX/1000) * SMR emission factor CT** = (Alt_cost - (SMR CAPEX * (SMR AF + SMR OPEX) / SMR operating hours * H2 LHV + (GAS PRICE/1000 * 3.6) / SMR efficiency * H2 LHV)) / SMR emission factor * 1000
    """
    return (
        smr_capex() * smr_af()
        + smr_fixed_opex()
        + gas_price() * smr_ng_usage()
        + grid_electricity_price() * smr_el_usage()
    ) / 1000


@component.add(
    name="Grey H2 variable cost",
    units="€/kgH2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "carbon_tax": 1,
        "smr_emission_factor": 1,
        "gas_price": 1,
        "smr_ng_usage": 1,
        "grid_electricity_price": 1,
        "smr_el_usage": 1,
    },
)
def grey_h2_variable_cost():
    return (
        carbon_tax() * smr_emission_factor()
        + gas_price() * smr_ng_usage()
        + grid_electricity_price() * smr_el_usage()
    ) / 1000


@component.add(
    name="H2 LHV", units="kWh/kg", comp_type="Constant", comp_subtype="Unchangeable"
)
def h2_lhv():
    """
    33.33 kWh/kg as LHV H2
    """
    return 33.33


@component.add(
    name="H2 subsidy length", units="years", comp_type="Constant", comp_subtype="Normal"
)
def h2_subsidy_length():
    return 10


@component.add(
    name="Initial GW AEC CAPEX",
    units="€/kW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"aec_capex_base": 1},
)
def initial_gw_aec_capex():
    return 1.3 * aec_capex_base()


@component.add(
    name="learning rate", units="percent", comp_type="Constant", comp_subtype="Normal"
)
def learning_rate():
    return 0.18


@component.add(
    name="One GW AEC CAPEX",
    units="€/kW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"aec_capex_base": 1},
)
def one_gw_aec_capex():
    return aec_capex_base()


@component.add(
    name="pilot plant capacity", units="GW", comp_type="Constant", comp_subtype="Normal"
)
def pilot_plant_capacity():
    """
    Can be used to include already installed capacity, which is not present in any of the sectors (pilot plants and demonstrations)
    """
    return 0.08


@component.add(
    name="pulse H2 subsidy",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"h2_subsidy_length": 1, "time": 1},
)
def pulse_h2_subsidy():
    return pulse(__data["time"], 2025, width=h2_subsidy_length())


@component.add(
    name="Raw green H2 cost",
    units="€/kgH2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_h2_capex": 1, "green_h2_opex": 1},
)
def raw_green_h2_cost():
    return green_h2_capex() + green_h2_opex()


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
    name="SMR CAPEX", units="€/(tH2/yr)", comp_type="Constant", comp_subtype="Normal"
)
def smr_capex():
    """
    €/(tH2/yr)
    """
    return 5306


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


@component.add(name="SMR costs", comp_type="Constant", comp_subtype="Normal")
def smr_costs():
    return 2


@component.add(
    name="SMR El usage", units="MWh/tH2", comp_type="Constant", comp_subtype="Normal"
)
def smr_el_usage():
    return 0.549


@component.add(
    name="SMR emission factor",
    units="tCO2/tH2",
    comp_type="Constant",
    comp_subtype="Normal",
)
def smr_emission_factor():
    return 8.545


@component.add(
    name="SMR fixed OPEX", units="€/tH2", comp_type="Constant", comp_subtype="Normal"
)
def smr_fixed_opex():
    return 311


@component.add(
    name="SMR lifetime", units="years", comp_type="Constant", comp_subtype="Normal"
)
def smr_lifetime():
    return 20


@component.add(
    name="SMR NG usage", units="GJ/tH2", comp_type="Constant", comp_subtype="Normal"
)
def smr_ng_usage():
    """
    GJ ng/t H2
    """
    return 170.9


@component.add(
    name="yearly total subsidies limit",
    units="M€",
    comp_type="Constant",
    comp_subtype="Normal",
)
def yearly_total_subsidies_limit():
    return 10000 * 100
