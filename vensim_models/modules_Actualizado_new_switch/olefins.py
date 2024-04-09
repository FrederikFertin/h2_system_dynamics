"""
Module olefins
Translated using PySD version 3.13.4
"""


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
    name='"HYDROGEN F. OLEFIN"',
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "synthetic_naphfta_demand_for_olefin_production": 1,
        "hydrogensyntheticnaphfta_rate": 1,
        "hydrogenbionaphfta_rate": 1,
        "bionaphfta_demand_for_olefin_production": 1,
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
    name='"hydrogen-syntheticnaphfta rate"',
    units="MWh H2/t Naphfta",
    comp_type="Constant",
    comp_subtype="Normal",
)
def hydrogensyntheticnaphfta_rate():
    return 5.85


@component.add(
    name='"naphta-olefin rate"',
    units="t Naphfta / t HVC",
    comp_type="Constant",
    comp_subtype="Normal",
)
def naphtaolefin_rate():
    return 1.66


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
