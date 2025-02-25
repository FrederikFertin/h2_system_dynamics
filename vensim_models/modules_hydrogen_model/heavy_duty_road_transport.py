"""
Module heavy_duty_road_transport
Translated using PySD version 3.14.0
"""

@component.add(
    name="ctrl HD RT",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"k_p": 1, "error_hd_rt": 1, "error_int_hd_rt": 1},
)
def ctrl_hd_rt():
    return k_p() * error_hd_rt() + error_int_hd_rt()


@component.add(
    name="demand change HD RT",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ctrl_hd_rt": 1},
)
def demand_change_hd_rt():
    return ctrl_hd_rt()


@component.add(
    name="error HD RT",
    units="e",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hd_rt_consumption": 1, "sum_hd_rt": 1},
)
def error_hd_rt():
    return hd_rt_consumption() - sum_hd_rt()


@component.add(
    name="error int HD RT",
    units="e",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_error_int_hd_rt": 1},
    other_deps={
        "_integ_error_int_hd_rt": {
            "initial": {"hd_rt_consumption": 1},
            "step": {"k_i": 1, "error_hd_rt": 1},
        }
    },
)
def error_int_hd_rt():
    return _integ_error_int_hd_rt()


_integ_error_int_hd_rt = Integ(
    lambda: k_i() * error_hd_rt(),
    lambda: hd_rt_consumption() * 0.0179,
    "_integ_error_int_hd_rt",
)


@component.add(
    name="HD average cost",
    units="€/GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hd_bev_consumption": 1,
        "hd_be_lco": 1,
        "hd_fc_lco": 1,
        "hd_fcev_consumption": 1,
        "hd_ice_lco": 1,
        "hd_fossil_consumption": 1,
        "diesel_lhv": 1,
        "hd_ice_energy_usage": 1,
        "sum_hd_rt": 1,
    },
)
def hd_average_cost():
    """
    €/GWh of diesel equivalent. (Total truck ownership costs). Unit check: GWh * €/km * km/kWh * 10^6 kWh/GWh = € -> €/GWh
    """
    return (
        (
            hd_bev_consumption() * hd_be_lco()
            + hd_fcev_consumption() * hd_fc_lco()
            + hd_fossil_consumption() * hd_ice_lco()
        )
        / (hd_ice_energy_usage() * diesel_lhv())
        * 10**6
        / sum_hd_rt()
    )


@component.add(
    name="HD BEV competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hd_ice_lco": 1, "hd_be_lco": 2, "hd_fc_lco": 1},
)
def hd_bev_competitiveness():
    return np.minimum(hd_ice_lco() / hd_be_lco(), hd_fc_lco() / hd_be_lco())


@component.add(
    name="HD BEV consumption",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_hd_bev_consumption": 1},
    other_deps={
        "_integ_hd_bev_consumption": {
            "initial": {},
            "step": {"hd_bev_investment": 1, "hd_bev_decay": 1},
        }
    },
)
def hd_bev_consumption():
    """
    0.014% of the trucks in Europe in 2022 are electrical. All are virtually fossil.
    """
    return _integ_hd_bev_consumption()


_integ_hd_bev_consumption = Integ(
    lambda: hd_bev_investment() - hd_bev_decay(), lambda: 0, "_integ_hd_bev_consumption"
)


@component.add(
    name="HD BEV decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hd_bev_consumption": 1, "truck_lifetime": 1},
)
def hd_bev_decay():
    return hd_bev_consumption() / truck_lifetime()


@component.add(
    name="HD BEV emissions",
    units="tCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hd_bev_consumption": 1,
        "hd_ice_efficiency": 1,
        "charging_efficiency": 1,
        "hd_ev_efficiency": 1,
        "electricity_emission_factor": 1,
    },
)
def hd_bev_emissions():
    return (
        hd_bev_consumption()
        * hd_ice_efficiency()
        / (charging_efficiency() * hd_ev_efficiency())
        * electricity_emission_factor()
        * 1000
    )


@component.add(
    name="HD BEV imitators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hd_rt_reinvestment": 1, "hd_bev_investment_level": 1},
)
def hd_bev_imitators():
    return hd_rt_reinvestment() * hd_bev_investment_level()


@component.add(
    name="HD BEV inno switch",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_hd_bev_inno_switch": 1},
    other_deps={
        "_smooth_hd_bev_inno_switch": {
            "initial": {
                "hd_bev_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
            "step": {
                "hd_bev_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
        }
    },
)
def hd_bev_inno_switch():
    return _smooth_hd_bev_inno_switch()


_smooth_hd_bev_inno_switch = Smooth(
    lambda: if_then_else(
        hd_bev_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            hd_bev_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 2,
    lambda: if_then_else(
        hd_bev_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            hd_bev_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 3,
    "_smooth_hd_bev_inno_switch",
)


@component.add(
    name="HD BEV innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hd_bev_inno_switch": 1,
        "hd_rt_reinvestment": 1,
        "innovators": 1,
        "hd_bev_consumption": 1,
        "sum_hd_rt": 2,
    },
)
def hd_bev_innovators():
    return (
        hd_bev_inno_switch()
        * hd_rt_reinvestment()
        * innovators()
        * (sum_hd_rt() - hd_bev_consumption())
        / sum_hd_rt()
    )


@component.add(
    name="HD BEV investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hd_bev_imitators": 1, "hd_bev_innovators": 1},
)
def hd_bev_investment():
    return hd_bev_imitators() + hd_bev_innovators()


@component.add(
    name="HD BEV investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hd_rt_equalizer": 1, "hd_bev_level": 1},
)
def hd_bev_investment_level():
    return hd_rt_equalizer() * hd_bev_level()


@component.add(
    name="HD BEV level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "hd_bev_competitiveness": 1,
        "cross": 1,
        "hd_bev_consumption": 1,
        "sum_hd_rt": 1,
    },
)
def hd_bev_level():
    return (
        1
        / (1 + np.exp(slope() * (cross() - hd_bev_competitiveness())))
        * hd_bev_consumption()
        / sum_hd_rt()
    )


@component.add(
    name="HD FCEV competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hd_be_lco": 1, "hd_fc_lco": 2, "hd_ice_lco": 1},
)
def hd_fcev_competitiveness():
    return np.minimum(hd_be_lco() / hd_fc_lco(), hd_ice_lco() / hd_fc_lco())


@component.add(
    name="HD FCEV consumption",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_hd_fcev_consumption": 1},
    other_deps={
        "_integ_hd_fcev_consumption": {
            "initial": {},
            "step": {"hd_fcev_investment": 1, "hd_fcev_decay": 1},
        }
    },
)
def hd_fcev_consumption():
    return _integ_hd_fcev_consumption()


_integ_hd_fcev_consumption = Integ(
    lambda: hd_fcev_investment() - hd_fcev_decay(),
    lambda: 0,
    "_integ_hd_fcev_consumption",
)


@component.add(
    name="HD FCEV decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hd_fcev_consumption": 1, "truck_lifetime": 1},
)
def hd_fcev_decay():
    return hd_fcev_consumption() / truck_lifetime()


@component.add(
    name="HD FCEV imitators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hd_rt_reinvestment": 1, "hd_fcev_investment_level": 1},
)
def hd_fcev_imitators():
    return hd_rt_reinvestment() * hd_fcev_investment_level()


@component.add(
    name="HD FCEV inno switch",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_hd_fcev_inno_switch": 1},
    other_deps={
        "_smooth_hd_fcev_inno_switch": {
            "initial": {
                "hd_fcev_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
            "step": {
                "hd_fcev_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
        }
    },
)
def hd_fcev_inno_switch():
    return _smooth_hd_fcev_inno_switch()


_smooth_hd_fcev_inno_switch = Smooth(
    lambda: if_then_else(
        hd_fcev_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            hd_fcev_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 2,
    lambda: if_then_else(
        hd_fcev_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            hd_fcev_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 3,
    "_smooth_hd_fcev_inno_switch",
)


@component.add(
    name="HD FCEV innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hd_rt_reinvestment": 1,
        "innovators": 1,
        "hd_fcev_inno_switch": 1,
        "hd_fcev_consumption": 1,
        "sum_hd_rt": 2,
    },
)
def hd_fcev_innovators():
    return (
        hd_rt_reinvestment()
        * innovators()
        * hd_fcev_inno_switch()
        * (sum_hd_rt() - hd_fcev_consumption())
        / sum_hd_rt()
    )


@component.add(
    name="HD FCEV investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hd_fcev_imitators": 1, "hd_fcev_innovators": 1},
)
def hd_fcev_investment():
    return hd_fcev_imitators() + hd_fcev_innovators()


@component.add(
    name="HD FCEV investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hd_rt_equalizer": 1, "hd_fcev_level": 1},
)
def hd_fcev_investment_level():
    return hd_rt_equalizer() * hd_fcev_level()


@component.add(
    name="HD FCEV level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "hd_fcev_competitiveness": 1,
        "cross": 1,
        "hd_fcev_consumption": 1,
        "sum_hd_rt": 1,
    },
)
def hd_fcev_level():
    return (
        1
        / (1 + np.exp(slope() * (cross() - hd_fcev_competitiveness())))
        * hd_fcev_consumption()
        / sum_hd_rt()
    )


@component.add(
    name="HD Fossil competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hd_be_lco": 1, "hd_ice_lco": 2, "hd_fc_lco": 1},
)
def hd_fossil_competitiveness():
    return np.minimum(hd_be_lco() / hd_ice_lco(), hd_fc_lco() / hd_ice_lco())


@component.add(
    name="HD Fossil consumption",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_hd_fossil_consumption": 1},
    other_deps={
        "_integ_hd_fossil_consumption": {
            "initial": {"hd_rt_consumption": 1},
            "step": {"hd_fossil_investment": 1, "hd_fossil_decay": 1},
        }
    },
)
def hd_fossil_consumption():
    """
    0.014% of the trucks in Europe in 2022 are electrical. All are virtually fossil.
    """
    return _integ_hd_fossil_consumption()


_integ_hd_fossil_consumption = Integ(
    lambda: hd_fossil_investment() - hd_fossil_decay(),
    lambda: hd_rt_consumption(),
    "_integ_hd_fossil_consumption",
)


@component.add(
    name="HD Fossil decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hd_fossil_consumption": 1,
        "hd_fossil_early_decommission_rate": 1,
        "truck_lifetime": 1,
    },
)
def hd_fossil_decay():
    return hd_fossil_consumption() * (
        hd_fossil_early_decommission_rate() + 1 / truck_lifetime()
    )


@component.add(
    name="HD Fossil early decommission rate",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hd_fossil_competitiveness": 1},
)
def hd_fossil_early_decommission_rate():
    return 1 / (1 + np.exp(-5 * -hd_fossil_competitiveness())) * 0


@component.add(
    name="HD Fossil investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hd_fossil_investment_level": 1, "hd_rt_reinvestment": 1},
)
def hd_fossil_investment():
    return hd_fossil_investment_level() * hd_rt_reinvestment()


@component.add(
    name="HD Fossil investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hd_rt_equalizer": 1, "hd_fossil_level": 1},
)
def hd_fossil_investment_level():
    return hd_rt_equalizer() * hd_fossil_level()


@component.add(
    name="HD Fossil level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "hd_fossil_competitiveness": 1,
        "cross": 1,
        "hd_fossil_consumption": 1,
        "sum_hd_rt": 1,
    },
)
def hd_fossil_level():
    return (
        1
        / (1 + np.exp(slope() * (cross() - hd_fossil_competitiveness())))
        * hd_fossil_consumption()
        / sum_hd_rt()
    )


@component.add(
    name="HD H2 WTP",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hd_be_lco": 1,
        "hd_ice_lco": 1,
        "hd_fc_lco_without_h2": 1,
        "hd_fc_energy_usage": 1,
    },
)
def hd_h2_wtp():
    return (
        np.minimum(hd_be_lco(), hd_ice_lco()) - hd_fc_lco_without_h2()
    ) / hd_fc_energy_usage()


@component.add(
    name="HD ICE efficiency",
    units="percent",
    comp_type="Constant",
    comp_subtype="Normal",
)
def hd_ice_efficiency():
    """
    Builds on the assumption that the EV truck has an efficiency of 85% and the fuel economy is determined by the fits found by Noll et al. (https://doi.org/10.1016/j.apenergy.2021.118079)
    """
    return 0.343


@component.add(
    name="HD ICE emissions",
    units="tCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hd_fossil_consumption": 1, "diesel_emission_factor": 1},
)
def hd_ice_emissions():
    return hd_fossil_consumption() * diesel_emission_factor() * 10**6


@component.add(
    name="HD RT consumption",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"rt_energy_demand": 1, "heavy_duty_fraction": 1},
)
def hd_rt_consumption():
    return rt_energy_demand() * heavy_duty_fraction()


@component.add(
    name="HD RT equalizer",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hd_fossil_level": 1, "hd_fcev_level": 1, "hd_bev_level": 1},
)
def hd_rt_equalizer():
    return 1 / (hd_fossil_level() + hd_fcev_level() + hd_bev_level())


@component.add(
    name="HD RT reinvestment",
    units="GWh",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_hd_rt_reinvestment": 1},
    other_deps={
        "_integ_hd_rt_reinvestment": {
            "initial": {"hd_rt_consumption": 1, "truck_lifetime": 1},
            "step": {
                "demand_change_hd_rt": 1,
                "hd_fossil_decay": 1,
                "hd_fcev_decay": 1,
                "hd_bev_decay": 1,
                "hd_fossil_investment": 1,
                "hd_fcev_investment": 1,
                "hd_bev_investment": 1,
            },
        }
    },
)
def hd_rt_reinvestment():
    return _integ_hd_rt_reinvestment()


_integ_hd_rt_reinvestment = Integ(
    lambda: demand_change_hd_rt()
    + hd_fossil_decay()
    + hd_fcev_decay()
    + hd_bev_decay()
    - hd_fossil_investment()
    - hd_fcev_investment()
    - hd_bev_investment(),
    lambda: hd_rt_consumption() / truck_lifetime(),
    "_integ_hd_rt_reinvestment",
)


@component.add(
    name="heavy duty emissions",
    units="tCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hd_bev_emissions": 1, "hd_ice_emissions": 1},
)
def heavy_duty_emissions():
    return hd_bev_emissions() + hd_ice_emissions()


@component.add(
    name="Heavy duty fraction",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"light_duty_fraction": 1},
)
def heavy_duty_fraction():
    """
    Fraction of road transport energy consumption which is heavy duty.
    """
    return 1 - light_duty_fraction()


@component.add(
    name="heavy duty hydrogen demand",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hd_fcev_consumption": 1,
        "hd_ice_efficiency": 1,
        "hd_fcev_efficiency": 1,
        "h2_lhv": 1,
    },
)
def heavy_duty_hydrogen_demand():
    """
    GWh * MWh/GWh / MWh/t
    """
    return (
        hd_fcev_consumption()
        * hd_ice_efficiency()
        / hd_fcev_efficiency()
        * 1000
        / h2_lhv()
    )


@component.add(
    name="sum HD RT",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hd_fossil_consumption": 1,
        "hd_fcev_consumption": 1,
        "hd_bev_consumption": 1,
    },
)
def sum_hd_rt():
    return hd_fossil_consumption() + hd_fcev_consumption() + hd_bev_consumption()


@component.add(
    name="truck lifetime", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def truck_lifetime():
    return 17.5
