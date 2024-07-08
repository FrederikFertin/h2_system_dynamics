"""
Module domestic_ship_propulsion_costs
Translated using PySD version 3.14.0
"""

@component.add(
    name="Battery capacity", units="MJ", comp_type="Constant", comp_subtype="Normal"
)
def battery_capacity():
    """
    Expected battery capacity of regionally sailing cargo ships. Based on Chinese example, which sails on a route with 600 nautical miles. https://maritime-executive.com/article/largest-electric-battery-powered-con tainerships-commissioned-in-china
    """
    return 50000 * 3.6


@component.add(
    name="Battery Ship CAPEX",
    units="€/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "lfp_capex": 1,
        "lfp_cycle_lifetime": 1,
        "lfp_lifetime": 1,
        "lfp_af": 1,
        "usd_to_eur": 1,
        "electric_ship_efficiency": 1,
    },
)
def battery_ship_capex():
    return (
        lfp_capex()
        / lfp_cycle_lifetime()
        * (lfp_af() / (1 / lfp_lifetime()))
        * usd_to_eur()
        / electric_ship_efficiency()
    )


@component.add(
    name="Battery Ship OPEX",
    units="€/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "electricity_price": 1,
        "charging_efficiency": 2,
        "charging_infrastructure_cost": 1,
        "usd_to_eur": 1,
        "opex_electrical": 1,
        "electric_ship_efficiency": 1,
    },
)
def battery_ship_opex():
    return (
        electricity_price() / 3.6 / charging_efficiency()
        + (charging_infrastructure_cost() / charging_efficiency() + opex_electrical())
        * usd_to_eur()
    ) / electric_ship_efficiency()


@component.add(
    name="Charging efficiency",
    units="percent",
    comp_type="Constant",
    comp_subtype="Normal",
)
def charging_efficiency():
    return 0.9


@component.add(
    name="Charging infrastructure cost",
    units="$/MJ",
    comp_type="Constant",
    comp_subtype="Normal",
)
def charging_infrastructure_cost():
    return 0.029 / 3.6


@component.add(
    name="Electric ship efficiency",
    units="percent",
    comp_type="Constant",
    comp_subtype="Normal",
)
def electric_ship_efficiency():
    """
    Assumption from: https://static-content.springer.com/esm/art%3A10.1038%2Fs41560-022-01065-y/ MediaObjects/41560_2022_1065_MOESM1_ESM.pdf
    """
    return 0.95 * 0.95


@component.add(
    name="Electrical propulsion cost",
    units="€/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"battery_ship_capex": 1, "battery_ship_opex": 1},
)
def electrical_propulsion_cost():
    return battery_ship_capex() + battery_ship_opex()


@component.add(name="fuel cell efficiency", comp_type="Constant", comp_subtype="Normal")
def fuel_cell_efficiency():
    return 0.55


@component.add(
    name="H2 propulsion cost",
    units="€/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "green_h2_price": 1,
        "lhv_h2": 1,
        "usd_to_eur": 1,
        "opex_ice": 1,
        "fuel_cell_efficiency": 1,
    },
)
def h2_propulsion_cost():
    return (
        green_h2_price() / (lhv_h2() * 3.6) + opex_ice() * usd_to_eur()
    ) / fuel_cell_efficiency()


@component.add(
    name="HFO propulsion cost",
    units="€/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hfo_cost": 1, "usd_to_eur": 1, "opex_ice": 1, "ice_efficiency": 1},
)
def hfo_propulsion_cost():
    return (hfo_cost() + opex_ice() * usd_to_eur()) / ice_efficiency()


@component.add(
    name="ICE efficiency", units="percent", comp_type="Constant", comp_subtype="Normal"
)
def ice_efficiency():
    """
    Considering the same efficiency for all the ICE engines. Assumption from: https://static-content.springer.com/esm/art%3A10.1038%2Fs41560-022-01065-y/ MediaObjects/41560_2022_1065_MOESM1_ESM.pdf
    """
    return 0.4


@component.add(
    name="LFP AF",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"discount_rate": 2, "lfp_lifetime": 1},
)
def lfp_af():
    return 1 / ((1 - (1 + discount_rate()) ** -lfp_lifetime()) / discount_rate())


@component.add(
    name="LFP CAPEX", units="$/MJ", comp_type="Constant", comp_subtype="Normal"
)
def lfp_capex():
    """
    100 $/kWh for an LFP battery
    """
    return 100 / 3.6


@component.add(
    name="LFP cycle lifetime",
    units="cycles",
    comp_type="Constant",
    comp_subtype="Normal",
)
def lfp_cycle_lifetime():
    return 5000


@component.add(
    name="LFP lifetime", units="years", comp_type="Constant", comp_subtype="Normal"
)
def lfp_lifetime():
    return 20


@component.add(
    name="MeOH propulsion cost",
    units="€/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "green_biomeoh_price": 1,
        "usd_to_eur": 1,
        "opex_ice": 1,
        "ice_efficiency": 1,
    },
)
def meoh_propulsion_cost():
    return (green_biomeoh_price() + opex_ice() * usd_to_eur()) / ice_efficiency()


@component.add(
    name="OPEX Electrical",
    units="$/MJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"opex_ice": 1},
)
def opex_electrical():
    """
    50% of O&M associated with an ICE engine.
    """
    return opex_ice() * 0.5


@component.add(
    name="OPEX ICE", units="$/MJ", comp_type="Constant", comp_subtype="Normal"
)
def opex_ice():
    return 5 / 3600
