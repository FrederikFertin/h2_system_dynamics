"""
Module light_duty_road_transport
Translated using PySD version 3.14.0
"""

@component.add(name="Car Lifetime", comp_type="Constant", comp_subtype="Normal")
def car_lifetime():
    return 20


@component.add(
    name="ctrl LD RT",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"k_p": 1, "error_ld_rt": 1, "error_int_ld_rt": 1},
)
def ctrl_ld_rt():
    return k_p() * error_ld_rt() + error_int_ld_rt()


@component.add(
    name="demand change LD RT",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ctrl_ld_rt": 1},
)
def demand_change_ld_rt():
    return ctrl_ld_rt()


@component.add(
    name="Diesel Vehicle efficiency",
    units="percent",
    comp_type="Constant",
    comp_subtype="Normal",
)
def diesel_vehicle_efficiency():
    return 0.35


@component.add(
    name="error int LD RT",
    units="e",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_error_int_ld_rt": 1},
    other_deps={
        "_integ_error_int_ld_rt": {
            "initial": {"ld_rt_consumption": 1},
            "step": {"k_i": 1, "error_ld_rt": 1},
        }
    },
)
def error_int_ld_rt():
    return _integ_error_int_ld_rt()


_integ_error_int_ld_rt = Integ(
    lambda: k_i() * error_ld_rt(),
    lambda: ld_rt_consumption() * 0.0179,
    "_integ_error_int_ld_rt",
)


@component.add(
    name="error LD RT",
    units="e",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ld_rt_consumption": 1, "sum_ld_rt": 1},
)
def error_ld_rt():
    return ld_rt_consumption() - sum_ld_rt()


@component.add(
    name="FCEV efficiency", units="percent", comp_type="Constant", comp_subtype="Normal"
)
def fcev_efficiency():
    """
    65% efficiency from energy content of H2 to energy delivered to the wheels.
    """
    return 0.65


@component.add(
    name="LD BEV competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ld_ownership_cost_diesel": 1,
        "ld_ownership_cost_bev": 2,
        "ld_ownership_cost_fcev": 1,
    },
)
def ld_bev_competitiveness():
    return np.minimum(
        ld_ownership_cost_diesel() / ld_ownership_cost_bev(),
        ld_ownership_cost_fcev() / ld_ownership_cost_bev(),
    )


@component.add(
    name="LD BEV consumption",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_ld_bev_consumption": 1},
    other_deps={
        "_integ_ld_bev_consumption": {
            "initial": {"ld_rt_consumption": 1},
            "step": {"ld_bev_investment": 1, "ld_bev_decay": 1},
        }
    },
)
def ld_bev_consumption():
    return _integ_ld_bev_consumption()


_integ_ld_bev_consumption = Integ(
    lambda: ld_bev_investment() - ld_bev_decay(),
    lambda: ld_rt_consumption() * 0.05,
    "_integ_ld_bev_consumption",
)


@component.add(
    name="LD BEV decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ld_bev_consumption": 1, "car_lifetime": 1},
)
def ld_bev_decay():
    return ld_bev_consumption() / car_lifetime()


@component.add(
    name="LD BEV investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ld_rt_reinvestment": 1, "ld_bev_investment_level": 1},
)
def ld_bev_investment():
    return ld_rt_reinvestment() * ld_bev_investment_level()


@component.add(
    name="LD BEV investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ld_rt_equalizer": 1, "ld_bev_level": 1},
)
def ld_bev_investment_level():
    return ld_rt_equalizer() * ld_bev_level()


@component.add(
    name="LD BEV level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "ld_bev_competitiveness": 1,
        "cross_innovation": 1,
        "ld_bev_consumption": 1,
        "sum_ld_rt": 1,
    },
)
def ld_bev_level():
    return (
        1
        / (1 + np.exp(slope() * (cross_innovation() - ld_bev_competitiveness())))
        * ld_bev_consumption()
        / sum_ld_rt()
    )


@component.add(
    name="LD FCEV competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ld_ownership_cost_bev": 1,
        "ld_ownership_cost_fcev": 2,
        "ld_ownership_cost_diesel": 1,
    },
)
def ld_fcev_competitiveness():
    return np.minimum(
        ld_ownership_cost_bev() / ld_ownership_cost_fcev(),
        ld_ownership_cost_diesel() / ld_ownership_cost_fcev(),
    )


@component.add(
    name="LD FCEV consumption",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_ld_fcev_consumption": 1},
    other_deps={
        "_integ_ld_fcev_consumption": {
            "initial": {},
            "step": {"ld_fcev_investment": 1, "ld_fcev_decay": 1},
        }
    },
)
def ld_fcev_consumption():
    return _integ_ld_fcev_consumption()


_integ_ld_fcev_consumption = Integ(
    lambda: ld_fcev_investment() - ld_fcev_decay(),
    lambda: 0,
    "_integ_ld_fcev_consumption",
)


@component.add(
    name="LD FCEV decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ld_fcev_consumption": 1, "car_lifetime": 1},
)
def ld_fcev_decay():
    return ld_fcev_consumption() / car_lifetime()


@component.add(
    name="LD FCEV imitators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ld_rt_reinvestment": 1, "ld_fcev_investment_level": 1},
)
def ld_fcev_imitators():
    return ld_rt_reinvestment() * ld_fcev_investment_level()


@component.add(
    name="LD FCEV inno switch",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ld_fcev_competitiveness": 1},
)
def ld_fcev_inno_switch():
    return if_then_else(ld_fcev_competitiveness() > 0.5, lambda: 1, lambda: 0)


@component.add(
    name="LD FCEV innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ld_rt_reinvestment": 1,
        "innovators": 1,
        "ld_fcev_inno_switch": 1,
        "ld_fcev_consumption": 1,
        "sum_ld_rt": 2,
    },
)
def ld_fcev_innovators():
    return (
        ld_rt_reinvestment()
        * innovators()
        * ld_fcev_inno_switch()
        * (sum_ld_rt() - ld_fcev_consumption())
        / sum_ld_rt()
    )


@component.add(
    name="LD FCEV investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ld_fcev_imitators": 1, "ld_fcev_innovators": 1},
)
def ld_fcev_investment():
    return ld_fcev_imitators() + ld_fcev_innovators()


@component.add(
    name="LD FCEV investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ld_rt_equalizer": 1, "ld_fcev_level": 1},
)
def ld_fcev_investment_level():
    return ld_rt_equalizer() * ld_fcev_level()


@component.add(
    name="LD FCEV level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "ld_fcev_competitiveness": 1,
        "cross_innovation": 1,
        "ld_fcev_consumption": 1,
        "sum_ld_rt": 1,
    },
)
def ld_fcev_level():
    return (
        1
        / (1 + np.exp(slope() * (cross_innovation() - ld_fcev_competitiveness())))
        * ld_fcev_consumption()
        / sum_ld_rt()
    )


@component.add(
    name="LD Fossil competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ld_ownership_cost_bev": 1,
        "ld_ownership_cost_diesel": 2,
        "ld_ownership_cost_fcev": 1,
    },
)
def ld_fossil_competitiveness():
    return np.minimum(
        ld_ownership_cost_bev() / ld_ownership_cost_diesel(),
        ld_ownership_cost_fcev() / ld_ownership_cost_diesel(),
    )


@component.add(
    name="LD Fossil consumption",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_ld_fossil_consumption": 1},
    other_deps={
        "_integ_ld_fossil_consumption": {
            "initial": {"ld_rt_consumption": 1},
            "step": {"ld_fossil_investment": 1, "ld_fossil_decay": 1},
        }
    },
)
def ld_fossil_consumption():
    return _integ_ld_fossil_consumption()


_integ_ld_fossil_consumption = Integ(
    lambda: ld_fossil_investment() - ld_fossil_decay(),
    lambda: ld_rt_consumption() * 0.95,
    "_integ_ld_fossil_consumption",
)


@component.add(
    name="LD Fossil decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ld_fossil_consumption": 1, "car_lifetime": 1},
)
def ld_fossil_decay():
    return ld_fossil_consumption() / car_lifetime()


@component.add(
    name="LD Fossil investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ld_fossil_investment_level": 1, "ld_rt_reinvestment": 1},
)
def ld_fossil_investment():
    return ld_fossil_investment_level() * ld_rt_reinvestment()


@component.add(
    name="LD Fossil investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ld_rt_equalizer": 1, "ld_fossil_level": 1},
)
def ld_fossil_investment_level():
    return ld_rt_equalizer() * ld_fossil_level()


@component.add(
    name="LD Fossil level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "cross_conventional": 1,
        "ld_fossil_competitiveness": 1,
        "ld_fossil_consumption": 1,
        "sum_ld_rt": 1,
    },
)
def ld_fossil_level():
    return (
        1
        / (1 + np.exp(slope() * (cross_conventional() - ld_fossil_competitiveness())))
        * ld_fossil_consumption()
        / sum_ld_rt()
    )


@component.add(
    name="LD RT consumption",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"rt_energy_demand": 1, "light_duty_fraction": 1},
)
def ld_rt_consumption():
    return rt_energy_demand() * light_duty_fraction()


@component.add(
    name="LD RT equalizer",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ld_fossil_level": 1, "ld_fcev_level": 1, "ld_bev_level": 1},
)
def ld_rt_equalizer():
    return 1 / (ld_fossil_level() + ld_fcev_level() + ld_bev_level())


@component.add(
    name="LD RT reinvestment",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_ld_rt_reinvestment": 1},
    other_deps={
        "_integ_ld_rt_reinvestment": {
            "initial": {"ld_rt_consumption": 1, "car_lifetime": 1},
            "step": {
                "demand_change_ld_rt": 1,
                "ld_fossil_decay": 1,
                "ld_fcev_decay": 1,
                "ld_bev_decay": 1,
                "ld_fossil_investment": 1,
                "ld_fcev_investment": 1,
                "ld_bev_investment": 1,
            },
        }
    },
)
def ld_rt_reinvestment():
    return _integ_ld_rt_reinvestment()


_integ_ld_rt_reinvestment = Integ(
    lambda: demand_change_ld_rt()
    + ld_fossil_decay()
    + ld_fcev_decay()
    + ld_bev_decay()
    - ld_fossil_investment()
    - ld_fcev_investment()
    - ld_bev_investment(),
    lambda: ld_rt_consumption() * (0.0179 + 1 / car_lifetime()),
    "_integ_ld_rt_reinvestment",
)


@component.add(name="Light duty fraction", comp_type="Constant", comp_subtype="Normal")
def light_duty_fraction():
    """
    Fraction of road transport energy consumption which is light duty.
    """
    return 0.7323


@component.add(
    name="light duty hydrogen demand",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ld_fcev_consumption": 1,
        "diesel_vehicle_efficiency": 1,
        "fcev_efficiency": 1,
        "lhv_h2": 1,
    },
)
def light_duty_hydrogen_demand():
    """
    GWh * MWh/GWh / MWh/t
    """
    return (
        ld_fcev_consumption()
        * diesel_vehicle_efficiency()
        / fcev_efficiency()
        * 1000
        / lhv_h2()
    )


@component.add(
    name="RT energy demand",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def rt_energy_demand():
    """
    1.56% increase per year compared to the base year (2019)
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
            867029.0,
            880555.0,
            894291.0,
            908242.0,
            922411.0,
            936800.0,
            951414.0,
            966257.0,
            981330.0,
            996639.0,
            1012190.0,
            1027980.0,
            1044010.0,
            1060300.0,
            1076840.0,
            1093640.0,
            1110700.0,
            1128030.0,
            1145620.0,
            1163500.0,
            1181650.0,
            1200080.0,
            1218800.0,
            1237810.0,
            1257120.0,
            1276740.0,
            1296650.0,
            1316880.0,
            1337420.0,
            1358290.0,
            1379480.0,
            1401000.0,
        ],
    )


@component.add(
    name="sum LD RT",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ld_fossil_consumption": 1,
        "ld_fcev_consumption": 1,
        "ld_bev_consumption": 1,
    },
)
def sum_ld_rt():
    return ld_fossil_consumption() + ld_fcev_consumption() + ld_bev_consumption()
