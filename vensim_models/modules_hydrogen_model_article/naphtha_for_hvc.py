"""
Module naphtha_for_hvc
Translated using PySD version 3.14.0
"""

@component.add(
    name="bio naphtha competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "naphtha_cost": 1,
        "bionaphtha_cost": 3,
        "synnaphtha_cost": 1,
        "pyrolysisnaphtha_cost": 1,
    },
)
def bio_naphtha_competitiveness():
    return np.minimum(
        naphtha_cost() / bionaphtha_cost(),
        np.minimum(
            synnaphtha_cost() / bionaphtha_cost(),
            pyrolysisnaphtha_cost() / bionaphtha_cost(),
        ),
    )


@component.add(
    name="bio naphtha decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"biogenic_naphtha": 1, "feedstock_lockin": 1},
)
def bio_naphtha_decay():
    return biogenic_naphtha() / feedstock_lockin()


@component.add(
    name="bio naphtha imitators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"bio_naphtha_investment_level": 1, "naphtha_feedstock_reinvestment": 1},
)
def bio_naphtha_imitators():
    return bio_naphtha_investment_level() * naphtha_feedstock_reinvestment()


@component.add(
    name="bio naphtha inno switch",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_bio_naphtha_inno_switch": 1},
    other_deps={
        "_smooth_bio_naphtha_inno_switch": {
            "initial": {
                "bio_naphtha_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
            "step": {
                "bio_naphtha_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
        }
    },
)
def bio_naphtha_inno_switch():
    return _smooth_bio_naphtha_inno_switch()


_smooth_bio_naphtha_inno_switch = Smooth(
    lambda: if_then_else(
        bio_naphtha_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            bio_naphtha_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 2,
    lambda: if_then_else(
        bio_naphtha_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            bio_naphtha_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 3,
    "_smooth_bio_naphtha_inno_switch",
)


@component.add(
    name="bio naphtha innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "bio_naphtha_inno_switch": 1,
        "naphtha_feedstock_reinvestment": 1,
        "innovators": 1,
        "biogenic_naphtha": 1,
        "sum_naphtha": 2,
    },
)
def bio_naphtha_innovators():
    return (
        bio_naphtha_inno_switch()
        * naphtha_feedstock_reinvestment()
        * innovators()
        * (sum_naphtha() - biogenic_naphtha())
        / sum_naphtha()
    )


@component.add(
    name="bio naphtha investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"bio_naphtha_imitators": 1, "bio_naphtha_innovators": 1},
)
def bio_naphtha_investment():
    return np.maximum(bio_naphtha_imitators() + bio_naphtha_innovators(), 0)


@component.add(
    name="bio naphtha investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"naphtha_equalizer": 1, "bio_naphtha_level": 1},
)
def bio_naphtha_investment_level():
    return naphtha_equalizer() * bio_naphtha_level()


@component.add(
    name="bio naphtha level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "cross": 1,
        "bio_naphtha_competitiveness": 1,
        "biogenic_naphtha": 1,
        "sum_naphtha": 1,
    },
)
def bio_naphtha_level():
    return (
        1
        / (1 + np.exp(slope() * (cross() - bio_naphtha_competitiveness())))
        * biogenic_naphtha()
        / sum_naphtha()
    )


@component.add(
    name="Biogenic naphtha",
    units="MT naphtha",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_biogenic_naphtha": 1},
    other_deps={
        "_smooth_biogenic_naphtha": {
            "initial": {"bio_naphtha_investment": 1, "bio_naphtha_decay": 1},
            "step": {"bio_naphtha_investment": 1, "bio_naphtha_decay": 1},
        },
        "_integ_biogenic_naphtha": {
            "initial": {},
            "step": {"_smooth_biogenic_naphtha": 1},
        },
    },
)
def biogenic_naphtha():
    return _integ_biogenic_naphtha()


_smooth_biogenic_naphtha = Smooth(
    lambda: bio_naphtha_investment() - bio_naphtha_decay(),
    lambda: 1,
    lambda: bio_naphtha_investment() - bio_naphtha_decay(),
    lambda: 1,
    "_smooth_biogenic_naphtha",
)

_integ_biogenic_naphtha = Integ(
    lambda: _smooth_biogenic_naphtha(), lambda: 0, "_integ_biogenic_naphtha"
)


@component.add(
    name="BioNaphtha H2 Usage",
    units="MWh H2/t Naphtha",
    comp_type="Constant",
    comp_subtype="Normal",
)
def bionaphtha_h2_usage():
    return 0.78


@component.add(
    name="BioNaphtha hydrogen demand",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"biogenic_naphtha": 1, "bionaphtha_h2_usage": 1},
)
def bionaphtha_hydrogen_demand():
    return biogenic_naphtha() * bionaphtha_h2_usage() / 33.33 * 10**6


@component.add(
    name="ctrl naphtha",
    units="GWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"k_p": 1, "error_naphtha": 1, "errorint_naphtha": 1},
)
def ctrl_naphtha():
    return k_p() * error_naphtha() + errorint_naphtha()


@component.add(
    name="demand change naphtha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ctrl_naphtha": 1},
)
def demand_change_naphtha():
    return ctrl_naphtha()


@component.add(
    name="error naphtha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"naphtha_production": 1, "sum_naphtha": 1},
)
def error_naphtha():
    return naphtha_production() - sum_naphtha()


@component.add(
    name="errorint naphtha",
    units="e",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_errorint_naphtha": 1},
    other_deps={
        "_integ_errorint_naphtha": {
            "initial": {"naphtha_production": 1},
            "step": {"k_i": 1, "error_naphtha": 1},
        }
    },
)
def errorint_naphtha():
    return _integ_errorint_naphtha()


_integ_errorint_naphtha = Integ(
    lambda: k_i() * error_naphtha(),
    lambda: -naphtha_production() / 100,
    "_integ_errorint_naphtha",
)


@component.add(
    name="F naphtha competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "bionaphtha_cost": 1,
        "naphtha_cost": 3,
        "synnaphtha_cost": 1,
        "pyrolysisnaphtha_cost": 1,
    },
)
def f_naphtha_competitiveness():
    return np.minimum(
        bionaphtha_cost() / naphtha_cost(),
        np.minimum(
            synnaphtha_cost() / naphtha_cost(), pyrolysisnaphtha_cost() / naphtha_cost()
        ),
    )


@component.add(
    name="F naphtha decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fossil_naphtha": 1,
        "feedstock_lockin": 1,
        "f_naphtha_early_decommission_rate": 1,
    },
)
def f_naphtha_decay():
    return fossil_naphtha() * (
        f_naphtha_early_decommission_rate() + 1 / feedstock_lockin()
    )


@component.add(
    name="F naphtha early decommission rate",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"f_naphtha_competitiveness": 1},
)
def f_naphtha_early_decommission_rate():
    return 1 / (1 + np.exp(-5 * -f_naphtha_competitiveness())) * 0


@component.add(
    name="F naphtha investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"naphtha_feedstock_reinvestment": 1, "f_naphtha_investment_level": 1},
)
def f_naphtha_investment():
    return np.maximum(
        naphtha_feedstock_reinvestment() * f_naphtha_investment_level(), 0
    )


@component.add(
    name="F naphtha investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"naphtha_equalizer": 1, "f_naphtha_level": 1},
)
def f_naphtha_investment_level():
    return naphtha_equalizer() * f_naphtha_level()


@component.add(
    name="F naphtha level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "cross": 1,
        "f_naphtha_competitiveness": 1,
        "fossil_naphtha": 1,
        "sum_naphtha": 1,
    },
)
def f_naphtha_level():
    return (
        1
        / (1 + np.exp(slope() * (cross() - f_naphtha_competitiveness())))
        * fossil_naphtha()
        / sum_naphtha()
    )


@component.add(
    name="feedstock lockin", units="years", comp_type="Constant", comp_subtype="Normal"
)
def feedstock_lockin():
    return 10


@component.add(
    name="Fossil naphtha",
    units="MT naphtha",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_fossil_naphtha": 1},
    other_deps={
        "_integ_fossil_naphtha": {
            "initial": {"naphtha_production": 1},
            "step": {"f_naphtha_investment": 1, "f_naphtha_decay": 1},
        }
    },
)
def fossil_naphtha():
    return _integ_fossil_naphtha()


_integ_fossil_naphtha = Integ(
    lambda: f_naphtha_investment() - f_naphtha_decay(),
    lambda: naphtha_production(),
    "_integ_fossil_naphtha",
)


@component.add(
    name="naphta olefin rate",
    units="t Naphfta / t HVC",
    comp_type="Constant",
    comp_subtype="Normal",
)
def naphta_olefin_rate():
    return 1.66


@component.add(
    name="naphtha average cost",
    units="€/GJ Naphtha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biogenic_naphtha": 1,
        "bionaphtha_cost": 1,
        "naphtha_cost": 1,
        "fossil_naphtha": 1,
        "recycled_naphtha": 1,
        "pyrolysisnaphtha_cost": 1,
        "synnaphtha_cost": 1,
        "synthetic_naphtha": 1,
        "sum_naphtha": 1,
    },
)
def naphtha_average_cost():
    return (
        biogenic_naphtha() * bionaphtha_cost()
        + fossil_naphtha() * naphtha_cost()
        + recycled_naphtha() * pyrolysisnaphtha_cost()
        + synthetic_naphtha() * synnaphtha_cost()
    ) / sum_naphtha()


@component.add(
    name="naphtha biomass demand",
    units="GWh Biomass",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"biogenic_naphtha": 1, "naphtha_lhv": 1},
)
def naphtha_biomass_demand():
    return biogenic_naphtha() * (naphtha_lhv() / 3600) * 10**6


@component.add(
    name="Naphtha CO2 WTP",
    units="€/tCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "bionaphtha_cost": 1,
        "synnaphtha_cost": 1,
        "carbon_tax": 1,
        "naphtha_cost": 1,
        "naphtha_emission_factor": 2,
    },
)
def naphtha_co2_wtp():
    """
    €/GJ / (tCO2/GJ)
    """
    return (
        np.minimum(bionaphtha_cost(), synnaphtha_cost())
        - (naphtha_cost() - carbon_tax() * naphtha_emission_factor())
    ) / naphtha_emission_factor()


@component.add(
    name="naphtha emissions",
    units="tCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fossil_naphtha": 1, "naphtha_lhv": 1, "naphtha_emission_factor": 1},
)
def naphtha_emissions():
    """
    https://www.eea.europa.eu/publications/managing-the-systemic-use-of This article cites a plastic industry pollution of 208 MT CO2eq in 2018. Really close to what is predicted here.
    """
    return fossil_naphtha() * naphtha_lhv() * naphtha_emission_factor() * 10**6


@component.add(
    name="naphtha equalizer",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "bio_naphtha_level": 1,
        "recycled_level": 1,
        "syn_naphtha_level": 1,
        "f_naphtha_level": 1,
    },
)
def naphtha_equalizer():
    return 1 / (
        bio_naphtha_level() + recycled_level() + syn_naphtha_level() + f_naphtha_level()
    )


@component.add(
    name="naphtha feedstock reinvestment",
    units="MT naphtha",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_naphtha_feedstock_reinvestment": 1},
    other_deps={
        "_integ_naphtha_feedstock_reinvestment": {
            "initial": {"naphtha_production": 1, "feedstock_lockin": 1},
            "step": {
                "bio_naphtha_decay": 1,
                "demand_change_naphtha": 1,
                "syn_naphtha_decay": 1,
                "f_naphtha_decay": 1,
                "recycled_decay": 1,
                "bio_naphtha_investment": 1,
                "syn_naphtha_investment": 1,
                "f_naphtha_investment": 1,
                "recycled_investment": 1,
            },
        }
    },
)
def naphtha_feedstock_reinvestment():
    return _integ_naphtha_feedstock_reinvestment()


_integ_naphtha_feedstock_reinvestment = Integ(
    lambda: bio_naphtha_decay()
    + demand_change_naphtha()
    + syn_naphtha_decay()
    + f_naphtha_decay()
    + recycled_decay()
    - bio_naphtha_investment()
    - syn_naphtha_investment()
    - f_naphtha_investment()
    - recycled_investment(),
    lambda: naphtha_production() / feedstock_lockin() * 0.8,
    "_integ_naphtha_feedstock_reinvestment",
)


@component.add(
    name="naphtha hydrogen demand",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"bionaphtha_hydrogen_demand": 1, "synnaphtha_hydrogen_demand": 1},
)
def naphtha_hydrogen_demand():
    return bionaphtha_hydrogen_demand() + synnaphtha_hydrogen_demand()


@component.add(
    name="Naphtha LHV", units="MJ/kg", comp_type="Constant", comp_subtype="Normal"
)
def naphtha_lhv():
    return 44.9


@component.add(
    name="naphtha production",
    units="MT naphtha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "olefin_production": 1,
        "mto": 1,
        "naphta_olefin_rate": 1,
        "pulse_size": 1,
        "pulse_naphtha": 1,
    },
)
def naphtha_production():
    """
    Based on a 65.7% yield in the naphtha to olefin conversion: https://doi.org/10.1016/j.enconman.2017.10.061
    """
    return (
        (olefin_production() - mto())
        * naphta_olefin_rate()
        / 10**6
        * (1 - pulse_size() * pulse_naphtha())
    )


@component.add(
    name="pulse naphtha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1},
)
def pulse_naphtha():
    return pulse(__data["time"], 2030, width=0.5)


@component.add(name="pulse size", comp_type="Constant", comp_subtype="Normal")
def pulse_size():
    return 0


@component.add(
    name="PyrolysisNaphtha cost",
    units="€/GJ",
    comp_type="Constant",
    comp_subtype="Normal",
)
def pyrolysisnaphtha_cost():
    return 60


@component.add(
    name="recycled competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "naphtha_cost": 1,
        "pyrolysisnaphtha_cost": 3,
        "synnaphtha_cost": 1,
        "bionaphtha_cost": 1,
    },
)
def recycled_competitiveness():
    return np.minimum(
        naphtha_cost() / pyrolysisnaphtha_cost(),
        np.minimum(
            bionaphtha_cost() / pyrolysisnaphtha_cost(),
            synnaphtha_cost() / pyrolysisnaphtha_cost(),
        ),
    )


@component.add(
    name="recycled decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"recycled_naphtha": 1, "feedstock_lockin": 1},
)
def recycled_decay():
    return recycled_naphtha() / feedstock_lockin()


@component.add(
    name="recycled imitators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"naphtha_feedstock_reinvestment": 1, "recycled_investment_level": 1},
)
def recycled_imitators():
    return naphtha_feedstock_reinvestment() * recycled_investment_level()


@component.add(
    name="recycled inno switch",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_recycled_inno_switch": 1},
    other_deps={
        "_smooth_recycled_inno_switch": {
            "initial": {
                "recycled_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
            "step": {
                "recycled_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
        }
    },
)
def recycled_inno_switch():
    return _smooth_recycled_inno_switch()


_smooth_recycled_inno_switch = Smooth(
    lambda: if_then_else(
        recycled_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            recycled_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 2,
    lambda: if_then_else(
        recycled_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            recycled_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 3,
    "_smooth_recycled_inno_switch",
)


@component.add(
    name="recycled innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "naphtha_feedstock_reinvestment": 1,
        "innovators": 1,
        "recycled_inno_switch": 1,
        "recycled_naphtha": 1,
        "sum_naphtha": 2,
    },
)
def recycled_innovators():
    return (
        naphtha_feedstock_reinvestment()
        * innovators()
        * recycled_inno_switch()
        * (sum_naphtha() - recycled_naphtha())
        / sum_naphtha()
    )


@component.add(
    name="recycled investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"recycled_imitators": 1, "recycled_innovators": 1},
)
def recycled_investment():
    return np.maximum(recycled_imitators() + recycled_innovators(), 0)


@component.add(
    name="recycled investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"naphtha_equalizer": 1, "recycled_level": 1},
)
def recycled_investment_level():
    return naphtha_equalizer() * recycled_level()


@component.add(
    name="recycled level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "recycled_competitiveness": 1,
        "cross": 1,
        "recycled_naphtha": 1,
        "sum_naphtha": 1,
    },
)
def recycled_level():
    return (
        1
        / (1 + np.exp(slope() * (cross() - recycled_competitiveness())))
        * recycled_naphtha()
        / sum_naphtha()
    )


@component.add(
    name="Recycled naphtha",
    units="MT naphtha",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_recycled_naphtha": 1},
    other_deps={
        "_integ_recycled_naphtha": {
            "initial": {},
            "step": {"recycled_investment": 1, "recycled_decay": 1},
        }
    },
)
def recycled_naphtha():
    return _integ_recycled_naphtha()


_integ_recycled_naphtha = Integ(
    lambda: recycled_investment() - recycled_decay(),
    lambda: 0,
    "_integ_recycled_naphtha",
)


@component.add(
    name="sum naphtha",
    units="t Naphtha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biogenic_naphtha": 1,
        "recycled_naphtha": 1,
        "synthetic_naphtha": 1,
        "fossil_naphtha": 1,
    },
)
def sum_naphtha():
    return (
        biogenic_naphtha() + recycled_naphtha() + synthetic_naphtha() + fossil_naphtha()
    )


@component.add(
    name="syn naphtha competitiveness",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "naphtha_cost": 1,
        "synnaphtha_cost": 3,
        "pyrolysisnaphtha_cost": 1,
        "bionaphtha_cost": 1,
    },
)
def syn_naphtha_competitiveness():
    return np.minimum(
        naphtha_cost() / synnaphtha_cost(),
        np.minimum(
            bionaphtha_cost() / synnaphtha_cost(),
            pyrolysisnaphtha_cost() / synnaphtha_cost(),
        ),
    )


@component.add(
    name="syn naphtha decay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"synthetic_naphtha": 1, "feedstock_lockin": 1},
)
def syn_naphtha_decay():
    return synthetic_naphtha() / feedstock_lockin()


@component.add(
    name="syn naphtha imitators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"naphtha_feedstock_reinvestment": 1, "syn_naphtha_investment_level": 1},
)
def syn_naphtha_imitators():
    return naphtha_feedstock_reinvestment() * syn_naphtha_investment_level()


@component.add(
    name="syn naphtha inno switch",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_syn_naphtha_inno_switch": 1},
    other_deps={
        "_smooth_syn_naphtha_inno_switch": {
            "initial": {
                "syn_naphtha_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
            "step": {
                "syn_naphtha_competitiveness": 2,
                "inno_switch_level": 1,
                "early_switch_level": 1,
            },
        }
    },
)
def syn_naphtha_inno_switch():
    return _smooth_syn_naphtha_inno_switch()


_smooth_syn_naphtha_inno_switch = Smooth(
    lambda: if_then_else(
        syn_naphtha_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            syn_naphtha_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 2,
    lambda: if_then_else(
        syn_naphtha_competitiveness() > inno_switch_level(),
        lambda: if_then_else(
            syn_naphtha_competitiveness() > early_switch_level(), lambda: 3, lambda: 1
        ),
        lambda: 0,
    ),
    lambda: 3,
    "_smooth_syn_naphtha_inno_switch",
)


@component.add(
    name="syn naphtha innovators",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "naphtha_feedstock_reinvestment": 1,
        "innovators": 1,
        "syn_naphtha_inno_switch": 1,
        "synthetic_naphtha": 1,
        "sum_naphtha": 2,
    },
)
def syn_naphtha_innovators():
    return (
        naphtha_feedstock_reinvestment()
        * innovators()
        * syn_naphtha_inno_switch()
        * (sum_naphtha() - synthetic_naphtha())
        / sum_naphtha()
    )


@component.add(
    name="syn naphtha investment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"syn_naphtha_innovators": 1, "syn_naphtha_imitators": 1},
)
def syn_naphtha_investment():
    return np.maximum(syn_naphtha_innovators() + syn_naphtha_imitators(), 0)


@component.add(
    name="syn naphtha investment level",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"naphtha_equalizer": 1, "syn_naphtha_level": 1},
)
def syn_naphtha_investment_level():
    return naphtha_equalizer() * syn_naphtha_level()


@component.add(
    name="syn naphtha level",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "slope": 1,
        "cross": 1,
        "syn_naphtha_competitiveness": 1,
        "synthetic_naphtha": 1,
        "sum_naphtha": 1,
    },
)
def syn_naphtha_level():
    return (
        1
        / (1 + np.exp(slope() * (cross() - syn_naphtha_competitiveness())))
        * synthetic_naphtha()
        / sum_naphtha()
    )


@component.add(
    name="SynNaphtha H2 Usage",
    units="MWh H2/t Naphfta",
    comp_type="Constant",
    comp_subtype="Normal",
)
def synnaphtha_h2_usage():
    return 5.85


@component.add(
    name="SynNaphtha hydrogen demand",
    units="t H2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"synthetic_naphtha": 1, "synnaphtha_h2_usage": 1},
)
def synnaphtha_hydrogen_demand():
    return synthetic_naphtha() * synnaphtha_h2_usage() / 33.33 * 10**6


@component.add(
    name="Synthetic naphtha",
    units="MT naphtha",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_synthetic_naphtha": 1},
    other_deps={
        "_smooth_synthetic_naphtha": {
            "initial": {"syn_naphtha_investment": 1, "syn_naphtha_decay": 1},
            "step": {"syn_naphtha_investment": 1, "syn_naphtha_decay": 1},
        },
        "_integ_synthetic_naphtha": {
            "initial": {},
            "step": {"_smooth_synthetic_naphtha": 1},
        },
    },
)
def synthetic_naphtha():
    return _integ_synthetic_naphtha()


_smooth_synthetic_naphtha = Smooth(
    lambda: syn_naphtha_investment() - syn_naphtha_decay(),
    lambda: 1,
    lambda: syn_naphtha_investment() - syn_naphtha_decay(),
    lambda: 1,
    "_smooth_synthetic_naphtha",
)

_integ_synthetic_naphtha = Integ(
    lambda: _smooth_synthetic_naphtha(), lambda: 0, "_integ_synthetic_naphtha"
)
