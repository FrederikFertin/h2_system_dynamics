"""
Module renewable_kerosene_and_naphtha_production
Translated using PySD version 3.14.0
"""

@component.add(
    name="BioKero AF",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"discount_rate": 2, "biokero_lifetime": 1},
)
def biokero_af():
    return 1 / ((1 - (1 + discount_rate()) ** -biokero_lifetime()) / discount_rate())


@component.add(
    name="BioKero Biomass usage",
    units="MWh/MWh inputs",
    comp_type="Constant",
    comp_subtype="Normal",
)
def biokero_biomass_usage():
    return 0.779


@component.add(
    name="BioKero CAPEX",
    units="€/MWfuel",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def biokero_capex():
    return np.interp(time(), [2019, 2030, 2040, 2050], [960000, 810000, 750000, 710000])


@component.add(
    name="BioKero cost",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hvo_jet_total_costs": 1,
        "biokero_fraction": 1,
        "biokero_revenue_fraction": 1,
    },
)
def biokero_cost():
    """
    10% of the production costs is assumed covered through coproduct selling of naphtha and LPG.
    """
    return hvo_jet_total_costs() / biokero_fraction() * biokero_revenue_fraction()


@component.add(
    name="BioKero cost without H2",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biokero_cost": 1,
        "h2_lhv": 1,
        "biokero_fraction": 1,
        "biokero_revenue_fraction": 1,
        "ft_h2_cost": 1,
        "biokero_h2_usage": 1,
    },
)
def biokero_cost_without_h2():
    return (
        biokero_cost()
        - 1000
        * ft_h2_cost()
        / h2_lhv()
        * biokero_h2_usage()
        / 3.6
        * biokero_revenue_fraction()
        / biokero_fraction()
    )


@component.add(
    name="BioKero Electricity Usage",
    units="MWh/MWh inputs",
    comp_type="Constant",
    comp_subtype="Normal",
)
def biokero_electricity_usage():
    """
    MWh electricity per MWh input energy
    """
    return 0.003


@component.add(
    name="BioKero Excess Heat",
    units="MWh/MWh input",
    comp_type="Constant",
    comp_subtype="Normal",
)
def biokero_excess_heat():
    """
    MWh heat per MWh of energy input
    """
    return 0.027


@component.add(
    name="BioKero fraction",
    units="percent",
    comp_type="Constant",
    comp_subtype="Normal",
)
def biokero_fraction():
    """
    Percent of liquid fuels which is jetfuel
    """
    return 0.66


@component.add(
    name="BioKero Gas Usage",
    units="MWh/MWh",
    comp_type="Constant",
    comp_subtype="Normal",
)
def biokero_gas_usage():
    """
    MWh natural gas per MWh energy input
    """
    return 0.119


@component.add(
    name="BioKero H2 Usage",
    units="MWh/MWh",
    comp_type="Constant",
    comp_subtype="Normal",
)
def biokero_h2_usage():
    """
    MWh H2 per MWh energy input
    """
    return 0.099


@component.add(
    name="BioKero H2 WTP",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "jetfuel_cost": 1,
        "biokero_cost_without_h2": 1,
        "h2_lhv": 1,
        "biokero_revenue_fraction": 1,
        "biokero_fraction": 1,
        "biokero_h2_usage": 1,
    },
)
def biokero_h2_wtp():
    return (jetfuel_cost() - biokero_cost_without_h2()) / (
        1000
        / h2_lhv()
        * biokero_h2_usage()
        / 3.6
        * biokero_revenue_fraction()
        / biokero_fraction()
    )


@component.add(
    name="BioKero Lifetime", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def biokero_lifetime():
    return 25


@component.add(
    name="BioKero operating hours",
    units="hours",
    comp_type="Constant",
    comp_subtype="Normal",
)
def biokero_operating_hours():
    """
    2 weeks of planned downtime per year
    """
    return 8760 * 50 / 52


@component.add(
    name="BioKero OPEX", units="€/MW", comp_type="Constant", comp_subtype="Normal"
)
def biokero_opex():
    """
    €/MW/year of installed output jetfuel capacity.
    """
    return 36000


@component.add(
    name="BioKero revenue fraction",
    units="percent",
    comp_type="Constant",
    comp_subtype="Normal",
)
def biokero_revenue_fraction():
    """
    Fraction of revenues expected from bio kerosene
    """
    return 0.9


@component.add(
    name="BioKero variable", units="€/MWh", comp_type="Constant", comp_subtype="Normal"
)
def biokero_variable():
    """
    €/MWh of output
    """
    return 8.501


@component.add(
    name="BioNaphtha cost",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hvo_jet_total_costs": 1,
        "naphtha_fraction_bio": 1,
        "bionaphtha_revenue_fraction": 1,
    },
)
def bionaphtha_cost():
    """
    The naphtha coproduct sale cover 7.5% of the production costs. The LPG coproduct sale cover the remaining 2.5% of the production costs. Note here is that the naphtha output is quite low, which does not motivate this as the primary method to produce biogenic naphtha.
    """
    return (
        hvo_jet_total_costs() / naphtha_fraction_bio() * bionaphtha_revenue_fraction()
    )


@component.add(
    name="BioNaphtha cost without H2",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "bionaphtha_cost": 1,
        "h2_lhv": 1,
        "ft_h2_cost": 1,
        "naphtha_fraction_bio": 1,
        "biokero_h2_usage": 1,
        "bionaphtha_revenue_fraction": 1,
    },
)
def bionaphtha_cost_without_h2():
    return (
        bionaphtha_cost()
        - 1000
        * ft_h2_cost()
        / h2_lhv()
        * biokero_h2_usage()
        / 3.6
        * bionaphtha_revenue_fraction()
        / naphtha_fraction_bio()
    )


@component.add(
    name="BioNaphtha H2 WTP",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "naphtha_cost": 1,
        "bionaphtha_cost_without_h2": 1,
        "h2_lhv": 1,
        "naphtha_fraction_bio": 1,
        "biokero_h2_usage": 1,
    },
)
def bionaphtha_h2_wtp():
    return (naphtha_cost() - bionaphtha_cost_without_h2()) / (
        10**6 / h2_lhv() * biokero_h2_usage() / 3600 * 0.1 / naphtha_fraction_bio()
    )


@component.add(
    name="BioNaphtha revenue fraction",
    units="percent",
    comp_type="Constant",
    comp_subtype="Normal",
)
def bionaphtha_revenue_fraction():
    return 0.075


@component.add(
    name="HVO Jet Total Costs",
    units="€/GJ input",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biokero_electricity_usage": 1,
        "renewable_electricity_price": 1,
        "biogas_cost": 1,
        "biokero_gas_usage": 1,
        "uco_price": 1,
        "biokero_biomass_usage": 1,
        "h2_lhv": 1,
        "biokero_h2_usage": 1,
        "ft_h2_cost": 1,
        "heat_cost": 1,
        "biokero_excess_heat": 1,
        "biokero_fraction": 1,
        "biokero_opex": 1,
        "biokero_operating_hours": 1,
        "biokero_capex": 1,
        "biokero_variable": 1,
        "biokero_af": 1,
    },
)
def hvo_jet_total_costs():
    return (
        (
            biokero_electricity_usage() * renewable_electricity_price()
            + biokero_gas_usage() * biogas_cost() * 3.6
            + biokero_biomass_usage() * uco_price() * 3.6
            + biokero_h2_usage() * ft_h2_cost() / h2_lhv() * 1000
            - biokero_excess_heat() * heat_cost()
        )
        + (
            (biokero_af() * biokero_capex() + biokero_opex())
            / biokero_operating_hours()
            + biokero_variable()
        )
        * biokero_fraction()
    ) / 3.6


@component.add(
    name="Jetfuel LHV", units="MJ/kg", comp_type="Constant", comp_subtype="Unchangeable"
)
def jetfuel_lhv():
    """
    https://en.wikipedia.org/wiki/Jet_fuel
    """
    return 43


@component.add(
    name="LPG fraction bio",
    units="MWh/MWh input",
    comp_type="Constant",
    comp_subtype="Normal",
)
def lpg_fraction_bio():
    """
    LPG and fuel gas 50/50 mix.
    """
    return 0.192


@component.add(
    name="Naphtha fraction bio",
    units="percent",
    comp_type="Constant",
    comp_subtype="Normal",
)
def naphtha_fraction_bio():
    """
    Percent of liquid fuels which is naphtha
    """
    return 0.065


@component.add(
    name="SynKero AF",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"discount_rate": 2, "synkero_lifetime": 1},
)
def synkero_af():
    return 1 / ((1 - (1 + discount_rate()) ** -synkero_lifetime()) / discount_rate())


@component.add(
    name="SynKero CAPEX",
    units="€/MWfuel",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def synkero_capex():
    return np.interp(
        time(),
        [2019.0, 2030.0, 2040.0, 2050.0],
        [2100000.0, 1600000.0, 1100000.0, 900000.0],
    )


@component.add(
    name="SynKero CO2 usage",
    units="tCO2/tliquids",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def synkero_co2_usage():
    """
    tCo2 per tons of output liquid fuels
    """
    return np.interp(time(), [2019.0, 2030.0, 2040.0, 2050.0], [4.3, 3.9, 3.6, 3.3])


@component.add(
    name="SynKero cost",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ps_cc_cost": 1,
        "cc_capture_rate": 1,
        "synkero_co2_usage": 1,
        "jetfuel_lhv": 1,
        "h2_lhv": 1,
        "synkero_output": 1,
        "renewable_electricity_price": 1,
        "heat_cost": 1,
        "synkero_electricity_usage": 1,
        "synkero_excess_heat": 1,
        "ft_h2_cost": 1,
        "synkero_h2_usage": 1,
        "synkero_operating_hours": 1,
        "synkero_af": 1,
        "synkero_capex": 1,
        "synkero_opex": 1,
        "synkero_variable": 1,
        "synkero_fraction": 1,
    },
)
def synkero_cost():
    """
    Carbon cost in €/MWh output assuming all outputs LHV is equal to jetfuel's. The additional variable costs in €/MWh output using SynKero Output as the efficiency of the process. Here the potential heat sale is also subtracted. Then the annualized capex is added in €/MWh and fixed + variable OPEX in the same unit. Finally it is all divided by the jetfuel fraction, which assumes that 60% of the output is jetfuel. This price in €/MWh is then multiplied by 0.8, which assumes that sale of byproducts in the form of gasoline (20%) and LPG (20%) can bring in further cost reductions. 3600 is the conversion from MWh to MJ.
    """
    return (
        (
            ps_cc_cost() / cc_capture_rate() * synkero_co2_usage() / jetfuel_lhv() * 3.6
            + (
                renewable_electricity_price() * synkero_electricity_usage()
                + 1000 * ft_h2_cost() / h2_lhv() * synkero_h2_usage()
                - heat_cost() * synkero_excess_heat()
            )
            / synkero_output()
            + synkero_af() * synkero_capex() / synkero_operating_hours()
            + synkero_opex()
            + synkero_variable()
        )
        / synkero_fraction()
        * 0.8
        / 3.6
    )


@component.add(
    name="SynKero cost without H2",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "synkero_cost": 1,
        "h2_lhv": 1,
        "synkero_output": 1,
        "synkero_fraction": 1,
        "ft_h2_cost": 1,
        "synkero_h2_usage": 1,
    },
)
def synkero_cost_without_h2():
    return (
        synkero_cost()
        - 1000
        * ft_h2_cost()
        / h2_lhv()
        * synkero_h2_usage()
        / synkero_output()
        / synkero_fraction()
        * 0.8
        / 3.6
    )


@component.add(
    name="SynKero Electricity Usage",
    units="MWh/MWh",
    comp_type="Constant",
    comp_subtype="Normal",
)
def synkero_electricity_usage():
    """
    MWh electricity per MWh input energy
    """
    return 0.005


@component.add(
    name="SynKero Excess Heat",
    units="MWh/MWh",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def synkero_excess_heat():
    """
    MWh heat per MWh input energy (losses)
    """
    return np.interp(time(), [2019.0, 2030.0, 2040.0, 2050.0], [0.3, 0.27, 0.27, 0.25])


@component.add(
    name="SynKero fraction",
    units="percent",
    comp_type="Constant",
    comp_subtype="Normal",
)
def synkero_fraction():
    """
    Percent of liquid fuels which is jetfuel
    """
    return 0.6


@component.add(
    name="SynKero H2 Usage",
    units="MWh/MWh",
    comp_type="Constant",
    comp_subtype="Normal",
)
def synkero_h2_usage():
    """
    MWh H2 per MWh energy input
    """
    return 0.995


@component.add(
    name="SynKero H2 WTP",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "jetfuel_cost": 1,
        "synkero_cost_without_h2": 1,
        "h2_lhv": 1,
        "synkero_output": 1,
        "synkero_h2_usage": 1,
        "synkero_fraction": 1,
    },
)
def synkero_h2_wtp():
    return (jetfuel_cost() - synkero_cost_without_h2()) / (
        1000
        / h2_lhv()
        * synkero_h2_usage()
        / synkero_output()
        / synkero_fraction()
        * 0.8
        / 3.6
    )


@component.add(
    name="SynKero Lifetime", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def synkero_lifetime():
    return 25


@component.add(
    name="SynKero operating hours",
    units="hours",
    comp_type="Constant",
    comp_subtype="Normal",
)
def synkero_operating_hours():
    """
    3 weeks of planned downtime per year
    """
    return 8760 * 49 / 52


@component.add(
    name="SynKero OPEX",
    units="€/MWh",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def synkero_opex():
    """
    €/MWh of liquids/fuels
    """
    return np.interp(time(), [2019.0, 2030.0, 2040.0, 2050.0], [16.9, 12.7, 8.5, 7.4])


@component.add(
    name="SynKero Output",
    units="MWh/MWh",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def synkero_output():
    """
    MWh liquids per MWh of energy input (efficiency)
    """
    return np.interp(time(), [2019.0, 2030.0, 2040.0, 2050.0], [0.65, 0.7, 0.73, 0.75])


@component.add(
    name="SynKero variable",
    units="€/MWh",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def synkero_variable():
    """
    €/MWh of liquids/fuels
    """
    return np.interp(time(), [2019.0, 2030.0, 2040.0, 2050.0], [5.3, 4.2, 3.2, 2.1])


@component.add(
    name="SynNaphtha cost",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"synkero_cost": 1, "synkero_fraction": 1, "synnaphtha_fraction": 1},
)
def synnaphtha_cost():
    """
    Assume that 80 % of the costs are covered by the jetfuel revenue (jetfuel is 60% of the output) - then assume that 30 % of the output is suitable as naphtha and sell that, covering the 20% remaining costs.
    """
    return (synkero_cost() / 0.8 * synkero_fraction()) * 0.2 / synnaphtha_fraction()


@component.add(
    name="SynNaphtha cost without H2",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "synkero_cost_without_h2": 1,
        "synkero_fraction": 1,
        "synnaphtha_fraction": 1,
    },
)
def synnaphtha_cost_without_h2():
    return (
        (synkero_cost_without_h2() / 0.8 * synkero_fraction())
        * 0.2
        / synnaphtha_fraction()
    )


@component.add(
    name="SynNaphtha fraction",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"synkero_fraction": 1},
)
def synnaphtha_fraction():
    """
    Assumes that 75% of the remaining Fischer Tropsch liquids can be used as naphtha. If the kerosene fraction is 60% (base assumption) then this leaves 10 % of FT liquids as byproducts which are probably light products (LPG/fuel gas).
    """
    return (1 - synkero_fraction()) * 0.75


@component.add(
    name="SynNaphtha H2 WTP",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "naphtha_cost": 1,
        "synnaphtha_cost_without_h2": 1,
        "h2_lhv": 1,
        "synkero_output": 1,
        "synkero_h2_usage": 1,
        "synnaphtha_fraction": 1,
        "synkero_fraction": 1,
    },
)
def synnaphtha_h2_wtp():
    return (naphtha_cost() - synnaphtha_cost_without_h2()) / (
        10**6
        / h2_lhv()
        * synkero_h2_usage()
        / synkero_output()
        / 3600
        * 0.2
        / synnaphtha_fraction()
    ) + synkero_fraction() * 0


@component.add(
    name="UCO PRICE",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biomass_price": 1,
        "usd_to_eur": 1,
        "biomass_price_init": 1,
        "inflation_lookup": 1,
    },
)
def uco_price():
    """
    UCO: used cooking oil. Price is assumed to develop similarly to biomass. Source for historical cost: (around 900 $/t (25 $/GJ assuming LHV of 36 GJ/t) in 2024) https://www.spglobal.com/commodityinsights/en/market-insights/latest-news/a griculture/100423-global-uco-supply-to-double-by-2030-as-us-eu-policies-dri ve-asian-supply
    """
    return (
        biomass_price()
        * (25 * usd_to_eur())
        / biomass_price_init()
        * inflation_lookup(2024)
    )
