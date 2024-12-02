class result_loading_class:

    h2_summary = ["H2 DEMAND in TWh", "industry TWh", "trans TWh", "power TWh"]
    subsidy_summary = ["TOTAL GREEN HYDROGEN DEMAND", "Green H2 cost", "TOTAL SUBSIDIES"]

    # Define the sectors of the model
    steel_sector = ["Coal BF BOF", "Coal BF BOF CCS", "NGDRI EAF", "H2DRI EAF"]
    hvc_sector = ["Fossil naphtha", "Biogenic naphtha", "Synthetic naphtha"]
    meoh_sector = ["Grey MeOH", "Blue MeOH", "BioMeOH", "eMeOH"]
    fertilizer_sector = ["Grey NH3", "Blue NH3", "Green NH3"]
    temp_sector = ["Grey NG NM", "Blue NG NM", "Biogas NM", "H2 NM"]
    refining_sector = ["Grey refinery", "Blue refinery", "Green refinery"]
    industry_sectors = steel_sector + hvc_sector + fertilizer_sector + temp_sector + refining_sector + meoh_sector

    int_aviation_sector = ["Jetfuel consumption", "Syn kerosene consumption", "Bio kerosene consumption"]
    dom_aviation_sector = ["Jetfuel consumption dom", "Syn kerosene consumption dom", "Bio kerosene consumption dom"]
    int_shipping_sector = ["HFO shipping consumption", "NH3 shipping consumption", "MeOH shipping consumption"]
    dom_shipping_sector = ["Domestic HFO shipping consumption", "Domestic battery shipping consumption", "Domestic MeOH shipping consumption", "Domestic H2 shipping consumption"]
    ld_road_transport_sector = ["LD Fossil consumption", "LD BEV consumption", "LD FCEV consumption"]
    hd_road_transport_sector = ["HD Fossil consumption", "HD BEV consumption", "HD FCEV consumption"]
    transport_sectors = int_aviation_sector + dom_aviation_sector + int_shipping_sector + dom_shipping_sector + ld_road_transport_sector + hd_road_transport_sector

    # Define the costs for each sector
    steel_costs = ["BF Coal cost", "BF CCS cost", "NGDRI cost", "H2DRI cost"]
    hvc_costs = ["Naphtha cost", "BioNaphtha cost", "SynNaphtha cost",]
    meoh_costs = ["convMeOH cost", "Blue MeOH cost", "Green bioMeOH cost", "Green eMeOH cost"]
    fertilizer_costs = ["Grey NH3 cost", "Blue NH3 cost", "fertilizer NH3 cost"]
    temp_costs = ["Grey NG cost", "Blue NG cost", "NM H2 GJ cost", "biogas cost"]
    refining_costs = ["Grey H2 cost", "Blue H2 cost", "refinery H2 cost"]

    int_aviation_costs = ["Jetfuel cost", "SynKero cost", "BioKero cost"]
    dom_aviation_costs = ["Jetfuel cost", "SynKero cost", "BioKero cost"]
    int_shipping_costs = ["HFO containership cost", "NH3 containership cost", "MeOH containership cost"]
    dom_shipping_costs = ["HFO ship cost", "BE ship cost", "MeOH ship cost", "FC ship cost"]
    ld_road_transport_costs = ["LD ICE LCO", "LD BE LCO", "LD FC LCO"]
    hd_road_transport_costs = ["HD ICE LCO", "HD BE LCO", "HD FC LCO"]

    sectors = industry_sectors + transport_sectors

    price_break_list = ["steel H2 WTP",
                    "SynNaphtha H2 WTP", 
                    "BioNaphtha H2 WTP", 
                    "eMeOH H2 WTP",
                    "bioMeOH H2 WTP",
                    "BioKero H2 WTP",
                    "SynKero H2 WTP", 
                    "fertilizer H2 WTP", 
                    "refinery H2 WTP", 
                    "high temperature H2 WTP",
                    "LD H2 WTP", 
                    "HD H2 WTP", 
                    "NH3 containership H2 WTP", 
                    "MeOH containership H2 WTP",
                    "MeOH ship H2 WTP", 
                    "FC ship H2 WTP",
                    ]

    # Define the dictionary of sectors, include a key for each sector which defines the unit used in the sector
    industry_sector_dict = {"steel": {"unit": "MT", "stocks" : steel_sector, "h2 demand" : "steel hydrogen demand", "emissions" : "steel emissions", "subsidy": "steel subsidy", "WTP": "steel H2 WTP", "CT revenue": "steel CT revenue", "costs": steel_costs},
                            "naphtha": {"unit": "MT", "stocks" : hvc_sector, "h2 demand" : "naphtha hydrogen demand", "emissions" : "naphtha emissions", "biomass": "naphtha biomass demand", "subsidy": "naphtha subsidy", "WTP": "SynNaphtha H2 WTP", "WTP 2": "BioNaphtha H2 WTP", "CT revenue": "naphtha CT revenue", "costs": hvc_costs},
                            "MeOH": {"unit": "MT", "stocks" : meoh_sector, "h2 demand" : "MeOH hydrogen demand", "emissions" : "MeOH emissions", "biomass": "MeOH biomass demand", "subsidy": "MeOH subsidy", "WTP": "eMeOH H2 WTP", "WTP 2": "bioMeOH H2 WTP", "CT revenue": "MeOH CT revenue", "costs": meoh_costs},
                            "fertilizer": {"unit": "MT", "stocks" : fertilizer_sector, "h2 demand" : "fertilizer hydrogen demand", "emissions" : "fertilizer emissions", "subsidy": "fertilizer subsidy", "WTP": "fertilizer H2 WTP", "CT revenue": "fertilizer CT revenue", "costs": fertilizer_costs},
                            "high temperature": {"unit": "GWh", "stocks" : temp_sector, "h2 demand" : "high temperature hydrogen demand", "emissions" : "high temperature emissions", "biomass": "high temperature biomass demand", "subsidy": "high temperature subsidy", "WTP": "high temperature H2 WTP", "CT revenue": "high temperature CT revenue", "costs": temp_costs},
                            "refining": {"unit": "MT", "stocks" : refining_sector, "h2 demand" : "refinery hydrogen demand", "emissions" : "refinery emissions", "subsidy": "refinery subsidy", "WTP": "refinery H2 WTP", "CT revenue": "refinery CT revenue", "costs": refining_costs}}

    transport_sector_dict = {"int_aviation": {"unit": "GWh", "stocks" : int_aviation_sector, "h2 demand" : "international aviation hydrogen demand", "emissions" : "international aviation emissions", "biomass": "international aviation biomass demand", "subsidy": "international aviation subsidy", "WTP": "SynKero H2 WTP", "WTP 2": "BioKero H2 WTP", "CT revenue": "international aviation CT revenue", "costs": int_aviation_costs},
                            "dom_aviation": {"unit": "GWh", "stocks" : dom_aviation_sector, "h2 demand" : "domestic aviation hydrogen demand", "emissions" : "domestic aviation emissions", "biomass": "domestic aviation biomass demand", "subsidy": "domestic aviation subsidy", "WTP": "SynKero H2 WTP", "WTP 2": "BioKero H2 WTP", "CT revenue": "domestic aviation CT revenue", "costs": dom_aviation_costs},
                            "int_shipping": {"unit": "GWh", "stocks" : int_shipping_sector, "h2 demand" : "international shipping hydrogen demand", "emissions" : "international shipping emissions", "biomass": "international shipping biomass demand", "subsidy": "international shipping subsidy", "WTP": "NH3 containership H2 WTP", "WTP 2": "MeOH containership H2 WTP", "CT revenue": "international shipping CT revenue", "costs": int_shipping_costs},
                            "dom_shipping": {"unit": "GWh", "stocks" : dom_shipping_sector, "h2 demand" : "domestic shipping hydrogen demand", "emissions" : "domestic shipping emissions", "biomass": "domestic shipping biomass demand", "subsidy": "domestic shipping subsidy", "WTP": "MeOH ship H2 WTP", "WTP 2": "FC ship H2 WTP", "CT revenue": "domestic shipping CT revenue",  "costs": dom_shipping_costs},
                            "ld_road_transport": {"unit": "GWh", "stocks" : ld_road_transport_sector, "h2 demand" : "light duty hydrogen demand", "emissions" : "light duty emissions", "subsidy": "light duty subsidy", "WTP": "LD H2 WTP", "CT revenue": "light duty CT revenue", "costs": ld_road_transport_costs},
                            "hd_road_transport": {"unit": "GWh", "stocks" : hd_road_transport_sector, "h2 demand" : "heavy duty hydrogen demand", "emissions" : "heavy duty emissions", "subsidy": "heavy duty subsidy", "WTP": "HD H2 WTP", "CT revenue": "heavy duty CT revenue", "costs": hd_road_transport_costs}}

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
            price_breaks[sub_sector] = sub_dict["WTP"]
            if "WTP 2" in sub_dict.keys():
                price_breaks[sub_sector + " 2"] = sub_dict["WTP 2"]
            if "biomass" in sub_dict.keys():
                biomass_demands[sub_sector] = sub_dict["biomass"]