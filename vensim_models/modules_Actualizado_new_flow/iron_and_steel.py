"""
Module iron_and_steel
Translated using PySD version 3.13.4
"""


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
    name='"HYDROGEN F. STEEL"',
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"drieaf": 1, "h2_to_steel": 1},
)
def hydrogen_f_steel():
    return drieaf() * 10**6 * h2_to_steel()


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
