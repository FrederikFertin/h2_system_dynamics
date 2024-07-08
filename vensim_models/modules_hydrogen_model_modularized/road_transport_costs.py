"""
Module road_transport_costs
Translated using PySD version 3.14.0
"""

@component.add(
    name="Diesel Emission Factor",
    units="tCO2/kWh",
    comp_type="Constant",
    comp_subtype="Normal",
)
def diesel_emission_factor():
    """
    Source: DOI 10.1007/s40095-015-0160-6 EF: 74.01 kgCO2/GJ / (1000 kg/t) / (1000/3.6 kWh/GJ) = 0.0003 t/CO2/kWh
    """
    return 74.01 / 1000 / (1000 / 3.6)


@component.add(
    name="Electricity Taxes",
    units="percent",
    comp_type="Constant",
    comp_subtype="Normal",
)
def electricity_taxes():
    return 2


@component.add(name="HD BEV CAPEX", comp_type="Constant", comp_subtype="Normal")
def hd_bev_capex():
    """
    See Carmen's thesis for source and derivation.
    """
    return 390000


@component.add(
    name="HD BEV efficiency",
    units="kWh/km",
    comp_type="Constant",
    comp_subtype="Normal",
)
def hd_bev_efficiency():
    return 2.26


@component.add(
    name="HD Diesel CAPEX", units="€", comp_type="Constant", comp_subtype="Normal"
)
def hd_diesel_capex():
    return 1.5 * 1000000.0


@component.add(
    name="HD Diesel efficiency",
    units="kWh/km",
    comp_type="Constant",
    comp_subtype="Normal",
)
def hd_diesel_efficiency():
    return 4.33


@component.add(name="HD FCEV CAPEX", comp_type="Constant", comp_subtype="Normal")
def hd_fcev_capex():
    """
    See Carmen's thesis for source and derivation.
    """
    return 325000


@component.add(
    name="HD FCEV efficiency",
    units="kWh/km",
    comp_type="Constant",
    comp_subtype="Normal",
)
def hd_fcev_efficiency():
    return 3.53


@component.add(
    name="HD ownership cost BEV",
    units="€",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hd_bev_capex": 1,
        "hd_truck_mileage": 1,
        "hd_bev_efficiency": 1,
        "electricity_taxes": 1,
        "electricity_price": 1,
    },
)
def hd_ownership_cost_bev():
    return (
        hd_bev_capex()
        + electricity_price()
        * electricity_taxes()
        * hd_bev_efficiency()
        * hd_truck_mileage()
    )


@component.add(
    name="HD ownership cost diesel",
    units="€",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hd_diesel_capex": 1,
        "hd_diesel_efficiency": 1,
        "diesel_emission_factor": 1,
        "carbon_tax": 1,
        "diesel_price": 1,
        "hd_truck_mileage": 1,
        "lhv_diesel": 1,
    },
)
def hd_ownership_cost_diesel():
    return (
        hd_diesel_capex()
        + (diesel_price() / lhv_diesel() + carbon_tax() * diesel_emission_factor())
        * hd_truck_mileage()
        * hd_diesel_efficiency()
    )


@component.add(
    name="HD ownership cost FCEV",
    units="€",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hd_fcev_capex": 1,
        "lhv_h2": 1,
        "hd_truck_mileage": 1,
        "hd_fcev_efficiency": 1,
        "green_h2_price": 1,
    },
)
def hd_ownership_cost_fcev():
    """
    33.33 (kWh/kg H2)
    """
    return (
        hd_fcev_capex()
        + green_h2_price() / lhv_h2() * hd_fcev_efficiency() * hd_truck_mileage()
    )


@component.add(
    name="HD Truck Mileage", units="km", comp_type="Constant", comp_subtype="Normal"
)
def hd_truck_mileage():
    """
    Lifetime km driven.
    """
    return 1200000.0


@component.add(
    name="LD BEV CAPEX", units="€", comp_type="Constant", comp_subtype="Normal"
)
def ld_bev_capex():
    """
    See Carmen's thesis for source and derivation.
    """
    return 35000


@component.add(
    name="LD BEV efficiency",
    units="kWh/km",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ld_bev_efficiency():
    return 0.45


@component.add(
    name="LD BEV OPEX",
    units="€",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "electricity_price": 1,
        "electricity_taxes": 1,
        "ld_bev_efficiency": 1,
        "ld_car_mileage": 1,
    },
)
def ld_bev_opex():
    return (
        electricity_price()
        * electricity_taxes()
        * ld_bev_efficiency()
        * ld_car_mileage()
    )


@component.add(name="LD Car Mileage", comp_type="Constant", comp_subtype="Normal")
def ld_car_mileage():
    return 240000


@component.add(
    name="LD Diesel CAPEX", units="€", comp_type="Constant", comp_subtype="Normal"
)
def ld_diesel_capex():
    """
    See Carmen's thesis for source and derivation.
    """
    return 24000


@component.add(
    name="LD Diesel efficiency",
    units="kWh/km",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ld_diesel_efficiency():
    return 0.87


@component.add(
    name="LD Diesel OPEX",
    units="€",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "diesel_price": 1,
        "lhv_diesel": 1,
        "diesel_emission_factor": 1,
        "carbon_tax": 1,
        "ld_car_mileage": 1,
        "ld_diesel_efficiency": 1,
    },
)
def ld_diesel_opex():
    return (
        (diesel_price() / lhv_diesel() + carbon_tax() * diesel_emission_factor())
        * ld_car_mileage()
        * ld_diesel_efficiency()
    )


@component.add(
    name="LD FCEV CAPEX", units="€", comp_type="Constant", comp_subtype="Normal"
)
def ld_fcev_capex():
    """
    See Carmen's thesis for source and derivation.
    """
    return 57000


@component.add(
    name="LD FCEV efficiency",
    units="kWh/km",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ld_fcev_efficiency():
    return 0.71


@component.add(
    name="LD FCEV OPEX",
    units="€",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "green_h2_price": 1,
        "lhv_h2": 1,
        "ld_fcev_efficiency": 1,
        "ld_car_mileage": 1,
    },
)
def ld_fcev_opex():
    return green_h2_price() / lhv_h2() * ld_fcev_efficiency() * ld_car_mileage()


@component.add(
    name="LD ownership cost BEV",
    units="€",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ld_bev_capex": 1, "ld_bev_opex": 1},
)
def ld_ownership_cost_bev():
    """
    Read Carmen's thesis for explanation on the cost sources. 35000 € is cost of car. 240000 km is driving range over the car's lifetime. Electricity Price: €/kWh. Then 0.45 is kWh/km.
    """
    return ld_bev_capex() + ld_bev_opex()


@component.add(
    name="LD ownership cost diesel",
    units="€",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ld_diesel_capex": 1, "ld_diesel_opex": 1},
)
def ld_ownership_cost_diesel():
    """
    Read Carmen's thesis for explanation on the cost sources. 28000 € is cost of car. 240000 km is driving range over the car's lifetime. 10.7 kWh/l of diesel is LHV of Diesel. Price/LHV: €/kWh. Then 0.87 is kWh/km.
    """
    return ld_diesel_capex() + ld_diesel_opex()


@component.add(
    name="LD ownership cost FCEV",
    units="€",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ld_fcev_capex": 1, "ld_fcev_opex": 1},
)
def ld_ownership_cost_fcev():
    """
    Read Carmen's thesis for explanation on the cost sources. 57000 € is cost of car. 240000 km is driving range over the car's lifetime. 33.33 kWh/kg is LHV of H2. Price/LHV: €/kWh. Then 0.71 is kWh/km.
    """
    return ld_fcev_capex() + ld_fcev_opex()


@component.add(
    name="LHV Diesel", units="kWh/l", comp_type="Constant", comp_subtype="Normal"
)
def lhv_diesel():
    """
    Source: DOI 10.1007/s40095-015-0160-6 Based on table 5: Diesel LHV 0.0371 GJ/l.
    """
    return 10.31
