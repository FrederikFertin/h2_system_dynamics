class result_loading_class:

    h2_summary = ["H2 DEMAND in TWh", "industry TWh", "trans TWh", "power TWh"]
    subsidy_summary = ["TOTAL GREEN HYDROGEN DEMAND", "Green H2 cost", "TOTAL SUBSIDIES"]

    # Define the sectors of the model
    steel_sector = ["Coal BF BOF", "Coal BF BOF CCS", "HDRI EAF"]
    hvc_sector = ["Fossil naphtha", "Bio naphtha", "Synthetic naphtha"]
    #meoh_sector = ["Grey MeOH", "Blue MeOH", "BioMeOH", "eMeOH"]
    fertilizer_sector = ["Grey NH3", "Blue NH3", "Green NH3"]
    temp_sector = ["NG NM", "Blue NG NM", "Biogas NM", "H2 NM"]
    refining_sector = ["Grey refinery", "Blue refinery", "Green refinery"]
    industry_sectors = steel_sector + hvc_sector + fertilizer_sector + temp_sector + refining_sector # + meoh_sector

    int_aviation_sector = ["Jetfuel consumption", "Syn kerosene consumption", "Bio kerosene consumption"]
    dom_aviation_sector = ["Jetfuel consumption dom", "Syn kerosene consumption dom", "Bio kerosene consumption dom"]
    int_shipping_sector = ["HFO shipping consumption", "NH3 shipping consumption", "MeOH shipping consumption"]
    dom_shipping_sector = ["Domestic HFO shipping consumption", "Domestic battery shipping consumption", "Domestic MeOH shipping consumption", "Domestic H2 shipping consumption"]
    ld_road_transport_sector = ["LD Fossil consumption", "LD BEV consumption", "LD FCEV consumption"]
    hd_road_transport_sector = ["HD Fossil consumption", "HD BEV consumption", "HD FCEV consumption"]
    transport_sectors = int_aviation_sector + dom_aviation_sector + int_shipping_sector + dom_shipping_sector + ld_road_transport_sector + hd_road_transport_sector

    sectors = industry_sectors + transport_sectors

    price_break_list = ["steel H2 price break",
                    "SynNaphtha H2 price break", 
                    "BioNaphtha H2 price break", 
                    "BioKero H2 price break",
                    "SynKero H2 price break", 
                    "fertilizer H2 price break", 
                    "refinery H2 price break", 
                    "NM H2 price break",
                    "LD H2 price break", 
                    "HD H2 price break", 
                    "NH3 containership H2 price break", 
                    "MeOH containership H2 price break",
                    "MeOH ship H2 price break", 
                    "FC ship H2 price break",
                    ]

    # Define the dictionary of sectors, include a key for each sector which defines the unit used in the sector
    industry_sector_dict = {"steel": {"unit": "MT", "stocks" : steel_sector, "h2 demand" : "steel hydrogen demand", "emissions" : "steel emissions", "subsidy": "steel subsidy", "price break": "steel H2 price break"},
                            "naphtha": {"unit": "MT", "stocks" : hvc_sector, "h2 demand" : "naphtha hydrogen demand", "emissions" : "naphtha emissions", "biomass": "naphtha biomass demand", "subsidy": "naphtha subsidy", "price break": "SynNaphtha H2 price break", "price break 2": "BioNaphtha H2 price break"},
                            #"MeOH": {"unit": "MT", "stocks" : meoh_sector, "h2 demand" : "MeOH hydrogen demand", "emissions" : "MeOH emissions", "biomass": "MeOH biomass demand", "subsidy": "MeOH subsidy"},
                            "fertilizer": {"unit": "MT", "stocks" : fertilizer_sector, "h2 demand" : "fertilizer hydrogen demand", "emissions" : "fertilizer emissions", "subsidy": "fertilizer subsidy", "price break": "fertilizer H2 price break"},
                            "high temperature": {"unit": "GWh", "stocks" : temp_sector, "h2 demand" : "high temperature hydrogen demand", "emissions" : "high temperature emissions", "biomass": "high temperature biomass demand", "subsidy": "high temperature subsidy", "price break": "NM H2 price break"},
                            "refining": {"unit": "MT", "stocks" : refining_sector, "h2 demand" : "refinery hydrogen demand", "emissions" : "refinery emissions", "subsidy": "refinery subsidy", "price break": "refinery H2 price break"}}

    transport_sector_dict = {"int_aviation": {"unit": "GWh", "stocks" : int_aviation_sector, "h2 demand" : "international aviation hydrogen demand", "emissions" : "international aviation emissions", "biomass": "international aviation biomass demand", "subsidy": "international aviation subsidy", "price break": "SynKero H2 price break", "price break 2": "BioKero H2 price break"},
                            "dom_aviation": {"unit": "GWh", "stocks" : dom_aviation_sector, "h2 demand" : "domestic aviation hydrogen demand", "emissions" : "domestic aviation emissions", "biomass": "domestic aviation biomass demand", "subsidy": "domestic aviation subsidy", "price break": "SynKero H2 price break", "price break 2": "BioKero H2 price break"},
                            "int_shipping": {"unit": "GWh", "stocks" : int_shipping_sector, "h2 demand" : "international shipping hydrogen demand", "emissions" : "international shipping emissions", "biomass": "international shipping biomass demand", "subsidy": "international shipping subsidy", "price break": "NH3 containership H2 price break", "price break 2": "MeOH containership H2 price break"},
                            "dom_shipping": {"unit": "GWh", "stocks" : dom_shipping_sector, "h2 demand" : "domestic shipping hydrogen demand", "emissions" : "domestic shipping emissions", "biomass": "domestic shipping biomass demand", "subsidy": "domestic shipping subsidy", "price break": "MeOH ship H2 price break", "price break 2": "FC ship H2 price break"},
                            "ld_road_transport": {"unit": "GWh", "stocks" : ld_road_transport_sector, "h2 demand" : "light duty hydrogen demand", "emissions" : "light duty emissions", "subsidy": "light duty subsidy", "price break": "LD H2 price break"},
                            "hd_road_transport": {"unit": "GWh", "stocks" : hd_road_transport_sector, "h2 demand" : "heavy duty hydrogen demand", "emissions" : "heavy duty emissions", "subsidy": "heavy duty subsidy", "price break": "HD H2 price break"}}

    sector_dict = {"industry": industry_sector_dict, "transport": transport_sector_dict}

    hydrogen_demands = {"power" : "power hydrogen demand"}
    subsidies = {"power" : "power subsidy"}
    biomass_demands = {}
    emissions = {}
    price_breaks = {}

    for main_sector in sector_dict.keys():
        for i, (sub_sector, sub_dict) in enumerate(sector_dict[main_sector].items()):
            hydrogen_demands[sub_sector] = sub_dict["h2 demand"]
            subsidies[sub_sector] = sub_dict["subsidy"]
            emissions[sub_sector] = sub_dict["emissions"]
            price_breaks[sub_sector] = sub_dict["price break"]
            if "price break 2" in sub_dict.keys():
                price_breaks[sub_sector + " 2"] = sub_dict["price break 2"]
            if "biomass" in sub_dict.keys():
                biomass_demands[sub_sector] = sub_dict["biomass"]