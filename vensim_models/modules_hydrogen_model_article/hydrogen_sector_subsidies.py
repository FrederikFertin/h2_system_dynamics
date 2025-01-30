"""
Module hydrogen_sector_subsidies
Translated using PySD version 3.14.0
"""

@component.add(
    name="fertilizer H2 actual subsidy",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_h2_cost": 1, "fertilizer_h2_cost": 1},
)
def fertilizer_h2_actual_subsidy():
    return green_h2_cost() - fertilizer_h2_cost()


@component.add(
    name="fertilizer H2 cost",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_h2_cost": 1, "fertilizer_h2_subsidy": 1},
)
def fertilizer_h2_cost():
    return np.maximum(0.1, green_h2_cost() - fertilizer_h2_subsidy())


@component.add(
    name="fertilizer H2 subsidy",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fertilizer_subsidy_ytd": 1,
        "fertilizer_h2_subsidy_limit": 1,
        "fertilizer_h2_subsidy_length": 1,
        "time": 1,
        "fertilizer_h2_subsidy_size": 1,
    },
)
def fertilizer_h2_subsidy():
    return if_then_else(
        fertilizer_subsidy_ytd() < fertilizer_h2_subsidy_limit(),
        lambda: pulse(__data["time"], 2025, width=fertilizer_h2_subsidy_length())
        * fertilizer_h2_subsidy_size(),
        lambda: 0,
    )


@component.add(
    name="fertilizer H2 subsidy length",
    units="years",
    comp_type="Constant",
    comp_subtype="Normal",
)
def fertilizer_h2_subsidy_length():
    return 10


@component.add(
    name="fertilizer H2 subsidy limit",
    units="M€",
    comp_type="Constant",
    comp_subtype="Normal",
)
def fertilizer_h2_subsidy_limit():
    return 10**9


@component.add(
    name="fertilizer H2 subsidy size",
    units="€/kg",
    comp_type="Constant",
    comp_subtype="Normal",
)
def fertilizer_h2_subsidy_size():
    return 0


@component.add(
    name="FT H2 actual subsidy",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_h2_cost": 1, "ft_h2_cost": 1},
)
def ft_h2_actual_subsidy():
    return green_h2_cost() - ft_h2_cost()


@component.add(
    name="FT H2 cost",
    units="€/kgH2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_h2_cost": 1, "ft_h2_subsidy": 1},
)
def ft_h2_cost():
    return np.maximum(green_h2_cost() - ft_h2_subsidy(), 0.1)


@component.add(
    name="FT H2 subsidy",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_aviation_subsidy_ytd": 1,
        "international_aviation_subsidy_ytd": 1,
        "naphtha_subsidy_ytd": 1,
        "ft_h2_subsidy_limit": 1,
        "ft_h2_subsidy_size": 1,
        "ft_h2_subsidy_length": 1,
        "time": 1,
    },
)
def ft_h2_subsidy():
    return if_then_else(
        domestic_aviation_subsidy_ytd()
        + international_aviation_subsidy_ytd()
        + naphtha_subsidy_ytd()
        < ft_h2_subsidy_limit(),
        lambda: pulse(__data["time"], 2025, width=ft_h2_subsidy_length())
        * ft_h2_subsidy_size(),
        lambda: 0,
    )


@component.add(
    name="FT H2 subsidy length",
    units="years",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ft_h2_subsidy_length():
    return 10


@component.add(
    name="FT H2 subsidy limit", units="M€", comp_type="Constant", comp_subtype="Normal"
)
def ft_h2_subsidy_limit():
    return 10**9


@component.add(
    name="FT H2 subsidy size", units="€/kg", comp_type="Constant", comp_subtype="Normal"
)
def ft_h2_subsidy_size():
    return 0


@component.add(
    name="HD H2 actual subsidy",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_h2_cost": 1, "hd_h2_cost": 1},
)
def hd_h2_actual_subsidy():
    return green_h2_cost() - hd_h2_cost()


@component.add(
    name="HD H2 cost",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_h2_cost": 1, "hd_h2_subsidy": 1},
)
def hd_h2_cost():
    return np.maximum(0.1, green_h2_cost() - hd_h2_subsidy())


@component.add(
    name="HD H2 subsidy",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "heavy_duty_subsidy_ytd": 1,
        "hd_h2_subsidy_limit": 1,
        "hd_h2_subsidy_size": 1,
        "time": 1,
        "hd_h2_subsidy_length": 1,
    },
)
def hd_h2_subsidy():
    return if_then_else(
        heavy_duty_subsidy_ytd() < hd_h2_subsidy_limit(),
        lambda: pulse(__data["time"], 2025, width=hd_h2_subsidy_length())
        * hd_h2_subsidy_size(),
        lambda: 0,
    )


@component.add(
    name="HD H2 subsidy length",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def hd_h2_subsidy_length():
    return 10


@component.add(
    name="HD H2 subsidy limit", units="M€", comp_type="Constant", comp_subtype="Normal"
)
def hd_h2_subsidy_limit():
    return 10**9


@component.add(
    name="HD H2 subsidy size", units="€/kg", comp_type="Constant", comp_subtype="Normal"
)
def hd_h2_subsidy_size():
    return 0


@component.add(
    name="LD H2 actual subsidy",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_h2_cost": 1, "ld_h2_cost": 1},
)
def ld_h2_actual_subsidy():
    return green_h2_cost() - ld_h2_cost()


@component.add(
    name="LD H2 cost",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_h2_cost": 1, "ld_h2_subsidy": 1},
)
def ld_h2_cost():
    return np.maximum(0.1, green_h2_cost() - ld_h2_subsidy())


@component.add(
    name="LD H2 subsidy",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "light_duty_subsidy_ytd": 1,
        "ld_h2_subsidy_limit": 1,
        "ld_h2_subsidy_size": 1,
        "ld_h2_subsidy_length": 1,
        "time": 1,
    },
)
def ld_h2_subsidy():
    return if_then_else(
        light_duty_subsidy_ytd() < ld_h2_subsidy_limit(),
        lambda: pulse(__data["time"], 2025, width=ld_h2_subsidy_length())
        * ld_h2_subsidy_size(),
        lambda: 0,
    )


@component.add(
    name="LD H2 subsidy length",
    units="years",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ld_h2_subsidy_length():
    return 10


@component.add(
    name="LD H2 subsidy limit", units="M€", comp_type="Constant", comp_subtype="Normal"
)
def ld_h2_subsidy_limit():
    return 10**9


@component.add(
    name="LD H2 subsidy size", units="€/kg", comp_type="Constant", comp_subtype="Normal"
)
def ld_h2_subsidy_size():
    return 0


@component.add(
    name="NM H2 actual subsidy",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_h2_cost": 1, "nm_h2_cost": 1},
)
def nm_h2_actual_subsidy():
    return green_h2_cost() - nm_h2_cost()


@component.add(
    name="NM H2 cost",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_h2_cost": 1, "nm_h2_subsidy": 1},
)
def nm_h2_cost():
    return np.maximum(0.1, green_h2_cost() - nm_h2_subsidy())


@component.add(
    name="NM H2 GJ cost",
    units="€/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nm_h2_cost": 1},
)
def nm_h2_gj_cost():
    return nm_h2_cost() / 120 * 1000


@component.add(
    name="NM H2 subsidy",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "high_temperature_subsidy_ytd": 1,
        "nm_h2_subsidy_limit": 1,
        "nm_h2_subsidy_length": 1,
        "time": 1,
        "nm_h2_subsidy_size": 1,
    },
)
def nm_h2_subsidy():
    return if_then_else(
        high_temperature_subsidy_ytd() < nm_h2_subsidy_limit(),
        lambda: pulse(__data["time"], 2025, width=nm_h2_subsidy_length())
        * nm_h2_subsidy_size(),
        lambda: 0,
    )


@component.add(
    name="NM H2 subsidy length",
    units="years",
    comp_type="Constant",
    comp_subtype="Normal",
)
def nm_h2_subsidy_length():
    return 10


@component.add(
    name="NM H2 subsidy limit", units="M€", comp_type="Constant", comp_subtype="Normal"
)
def nm_h2_subsidy_limit():
    return 10**9


@component.add(
    name="NM H2 subsidy size", units="€/kg", comp_type="Constant", comp_subtype="Normal"
)
def nm_h2_subsidy_size():
    return 0


@component.add(
    name="refinery H2 actual subsidy",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_h2_cost": 1, "refinery_h2_cost": 1},
)
def refinery_h2_actual_subsidy():
    return green_h2_cost() - refinery_h2_cost()


@component.add(
    name="refinery H2 cost",
    units="€/kgH2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_h2_cost": 1, "refinery_h2_subsidy": 1},
)
def refinery_h2_cost():
    return np.maximum(0.1, green_h2_cost() - refinery_h2_subsidy())


@component.add(
    name="refinery H2 subsidy",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "refinery_subsidy_ytd": 1,
        "refinery_h2_subsidy_limit": 1,
        "refinery_h2_subsidy_length": 1,
        "refinery_h2_subsidy_size": 1,
        "time": 1,
    },
)
def refinery_h2_subsidy():
    return if_then_else(
        refinery_subsidy_ytd() < refinery_h2_subsidy_limit(),
        lambda: pulse(__data["time"], 2025, width=refinery_h2_subsidy_length())
        * refinery_h2_subsidy_size(),
        lambda: 0,
    )


@component.add(
    name="refinery H2 subsidy length",
    units="years",
    comp_type="Constant",
    comp_subtype="Normal",
)
def refinery_h2_subsidy_length():
    return 10


@component.add(
    name="refinery H2 subsidy limit",
    units="M€",
    comp_type="Constant",
    comp_subtype="Normal",
)
def refinery_h2_subsidy_limit():
    return 10**9


@component.add(
    name="refinery H2 subsidy size",
    units="€/kg",
    comp_type="Constant",
    comp_subtype="Normal",
)
def refinery_h2_subsidy_size():
    return 0


@component.add(
    name="shipping MeOH H2 actual subsidy",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_h2_cost": 1, "shipping_meoh_h2_cost": 1},
)
def shipping_meoh_h2_actual_subsidy():
    return green_h2_cost() - shipping_meoh_h2_cost()


@component.add(
    name="shipping MeOH H2 cost",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_h2_cost": 1, "shipping_meoh_h2_subsidy": 1},
)
def shipping_meoh_h2_cost():
    return np.maximum(0.1, green_h2_cost() - shipping_meoh_h2_subsidy())


@component.add(
    name="shipping MeOH H2 subsidy",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "shipping_meoh_subsidy_ytd": 1,
        "shipping_meoh_h2_subsidy_limit": 1,
        "shipping_meoh_h2_subsidy_length": 1,
        "shipping_meoh_h2_subsidy_size": 1,
        "time": 1,
    },
)
def shipping_meoh_h2_subsidy():
    return if_then_else(
        shipping_meoh_subsidy_ytd() < shipping_meoh_h2_subsidy_limit(),
        lambda: pulse(__data["time"], 2025, width=shipping_meoh_h2_subsidy_length())
        * shipping_meoh_h2_subsidy_size(),
        lambda: 0,
    )


@component.add(
    name="shipping MeOH H2 subsidy length",
    units="years",
    comp_type="Constant",
    comp_subtype="Normal",
)
def shipping_meoh_h2_subsidy_length():
    return 10


@component.add(
    name="shipping MeOH H2 subsidy limit",
    units="M€",
    comp_type="Constant",
    comp_subtype="Normal",
)
def shipping_meoh_h2_subsidy_limit():
    return 10**9


@component.add(
    name="shipping MeOH H2 subsidy size",
    units="€/kg",
    comp_type="Constant",
    comp_subtype="Normal",
)
def shipping_meoh_h2_subsidy_size():
    return 0


@component.add(
    name="shipping NH3 H2 actual subsidy",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_h2_cost": 1, "shipping_nh3_h2_cost": 1},
)
def shipping_nh3_h2_actual_subsidy():
    return green_h2_cost() - shipping_nh3_h2_cost()


@component.add(
    name="shipping NH3 H2 cost",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_h2_cost": 1, "shipping_nh3_h2_subsidy": 1},
)
def shipping_nh3_h2_cost():
    return np.maximum(0.1, green_h2_cost() - shipping_nh3_h2_subsidy())


@component.add(
    name="shipping NH3 H2 subsidy",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "shipping_nh3_subsidy_ytd": 1,
        "shipping_nh3_h2_subsidy_limit": 1,
        "shipping_nh3_h2_subsidy_length": 1,
        "shipping_nh3_h2_subsidy_size": 1,
        "time": 1,
    },
)
def shipping_nh3_h2_subsidy():
    return if_then_else(
        shipping_nh3_subsidy_ytd() < shipping_nh3_h2_subsidy_limit(),
        lambda: pulse(__data["time"], 2025, width=shipping_nh3_h2_subsidy_length())
        * shipping_nh3_h2_subsidy_size(),
        lambda: 0,
    )


@component.add(
    name="shipping NH3 H2 subsidy length",
    units="years",
    comp_type="Constant",
    comp_subtype="Normal",
)
def shipping_nh3_h2_subsidy_length():
    return 10


@component.add(
    name="shipping NH3 H2 subsidy limit",
    units="M€",
    comp_type="Constant",
    comp_subtype="Normal",
)
def shipping_nh3_h2_subsidy_limit():
    return 10**9


@component.add(
    name="shipping NH3 H2 subsidy size",
    units="€/kg",
    comp_type="Constant",
    comp_subtype="Normal",
)
def shipping_nh3_h2_subsidy_size():
    return 0


@component.add(
    name="steel H2 actual subsidy",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_h2_cost": 1, "steel_h2_cost": 1},
)
def steel_h2_actual_subsidy():
    return green_h2_cost() - steel_h2_cost()


@component.add(
    name="steel H2 cost",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"green_h2_cost": 1, "steel_h2_subsidy": 1},
)
def steel_h2_cost():
    return np.maximum(0.1, green_h2_cost() - steel_h2_subsidy())


@component.add(
    name="steel H2 subsidy",
    units="€/kg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "steel_subsidy_ytd": 1,
        "steel_h2_subsidy_limit": 1,
        "steel_h2_subsidy_length": 1,
        "steel_h2_subsidy_size": 1,
        "time": 1,
    },
)
def steel_h2_subsidy():
    return if_then_else(
        steel_subsidy_ytd() < steel_h2_subsidy_limit(),
        lambda: pulse(__data["time"], 2025, width=steel_h2_subsidy_length())
        * steel_h2_subsidy_size(),
        lambda: 0,
    )


@component.add(
    name="steel H2 subsidy length",
    units="years",
    comp_type="Constant",
    comp_subtype="Normal",
)
def steel_h2_subsidy_length():
    return 10


@component.add(
    name="steel H2 subsidy limit",
    units="M€",
    comp_type="Constant",
    comp_subtype="Normal",
)
def steel_h2_subsidy_limit():
    return 10**9


@component.add(
    name="steel H2 subsidy size",
    units="€/kg",
    comp_type="Constant",
    comp_subtype="Normal",
)
def steel_h2_subsidy_size():
    return 0
